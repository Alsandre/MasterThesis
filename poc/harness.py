#!/usr/bin/env python3
"""
Profile C proof-of-concept memory harness.
Implements four memory conditions (A / B / B+ / C) over multi-session dialogue
transcripts, outside the voice pipeline, to demonstrate and evaluate the
mechanisms of the Profile C architecture (thesis §3.4).

Cheapest-viable-cut per F18: implements B+, gist/anchor representation, lazy
Ebbinghaus decay + reinforcement, salience-gated encoding, and episodic->semantic
consolidation. Deferred (noted in results): associative pre-expansion, the
anchor-regex exact-recall trigger, Bayesian-surprise segmentation (uses a simple
per-utterance event unit), and the programmatic sensitivity sweep.

LLM + embeddings: OpenAI (gpt-4o-mini, text-embedding-3-small) via urllib.
"""
import os, json, math, time, urllib.request, urllib.error, hashlib, sys
import numpy as np

# ---------- config ----------
CHAT_MODEL = "gpt-4o-mini"
EMBED_MODEL = "text-embedding-3-small"
WORKING_WINDOW = 6          # volatile recent-turn window shared by all conditions
RETRIEVE_K = 4              # long-term memories injected per turn (shared budget)
DECAY_S_BASE = 2.0         # Ebbinghaus base stability (in session units); externally-anchored placeholder
SALIENCE_GAIN = 1.0        # (unused after salience-scaled stability)
FORGET_FLOOR = 0.10        # retrievability floor
CONSOLIDATE_N = 2          # min recurring events to form a semantic fact
SEM_BONUS = 1.25           # capped semantic-tier preference multiplier

_ENV = {}
def load_env(path=os.path.expanduser("~/code/Code_Personal/voice_companion/.env")):
    for line in open(path):
        line = line.strip()
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1); _ENV[k.strip()] = v.strip().strip('"').strip("'")
load_env()
OPENAI_KEY = _ENV["OPENAI_API_KEY"]

# ---------- api usage tracking ----------
USAGE = {"chat_calls": 0, "chat_in": 0, "chat_out": 0, "embed_calls": 0, "embed_tok": 0}

def _post(url, payload, timeout=60):
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, data=json.dumps(payload).encode(),
                headers={"authorization": "Bearer " + OPENAI_KEY, "content-type": "application/json"})
            return json.loads(urllib.request.urlopen(req, timeout=timeout).read())
        except urllib.error.HTTPError as e:
            body = e.read().decode()[:200]
            if e.code in (429, 500, 502, 503) and attempt < 3:
                time.sleep(2 * (attempt + 1)); continue
            raise RuntimeError(f"HTTP {e.code}: {body}")
        except Exception as e:
            if attempt < 3: time.sleep(2 * (attempt + 1)); continue
            raise
    raise RuntimeError("unreachable")

def llm(prompt, system=None, max_tokens=300, temperature=0.4):
    msgs = ([{"role": "system", "content": system}] if system else []) + [{"role": "user", "content": prompt}]
    r = _post("https://api.openai.com/v1/chat/completions",
              {"model": CHAT_MODEL, "messages": msgs, "max_tokens": max_tokens, "temperature": temperature})
    u = r.get("usage", {})
    USAGE["chat_calls"] += 1; USAGE["chat_in"] += u.get("prompt_tokens", 0); USAGE["chat_out"] += u.get("completion_tokens", 0)
    return r["choices"][0]["message"]["content"].strip()

_EMB_CACHE = {}
def embed(texts):
    if isinstance(texts, str): texts = [texts]
    out, need, need_idx = [None] * len(texts), [], []
    for i, t in enumerate(texts):
        h = hashlib.md5(t.encode()).hexdigest()
        if h in _EMB_CACHE: out[i] = _EMB_CACHE[h]
        else: need.append(t); need_idx.append((i, h))
    if need:
        r = _post("https://api.openai.com/v1/embeddings", {"model": EMBED_MODEL, "input": need})
        USAGE["embed_calls"] += 1; USAGE["embed_tok"] += r.get("usage", {}).get("total_tokens", 0)
        for (i, h), d in zip(need_idx, r["data"]):
            v = np.array(d["embedding"], dtype=np.float32); _EMB_CACHE[h] = v; out[i] = v
    return out

def cos(a, b):
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-9))

# ---------- memory conditions ----------
class MemA:
    """No long-term memory. Only the shared working window (handled by runner)."""
    name = "A"
    def end_session(self, sid, events): pass
    def retrieve(self, query, now): return [], 0.0

class MemB:
    """Verbatim RAG: store every user turn verbatim; retrieve top-k by cosine; inject verbatim."""
    name = "B"
    def __init__(self): self.items = []  # {text, emb}
    def end_session(self, sid, events):
        for ev in events:
            self.items.append({"text": ev, "emb": embed(ev)[0]})
    def retrieve(self, query, now):
        if not self.items: return [], 0.0
        q = embed(query)[0]; t0 = time.perf_counter()
        scored = sorted(self.items, key=lambda m: cos(q, m["emb"]), reverse=True)[:RETRIEVE_K]
        dt = (time.perf_counter() - t0) * 1000
        return [("verbatim", m["text"]) for m in scored], dt

class MemBplus:
    """Curated static memory (active control): offline gist per event, retrieve top-k by cosine.
       NO decay, NO salience, NO consolidation."""
    name = "B+"
    def __init__(self): self.items = []  # {gist, emb}
    def end_session(self, sid, events):
        for ev in events:
            g = _gist(ev)
            self.items.append({"gist": g, "emb": embed(g)[0]})
    def retrieve(self, query, now):
        if not self.items: return [], 0.0
        q = embed(query)[0]; t0 = time.perf_counter()
        scored = sorted(self.items, key=lambda m: cos(q, m["emb"]), reverse=True)[:RETRIEVE_K]
        dt = (time.perf_counter() - t0) * 1000
        return [("gist", m["gist"]) for m in scored], dt

class MemC:
    """Profile C: salience-gated events, gist(+anchor), Ebbinghaus decay+reinforcement,
       episodic->semantic consolidation, gist-first retrieval."""
    name = "C"
    def __init__(self):
        self.episodes = []   # {gist, anchor, emb, S, last, salience}
        self.semantic = []   # {fact, emb, S, last, src}
    def end_session(self, sid, events):
        # salience-gated encoding + gist/anchor (one batched LLM call for salience)
        sals = _salience_batch(events)
        for ev, sal in zip(events, sals):
            g, anchor = _gist_anchor(ev)
            # stability scales with salience: low-salience (trivia) decays fast, salient content persists
            S0 = DECAY_S_BASE * max(0.1, sal)
            self.episodes.append({"gist": g, "anchor": anchor, "emb": embed(g)[0],
                                   "S": S0, "last": sid, "salience": sal})
        # consolidation: cluster episodes by gist similarity; abstract recurring -> semantic fact
        self._consolidate(sid)
    def _consolidate(self, now):
        used = set()
        for i, a in enumerate(self.episodes):
            if i in used: continue
            cluster = [i]
            for j in range(i + 1, len(self.episodes)):
                if j in used: continue
                if cos(a["emb"], self.episodes[j]["emb"]) > 0.55:
                    cluster.append(j)
            if len(cluster) >= CONSOLIDATE_N:
                gists = [self.episodes[k]["gist"] for k in cluster]
                fact = _semantic_fact(gists)
                # avoid duplicate semantic facts
                femb = embed(fact)[0]
                if all(cos(femb, s["emb"]) < 0.8 for s in self.semantic):
                    self.semantic.append({"fact": fact, "emb": femb, "S": DECAY_S_BASE * 2.5,
                                          "last": now, "src": [self.episodes[k]["gist"] for k in cluster]})
                for k in cluster: used.add(k)
    def _R(self, m, now):
        dt = max(0, now - m["last"])
        return math.exp(-dt / max(0.3, m["S"]))
    def retrieve(self, query, now):
        q = embed(query)[0]; t0 = time.perf_counter()
        cands = []
        for m in self.semantic:
            R = self._R(m, now)
            if R < FORGET_FLOOR: continue
            cands.append((cos(q, m["emb"]) * R * SEM_BONUS, ("semantic", m["fact"]), m))
        for m in self.episodes:
            R = self._R(m, now)
            if R < FORGET_FLOOR: continue
            cands.append((cos(q, m["emb"]) * R, ("episodic", m["gist"]), m))
        cands.sort(key=lambda x: x[0], reverse=True)
        top = cands[:RETRIEVE_K]
        dt = (time.perf_counter() - t0) * 1000
        # reinforcement (offline-queued in design; applied here post-retrieval)
        for _, _, m in top:
            m["S"] += 0.5; m["last"] = now
        return [payload for _, payload, _ in top], dt

# ---------- offline LLM ops ----------
def _gist(event_text):
    return llm(f"Paraphrase the essential meaning of this from a conversation, in ONE short sentence "
               f"(<=20 words), third person, keeping key entities and facts:\n\n{event_text}",
               max_tokens=60, temperature=0.2)

def _gist_anchor(event_text):
    r = llm(f"From this conversation snippet, output JSON with keys 'gist' (one <=20-word sentence "
            f"paraphrasing the meaning, third person) and 'anchor' (the single most important verbatim "
            f"quote, <=1 sentence):\n\n{event_text}", max_tokens=120, temperature=0.2)
    try:
        j = json.loads(r[r.index("{"):r.rindex("}") + 1]); return j.get("gist", "").strip(), j.get("anchor", "").strip()
    except Exception:
        return _gist(event_text), ""

def _salience_batch(events):
    joined = "\n".join(f"[{i}] {e}" for i, e in enumerate(events))
    r = llm("Rate each item's memory salience 0.0-1.0 for a personal companion. "
            "Pure trivia or incidental one-off details (weather, a forgotten film title, a place mentioned "
            "once in passing, small talk) -> 0.0-0.2. Core personal facts, names, allergies, emotions, "
            "commitments, and recurring concerns -> 0.7-1.0. "
            "Output a JSON list of floats, one per item, in order.\n\n" + joined, max_tokens=200, temperature=0.0)
    try:
        arr = json.loads(r[r.index("["):r.rindex("]") + 1]); arr = [float(x) for x in arr]
        if len(arr) == len(events): return arr
    except Exception: pass
    return [0.5] * len(events)

def _semantic_fact(gists):
    return llm("These recurring memories concern the same user. State ONE durable general fact about the "
               "user they imply, in <=15 words, third person (e.g. 'works under tight deadlines'):\n\n"
               + "\n".join(f"- {g}" for g in gists), max_tokens=40, temperature=0.2)

# ---------- agent + judge ----------
AGENT_SYS = ("You are a warm, brief voice companion. Reply in 1-3 sentences. Use the provided MEMORY "
             "naturally when relevant; never invent facts not in memory or the conversation. If memory is "
             "empty and you don't know, respond naturally without pretending to remember.")

def agent_reply(working, memory_ctx, user_turn):
    mem = "\n".join(f"- ({kind}) {txt}" for kind, txt in memory_ctx) or "(no long-term memory available)"
    convo = "\n".join(f"{r}: {t}" for r, t in working)
    prompt = f"MEMORY (long-term):\n{mem}\n\nRECENT CONVERSATION:\n{convo}\n\nUser: {user_turn}\n\nCompanion:"
    return llm(prompt, system=AGENT_SYS, max_tokens=120, temperature=0.5)

def judge_recall(fact, question, answer):
    r = llm(f"Question: {question}\nAnswer: {answer}\nDoes the answer correctly recall this fact: \"{fact}\"? "
            f"Reply strictly 'YES' or 'NO'.", max_tokens=4, temperature=0.0)
    return r.strip().upper().startswith("YES")

JUDGE_CONSTRUCTS = {
    "social_presence": "the sense of being with another social entity who is present and attentive",
    "alliance": "a bond-like working relationship; the user feels understood and supported",
    "humanlikeness": "the agent feels human-like rather than mechanical/tool-like",
    "intelligence": "the agent seems competent, knowledgeable, and sharp",
    "privacy_comfort": "the way it references past info feels comfortable and non-intrusive (not creepy/surveilling)",
}
def judge_transcript(transcript):
    scores = {}
    rubric = "\n".join(f"- {k}: {v}" for k, v in JUDGE_CONSTRUCTS.items())
    r = llm(f"You are rating a companion agent from a multi-session conversation transcript, as the user would "
            f"perceive it. Rate each construct 1-7 (1=very low, 7=very high):\n{rubric}\n\n"
            f"TRANSCRIPT:\n{transcript}\n\nOutput strict JSON mapping each construct name to an integer 1-7.",
            max_tokens=150, temperature=0.0)
    try:
        j = json.loads(r[r.index("{"):r.rindex("}") + 1])
        for k in JUDGE_CONSTRUCTS: scores[k] = int(j[k])
    except Exception:
        for k in JUDGE_CONSTRUCTS: scores[k] = None
    return scores

if __name__ == "__main__":
    # smoke test
    print("smoke: gist ->", _gist("I have a golden retriever named Bruno and I'm allergic to peanuts."))
    print("usage:", USAGE)
