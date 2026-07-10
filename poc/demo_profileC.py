#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Profile C — offline narrated demo (mirrors poc/harness.py, no API/network).

For a live defense demo the real harness.py is risky: it calls OpenAI
(gpt-4o-mini + text-embedding-3-small) for salience, gist and embeddings.
This script keeps the SAME ALGORITHM and CONSTANTS as harness.py's MemC, but:
  - salience score and gist are pre-scripted per line (curated dialogue),
  - embeddings use a tiny local bag-of-words vectoriser instead of the API.
Everything else — S0 = 2.0*max(0.1, salience), lazy Ebbinghaus decay
R = exp(-Dt/S), reinforcement S += 0.5, consolidation (cos>0.55, >=2 -> S=5.0),
dedup (cos<0.8), gist-first retrieval with SEM_BONUS=1.25 — is identical.

Run:  python3 poc/demo_profileC.py        (add  --plain  to disable colour)
"""
import math, re, sys, time

# ---- constants: identical to harness.py ----
DECAY_S_BASE = 2.0
RETRIEVE_K   = 4
FORGET_FLOOR = 0.10
CONSOLIDATE_N = 2
SEM_BONUS    = 1.25

PLAIN = "--plain" in sys.argv
def c(code, s):
    return s if PLAIN else f"\033[{code}m{s}\033[0m"
def b(s): return c("1", s)
def dim(s): return c("2", s)
def acc(s): return c("38;5;111", s)     # blue
def ok(s): return c("38;5;114", s)      # green
def warn(s): return c("38;5;179", s)    # amber
def hr(): print(dim("─" * 66))

# ---- curated multi-session dialogue: (session, user_msg_KA, gist_EN, salience) ----
DIALOGUE = [
 (1, "მე მქვია ლექსო, თბილისში ვცხოვრობ",        "user's name is Lekso and lives in Tbilisi",             0.90),
 (1, "ხვალ პროექტის დედლაინი მაქვს",              "user has a work deadline tomorrow",                     0.80),
 (1, "დღეს ამინდი მზიანია",                        "the weather is sunny today",                            0.10),
 (2, "ისევ დედლაინის სტრესში ვარ",                 "user is stressed about a work deadline",                0.75),
 (2, "წუხელ ფილმი ვნახე, სახელი დამავიწყდა",       "user watched a film last night but forgot its title",   0.15),
 (3, "ამ კვირას კიდევ ერთი დედლაინი მომიწია",       "user faces another work deadline this week",            0.80),
 (3, "არაქისზე ალერგია მაქვს",                     "user is allergic to peanuts",                           0.95),
]
QUERY = (4, "დამეხმარე, როგორ დავგეგმო სამუშაო დედლაინამდე", "help me plan work around my deadline")

STOP = {"user","the","a","an","is","and","its","it","to","of","in","on","about","but","this","week",
        "tomorrow","last","night","them","again","today","another","has","have","me","my","around",
        "help","under","with","recurrently"}
def toks(t):
    # crude stem: strip a trailing plural 's' so deadline/deadlines, work/works match
    return [w[:-1] if len(w) > 3 and w.endswith("s") else w for w in re.findall(r"[a-z]+", t.lower())]
def vec(t):
    v = {}
    for w in toks(t):
        if w in STOP: continue
        v[w] = v.get(w, 0) + 1
    return v
def cos(a, b):
    if not a or not b: return 0.0
    dot = sum(a[w] * b.get(w, 0) for w in a)
    na = math.sqrt(sum(x*x for x in a.values())); nb = math.sqrt(sum(x*x for x in b.values()))
    return dot / (na * nb + 1e-9)
def semantic_fact(gists):
    freq = {}
    for g in gists:
        for w in set(toks(g)):
            if w not in STOP: freq[w] = freq.get(w, 0) + 1
    theme = max(freq, key=freq.get) if freq else "topic"
    # (real system: one LLM call abstracts the cluster; here a readable preset)
    if "deadline" in freq:
        return "user works under tight work deadlines", "deadline"
    return f"user recurrently deals with {theme}", theme

# ---- Profile C state (mirrors harness.py MemC) ----
episodes = []   # {gist, emb, S, last, salience}
semantic = []   # {fact, emb, S, last, src}

def R(m, now):
    dt = max(0, now - m["last"])
    return math.exp(-dt / max(0.3, m["S"]))

def encode(sid, gist, sal):
    S0 = DECAY_S_BASE * max(0.1, sal)
    episodes.append({"gist": gist, "emb": vec(gist), "S": S0, "last": sid, "salience": sal})
    return S0

def consolidate(now):
    used, made = set(), []
    for i, a in enumerate(episodes):
        if i in used: continue
        cluster = [i]
        for j in range(i + 1, len(episodes)):
            if j in used: continue
            if cos(a["emb"], episodes[j]["emb"]) > 0.55: cluster.append(j)
        if len(cluster) >= CONSOLIDATE_N:
            gists = [episodes[k]["gist"] for k in cluster]
            fact, theme = semantic_fact(gists)
            femb = vec(fact)
            if all(cos(femb, s["emb"]) < 0.8 for s in semantic):
                semantic.append({"fact": fact, "emb": femb, "S": DECAY_S_BASE * 2.5, "last": now,
                                 "src": gists}); made.append((fact, cluster, theme))
            for k in cluster: used.add(k)
    return made

def retrieve(query, now):
    q = vec(query); cands = []
    for m in semantic:
        r = R(m, now)
        if r < FORGET_FLOOR: continue
        cands.append((cos(q, m["emb"]) * r * SEM_BONUS, "semantic", m["fact"], r, m))
    for m in episodes:
        r = R(m, now)
        if r < FORGET_FLOOR: continue
        cands.append((cos(q, m["emb"]) * r, "episodic", m["gist"], r, m))
    cands.sort(key=lambda x: x[0], reverse=True)
    return cands, cands[:RETRIEVE_K]

# ---------------- narrated run ----------------
def main():
    print()
    print(b("  Profile C — მეხსიერების დემონსტრაცია  ") + dim("(offline · mirrors harness.py)"))
    print(dim("  კონსტანტები: S0=2.0·salience · R=exp(−Δt/S) · გამყარება +0.5 · "
              "კონსოლიდაცია cos>0.55,≥2→S=5.0 · ზღვარი R<0.10 · SEM_BONUS ×1.25"))
    print()

    by_session = {}
    for sid, msg, gist, sal in DIALOGUE: by_session.setdefault(sid, []).append((msg, gist, sal))

    for sid in sorted(by_session):
        hr(); print(b(f"  სესია {sid}") + dim("   — კოდირება (salience-gating)"))
        for msg, gist, sal in by_session[sid]:
            S0 = encode(sid, gist, sal)
            tag = warn("ტრივია") if sal < 0.3 else ok("მნიშვნელოვანი")
            print(f"   „{msg}“")
            print(f"      salience {b(f'{sal:.2f}')} [{tag}]  →  S₀ = {b(f'{S0:.2f}')}   {dim('gist: '+gist)}")
        made = consolidate(sid)
        for fact, cluster, theme in made:
            print()
            print("   " + acc("⚙ კონსოლიდაცია: ") + f"{len(cluster)} ეპიზოდი (თემა „{theme}“) → "
                  + b(f'სემანტიკური ფაქტი') + f"  «{ok(fact)}»  " + dim("S=5.0"))

    # decay snapshot at query time
    now = QUERY[0]
    hr(); print(b(f"  სესია {now}") + dim(f"   — მოძიების წინ: მეხსიერების მდგომარეობა (Δt-ის მიხედვით)"))
    allm = [("SEM", m) for m in semantic] + [("EPI", m) for m in episodes]
    for kind, m in allm:
        r = R(m, now)
        txt = m.get("fact") or m["gist"]
        state = ok("ცოცხალი") if r >= FORGET_FLOOR else warn("დავიწყებული  ✗")
        rr = b(f"{r:.3f}") if r >= FORGET_FLOOR else warn(f"{r:.3f}")
        print(f"   [{dim(kind)}] R={rr}  {state}   {dim(txt[:44])}")

    # retrieval
    hr(); print(b("  მოძიება") + dim(f"   query: „{QUERY[1]}“"))
    cands, top = retrieve(QUERY[2], now)
    print(dim("   ქულა = cos(query, mem) × R" + "  (×1.25 სემანტიკურ ფაქტებზე)"))
    for score, kind, txt, r, m in cands:
        mark = ok("  ★ TOP") if (score, kind, txt, r, m) in top else "     "
        kk = acc(kind)
        print(f"   {mark}  score {b(f'{score:.3f}')}  ({kk}, R={r:.2f})  {dim(txt[:42])}")
    print()
    print("   " + b("→ დაბრუნებული TOP-4:"))
    for score, kind, txt, r, m in top:
        print(f"      • ({acc(kind)}) {txt}")
    # reinforcement
    for score, kind, txt, r, m in top: m["S"] += 0.5; m["last"] = now
    print()
    print("   " + acc("⟳ გამყარება: ") + dim("დაბრუნებულ მოგონებებზე S += 0.5, საათი განულდა (last = now)"))

    hr()
    print(ok("  დასკვნა: ") + "ტრივია (ამინდი, ფილმი) ჩაქრა; განმეორებადი დედლაინები "
          + b("განზოგადდა ცოდნად") + "; მოძიებამ სიახლითა და რელევანტურობით ამოიღო "
          + "მთავარი — და გამოყენებამ ის კიდევ გააძლიერა.")
    print()

if __name__ == "__main__":
    main()
