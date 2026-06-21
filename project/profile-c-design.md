# Profile C — Human-Memory Architecture (Design Spec for §3.2)

**Status:** design v1, 2026-06-21 — paper-only (no code). Produced by a 3-design tournament + adversarial critique + synthesis. Source for the future §3.2 thesis prose AND the eventual build blueprint. Grounding: `references.md` F6 (theory→implementation map), F17 (system constraints), `draft-en.md` §2.2 (behavioral signatures).

> **This is a design proposal for Lekso's review, not an approved spec.** Decisions flagged 🔶 are his to make. The B+ control (below) is a non-trivial change to the experiment.

---

## 0. Organizing principle

Within an **identical inference-time envelope** (same LLM brain, retrieval trigger, injection point, per-turn latency, total retrievable-token budget, *and* matched effective history-coverage), **Profile C injects what a human would remember** — salience-gated, gist-compressed, time-decayed, offline-consolidated episodic→semantic knowledge — **while B injects what a recorder replays.** The independent variable is the *human-memory dynamics of the process*, isolated from generic LLM curation by a **B+ active control** that receives the same offline gisting/cleanup but none of the decay/salience/consolidation.

**Memory unit = the EVENT** (a Tulving episode [22]): a topically/temporally bounded segment of contiguous turns, not the raw turn (B's unit) and not an isolated extracted fact (which would import a second, B-absent confound — fact selection). The event is the episodic atom; consolidation later distills recurring events into a second, derived unit — a durable **semantic profile fact**.

---

## 1. The five-stage memory lifecycle

Each stage names: **mechanism · theory grounding (F-number) · observable behavioral signature · timing (sync/async) · parameters**.

### Stage 1 — Encoding (salience-gated write) · *async*
- **Mechanism:** raw turns live only in the volatile ~20-turn working window (shared verbatim with A and B — held constant). Nothing graduates to long-term store synchronously. Asynchronously at session end: (a) segment the buffered transcript into **events** at embedding-distance/time-gap boundaries (cheap stand-in for EM-LLM Bayesian-surprise [8]); (b) one small-LLM rubric call scores **salience S0∈[0,1]** from four a-priori-fixed dimensions — self-disclosure density, emotional intensity, explicit emphasis/repetition, goal/commitment content. Below-floor events are **soft-discarded** (written at very low stability — a tip-of-the-tongue trace recoverable under strong cue), not hard-deleted. Survivors get initial stability `S0_stability = S_base·(1 + k·S0)`.
- **Grounding:** Atkinson–Shiffrin multi-store [20] — rehearsal/attention as the STS→LTS gate (F6 modal-model row). Event boundaries: Tulving [22] + Zacks [31] via EM-LLM [8]. Note: salience is used at **write** time (encoding selectivity) — distinct from Generative Agents' *retrieval-only* importance, which F6 flags as ACT-R-*like*, not theory-grounded.
- **Signature:** durably keeps what the user stressed/disclosed/revisited; lets incidental small-talk fade; memories organized around episodes ("when you told me about the move"), not stray sentences. Soft-discarded trivia is weakly reconstructable under explicit cue → forgetting reads as *warm*, not *not-listening*.

### Stage 2 — Representation (gist + verbatim anchor, dual-decay) · *async*
- **Mechanism:** each event stores a **gist** (one ~30–50-token paraphrase of meaning/entities/stance) + structured slots + a single **verbatim anchor** (≤1 sentence, the most salient quote, retained for grounding/audit but *not* the default payload). The gist is embedded and injected. Gist stability `S_gist` > anchor stability `S_anchor` (gist outlives wording). **Fairness constraint: per-event gist payload ≤ B's average per-turn verbatim payload** — C is never given fatter context items.
- **Grounding:** fuzzy-trace [24] (F6 ReadAgent row) — parallel verbatim+gist, gist more durable; ReadAgent gisting [9]. Directly targets the Cox finding [11] (F4): paraphrase preferred, verbatim raises privacy concern.
- **Signature:** the agent paraphrases ("you'd been worried about a deadline") rather than quoting; a user cannot catch it parroting the transcript. **This is the single most user-detectable C-vs-B difference and the lever H2b (privacy/trust) targets.**

### Stage 3 — Decay + reinforcement (Ebbinghaus, lazy) · *both*
- **Mechanism:** each trace has retrievability `R = exp(−Δt / S)` computed **lazily at retrieval time** as a score multiplier (no background ticking, no synchronous write). On successful re-mention, spaced-repetition reinforcement grows `S` and resets last-access; the write-back is **queued offline** so the synchronous path stays read-only like B. Sub-floor traces (R < ε) are excluded and pruned offline only once absorbed into a semantic fact.
- **Grounding:** Ebbinghaus [23] (F6 MemoryBank row); precedent MemoryBank/SiliconFriend [6]. Semantic facts (stage 4) decay too (not near-permanent) so the Ebbinghaus dynamic stays the live IV, not a cosmetic layer.
- **Signature:** mentioned-once-long-ago fades; returned-to-repeatedly becomes rock-solid. B has no decay → C's "natural forgetting" vs B's "eerie total recall."

### Stage 4 — Consolidation (episodic→semantic, offline "sleep") · *async*
- **Mechanism:** offline batch job between sessions. (a) cluster episodic events by entity/gist similarity; (b) for clusters recurring across ≥N events, one small-LLM call abstracts a durable **semantic profile fact** ("works under tight deadlines") with HippoRAG-style [7] back-pointers to source episodes; (c) down-weight/prune absorbed episodes (replay-then-transfer); (d) resolve contradictions toward most-recent/most-reinforced; (e) **pre-expand** associative neighbours offline (so any associative recall at inference is a single vector query — no synchronous graph traversal). The shared LLM is never retrained; consolidation only reorganizes the store.
- **Grounding:** complementary learning systems [25] (F6 "dreaming" row); Tulving episodic→semantic [22]; hippocampal indexing [26]/[7]; industry "dreaming" signal [18,19] (cited as signal, not science).
- **Signature:** over weeks the agent shifts from "last Tuesday you said…" to "I know you tend to…" — it sounds like it **learned** about the user, an emergent generalization it never literally heard. **The single most C-distinctive, B-impossible behavior, and the predicted source of C's relational advantage.**

### Stage 5 — Retrieval (gist-first, composite-scored, single read-only query) · *sync*
- **Mechanism:** same trigger/injection point as B. (a) embed the current turn (the only sync embedding, identical to B); (b) **one** vector query returning ~20 candidates across both tiers, incl. offline-pre-expanded associative neighbours; (c) rank by `activation = relevance(cosine) · R(decay) · capped semantic-bonus` — **salience is NOT a retrieval term** (it gates write + decay only; this removes the triple-counting the critique flagged); all exponents fixed at 1; (d) fill **exactly B's token budget**, semantic-first; verbatim anchor included only on an explicit exact-recall request via a **cheap deterministic regex/keyword trigger** (zero in-turn LLM calls ever); (e) reinforcement/last-access queued offline.
- **Grounding:** Tulving cue-dependent retrieval [22]; fuzzy-trace gist-first [24]; Ebbinghaus retrievability [23]; CLS semantic-preference [25]; hippocampal reconstruction [26]/[7] (pre-expanded offline).
- **Signature:** surfaces the relevant generalization first, the specific episode only if pressed — recall feels like a person who "knows you," not a search engine. Same latency + budget as B; different content.

---

## 2. The fairness architecture (the central methodological achievement)

The whole study lives or dies on this: **C must win because of *how* it remembers, not because it remembers *more* or *cleaner*.** Three confounds and their controls:

| Confound | Control |
|---|---|
| **Curation/legibility** — C's gisted, coreference-resolved prose is just more legible than B's raw fragments | **🔶 B+ ACTIVE CONTROL:** identical offline LLM gisting/cleanup, same compression + token budget, but **NO decay, NO salience-gating, NO consolidation** — pure cosine top-k over cleaned gists. `C > B+` ⟹ the effect is human-memory *dynamics*. `C ≈ B+` ⟹ it was legibility, and the claim is revised honestly. |
| **Compression** — equal tokens ≠ equal information | effective **history-coverage logged per turn** as a manipulation check; B+ holds compression constant |
| **Compute/storage/latency** — extra offline LLM passes | all expensive ops **offline** (the CLS "sleep" premise); synchronous path read-only, zero in-turn LLM calls, per-turn retrieval latency **measured + reported** for B/B+/C; per-event payload ≤ B's |

**Held constant across A/B/B+/C:** LLM brain, retrieval trigger, injection point, per-turn latency budget, total retrievable-token budget, query embedding model, volatile working window.

---

## 3. Parameters & how each is set (defeats cherry-picking)

| Parameter | Value | How set |
|---|---|---|
| `MAX_HISTORY` (working window) | ~20 turns | Atkinson–Shiffrin STS [20]; identical to A/B (constant) |
| `τ_seg` (event boundary) | pilot → ~F1 vs human boundary labels | calibrated to human topic-shift judgments, **not** the outcome |
| salience rubric (dims + prompt) | fixed a priori; prompt pre-registered verbatim | dimensions from §2.2 multi-store signature; LLM tag **validated vs ≥2–3 human annotators** (report agreement) |
| `τ_write` + soft-discard | write-rate ≈ human-consensus "worth-remembering" fraction | external behavioral target, not the social DV |
| `k` (salience→stability) | 1.0 (fixed) | removes a free knob; max salience exactly doubles initial stability |
| `S_gist : S_anchor` | >1 (theory); ~3:1 magnitude | direction fixed by fuzzy-trace; magnitude pilot-calibrated |
| `S_base, α, ε` (decay) | seeded from MemoryBank [6] | **externally anchored** + **required sensitivity analysis** (S_base ½×/2×, α, ε, power-law variant) |
| `N` + cluster cutoff (consolidation) | N≥2–3, cosine ~0.75 | precision-first; pre-registered |
| activation form | `relevance · R · capped-bonus`, exponents=1 | salience dropped as retrieval term; no free weights |
| token budget + history-coverage | identical to B; coverage logged | the central confound control |

**Everything pre-registered before data collection.** Decay timescale tied to the 2–3 week window via a-priori **power analysis** (so a null isn't just cold-start).

---

## 4. Latency (fits the F17 ~2–5 s voice turn)

Synchronous per turn: embed (≈tens of ms, = B) → **one** vector query (sqlite-vec/LanceDB, <100 ms) → O(k≈20) arithmetic (decay read lazily) → select to budget → inject + LLM. Same *shape* of work as B; added cost is sub-ms arithmetic dwarfed by STT/LLM/TTS. **Zero in-turn LLM calls** (deterministic verbatim trigger). Read-only hot path (reinforcement queued offline). Associative expansion pre-computed offline. **All** expensive ops (segmentation, salience scoring, gisting, consolidation) are offline. Parity reported empirically, not asserted.

---

## 5. Top failure modes → mitigations (full list in workflow output)
- **Legibility confound (THE threat)** → B+ active control.
- **Over-aggressive forgetting reading as worse than B** (the F2 relationship-breaker) → soft-discard (no literal blanks); identity facts (names/commitments) at high stability; decay externally anchored + sensitivity-tested.
- **False consolidation** (confident wrong generalization, *worse* than B because persistent) → N≥2–3 + cutoff (precision-first); source pointers; contradiction-resolution; pilot spot-audit.
- **Cold-start / usage confound** (C's strength scales with chattiness) → 2–3 wk horizon; saturation/power analysis; consolidation-density logged as covariate; optional scripted seeding for low-usage users.
- **Within-subject carryover** (C's consolidation contaminates B rating) → isolated per-condition stores, counterbalanced order, washout, pre-registered order-effect test, consider a between-subjects arm.
- **Decay made cosmetic** (semantic facts near-permanent) → semantic facts decay too; bonus capped; report per-tier retrieval share over time.

---

## 6. 🔶 Design implications that ripple into the rest of the thesis (Lekso's decisions)

1. **The B+ control adds a 4th condition (A / B / B+ / C).** This is the right science but **4 within-subject arms × 2–3 weeks is likely infeasible** (8–12 weeks/participant). Options: (a) shorter per-condition exposure; (b) drop A (no-memory is an obvious floor — maybe a short calibration arm, not a full phase); (c) some arms between-subjects; (d) B vs B+ vs C only. **This is the biggest open methods decision and needs Sopho's input.**
2. **Hypotheses refine:** the *strong* claim becomes **C > B+** (isolates dynamics); C > B and B+ > B are secondary/expected. Update H1 once the condition set is fixed.
3. **Pre-registration becomes central** — the design's defensibility rests on pre-registering parameters, the sensitivity analysis, and the analysis plan. Worth an explicit §3.8 subsection.
4. **"Which brain" still open** — the offline passes (salience, gist, consolidation) need *a* small LLM (cheap, any provider); the *conversational* brain choice is separate and still to decide (F17 open Q).
5. **§3.2 thesis prose** will condense this doc; §3.3 (profiles table) gains B+; §3.8 (analysis) gains the sensitivity + power + pre-registration detail.

---

## 7. How this differs from prior systems (defense-ready)
- **MemoryBank/SiliconFriend [6]:** only the Ebbinghaus row (decay+reinforcement) on *verbatim* text — no gist coding, no event segmentation, no episodic→semantic consolidation.
- **Generative Agents [10]:** recency×importance×relevance, author-stated *not* theory-grounded (ACT-R-like, F6) — no Ebbinghaus, no fuzzy-trace dual code, no CLS consolidation.
- **C integrates all five committed theories** into one lifecycle and — crucially — is the first (in the literature available to us) evaluated on *perceived social constructs* with a curation-controlled design.
