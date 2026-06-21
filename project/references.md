# References & Findings Journal

Interesting and relevant findings collected during thesis research. Each entry: what it says, why it matters for the thesis, citation. Facts below were verified against primary sources (June 2026 research sweep, adversarially fact-checked). ⭐ = load-bearing for the thesis argument.

**Thesis:** „სასაუბრო ხელოვნური ინტელექტი: ასისტენტიდან თანამოსაუბრემდე ევოლუცია" — GTU, Informatics & Control Systems faculty. Last updated: **2026-06-11**.

---

## Standing convention: vocabulary discipline (three tiers)

Rhetorical strategy for thesis + defense is **setup-then-conquer**: stay technical throughout; reveal the "companion" connection at the culmination (discussion chapter / defense finale). The word is rationed so the reveal lands. Decided 2026-06-11.

1. **თანამოსაუბრე (interlocutor)** — OUR term, the thesis's own axis. Defined technically in the introduction via measurable properties (context persistence, identity continuity, initiative). Default word everywhere in our own voice.
2. **„კომპანიონი" / "companion"** — the LITERATURE's genre label. Used only when citing the studied phenomenon ("ე.წ. „კომპანიონ" აპლიკაციები — Replika, Character.AI"). Always at arm's length: quoted, attributed, never adopted as our vocabulary.
3. **Measured constructs** — when naming the dependent variable, use what is actually measured: სოციალური თანდასწრება (social presence), მომხმარებელ-აგენტის ალიანსი (user-agent alliance), აღქმული ადამიანურობა (perceived humanlikeness) — the ASAQ constructs. Never "companionship-ness" as a measurement.

Defense line this buys: „ჩვენ არ ვზომავთ ‘კომპანიონობას' როგორც განწყობას — ვზომავთ ვალიდირებულ კონსტრუქტებს."
Guardrail: motivation must still appear early (intro) — millions of users, memory failures breaking relationships (F2) — described as the phenomenon under study without adopting the term.

---

## F1. The memory gap — hard numbers ⭐
LLM conversational memory measurably lags humans:
- **LoCoMo benchmark:** long-context LLMs and RAG still lag human performance by **56% overall and 73% on temporal reasoning** in very long-term conversational memory (conversations up to 35 sessions).
- **LongMemEval (ICLR 2025):** commercial chat assistants show a **30% accuracy drop** in memorizing information across sustained interactions (500 questions over 115K–1.5M-token histories; tests information extraction, multi-session reasoning, temporal reasoning, knowledge updates, abstention).
- Temporal reasoning is the worst failure category across every benchmark examined.

**Use in thesis:** quantitative backbone of the problem statement (intro, საკვლევი პრობლემა). Substantiates "memory is the binding constraint" since reasoning and TTS are not the bottleneck (F8).

> Maharana et al., "Evaluating Very Long-Term Conversational Memory of LLM Agents," ACL 2024, arXiv:2402.17753 · Wu et al., "LongMemEval," ICLR 2025, arXiv:2410.10813

## F2. Identity continuity matters as much as recall — the Replika mourning study ⭐
When a Replika update changed companion behavior (ERP feature removal, Feb 2023 — a natural experiment), users exhibited **genuine mourning and product devaluation, statistically mediated by perceived identity discontinuity** of the companion. Separately, qualitative analysis of r/Replika (120 posts, 2,917 comments) documents memory failures — forgetting names, preferences, life events — as relationship-breakers: "particularly disheartening" for users.

**Use in thesis:** elevates memory from a QA feature to the *substrate of relationship continuity* — the companion's remembered identity IS the relationship. Bridges the technical chapter (memory architecture) and the human chapter (perceived companionship). Central to the intro's actuality argument and the lit review's "your place" section.

> De Freitas, Castelo, Uğuralp & Oğuz-Uğuralp, HBS Working Paper 25-018 (rev. May 2025), arXiv:2412.14190 · Ma, Mei & Su, qualitative Replika study (r/Replika analysis)

## F3. Memory failures break the companion feeling; the industry just agreed
Replika users cite memory loss as the top relationship-breaking flaw (F2). In 2025–2026 the industry operationalized consolidation: OpenAI's "Dreaming V3" (June 2026) and Anthropic's agent "dreaming" research preview (May 2026) both implement sleep-like background memory reorganization. **Caution:** neither has a peer-reviewed paper — cite as industry signal, not science.

**Use in thesis:** actuality (აქტუალობა) — the problem the thesis addresses is the one the industry declared central this year.

## F4. Memory is double-edged: more recall ≠ more companionship ⭐
- **Cox, Lee & Ooi (HAI '23; n=169, 3-week between-subjects):** a chatbot referencing the user's utterances from previous sessions is perceived as **more intelligent and engaging — but verbatim references heighten privacy concerns**; paraphrased references win.
- **MemoryGraph pilot (CUI 2025):** remembering things made the chatbot sound **smarter but less trustworthy**, unless memory was observable/visualizable to the user.

**Use in thesis:** (a) motivates condition design (verbatim vs human-like is exactly our B vs C); (b) fuzzy-trace theory predicts the fix — humans store gist, not verbatim; gist-first recall may avoid the surveillance feeling; (c) the Cox study is the methodological template for our user study.

> Cox, Lee & Ooi, HAI '23, arXiv:2308.04879 · MemoryGraph, CUI 2025, doi:10.1145/3719160.3737617

## F5. The verified research gap = the thesis contribution ⭐
**No published study (as of June 2026) compares multiple human-memory-theory-grounded architectures on user-perceived companionship/humanlikeness.** Existing perception studies manipulate memory presence as a binary on one system; existing architecture comparisons evaluate QA accuracy only. The intersection is empty — three independent adversarial searches failed to refute this.

**Use in thesis:** the novelty claim (theoretical value; lit review "your place" section). Phrase carefully: "no controlled head-to-head comparison found," not "first ever."

## F6. Theory → implementation map (citation backbone for lit review)
| Human memory theory | LLM implementation | Venue |
|---|---|---|
| Hippocampal memory indexing (Teyler & DiScenna) | HippoRAG — LLM=neocortex, KG+PageRank=hippocampus | NeurIPS 2024, arXiv:2405.14831 |
| Episodic memory / event segmentation | EM-LLM — Bayesian-surprise event boundaries, temporally contiguous retrieval | ICLR 2025, arXiv:2407.09450 |
| Ebbinghaus forgetting curve | MemoryBank/SiliconFriend — R=e^(−t/S) decay+reinforcement; **companion chatbot, closest precedent** | AAAI 2024, arXiv:2305.10250 |
| Fuzzy-trace theory (gist vs verbatim) | ReadAgent — episode pagination + gisting | ICML 2024 (DeepMind), arXiv:2402.09727 |
| ~ACT-R-like activation (recency·importance·relevance) | Generative Agents — ⚠️ authors' own design; cite as "ACT-R-like," NOT ACT-R-grounded | UIST 2023, arXiv:2304.03442 |
| Zettelkasten (note: NOT a human-memory theory) | A-MEM — agentic linked notes | NeurIPS 2025, arXiv:2502.12110 |
| Complementary learning systems | HEMA et al. | various |

Useful survey scaffold: "From Human Memory to AI Memory" (arXiv:2504.15965) — maps agent memory onto sensory/working/episodic/semantic/procedural taxonomy.

## F7. Proactivity boosts engagement (supports optional condition D)
- **ComPeer (UIST 2024, n=24, 1 week):** LLM agent that detects significant dialogue events and plans timing/content of proactive care → increased engagement and perceived peer support vs user-initiated baseline.
- **Inner Thoughts (CHI 2025):** intrinsic-motivation proactivity model **preferred 82% of the time** over reactive baseline.
- Gap: nobody isolated the memory×proactivity interaction; nudge-frequency dose-response unquantified.

> ComPeer, arXiv:2407.18064 · Inner Thoughts, arXiv:2501.00383 · taxonomy survey arXiv:2404.12670

## F8. TTS/voice is good enough; modality alone is not the magic
- Utterance-level TTS at/near human parity (Sesame CSM blind tests: no preference between generated and real without context; ElevenLabs Flash ~75ms model latency). Speech-to-speech stacks: 450–900ms time-to-first-voice vs human turn-gap 0–200ms.
- ⚠️ **MIT Media Lab/OpenAI 4-week RCT (n=981): no causal effect of voice vs text on loneliness/dependence** — relational outcomes driven by usage patterns and user traits, not modality polish.

**Use in thesis:** justifies "memory is the binding constraint" assumption; caution against overclaiming voice benefits. Voice remains novel for *memory* research: all memory benchmarks are text-only (F10).

> MIT/OpenAI RCT: arXiv:2503.17473

## F9. Benchmark credibility crisis (cite, don't trust)
- Zep claimed 84% on LoCoMo → Mem0's replication measured 58.44% → Zep corrected to 75.14%. Public vendor dispute (github.com/getzep/zep-papers issue #5).
- Independent 2026 audit: **6.4% (99/1,540) of LoCoMo gold answers are wrong** (ceiling 93.57%); the LLM judge accepted intentionally wrong answers 62.8% of the time (github.com/dial481/locomo-audit).

**Use in thesis:** methodology chapter — treat as a finding; justifies running our own harness with re-validated judging; strong "limitations of existing research" item for the lit review.

## F10. Voice-specific memory is unstudied
All major memory benchmarks (LoCoMo, LongMemEval, MSC) are text-only. No published work addresses memory retrieval under real-time voice latency budgets (~200–500ms for natural turn-taking). The memory-creepiness tradeoff (F4) has only been established in text chat. **A voice companion study is novel by modality alone.**

## F11. Measurement instruments
| Instrument | What | Items | Status |
|---|---|---|---|
| **ASAQ** (TU Delft) — primary | 19 constructs incl. social presence, user-agent alliance, believability | 90 long / **24 short** | Validated (IJHCS 2025), CC BY 4.0, free: ii.tudelft.nl/evalquest |

**Canonical DV naming (decided 2026-06-21, consistency audit):** the third primary construct is named **"perceived humanlikeness"** everywhere in our own voice (aim, RQ1, H1, glossary); it is *operationalized* via ASAQ's **believability** subscale (+ Godspeed anthropomorphism). Don't use "believability" as the DV name — only as the instrument subscale. See §3.6 hypothesis↔instrument map in draft.md.
| Godspeed (Bartneck) | anthropomorphism, animacy, likeability, intelligence | 24 semantic differentials | Ubiquitous; psychometrically criticized — secondary |
| WAI-SR adaptation | working alliance (bond/goal/task) | 12 | Free for research; Woebot precedent (bond at human-therapy level in 5 days) |
| Machine Companionship Scale (Banks) | companionship-specific | TBD | Brand new 2025/26, unreplicated — optional |
| Cox-style privacy items | privacy concern re memory | few | Adapt from arXiv:2308.04879 |

## F12. Study-size norms (defends our n≈20)
Published norm for this class of system: GRACE n=21 (single session), ComPeer n=24 (1 week), OS-1 companion n=10+3 (2×7 days), Inner Thoughts n=24 formative (CHI 2025). HRI median sample is 21–37. A 20-participant, 2–3-week within-subject study is squarely in-norm.

## F13. Costs & billing
- Full LoCoMo run + LLM judge on Haiku 4.5 batch ≈ **$30–80**; entire experimental program < ~$300 (Sonnet-grade).
- ⚠️ **From June 15, 2026:** Anthropic moves `claude -p`/Agent SDK usage to a separate monthly credit pool (Max 5x = $100/mo, non-rollover). Voice Companion's master session uses `claude --print` → verify classification after the 15th; affects both the app and experiment budget.

## F14. Georgian language scope
- ElevenLabs Eleven v3 TTS supports Georgian (70+ languages); ElevenLabs Scribe STT: **10.9% WER on Georgian FLEURS**.
- Open-source Georgian ASR weak: fine-tuned Whisper ≈ 32 WER, only ~163h training data. No Georgian dialogue benchmark exists at all.
- **Decision:** thesis written in Georgian; system + experiments in English; scripted Georgian voice demo via ElevenLabs in the outlook chapter. (A tiny Georgian measurement = citable novelty if time permits.)

## F15. Plagiarism check — exact rules for master's theses (GTU regulation)
From `plagiarism-regulation.pdf` (Article 5.10 + annexes), verified by direct reading:
- Tool: **Strikeplagiarism.com**, run by a faculty operator; result within ~5 working days.
- Thresholds for a master's thesis (Georgian-language): **SC1 ≤ 60%** (share of text containing ≥5-word phrases matching other sources), **SC2 ≤ 10%** (≥25-word matching fragments), **QC3 ≤ 25%** (quotations). [Corrected 2026-06-21 by compliance audit — was QC3 ≤30%, which is the *bachelor's* threshold.]
- If thresholds are exceeded: work is returned, not accepted. Re-checks allowed **max 3 times total** (incl. the first); repeat checks cost 50 GEL.
- If the operator/department suspects plagiarism on review, an appeal path exists (Article 7).
- Author signs a declaration (Annex 2): "ნაშრომი მომზადებულია ჩემ მიერ და იგი არ არღვევს მესამე პირთა საავტორო უფლებებს" + printed/electronic versions identical.
- **The regulation contains NO AI-content clause** — it is entirely text-similarity based. (The Strikeplagiarism platform itself has offered an AI-detection module in recent years; whether GTU uses/acts on it is not specified in any document we have → ask the lecturer.)

**Use in thesis (process):** SC2 ≤10% is the binding constraint in practice — avoid any ≥25-word run that tracks a source's wording; paraphrase from notes, never from open source text. QC3 30% is generous — direct quotes are safe when marked and cited.

## F16. Companion-oriented use at scale (supports the actuality claim)
Zhang Y., Zhao D., Hancock J.T., Kraut R., Yang D., "The Rise of AI Companions: Interaction with AI Companions and Psychological Well-being" (arXiv:2506.12605, 2025): analysis of n=1,131 Character.AI users plus 4,664 chat sessions documents widespread companionship-oriented use of general-purpose chatbot platforms. ⚠️ Correlational study with negative well-being associations — do NOT cite for causal claims in either direction (see F8 caution and the MIT/OpenAI RCT null result).

**Use in thesis:** intro §1.3 actuality, cited as [5] — phrased as „ფართოდ გავრცელებული პრაქტიკა" (widespread practice), not „მასობრივი" (mass), per fact-check correction 2026-06-12.

## F17. Systematic audit (2026-06-21) — system-feasibility HARD BLOCKERS + consistency fixes ⭐
7-agent read-only audit (consistency, citation re-verification, GTU compliance, architecture map, feasibility, adversarial blocker-verification). Both hard blockers **confirmed by independent skeptics** reading the real `voice_companion` code.

### System reality (architecture map, verified)
- **Voice pipeline:** Whisper STT → local Qwen *or* OpenAI Realtime → Kokoro TTS; turn-based, ~2–5 s latency. Conversation memory is a **volatile in-process array** (`voicePipeline.js:102`, `MAX_HISTORY=20`, wiped each session).
- **No retrieval layer exists:** repo-wide grep for embeddings/vector/sqlite/faiss/chroma = **zero**.
- **The "brain" the gadget talks to** is the persistent master Claude Code session JSONL (`masterSession.js`), but it is **off the voice path** (reached only from the gadget *text box*, never from `voicePipeline`) and is **CC's opaque internal context management — not an instrumentable, swappable memory module**.
- **Single-user:** one global UUID, "Lekso" hardcoded in 4+ files, shared un-namespaced data dir, **no participant-id concept** (grep = zero), hardcoded ports 8321/8322, no electron-builder build config, macOS-native deps, 470 MB local ML stack launched by hand.
- **Logging that does exist:** `conversation-log.jsonl`, `decision-log.jsonl`, `task-history.jsonl`, orchestrator-actions.

### HARD BLOCKER 1 — agent is memoryless; brain memory opaque & unswappable (confirmed-hard)
The IV *is* memory (A/B/C). Today only **condition A (no memory)** is supported. Profiles **B (verbatim RAG) and C (human-modeled) do not exist and have no cheap mount point** — both must be built from scratch + a new voice→memory hook. Estimate **~4–8 weeks**, and that is *before* §3.2 (the actual profile-C design) is specified. No workaround found.

### HARD BLOCKER 2 — single-user; undeployable to 20 participants (confirmed-hard, *understated*)
Needs 20 isolated participants; the app can't reach them. Escape hatches all fail (20 macOS accounts collide on hardcoded ports + each needs its own Claude Max subscription; no build config; native deps). Realistic path: parameterize participant id (~1–2 wk) **plus** build a deployable client. No cheaper option exists.

### Other findings
- **Citation re-verification: CLEAN** — all load-bearing numbers and the riskiest bib entries ([8] EM-LLM, [9] ReadAgent, [27] A-MEM, [29] Mem0, [30] Zep, [31] Zacks) re-confirmed against primary sources. Prior work held. ([34] MemoryGraph authors still TODO; MSC added as [35], confirmed.)
- **Compliance gaps:** plagiarism declaration / Strikeplagiarism submission not tracked → now in draft.md Part 0; QC3 threshold corrected to ≤25% (master's); bibliography not yet in instruction §1.4 element order; "სურათების ნუსხა" vs instruction's "ნახაზების ნუსხა" (cosmetic).
- **Only ~15–20% of the study's system needs exist today** (condition A + logging + ASAQ/n≈20 scaffolding). B and C — the entire IV — are greenfield (~6–10 wk) gated behind an undefined §3.2.

### Open design questions exposed (author's call, before any build)
1. **Which brain?** local Qwen vs OpenAI Realtime vs the CC master session — each differs in memory-control and per-participant cost.
2. **§3.2 "profile C" is undefined** — salience/decay/consolidation/gist is a *name*, not a design. It is the intellectual core and must be designed *before* code.
3. Will master/RHM/ContextManager be kept or removed for the study build?

### Strategic implication
The thesis is in good shape; the system is **not** ready to be its apparatus, and the gap is bigger than the docs imply. **Build must not start before §3.2 is designed, a brain is chosen, and Sopho signs off stage 1** — else risk 8 weeks building B/C that a direction-correction invalidates. Reconnects to the [[master-thesis]] study-vs-demo / silicon-agents decision.

### Consistency fixes applied (8 issues, 2026-06-21)
(1) humanlikeness added to H1; (2) H2a/H2b marked secondary + hypothesis↔instrument map added (§3.6); (3) initiative stated as testable only in optional D; (4) DV naming canonicalized to "perceived humanlikeness"; (5) MSC bib entry [35] added; (6) unquoted "companion-genre" fixed; (7) modality-held-constant clause added (§1.2, §2.8); (8) benchmark verbs harmonized (KA §1.1).

## F18. Profile-C pressure-test (2026-06-22) — the central contrast is underpowered; reframe required ⭐⭐
5-agent adversarial pressure-test (statistician, null-skeptic, engineer, cognitive scientist → verdict). **Verdict: go-with-adjustments, 3 arms.** The dominant, unrefuted fact:

### The central contrast C>B+ cannot be a confirmatory test at n≈20
- **Effect-size priors** (grounded in Cox n=169 [11], a 142-paper social-cue meta-analysis g≈0.36, MemoryGraph): C>A is **large** (dz≈0.65–0.84); C>B small-medium (dz≈0.40); B+>B small (dz≈0.35); **C>B+ (the F5 novelty) is the SMALLEST — dz≈0.28 saturated, ~0.14–0.20 after cold-start dilution.** By construction it must be smallest: B+ already captures presence + clean gist/paraphrase, the two most robustly-supported memory wins.
- **Power:** at n=20 within-subject, Holm-corrected, the smallest detectable dz is **~0.78 (3-arm) to ~0.86 (4-arm)**. C>B+ realized power **2–12%.** Powering it needs **n≈116–159** — infeasible for the HRI/CUI class (F12 norm 20–24). n=30 doesn't rescue it (~17%).
- **4 arms is strictly WORSE:** the 6-comparison penalty raises every threshold and adds ~50% participant burden, buying only the C>A/B>A wins that are already near-certain.

### Null-risk on C>B+ rated HIGH (independent of power)
Memory *dynamics* (decay/salience/consolidation) over clean static memory may add little perceptual margin; forgetting is a documented **negative** interpersonal signal (an n=60 robot study: a forgetting robot lost perceived competence/trust). Consolidation is the only C-only stage with a *positive* mechanism and the slowest to accrue (cold-start).

### THE REFRAME (the decision this forces — Sopho-level)
**Stake the thesis on the curation-controlled APPARATUS + a sign-agnostic measurement, NOT on a positive C>B+.** Pre-register C>B+ as an **estimation target** (mean diff + 95% CI + dz, precision/equivalence logic); pre-register C>A and directional B+>B/C>B as the confirmatory tests where power exists. A clean **null is publishable**: "the perceptual value of 'human-like memory' is carried by gist-curation + presence, not by Ebbinghaus decay / salience / CLS consolidation" overturns a field assumption — and the B+ control was *designed* to make that interpretable. Pre-register null-handling so it reads as anticipated, not salvaged.

### Adjustments (full list in profile-c-design.md §8)
3 arms (B/B+/C, n=20, full 3 wk), A → short calibration touch · analyze the **late/post-consolidation window** (not grand mean) + log consolidation density as covariate · **warm, attributable forgetting** as a pre-registered rule (neutralizes the "being forgotten = I matter less" negative) · **amplify consolidation** (C verbalizes "I've noticed you tend to…") · add **event-sensitive + behavioral DVs + mandatory coded interviews** as null-insurance · honest theory relabeling ("composes" not "unifies" 5 theories; CLS as spirit-of-transfer; salience cited with levels-of-processing + emotional modulation; name omitted interference/reconstructive-distortion).

### Build (engineer): realistic **12–16 weeks** solo (consistent with F17), deployability under-counted. **Cheapest viable cut ~8–10 wk:** keep B+ + consolidation + simple lazy decay + gist/anchor; defer salience-gating, associative pre-expansion, anchor-regex, programmatic sensitivity sweep. **Cutting B+ or consolidation breaks the central claim — off the table.**

### Theory (cognitive scientist): the engine is genuinely ONE coherent object (chief virtue), B+ is its strongest methodological achievement. Hardest defense attacks: "your forgetting omits interference (the dominant human-forgetting dynamic)"; "precision-first consolidation engineers OUT the gist false-memory/schema distortion that fuzzy-trace + CLS most distinctively predict — on your primary humanlikeness axis"; "CLS is a misnomer (schema abstraction ≠ interleaved interference-protected learning)"; "salience-as-Atkinson-Shiffrin is really Craik-Lockhart depth-of-processing." → pre-empt in §3.2.

---

## Key resource links
- MemoryBank/SiliconFriend: https://arxiv.org/abs/2305.10250 · github.com/zhongwanjun/MemoryBank-SiliconFriend
- HippoRAG: https://arxiv.org/abs/2405.14831 · github.com/OSU-NLP-Group/HippoRAG
- EM-LLM: https://arxiv.org/abs/2407.09450 · github.com/em-llm/EM-LLM-model
- Cox et al. (memory references): https://arxiv.org/abs/2308.04879
- ComPeer: https://arxiv.org/abs/2407.18064 · Inner Thoughts: https://arxiv.org/abs/2501.00383
- ASAQ instrument: https://ii.tudelft.nl/evalquest/web/node/1
- LongMemEval: https://github.com/xiaowu0162/longmemeval (HF: xiaowu0162/longmemeval-cleaned)
- LoCoMo: https://github.com/snap-research/locomo · audit: https://github.com/dial481/locomo-audit
- Replika identity discontinuity: https://arxiv.org/pdf/2412.14190
- Survey "From Human Memory to AI Memory": https://arxiv.org/abs/2504.15965
- Generative Agents: https://arxiv.org/abs/2304.03442 · MemGPT/Letta: https://arxiv.org/abs/2310.08560
- Mem0: https://github.com/mem0ai/mem0 · Graphiti/Zep: https://github.com/getzep/graphiti
- Embedded vector stores: sqlite-vec (github.com/asg017/sqlite-vec) · LanceDB (github.com/lancedb/lancedb)
- Ollama embeddings: bge-m3 (1.2GB), nomic-embed-text (274MB), qwen3-embedding (639MB)

## Decision log
| Date | Decision |
|---|---|
| 2026-06-09 | Thesis workspace created |
| 2026-06-10 | University docs received (lecturer note, topics, formatting instructions, template, regulations) |
| 2026-06-11 | Title submitted: „სასაუბრო ხელოვნური ინტელექტი: ასისტენტიდან თანამოსაუბრემდე ევოლუცია" |
| 2026-06-11 | Research-direction sweep completed (8 agents, fact-checked); **Direction 1 chosen** (theory-grounded memory × perceived companionship) |
| 2026-06-11 | `project/` folder structure: `draft.md` (thesis text) + `references.md` (this journal) |
| 2026-06-11 | Vocabulary discipline adopted (three tiers, setup-then-conquer); terminology pass applied to draft.md |
| 2026-06-12 | §1 drafted (v1→v3): four-lens review + red-team applied; bibliography verified; defense-prep.md created |
| 2026-06-13 | Workflow pivot: English master (`draft-en.md`) + Lekso's manual Georgian translation as the authorship/learning step; `glossary.md` made binding; EN copy not published before defense |
| 2026-06-13 | §2 (Literature Review, Rich) drafted in EN → four-lens review + red-team applied (v2); bibliography extended [20]–[34], all verified; defense-prep Q9–Q15 added. Key fixes: event-segmentation correctly attributed to Zacks [31] not Tulving; "single-theory" framing sharpened to avoid strawman; glossary "companion" leaks quoted; voice-RCT [15] folded in as a strength |
| 2026-06-21 | GTU-compliant skeleton built into draft.md (front/back matter + §3–§5 sub-skeletons) |
| 2026-06-21 | **Systematic audit (F17):** 2 hard system-feasibility blockers confirmed (memoryless voice agent / opaque unswappable brain; single-user undeployable). Citation re-verification clean. 8 consistency issues fixed; MSC added [35]; QC3 threshold corrected. Build gated behind §3.2 design + brain choice + Sopho sign-off |
