#!/usr/bin/env python3
"""
Run the four memory conditions over synthetic multi-session dialogues and evaluate:
 - technical: cross-session recall of salient vs trivia facts; consolidation firing; retrieval latency
 - simulated-perception: LLM-judge ratings of social constructs per condition
Outputs results.json + a printed summary. Use --quick for 1 persona (validation).
"""
import sys, json, time, statistics as st
import harness as H

# ---------- personas: scripted USER turns, shared across all conditions ----------
# turn = {"u": utterance, optional "probe": {"fact":..., "kind":"salient"|"trivia"|"generalization", "q":question}}
PERSONAS = [
 {"name": "Nino",
  "sessions": [
    [ {"u": "Hi! I'm Nino. I'm a grad student and honestly my thesis deadline is stressing me out."},
      {"u": "I have a golden retriever named Bruno, he's the only thing keeping me sane."},
      {"u": "Oh and I'm allergic to peanuts, learned that the hard way as a kid."} ],
    [ {"u": "Rough week. The thesis is still hanging over me, barely slept."},
      {"u": "By the way the weather was really foggy this morning, kind of pretty."},
      {"u": "I'm thinking of a short trip to Batumi once this is over."} ],
    [ {"u": "Quick question — do you remember my dog's name?",
       "probe": {"fact": "the dog's name is Bruno", "kind": "salient", "q": "What is my dog's name?"}},
      {"u": "And what am I allergic to, do you recall?",
       "probe": {"fact": "allergic to peanuts", "kind": "salient", "q": "What am I allergic to?"}},
      {"u": "Also — what was the weather like when we talked a few days ago?",
       "probe": {"fact": "it was foggy that morning", "kind": "trivia", "q": "What was the weather that morning?"}} ],
    [ {"u": "Deadline's still crushing me. Feels like it never ends."},
      {"u": "Have you noticed anything about how I've been doing lately?",
       "probe": {"fact": "Nino is repeatedly stressed/anxious about the thesis deadline", "kind": "generalization",
                 "q": "What pattern have you noticed about how I've been?"}} ],
  ]},
 {"name": "Dato",
  "sessions": [
    [ {"u": "I'm Dato, I run a small startup. It's a lot."},
      {"u": "I've got two kids, Ana and Luka. They're five and seven."},
      {"u": "Also I'm lactose intolerant, so no dairy for me."} ],
    [ {"u": "Tension with my co-founder again today. We keep clashing on direction."},
      {"u": "We grabbed lunch at a place called Cafe Littera once, that was nice."},
      {"u": "The co-founder thing is really wearing me down honestly."} ],
    [ {"u": "Do you remember my kids' names?",
       "probe": {"fact": "the kids are Ana and Luka", "kind": "salient", "q": "What are my kids' names?"}},
      {"u": "And what's my dietary restriction?",
       "probe": {"fact": "lactose intolerant", "kind": "salient", "q": "What is my dietary restriction?"}},
      {"u": "What was that cafe we talked about?",
       "probe": {"fact": "Cafe Littera", "kind": "trivia", "q": "What cafe did I mention?"}} ],
    [ {"u": "Another hard day with the co-founder. Same friction."},
      {"u": "Do you see any recurring theme in what I bring up?",
       "probe": {"fact": "Dato has ongoing conflict/tension with his co-founder", "kind": "generalization",
                 "q": "What recurring theme do you notice?"}} ],
  ]},
 {"name": "Mari",
  "sessions": [
    [ {"u": "Hey, I'm Mari. I'm a nurse and I work night shifts, so I'm always a bit wrecked."},
      {"u": "I have a cat named Felix. He owns me, not the other way around."},
      {"u": "I'm learning piano lately, slowly."} ],
    [ {"u": "Night shift again, completely drained. This schedule is brutal."},
      {"u": "I saw a decent sci-fi film last night, can't remember the title though."},
      {"u": "I'm also moving apartments next month, dreading the packing."} ],
    [ {"u": "What's my cat's name, do you remember?",
       "probe": {"fact": "the cat's name is Felix", "kind": "salient", "q": "What is my cat's name?"}},
      {"u": "What instrument am I learning?",
       "probe": {"fact": "learning piano", "kind": "salient", "q": "What instrument am I learning?"}},
      {"u": "What kind of film did I mention watching?",
       "probe": {"fact": "a sci-fi film", "kind": "trivia", "q": "What film genre did I mention?"}} ],
    [ {"u": "Back on nights, exhausted as usual."},
      {"u": "Noticing anything about a pattern with me?",
       "probe": {"fact": "Mari is repeatedly exhausted from night shifts", "kind": "generalization",
                 "q": "What pattern do you notice about me?"}} ],
  ]},
]

CONDS = [H.MemA, H.MemB, H.MemBplus, H.MemC]

def run_condition(persona, cond_cls):
    mem = cond_cls()
    transcript_lines, probe_results, latencies, ctx_sizes = [], [], [], []
    for sid, session in enumerate(persona["sessions"]):
        working = []
        for turn in session:
            ctx, lat = mem.retrieve(turn["u"], now=sid)
            if ctx: latencies.append(lat); ctx_sizes.append(sum(len(t.split()) for _, t in ctx))
            reply = H.agent_reply(working, ctx, turn["u"])
            working += [("User", turn["u"]), ("Companion", reply)]
            working = working[-2 * H.WORKING_WINDOW:]
            transcript_lines.append(f"User: {turn['u']}\nCompanion: {reply}")
            if "probe" in turn:
                ok = H.judge_recall(turn["probe"]["fact"], turn["probe"]["q"], reply)
                probe_results.append({"kind": turn["probe"]["kind"], "fact": turn["probe"]["fact"],
                                      "reply": reply, "recalled": ok})
        mem.end_session(sid, [t["u"] for t in session])
    transcript = "\n\n".join(transcript_lines)
    judge = H.judge_transcript(transcript)
    sem = len(getattr(mem, "semantic", []))
    return {"probes": probe_results, "judge": judge, "latency_ms": latencies,
            "ctx_words": ctx_sizes, "semantic_facts": sem, "transcript": transcript}

def main():
    quick = "--quick" in sys.argv
    personas = PERSONAS[:1] if quick else PERSONAS
    t0 = time.time()
    results = {}  # cond -> list of per-persona result
    for cond_cls in CONDS:
        cn = cond_cls.name; results[cn] = []
        for p in personas:
            print(f"  running {cn} / {p['name']} ...", flush=True)
            results[cn].append({"persona": p["name"], **run_condition(p, cond_cls)})
    out = {"results": results, "usage": H.USAGE, "elapsed_s": round(time.time() - t0, 1),
           "config": {k: getattr(H, k) for k in ["CHAT_MODEL", "EMBED_MODEL", "RETRIEVE_K",
                      "DECAY_S_BASE", "CONSOLIDATE_N", "SEM_BONUS"]}}
    json.dump(out, open("results.json", "w"), indent=2)
    summarize(out)

def summarize(out):
    R = out["results"]
    print("\n================ SUMMARY ================")
    # recall by kind
    print("\nRecall accuracy (fraction of probes correctly recalled):")
    kinds = ["salient", "trivia", "generalization"]
    print(f"  {'cond':<4} " + " ".join(f"{k:>14}" for k in kinds))
    for cn, plist in R.items():
        by = {k: [] for k in kinds}
        for pr in plist:
            for pb in pr["probes"]: by[pb["kind"]].append(1 if pb["recalled"] else 0)
        row = " ".join(f"{(sum(by[k])/len(by[k]) if by[k] else 0):>14.2f}" for k in kinds)
        print(f"  {cn:<4} " + row)
    # judge
    print("\nSimulated-perception judge (mean 1-7 across personas):")
    cons = list(H.JUDGE_CONSTRUCTS.keys())
    print(f"  {'cond':<4} " + " ".join(f"{c[:9]:>10}" for c in cons))
    for cn, plist in R.items():
        means = []
        for c in cons:
            vals = [pr["judge"][c] for pr in plist if pr["judge"].get(c) is not None]
            means.append(st.mean(vals) if vals else float("nan"))
        print(f"  {cn:<4} " + " ".join(f"{m:>10.2f}" for m in means))
    # semantic facts + latency + ctx
    print("\nMechanism stats:")
    for cn, plist in R.items():
        sem = sum(pr["semantic_facts"] for pr in plist)
        lat = [x for pr in plist for x in pr["latency_ms"]]
        ctx = [x for pr in plist for x in pr["ctx_words"]]
        print(f"  {cn:<4} semantic_facts={sem:<3} "
              f"retrieval_ms(median)={ (st.median(lat) if lat else 0):.2f}  "
              f"ctx_words(mean)={ (st.mean(ctx) if ctx else 0):.1f}")
    u = out["usage"]
    print(f"\nAPI usage: chat_calls={u['chat_calls']} in={u['chat_in']} out={u['chat_out']} "
          f"embed_tok={u['embed_tok']} | elapsed={out['elapsed_s']}s")
    # rough cost (gpt-4o-mini $0.15/1M in, $0.60/1M out; embed-3-small $0.02/1M)
    cost = u['chat_in']/1e6*0.15 + u['chat_out']/1e6*0.60 + u['embed_tok']/1e6*0.02
    print(f"Estimated cost: ${cost:.3f}")

if __name__ == "__main__":
    main()
