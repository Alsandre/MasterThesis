# Georgian polish loop — resume playbook

Section-by-section Sonnet-5 polish of the Georgian translation, each verified against
the English + glossary before it lands. Both editions rebuild from source, so Georgian
polish flows into `thesis-ka` (body) and `thesis-en` (its Georgian abstract slot).

## Position — COMPLETE (30/30 sections + abstract + tables)
- DONE + committed: **ALL of §1–§5 (§1.1–§5.3)**, the **რეზიუმე/English Abstract** (`polish(abstract)`),
  and the **5-table terminology pass** (`polish(tables)`). 37 `polish(...)` commits total.
- The §5.3 closing line now echoes the thesis title (ასისტენტიდან თანამოსაუბრემდე ევოლუცია).
- The §5.3 & §2.3 headings + TOC were realigned to the glossary term (future work→სამომავლო გეგმები;
  LLM→დიდი ენობრივი მოდელი).
- Table pass also fixed the SAME terms wherever they lagged in body prose (curation→კურირება in 6
  paras; verbatim→სიტყვასიტყვითი; confound→ამრევი ფაქტორი; decay→დაქრობა), so the whole doc is
  now terminologically consistent.
- `git log --oneline | grep polish` is the authoritative done-list.

## Remaining open items (NOT part of the polish loop)
- Fold in the user's richer fluent Georgian abstract rewrite (Word/OneDrive) IF desired — the current
  რეზიუმე is now terminology-aligned, so this is optional, not required.
- VERIFIED_DATE (bibliography "last verified") = 04.07.2026 → set to real submission date if needed.
- Front-matter task #3 "fill front-matter facts" (no placeholders remain; confirm program/defense date).

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
