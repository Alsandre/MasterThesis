#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extract one section's aligned English+Georgian paragraphs for the polish loop.

The Georgian is the CURRENT, corrections-applied text (== thesis-ka.docx), so a
polished paragraph can be written back as a whole-paragraph correction later.

Usage: python3 extract_chunk.py "1.1"
Output (stdout): JSON {section, heading_ka, units:[{i,type,en,ka}]}  (p/bullet/num only)
"""
import sys, json, re
import build
from blueprint import parse_blueprint

sec = sys.argv[1] if len(sys.argv) > 1 else "1.1"

blocks = parse_blueprint(build.MD)     # English  (type, text)
poured = build.pour()                   # Georgian (type, corrected-text), aligned 1:1
assert len(blocks) == len(poured), f"alignment off: {len(blocks)} vs {len(poured)}"

start = next((k for k, (t, en) in enumerate(blocks)
              if t == 'h2' and re.match(r'^%s\b' % re.escape(sec), en.strip())), None)
if start is None:
    print(json.dumps({"error": f"section {sec} not found"}, ensure_ascii=False)); sys.exit(1)

units = []
for k in range(start + 1, len(blocks)):
    t = blocks[k][0]
    if t in ('h1', 'h2'):
        break
    if t in ('p', 'bullet', 'num'):
        units.append({"i": k, "type": t, "en": blocks[k][1], "ka": poured[k][1]})

print(json.dumps({"section": blocks[start][1], "heading_ka": poured[start][1],
                  "units": units}, ensure_ascii=False))
