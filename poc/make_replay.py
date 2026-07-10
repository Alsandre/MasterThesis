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

# ---- code modal: whole functions extracted verbatim from harness.py ----
_SRC = open(os.path.join(HERE, "harness.py"), encoding="utf-8").read().split("\n")
def _find(anchor, start=0):
    for k in range(start, len(_SRC)):
        if _SRC[k].strip().startswith(anchor):
            return k
    raise SystemExit(f"anchor not found in harness.py: {anchor!r}")
def _func_block(defanchor, after=None):
    st = _find(defanchor, _find(after) if after else 0)
    ind = len(_SRC[st]) - len(_SRC[st].lstrip())
    out = [_SRC[st]]
    for l in _SRC[st + 1:]:
        if l.strip() and (len(l) - len(l.lstrip())) <= ind:
            break
        out.append(l)
    while out and not out[-1].strip():
        out.pop()
    return [l[ind:] if len(l) > ind else "" for l in out]

_TOK = re.compile(r'(#.*)|("(?:[^"\\]|\\.)*")|\b(def|return|if|for|in|continue|else|not|and|or|lambda|break)\b|(\b\d+(?:\.\d+)?\b)|(\bself\b)|([A-Za-z_][A-Za-z0-9_]*)(?=\()')
def _hl(line):
    out, pos = [], 0
    for m in _TOK.finditer(line):
        out.append(html.escape(line[pos:m.start()]))
        cls = 'c' if m.group(1) else 's' if m.group(2) else 'k' if m.group(3) else 'n' if m.group(4) else 'sf' if m.group(5) else 'f'
        out.append(f'<span class="{cls}">{html.escape(m.group(0))}</span>')
        pos = m.end()
    out.append(html.escape(line[pos:]))
    return "".join(out)

FUNCS = [
    ("end_session", "MemC.end_session — კოდირება", _func_block("def end_session", after="class MemC:"), {
        "sals = _salience_batch(events)": "ერთი ჯგუფური LLM-გამოძახება: მნიშვნელოვნების ქულა ყველა რეპლიკას",
        "S0 = DECAY_S_BASE * max(0.1, sal)": "საწყისი სტაბილურობა მნიშვნელოვნების პროპორციულია — ტრივია სუსტად ინახება",
        "g, anchor = _gist_anchor(ev)": "არსი (gist) + ზუსტი ციტატა (anchor) თითო მოვლენაზე",
        "self._consolidate(sid)": "სესიის ბოლოს — ოფლაინ კონსოლიდაცია",
    }),
    ("_consolidate", "MemC._consolidate — კონსოლიდაცია", _func_block("def _consolidate", after="class MemC:"), {
        'if cos(a["emb"], self.episodes[j]["emb"]) > 0.55:': "მსგავსი ეპიზოდები (cos > 0.55) ერთ კლასტერად იყრება",
        "if len(cluster) >= CONSOLIDATE_N:": "მინიმუმ ორი განმეორება — ერთჯერადი მოვლენა ფაქტად არ იქცევა",
        "fact = _semantic_fact(gists)": "LLM წერს ერთ განზოგადებულ ფაქტს კლასტერიდან",
        'if all(cos(femb, s["emb"]) < 0.8 for s in self.semantic):': "დედუპლიკაცია: თითქმის იდენტური ფაქტი აღარ ემატება",
        'self.semantic.append({"fact": fact, "emb": femb, "S": DECAY_S_BASE * 2.5,': "ფაქტის სტაბილურობა გაძლიერებულია: S = 2.0 × 2.5 = 5.0",
    }),
    ("_R", "MemC._R — დავიწყების მრუდი", _func_block("def _R", after="class MemC:"), {
        "def _R(self, m, now):": "მოძიებადობა — ებინგჰაუზის მრუდის პირდაპირი იმპლემენტაცია",
        'dt = max(0, now - m["last"])': "რამდენი სესია გავიდა კვალთან ბოლო შეხებიდან",
        'return math.exp(-dt / max(0.3, m["S"]))': "R ექსპონენციალურად ეცემა; დიდი S — ნელი ქრობა",
    }),
    ("retrieve", "MemC.retrieve — მოძიება და გამყარება", _func_block("def retrieve", after="class MemC:"), {
        "if R < FORGET_FLOOR: continue": "R < 0.10 — ფუნქციურად დავიწყებულია, კანდიდატიც აღარ არის",
        'cands.append((cos(q, m["emb"]) * R * SEM_BONUS, ("semantic", m["fact"]), m))': "სემანტიკური ქულა: მსგავსება × სიახლე × 1.25 ბონუსი",
        'cands.append((cos(q, m["emb"]) * R, ("episodic", m["gist"]), m))': "ეპიზოდური ქულა: მსგავსება × სიახლე",
        "cands.sort(key=lambda x: x[0], reverse=True)": "საუკეთესო ქულით დალაგება",
        "top = cands[:RETRIEVE_K]": "საერთო ბიუჯეტი: TOP-4",
        'm["S"] += 0.5; m["last"] = now': "გამყარება: დაბრუნებული მოგონება მაგრდება და „ახლდება“",
    }),
    ("llm", "llm() — რეალური გამოძახებები", _func_block("def llm("), {
        'r = _post("https://api.openai.com/v1/chat/completions",': "ცოცხალი HTTP მოთხოვნა OpenAI-ს API-სკენ — არაფერი გათამაშებული",
        'USAGE["chat_calls"] += 1; USAGE["chat_in"] += u.get("prompt_tokens", 0); USAGE["chat_out"] += u.get("completion_tokens", 0)': "ტოკენების ზუსტი აღრიცხვა — ბოლო „მტკიცებულების“ სტრიქონის წყარო",
    }),
]

def _pane(lines, gmap):
    used, rows = set(), []
    for l in lines:
        key = l.strip()
        g = gmap.get(key) if (key in gmap and key not in used) else None
        cls = ' hl' if g else ''
        content = _hl(l) if l.strip() else '&nbsp;'
        rows.append(f'<div class="ln{cls}">{content}</div>')
        if g:
            used.add(key)
            rows.append(f'<div class="lg" style="padding-left:{len(l) - len(l.lstrip())}ch">— {html.escape(g)}</div>')
    return "".join(rows)

_tabs = "".join(f'<button data-t="{k}"{" class=on" if k == 0 else ""}>{name}</button>'
                for k, (name, _, _, _) in enumerate(FUNCS))
_panes = "".join(f'<div class="cmpane{" on" if k == 0 else ""}"><div class="cmlbl">{label}</div>{_pane(lines, gmap)}</div>'
                 for k, (name, label, lines, gmap) in enumerate(FUNCS))
MODAL = ('<div id="codemodal" class="cmodal" hidden><div class="cmbox">'
         '<div class="cmhead"><div class="cmtabs">' + _tabs + '</div>'
         '<span style="flex:1"></span><span class="cmfile">poc/harness.py · უცვლელი წყარო</span>'
         '<button id="cmclose">✕</button></div>'
         '<div class="cmbody">' + _panes + '</div></div></div>')

step_html = "".join(
    f'<div class="step" data-i="{i}"><div class="cap"><span class="ct">{t}</span> {c}</div>'
    f'<pre class="term">{render(b)}</pre></div>'
    for i, ((t, c), b) in enumerate(zip(CAPTIONS, steps))
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
.cmodal{position:fixed;inset:0;z-index:100;background:rgba(5,6,9,.74);backdrop-filter:blur(3px);display:flex;align-items:center;justify-content:center;padding:28px 16px}
.cmodal[hidden]{display:none}
.cmbox{width:min(1060px,96vw);max-height:86vh;display:flex;flex-direction:column;background:#101116;border:1px solid var(--line);border-radius:14px;box-shadow:0 24px 70px rgba(0,0,0,.6);overflow:hidden}
.cmhead{display:flex;align-items:center;gap:8px;padding:10px 14px;border-bottom:1px solid var(--line);background:#14151a}
.cmtabs{display:flex;gap:4px;flex-wrap:wrap}
.cmtabs button{font:600 12px "SF Mono",ui-monospace,Menlo,monospace;padding:6px 11px;border-radius:7px;border:1px solid var(--line);background:none;color:var(--mut);cursor:pointer}
.cmtabs button:hover{color:var(--acc);border-color:var(--acc)}
.cmtabs button.on{background:var(--acc);border-color:var(--acc);color:#fff}
.cmfile{color:var(--mut);font:11px "SF Mono",ui-monospace,Menlo,monospace;white-space:nowrap}
#cmclose{border:none;background:none;color:var(--mut);font-size:1.1rem;cursor:pointer;padding:2px 6px}
#cmclose:hover{color:var(--fg)}
.cmbody{overflow:auto;padding:14px 20px 18px}
.cmpane{display:none}.cmpane.on{display:block}
.cmlbl{font:700 11px "SF Mono",ui-monospace,Menlo,monospace;color:var(--acc);letter-spacing:.05em;margin-bottom:8px}
.cmpane .ln{white-space:pre;font:13px/1.62 "SF Mono",ui-monospace,Menlo,monospace;color:#d6d9e0;overflow-x:auto}
.cmpane .ln.hl{background:color-mix(in srgb,var(--acc) 14%,transparent);border-radius:4px;margin:0 -8px;padding:0 8px}
.cmpane .lg{font:italic 12px/1.5 -apple-system,"Noto Sans Georgian",sans-serif;color:color-mix(in srgb,var(--acc) 70%,var(--mut));margin:2px 0 6px;white-space:normal}
.cmpane .k{color:#c58bff}.cmpane .s{color:#5bbf7b}.cmpane .n{color:#e0a13a}.cmpane .f{color:#9aa6ff}.cmpane .sf{color:#8b8ea0;font-style:italic}.cmpane .c{color:#6d7280;font-style:italic}
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
__MODAL__
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
const cb=document.getElementById('codebtn'),cm=document.getElementById('codemodal');
const cmtabs=[...document.querySelectorAll('.cmtabs button')],cmpanes=[...document.querySelectorAll('.cmpane')];
let cmi=0;
function cmShow(t){cmi=t;cmtabs.forEach((b,k)=>b.classList.toggle('on',k===t));cmpanes.forEach((p,k)=>p.classList.toggle('on',k===t))}
cmtabs.forEach((b,k)=>b.onclick=()=>cmShow(k));
document.getElementById('cmclose').onclick=()=>{cm.hidden=true};
cm.addEventListener('click',e=>{if(e.target===cm)cm.hidden=true});
function codeToggle(){if(cm.hidden){cm.hidden=false;cmShow(Math.min(Math.max(i-1,0),cmpanes.length-1))}else{cm.hidden=true}}
cb.onclick=codeToggle;
document.getElementById('all').onclick=all;document.getElementById('reset').onclick=reset;
document.addEventListener('keydown',e=>{
  if(e.key==='Escape'&&!cm.hidden){cm.hidden=true;return}
  if(!cm.hidden){
    if(e.key==='ArrowRight'){e.preventDefault();cmShow((cmi+1)%cmpanes.length)}
    else if(e.key==='ArrowLeft'){e.preventDefault();cmShow((cmi+cmpanes.length-1)%cmpanes.length)}
    else if(e.key==='c'||e.key==='C')codeToggle();
    return}
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
            .replace("__DATE__", run_date)
            .replace("__MODAL__", MODAL))
open(OUT, "w", encoding="utf-8").write(page)
print(f"ok: {os.path.normpath(OUT)}  ({len(steps)} steps, {os.path.getsize(OUT)} bytes)")
