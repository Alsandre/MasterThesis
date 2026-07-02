#!/usr/bin/env python3
"""Validate that the Georgian translation aligns 1:1 with the English blueprint.

Walks the blueprint and the Georgian non-empty paragraphs in lockstep.
For tables, consumes one Georgian paragraph per NON-EMPTY English cell
(the translator dropped empty cells). Reports any misalignment with context.
"""
import sys
from docx import Document
from blueprint import parse_blueprint

MD = 'project/draft-en.md'
KA = 'project/draft-en ka.docx'

blocks = parse_blueprint(MD)

doc = Document(KA)
ka = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
print(f'Georgian non-empty paragraphs: {len(ka)}')

# para[0] is the title -> handled separately
title_ka = ka[0]
ka_body = ka[1:]
print(f'Georgian title paragraph: {title_ka[:70]}')
print(f'Georgian body paragraphs (excl title): {len(ka_body)}')
print('-'*70)

j = 0  # index into ka_body
errors = []
poured = []  # (block_type, en, ka)

def peek(k=0):
    return ka_body[j+k] if j+k < len(ka_body) else '<END>'

for bi, b in enumerate(blocks):
    typ = b[0]
    if typ in ('h1', 'h2', 'p', 'bullet', 'num'):
        en = b[1]
        if j >= len(ka_body):
            errors.append(f'block {bi} ({typ}) "{en[:40]}" -> RAN OUT of georgian paras')
            break
        poured.append((typ, en, ka_body[j]))
        j += 1
    elif typ == 'table':
        rows = b[1]
        grid = []
        for r in rows:
            grow = []
            for cell in r:
                if cell.strip():
                    if j >= len(ka_body):
                        errors.append(f'block {bi} (table cell) "{cell[:30]}" -> RAN OUT')
                        break
                    grow.append(ka_body[j]); j += 1
                else:
                    grow.append('')
            grid.append(grow)
        poured.append(('table', rows, grid))

print(f'Consumed {j} of {len(ka_body)} georgian body paragraphs.')
leftover = ka_body[j:]
if leftover:
    print(f'!! {len(leftover)} LEFTOVER georgian paragraphs (not consumed):')
    for k, t in enumerate(leftover):
        print(f'   [+{k}] {t[:80]}')
if errors:
    print('!! ERRORS:')
    for e in errors:
        print('  ', e)

# Spot-check: print heading alignment (en -> ka) to eyeball correctness
print('-'*70)
print('HEADING ALIGNMENT CHECK (en :: ka):')
for p in poured:
    if p[0] in ('h1', 'h2'):
        print(f'  [{p[0]}] {p[1][:45]:47s} :: {p[2][:55]}')

if not leftover and not errors:
    print('-'*70)
    print('ALIGNMENT OK — 1:1 clean.')
