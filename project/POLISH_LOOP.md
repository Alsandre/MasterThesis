# Georgian polish loop — resume playbook

Section-by-section Sonnet-5 polish of the Georgian translation, each verified against
the English + glossary before it lands. Both editions rebuild from source, so Georgian
polish flows into `thesis-ka` (body) and `thesis-en` (its Georgian abstract slot).

## Position at pause  (25/30 sections)
- DONE + committed: **§1 (1.1–1.6), §2 (2.1–2.8), §3 (3.1–3.8), §4.1, §4.2**
- IN FLIGHT at pause: **§4.3** — Sonnet-5 agent writing `scratchpad/polished_4.3.json`.
  ON RESUME: if that file exists & is valid JSON (3 prose units: 140,142,143 — 141 is Table 4.3),
  verify + write back + commit; else relaunch the §4.3 polish agent.
- REMAINING: §4.3, §4.4, §4.5, §5.1, §5.2, §5.3, then a **TABLE-TERMINOLOGY pass** over the
  5 tables (2.1, 3.1, 4.1, 4.2, 4.3) which the prose loop skips (extractor drops tables).
- `git log --oneline` is the authoritative done-list (one `polish(§x.y)` commit per section).

## Per-section mechanism
1. Extract: `python3 project/assemble/extract_chunk.py <sec>`  → JSON {units:[{i,type,en,ka}]}.
2. Polish: spawn a **Sonnet-5** agent (model: sonnet, general-purpose) that runs the extract,
   Reads `project/glossary.md`, revises each unit's Georgian, and writes
   `scratchpad/polished_<sec>.json` = `[{i,polished,note}]` — SAME unit count/order/`i`.
   Split large sections (>~6k KA chars / 8 units) into parallel halves by i-range (a/b), then combine.
   (§3.2 kept dropping mid-response as one pass → splitting fixed it.)
3. Verify (me): per-unit citations `[N]` preserved, all numbers/decimals preserved, honesty
   hedges intact, no discouraged forms (`შკალა ინტერაქცი სიგნატურ საუბრული ლატენტურ`), no ASCII quotes.
   NB: string checks often false-negative (spelled numbers, transliteration variants) — read to confirm.
4. Write back: append `{old: extracted ka, new: polished}` per unit to
   `project/assemble/corrections.json` (atomic tmp+rename), then rebuild BOTH:
   `python3 project/assemble/build.py && python3 format_thesis.py project/thesis-ka.docx`
   `python3 project/assemble/build_en.py && python3 format_thesis.py project/thesis-en.docx`
5. Commit per section (`polish(§x.y): …`, co-author Claude Opus 4.8 (1M context)).

## Polish-agent brief essentials
- English is the meaning anchor; preserve meaning EXACTLY, don't simplify; keep every citation,
  number, model name (gpt-4o-mini, text-embedding-3-small), and system/proper name.
- Style: inanimate plural subject → SINGULAR verb; „…" quotes; ~45-word ceiling; verbs one notch
  below the evidence; hedged novelty (never „პირველად").
- HONESTY (critical): PoC results are REAL; the human-subject study is FUTURE WORK / NOT conducted —
  never render it as done (use `ჩასატარებელი`/`ჯერ ჩაუტარებელი`, never `ჩატარებული`, for the human
  study); "no claim rests on human data"; don't strengthen/weaken any claim.
- Decided standard terms: future work→`სამომავლო გეგმები`; proof of concept→`კონცეფციის დამტკიცება`;
  behavioral signature→`ქცევითი ნიშან-თვისება`; user–agent alliance→`მომხმარებლისა და ხელოვნური აგენტის ალიანსი`;
  benchmark→`ეტალონური შეფასების ნაკრები (ბენჩმარკი)`; complementary learning systems→`კომპლემენტარული სასწავლო სისტემები`.

## Section anchors still to protect
- §4.3: privacy-comfort INVERSION (verbatim B/B+ = 7.00 highest, C = 5.67 lowest; OPPOSITE of human Cox [11]); small illustrative sample, no significance; C ≯ B+ on any construct.
- §4.4 Discussion: the dissociation (most-human C not judge-preferred); privacy inversion = demonstration-by-counterexample → human study is a NECESSITY, not discretionary.
- §4.5 Limitations: 3 personas/4 sessions/single judge pass; simulated≠human; session-units time; gpt-4o-mini ≠ eventual voice brain; transcripts not live voice.
- §5.1 three contributions (Profile C; B+ active control; PoC + two-track eval). §5.2 findings. §5.3 future work (full build; human study §3.5c; theoretical extension).

## Other open items (pre-loop)
- Sonnet's fluent Georgian abstract rewrite lives only in the Word copy — fold into source when finalized.
- VERIFIED_DATE (bibliography "last verified") = 04.07.2026 — change to real submission date if needed.
