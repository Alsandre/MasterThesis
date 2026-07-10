#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate project/defense-replay.html from a real run_live.py capture.
The capture (ANSI terminal output) is rendered VERBATIM — colors converted
to HTML, split into step-through blocks at the ── separators. Re-run this
after any new capture:  python3 poc/make_replay.py [capture.txt]
"""
import re, sys, os, html, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
CAP = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "live_run_1.txt")
OUT = os.path.join(HERE, "..", "presentation", "defense-replay.html")

raw = open(CAP, encoding="utf-8").read()
run_date = datetime.date.fromtimestamp(os.path.getmtime(CAP)).strftime("%d.%m.%Y")

ANSI = re.compile(r"\x1b\[([0-9;]+)m")
CLS = {"1": "b", "2": "d", "38;5;111": "c111", "38;5;114": "c114", "38;5;179": "c179"}

def line_to_html(line):
    parts = ANSI.split(line)
    out, attrs = [], set()
    for i, seg in enumerate(parts):
        if i % 2 == 1:  # code
            if seg == "0": attrs.clear()
            elif seg in CLS: attrs.add(CLS[seg])
            continue
        if not seg: continue
        esc = html.escape(seg)
        out.append(f'<span class="{" ".join(sorted(attrs))}">{esc}</span>' if attrs else esc)
    return "".join(out)

def strip_ansi(s): return ANSI.sub("", s)

# split into blocks at ──── separator lines
blocks, cur = [], []
for line in raw.split("\n"):
    if re.fullmatch(r"─{10,}", strip_ansi(line).strip()):
        blocks.append(cur); cur = []
    else:
        cur.append(line)
if cur: blocks.append(cur)
blocks = [b for b in blocks if any(strip_ansi(l).strip() for l in b)]
# blocks: [0]=header, then sessions / retrieval / usage
header, steps = blocks[0], blocks[1:]

def render(block):
    return "\n".join(line_to_html(l) for l in block)

CAPTIONS = [
    ("სესია 1 — კოდირება", "LLM რეალურ დროში აფასებს მნიშვნელოვნებას: სახელი 0.90, დედლაინი 0.80, ამინდი კი 0.20 — ტრივია. <b>ყველაფერი ინახება</b>, მაგრამ ტრივია დაბალი სტაბილურობით (S=0.4) — ის ფილტრით კი არა, დავიწყებით მოკვდება."),
    ("სესია 2 — კონსოლიდაცია", "დედლაინის თემა მეორდება → <b>⚙ კონსოლიდაცია</b>: იბადება სემანტიკური ფაქტი (S=5.0). ამინდი უკვე დავიწყებულია — R=0.082 &lt; 0.10 ზღვარს."),
    ("სესია 3 — მდგრადობა ხმაურის მიმართ", "⚠ საინტერესო მომენტი: LLM-მა განმეორებადი დედლაინი შეცდომით 0.20-ად შეაფასა. მაგრამ სისტემა მდგრადია — თემა უკვე კონსოლიდირებულია სემანტიკურ ფაქტად, ამიტომ ეს ცალკეული შეცდომა შედეგს ვერ აფუჭებს. დუბლიკატი ფაქტი კი ჩუმად მოიჭრა (cos ≥ 0.8)."),
    ("მოძიება — decay-შეწონილი TOP-4", "ქულა = cos × R (სემანტიკურზე ×1.25). სემანტიკური ფაქტი <b>#1 ადგილზეა</b>; ორივე ტრივია გამორიცხულია; დაბრუნებულები მაგრდება (S += 0.5)."),
    ("მტკიცებულება — რეალური API", "12 chat + 10 embedding გამოძახება, 953/291 ტოკენი — ღირებულება ≈ $0.0003. ეს ცოცხალი კოდის კვალია და არა წინასწარ დაწერილი ტექსტი."),
]
while len(CAPTIONS) < len(steps): CAPTIONS.append(("ნაბიჯი", ""))

CODES = [
    ("MemC.end_session — კოდირება",
     'sals = _salience_batch(events)\ng, anchor = _gist_anchor(ev)\nS0 = DECAY_S_BASE * max(0.1, sal)'),
    ("MemC._consolidate — კონსოლიდაცია",
     'if cos(a["emb"], self.episodes[j]["emb"]) > 0.55:\nif len(cluster) >= CONSOLIDATE_N:\n    fact = _semantic_fact(gists)   # "S": DECAY_S_BASE * 2.5'),
    ("MemC._R — დავიწყება · დედუპლიკაცია",
     'def _R(self, m, now):\n    dt = max(0, now - m["last"])\n    return math.exp(-dt / max(0.3, m["S"]))\nif all(cos(femb, s["emb"]) < 0.8 for s in self.semantic):'),
    ("MemC.retrieve — ქულა და გამყარება",
     'if R < FORGET_FLOOR: continue\ncands.append((cos(q, m["emb"]) * R * SEM_BONUS, …))\ncands.append((cos(q, m["emb"]) * R, …))\nm["S"] += 0.5; m["last"] = now'),
    ("llm() — რეალური გამოძახებების აღრიცხვა",
     'r = _post("https://api.openai.com/v1/chat/completions", …)\nUSAGE["chat_calls"] += 1\nUSAGE["chat_in"] += u.get("prompt_tokens", 0)'),
]
while len(CODES) < len(steps): CODES.append(("", ""))

step_html = "".join(
    f'<div class="step" data-i="{i}"><div class="cap"><span class="ct">{t}</span> {c}</div>'
    f'<pre class="term">{render(b)}</pre>'
    f'<div class="codestrip"><div class="cl">poc/harness.py · {lbl}</div><pre>{html.escape(code)}</pre></div></div>'
    for i, ((t, c), b, (lbl, code)) in enumerate(zip(CAPTIONS, steps, CODES))
)

page = """<!doctype html><html lang="ka" data-theme="dark"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Live Replay — რეალური გაშვების ჩანაწერი</title>
<style>
:root{--bg:#0f1013;--fg:#e9eaf0;--mut:#9a9daa;--line:#2a2c35;--acc:#9aa6ff;--card:#16171c;--ok:#5bbf7b;--warn:#e0a13a;--sem:#c58bff}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.5 -apple-system,"Segoe UI",Roboto,"Noto Sans Georgian",sans-serif;padding-top:36px}
.xnav{position:fixed;top:0;left:0;right:0;height:36px;z-index:60;display:flex;align-items:center;gap:3px;background:#0b0c0f;border-bottom:1px solid #23252d;padding:0 10px;font:600 12.5px/1 -apple-system,"Noto Sans Georgian",sans-serif}
.xnav a{color:#9aa0ad;text-decoration:none;padding:6px 10px;border-radius:6px;white-space:nowrap}
.xnav a:hover{color:#fff;background:#181a20}.xnav a.cur{color:#fff;background:#3b4cca}
.wrap{max-width:980px;margin:0 auto;padding:20px 20px 60px}
h1{font-size:1.5rem;margin:0 0 3px}
.sub{color:var(--mut);font-size:.8rem;margin:0 0 14px;font-family:"SF Mono",ui-monospace,Menlo,monospace}
.ctrl{position:sticky;top:36px;z-index:5;background:color-mix(in srgb,var(--bg) 88%,transparent);backdrop-filter:blur(8px);display:flex;gap:10px;align-items:center;flex-wrap:wrap;padding:10px 0;border-bottom:1px solid var(--line);margin-bottom:16px}
button{font:inherit;cursor:pointer;border:1px solid var(--line);background:var(--card);color:var(--fg);border-radius:9px;padding:8px 15px}
button:hover{border-color:var(--acc);color:var(--acc)}
#next{background:var(--acc);color:#fff;border-color:var(--acc);font-weight:700}
#next:disabled{opacity:.45;cursor:default;background:var(--card);color:var(--mut);border-color:var(--line)}
.prog{color:var(--mut);font-variant-numeric:tabular-nums;font-size:.85rem}
.kbd{color:var(--mut);font-size:.75rem;margin-left:auto}
.termwin{background:#0c0d10;border:1px solid var(--line);border-radius:12px;overflow:hidden;box-shadow:0 14px 40px rgba(0,0,0,.45)}
.tbar{display:flex;align-items:center;gap:6px;padding:9px 13px;background:#14151a;border-bottom:1px solid var(--line)}
.dot{width:11px;height:11px;border-radius:50%}
.tt{margin-left:8px;color:var(--mut);font:500 12px "SF Mono",ui-monospace,Menlo,monospace}
.tbody{padding:6px 0 14px}
.step{display:none}
.step.show{display:block;animation:fade .35s}
@keyframes fade{from{opacity:0;transform:translateY(5px)}to{opacity:1;transform:none}}
.cap{margin:14px 16px 4px;padding:9px 13px;background:color-mix(in srgb,var(--acc) 9%,transparent);border-left:3px solid var(--acc);border-radius:0 9px 9px 0;font-size:.85rem;color:var(--fg)}
.cap .ct{display:block;font-size:.68rem;font-weight:800;text-transform:uppercase;letter-spacing:.07em;color:var(--acc);margin-bottom:2px}
.cap b{color:var(--acc)}
pre.term{margin:4px 0 0;padding:6px 18px;overflow-x:auto;font:13px/1.55 "SF Mono",ui-monospace,Menlo,Consolas,monospace;color:#c9ccd6}
pre.term .b{font-weight:700;color:#eef0f6}
pre.term .d{color:#71757f}
pre.term .c111{color:#9aa6ff}.c114{color:#5bbf7b}.c179{color:#e0a13a}
pre.term .b.c114{color:#74d693}.b.c111{color:#b3bcff}
.hdr pre.term{padding-top:12px}
.foot{margin-top:20px;color:var(--mut);font-size:.78rem;border-top:1px solid var(--line);padding-top:12px;line-height:1.7}
.foot code{background:var(--line);padding:1px 5px;border-radius:4px;font-family:"SF Mono",ui-monospace,Menlo,monospace;font-size:.85em}
#codebtn.on{border-color:var(--acc);color:var(--acc);font-weight:700}
.codestrip{display:none;margin:8px 16px 0;border:1px dashed color-mix(in srgb,var(--acc) 55%,transparent);border-radius:9px;padding:8px 12px;background:color-mix(in srgb,var(--acc) 6%,transparent)}
body.showcode .codestrip{display:block}
.codestrip .cl{font:700 10.5px "SF Mono",ui-monospace,Menlo,monospace;color:var(--acc);letter-spacing:.05em;margin-bottom:4px}
.codestrip pre{margin:0;font:12px/1.55 "SF Mono",ui-monospace,Menlo,monospace;color:#c9ccd6;overflow-x:auto}
</style></head><body>
<div class="xnav"><a href="THESIS_BILINGUAL.html">📄 დოკუმენტი</a><a href="defense-prep.html">📋 Defense prep</a><a href="defense-presentation.html">▶ პრეზენტაცია</a><a href="defense-replay.html" class="cur">🖥 Replay</a><a href="defense-config.html">🛠 კონფიგურაცია</a><span style="flex:1"></span></div>
<div class="wrap">
<h1>რეალური გაშვების ჩანაწერი</h1>
<p class="sub">poc/run_live.py --demo · __DATE__ · უცვლელი გამონატანი (poc/live_run_1.txt) · harness.py + OpenAI</p>
<div class="ctrl">
  <button id="next">▶ შემდეგი ნაბიჯი</button>
  <button id="back">◀ უკან</button>
  <button id="all">ყველას ჩვენება</button>
  <button id="reset">↺ თავიდან</button>
  <button id="codebtn">&lt;/&gt; კოდი</button>
  <span class="prog"><span id="pi">0</span>/__N__</span>
  <span class="kbd">→ / Space — შემდეგი · ← — უკან · A — ყველა · R — თავიდან · C — კოდი</span>
</div>
<div class="termwin">
  <div class="tbar"><span class="dot" style="background:#ff5f57"></span><span class="dot" style="background:#febc2e"></span><span class="dot" style="background:#28c840"></span><span class="tt">python3 poc/run_live.py --demo</span></div>
  <div class="tbody">
    <div class="hdr"><pre class="term">__HEADER__</pre></div>
    __STEPS__
  </div>
</div>
<div class="foot">
ეს გვერდი <code>poc/live_run_1.txt</code>-ის ზუსტი ასლია — ტერმინალის ფერები HTML-ად არის გადაყვანილი, ტექსტი უცვლელია (<code>poc/make_replay.py</code>).
სარეზერვო ვარიანტი ტერმინალში: <code>cat poc/live_run_1.txt</code> · ცოცხალი გაშვება სცენაზე: <code>python3 poc/run_live.py --demo</code> (იგივე კოდი, ახალი API გამოძახებები).
</div>
</div>
<script>
const steps=[...document.querySelectorAll('.step')],N=steps.length;
let i=0,allMode=false;
const pi=document.getElementById('pi'),next=document.getElementById('next'),back=document.getElementById('back');
function show(){steps.forEach((s,k)=>s.classList.toggle('show',allMode||k===i-1))}
function sync(){pi.textContent=allMode?N:i;next.disabled=allMode||i>=N;back.disabled=allMode||i<=0;
  next.textContent=(allMode||i>=N)?'✓ დასრულდა':'▶ შემდეგი ნაბიჯი';}
function fwd(){if(!allMode&&i<N){i++;show();sync();
  steps[i-1].scrollIntoView({behavior:'smooth',block:'start'})}}
function bwd(){if(!allMode&&i>0){i--;show();sync();
  if(i>0)steps[i-1].scrollIntoView({behavior:'smooth',block:'start'})}}
function all(){allMode=true;show();sync()}
function reset(){allMode=false;i=0;show();sync();window.scrollTo({top:0,behavior:'smooth'})}
next.onclick=fwd;back.onclick=bwd;
const cb=document.getElementById('codebtn');
function codeToggle(){document.body.classList.toggle('showcode');cb.classList.toggle('on')}
cb.onclick=codeToggle;
document.getElementById('all').onclick=all;document.getElementById('reset').onclick=reset;
document.addEventListener('keydown',e=>{
  if(e.key==='ArrowRight'||e.key===' '){e.preventDefault();fwd()}
  else if(e.key==='ArrowLeft'){e.preventDefault();bwd()}
  else if(e.key==='a'||e.key==='A')all();
  else if(e.key==='r'||e.key==='R')reset();
  else if(e.key==='c'||e.key==='C')codeToggle();});
sync();
</script>
</body></html>
"""
page = (page.replace("__HEADER__", render(header))
            .replace("__STEPS__", step_html)
            .replace("__N__", str(len(steps)))
            .replace("__DATE__", run_date))
open(OUT, "w", encoding="utf-8").write(page)
print(f"ok: {os.path.normpath(OUT)}  ({len(steps)} steps, {os.path.getsize(OUT)} bytes)")
