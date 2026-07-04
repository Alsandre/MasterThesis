---
description: Format the thesis .docx to GTU/reference spec and regenerate the TOC, then verify.
argument-hint: "[docx path — defaults to project/thesis-ka.docx]"
---

Run the repeatable thesis formatter and verify the result. **Formatting only —
never edit wording or content.**

1. **Run it** from the repo root: `python3 format_thesis.py $ARGUMENTS`
   (no argument → it defaults to `project/thesis-ka.docx`). Show its log output.
   If it errors, stop and report the traceback — don't press on.

2. **Verify** by rendering the docx to PDF with LibreOffice headless
   (`/Applications/LibreOffice.app/Contents/MacOS/soffice --headless --convert-to
   pdf --outdir <scratch> <docx>`) into a scratch dir, then check:
   - TOC page: dot leaders + page numbers present, **no `XPGX` placeholders, no
     duplicate entries**
   - one chapter heading: black, centered, bold, on its own page
   - the **List of Figures / List of Tables sections still exist** (not deleted)

3. **Report**: what changed (from the formatter's log), the spot-check results,
   and any warnings (e.g. unresolved TOC page numbers). Remind me that TOC page
   numbers are LibreOffice-computed (verify in Word before submission) and that
   the dot leaders don't render in Google Docs — only desktop Word/LibreOffice.

Run this after any content change (new/renamed/reordered headings, merged
sections) — the TOC regenerates from whatever heading structure currently exists.
