#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Profile C — LIVE runner: the REAL harness.py code in action (OpenAI-backed).

Unlike demo_profileC.py (scripted, offline), this drives the ACTUAL MemC pipeline
from harness.py — real salience scoring, real gist/anchor, real embeddings, real
consolidation and decay-weighted retrieval. Nothing here is scripted; the
salience/gist prints are transparent traces around the real functions.

Modes:
  python3 poc/run_live.py --demo     # auto-play a 3-session sample, narrated
  python3 poc/run_live.py            # interactive REPL

Interactive commands:
  <text>        add a user turn to the current session
  /end          end the session -> real encoding + consolidation, show memory
  /ask <query>  run real decay-weighted retrieval
  /state        show current memory state
  /quit
"""
import sys, math
import harness as H   # the REAL implementation (loads .env / OPENAI_API_KEY)

PLAIN = "--plain" in sys.argv
def c(k, s): return s if PLAIN else f"\033[{k}m{s}\033[0m"
def b(s): return c("1", s)
def dim(s): return c("2", s)
def acc(s): return c("38;5;111", s)
def ok(s): return c("38;5;114", s)
def warn(s): return c("38;5;179", s)
def hr(): print(dim("─" * 68))

# ---- transparent tracing around the REAL functions (logic untouched) ----
_sal, _ga, _sf = H._salience_batch, H._gist_anchor, H._semantic_fact
def traced_salience(events):
    r = _sal(events)  # real OpenAI call
    for e, s in zip(events, r):
        tag = warn("ტრივია") if s < 0.3 else ok("მნიშვნელოვანი")
        print(f"     salience {b(f'{s:.2f}')} [{tag}]  ← „{e[:46]}“")
    return r
def traced_gist_anchor(ev):
    g, a = _ga(ev)  # real OpenAI call
    print(f"       gist:   {dim(g)}")
    if a: print(f"       anchor: {dim(a)}")
    return g, a
def traced_semantic_fact(gists):
    f = _sf(gists)  # real OpenAI call
    print("   " + acc("⚙ კონსოლიდაცია → სემანტიკური ფაქტი: ") + b(ok(f)) + dim("  (S=5.0)"))
    return f
H._salience_batch, H._gist_anchor, H._semantic_fact = traced_salience, traced_gist_anchor, traced_semantic_fact

def show_state(mem, now):
    if not (mem.episodes or mem.semantic):
        print(dim("   — მეხსიერება ცარიელია —")); return
    for m in mem.semantic:
        R = mem._R(m, now)
        st = ok("ცოცხალი") if R >= H.FORGET_FLOOR else warn("დავიწყებული ✗")
        print(f"   [{acc('SEM')}] R={b(f'{R:.3f}')} {st}  S={m['S']:.1f}  {dim(m['fact'][:44])}")
    for m in mem.episodes:
        R = mem._R(m, now)
        st = ok("ცოცხალი") if R >= H.FORGET_FLOOR else warn("დავიწყებული ✗")
        rr = b(f"{R:.3f}") if R >= H.FORGET_FLOOR else warn(f"{R:.3f}")
        print(f"   [{dim('EPI')}] R={rr} {st}  S={m['S']:.1f} sal={m['salience']:.2f}  {dim(m['gist'][:40])}")

def end_session(mem, sid, events):
    if not events: return
    hr(); print(b(f"  სესია {sid}") + dim(f"  — რეალური კოდირება ({len(events)} რეპლიკა) · OpenAI"))
    mem.end_session(sid, events)   # <-- the REAL pipeline runs here
    print(); print(b("  მეხსიერების მდგომარეობა:"))
    show_state(mem, sid)

def ask(mem, sid, query):
    hr(); print(b("  მოძიება") + dim(f"  query: „{query}“"))
    print(b("  კვალის მდგომარეობა მოძიების წინ (R = exp(−Δt/S)):"))
    show_state(mem, sid)
    hits, dt = mem.retrieve(query, sid)   # <-- REAL decay-weighted retrieval + reinforcement
    print(); print(b(f"  → დაბრუნებული TOP-{H.RETRIEVE_K}  ") + dim(f"({dt:.1f} ms)"))
    for kind, txt in hits:
        print(f"      • ({acc(kind)}) {txt}")
    print("   " + acc("⟳ გამყარება: ") + dim("დაბრუნებულ მოგონებებზე S += 0.5"))

SAMPLE = [
 (1, ["მე მქვია ლექსო, თბილისში ვცხოვრობ", "ხვალ პროექტის დედლაინი მაქვს", "დღეს ამინდი მზიანია"]),
 (2, ["ისევ დედლაინის სტრესში ვარ", "წუხელ ფილმი ვნახე, სახელი დამავიწყდა"]),
 (3, ["ამ კვირას კიდევ ერთი დედლაინი მომიწია", "არაქისზე ალერგია მაქვს"]),
]
QUERY = "დამეხმარე, როგორ დავგეგმო სამუშაო დედლაინამდე"

def header():
    print()
    print(b("  Profile C — LIVE ") + dim("(რეალური harness.py · OpenAI gpt-4o-mini + text-embedding-3-small)"))
    print()

def demo():
    header()
    mem = H.MemC()   # the REAL Profile C memory
    for sid, evs in SAMPLE:
        end_session(mem, sid, evs)
    ask(mem, 4, QUERY)
    hr()
    print(ok("  API გამოძახებები (რეალური): ") +
          f"chat={H.USAGE['chat_calls']} (in {H.USAGE['chat_in']}/out {H.USAGE['chat_out']} tok) · "
          f"embed={H.USAGE['embed_calls']} ({H.USAGE['embed_tok']} tok)")
    print(dim("  ↑ ეს ამტკიცებს, რომ კოდი ნამდვილად მუშაობს — არა წინასწარ ჩაწერილი პასუხები."))
    print()

def repl():
    header(); print(dim("  ბრძანებები: <ტექსტი> · /end · /ask <query> · /state · /quit\n"))
    mem = H.MemC(); sid = 1; buf = []
    while True:
        try: line = input(acc(f"  სესია {sid} > ")).strip()
        except (EOFError, KeyboardInterrupt): print(); break
        if not line: continue
        if line == "/quit": break
        elif line == "/end": end_session(mem, sid, buf); buf = []; sid += 1
        elif line == "/state": show_state(mem, sid)
        elif line.startswith("/ask"): ask(mem, sid, line[4:].strip() or QUERY)
        else: buf.append(line); print(dim(f"     + დაემატა ({len(buf)} რეპლიკა ბუფერში)"))
    print(dim("  ნახვამდის."))

if __name__ == "__main__":
    try:
        demo() if "--demo" in sys.argv else repl()
    except Exception as e:
        print(warn(f"\n  შეცდომა: {e}\n  (შეამოწმე ინტერნეტი / OPENAI_API_KEY .env-ში)"))
