#!/usr/bin/env python3
"""Parse draft-en.md into an ordered list of typed structural blocks.

Block types:
  ('h1', en_text)          # chapter  (## ...)      -> Heading 1
  ('h2', en_text)          # section  (### ...)     -> Heading 2
  ('p',  en_text)          # paragraph
  ('bullet', en_text)      # - item
  ('num', en_text)         # N. item
  ('table', rows)          # rows = list[list[cell_en]]  (grid, may contain '')

This is the STRUCTURE blueprint. Georgian text is poured into it in lockstep.
"""
import re

def parse_blueprint(md_path):
    lines = open(md_path, encoding='utf-8').read().split('\n')
    # start at first "## Abstract"
    start = next(i for i, l in enumerate(lines) if l.strip().startswith('## Abstract'))
    lines = lines[start:]

    blocks = []
    i, n = 0, len(lines)
    while i < n:
        raw = lines[i]
        s = raw.strip()

        if s == '' or s == '---':
            i += 1; continue
        # skip italic working-notes
        if re.match(r'^\*Status:', s) or re.match(r'^\*Bibliography:', s) or s.startswith('**This is the source'):
            i += 1; continue

        # table
        if s.startswith('|') and i + 1 < n and re.match(r'^\s*\|[\s:\-|]+\|\s*$', lines[i+1]):
            header = [c.strip() for c in s.strip().strip('|').split('|')]
            rows = [header]
            i += 2
            while i < n and lines[i].strip().startswith('|'):
                cells = [c.strip() for c in lines[i].strip().strip('|').split('|')]
                rows.append(cells)
                i += 1
            blocks.append(('table', rows))
            continue

        # headings
        m = re.match(r'^(#{2,3})\s+(.*)$', s)
        if m:
            lvl = 'h1' if len(m.group(1)) == 2 else 'h2'
            blocks.append((lvl, m.group(2).strip()))
            i += 1; continue

        # bullet
        if re.match(r'^-\s+', s):
            blocks.append(('bullet', re.sub(r'^-\s+', '', s)))
            i += 1; continue

        # numbered
        if re.match(r'^\d+\.\s+', s):
            blocks.append(('num', re.sub(r'^\d+\.\s+', '', s)))
            i += 1; continue

        # paragraph (single line each in this md)
        blocks.append(('p', s))
        i += 1

    return blocks


def strip_md(t):
    """Remove markdown inline emphasis / code for length comparison."""
    t = re.sub(r'\*\*(.+?)\*\*', r'\1', t)
    t = re.sub(r'\*(.+?)\*', r'\1', t)
    t = re.sub(r'`(.+?)`', r'\1', t)
    return t


if __name__ == '__main__':
    import sys
    bl = parse_blueprint(sys.argv[1] if len(sys.argv) > 1 else 'project/draft-en.md')
    counts = {}
    cells = 0
    for b in bl:
        counts[b[0]] = counts.get(b[0], 0) + 1
        if b[0] == 'table':
            cells += sum(len(r) for r in b[1])
    print('blocks:', len(bl))
    print('by type:', counts)
    print('table cells (grid, incl empty):', cells)
    # non-table blocks + non-empty table cells = expected georgian non-empty paragraphs
    nonempty_cells = 0
    for b in bl:
        if b[0] == 'table':
            nonempty_cells += sum(1 for r in b[1] for c in r if c.strip())
    non_table_blocks = sum(1 for b in bl if b[0] != 'table')
    print('EXPECTED georgian non-empty paras (excl title):', non_table_blocks + nonempty_cells)
