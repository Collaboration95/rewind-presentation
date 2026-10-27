"""Rewind app identity for the deck (27 Oct, ~12:00): Warm Glass tokens from
rewind-app src/ui/tokens.ts and web-styles.ts (origin/dev 2390589).

bg #f6ede3 · ink #33231a · accent #e0703a (decorative) / #A84A1A (text, AA 4.96:1)
· peach gradient #ffd2a6→#ff9f6b · glass cards · Fraunces (soft) headings,
Geist body, DM Mono numbers. Fonts are the app's own OFL files, embedded.
"""
import base64
from pathlib import Path

D = Path(__file__).resolve().parent

# Old calm-green deck colours → app colours. CI/CD semantic colours (blue, green,
# orange legend) are deliberately not mapped: they carry meaning.
COLOR_MAP = {
    '#1F6B55': '#A84A1A', '#1f6b55': '#A84A1A',
    '#247B72': '#A84A1A', '#247b72': '#A84A1A',
    '#367348': '#A84A1A', '#9a3d62': '#A84A1A',
    '#EEF4EF': '#F6EDE3', '#eef4ef': '#F6EDE3',
    '#12291F': '#33231A', '#12291f': '#33231A', '#15281F': '#33231A',
    '#163A2F': '#F6EDE3',
    '#45594F': '#5E4D43', '#45594f': '#5E4D43', '#50606a': '#5E4D43', '#52616a': '#5E4D43', '#53616a': '#5E4D43',
    '#24483B': '#4A3326', '#24483b': '#4A3326', '#22463A': '#4A3326',
    '#D3E1D6': '#EADBCB', '#d3e1d6': '#EADBCB', '#D3E2D7': '#EADBCB', '#d3e2d7': '#EADBCB',
    '#CFDDD2': '#EADBCB', '#cfddd2': '#EADBCB', '#CADBCE': '#E6D5C3', '#e1ebe3': '#F1E4D6', '#E1EBE3': '#F1E4D6',
    '#F7FAF7': '#FBF6F0', '#f7faf7': '#FBF6F0',
    '#8fb9a2': '#F0B48A', '#8FB9A2': '#F0B48A', '#A8DCC0': '#FFD2A6', '#a8dcc0': '#FFD2A6',
    '#9DB5A6': '#DCC3AE', '#9db5a6': '#DCC3AE', '#B5CBBC': '#DCC3AE', '#A9C2B1': '#D9BFA8',
    '#DCEBDD': '#FBE6D4', '#1E4D33': '#7A3512', '#93B89E': '#E8BE9C', '#3F5449': '#5E4D43',
    '#DDEBE1': '#FBE6D4', '#7CC4A0': '#FF9F6B', '#4a5c65': '#5E4D43', '#53636a': '#5E4D43',
}


def _font(name, file, weight='100 900'):
    data = base64.b64encode((D / 'assets/fonts' / file).read_bytes()).decode()
    return (f'@font-face{{font-family:"{name}";src:url(data:font/ttf;base64,{data}) format("truetype");'
            f'font-weight:{weight};font-display:block}}')


def fonts_css():
    return _font('Fraunces', 'Fraunces.ttf') + _font('Geist', 'Geist.ttf') + _font('DM Mono', 'DMMono-Regular.ttf', '400')


APPVIBE_CSS = r'''
:root{--sans:"Geist",-apple-system,BlinkMacSystemFont,"Helvetica Neue",Arial,sans-serif;--serif:"Fraunces",Georgia,serif;
--mono:"DM Mono",Menlo,monospace;--bg:#F6EDE3;--cream:#F6EDE3;--navy:#F6EDE3;--ink:#33231A;--muted:#5E4D43;
--line:#EADBCB;--card:rgba(255,255,255,.72);--accent2:#A84A1A;--orange:#A84A1A;--peach:linear-gradient(180deg,#ffd2a6,#ff9f6b);
--pm:#A84A1A;--sad:#A84A1A;--sdp:#A84A1A;--testing:#A84A1A;--devsecops:#A84A1A;--demo:#A84A1A}
html,body{font-family:var(--sans);color:var(--ink)}
#stage,.slide{background:var(--bg);color:var(--ink);font-family:var(--sans)}
/* Soft app glow, kept to the top-right corner so body text sits on plain cream. */
.slide{isolation:isolate}
.slide:not(.figure-slide):not(.chart-slide):not(.device-slide):not(.pipeline-slide)::before{content:'';position:absolute;right:-180px;top:-220px;width:620px;height:520px;border-radius:50%;
 background:radial-gradient(circle at 50% 50%,rgba(255,207,150,.5),rgba(255,168,110,.2) 40%,transparent 70%);filter:blur(30px);pointer-events:none;z-index:-1}
.slide h1{font-family:var(--serif);font-variation-settings:'SOFT' 100,'opsz' 72;font-weight:560;letter-spacing:-.6px;color:var(--ink)}
.kicker{font:600 15px var(--sans);letter-spacing:1.6px;text-transform:uppercase;color:var(--muted)}
h2{font-family:var(--serif);font-variation-settings:'SOFT' 100;font-weight:560}
.counter{font:500 14px var(--mono);color:var(--muted)}
.section-progress{gap:4px}.section-progress span{background:#EADBCB;border-radius:0 0 3px 3px}
.section-progress .done{background:#F0B48A;opacity:1}.section-progress .current{background:var(--peach)}
#bar{background:linear-gradient(90deg,#ffd2a6,#ff9f6b)!important}
pre,code,.command,.commands pre,.figure-fallback code,.image-counts{font-family:var(--mono)}
code{color:#4A3326}
/* Glass cards, as in the app's Glass primitive. */
.figure,.tt-left,.tt-example,.perf-stats div{background:rgba(255,255,255,.72);border:1px solid rgba(255,255,255,.9);border-radius:24px;
 box-shadow:inset 0 1px 1px #fff,0 18px 36px -18px rgba(160,90,40,.30),0 2px 6px -2px rgba(160,90,40,.12)}
.tt-example{border-left:6px solid #F0A06C}
.figuretitle,figcaption,.tt-label{font:600 14px var(--sans);letter-spacing:1.2px;text-transform:uppercase;color:var(--muted)}
.explain{color:var(--muted)}.explain b,.tt-catch b,.perf-p b,.sec-col>p b{color:var(--ink)}
.data th{font:600 14px var(--sans);letter-spacing:1px;text-transform:uppercase;color:var(--muted);border-bottom:2px solid #E3C9B2}
.data td{border-bottom-color:var(--line)}
.data.secscan{background:rgba(255,255,255,.72);border-radius:20px}
.tt-count,.perf-stats strong,.metric-row strong{font-family:var(--serif);font-variation-settings:'SOFT' 100,'opsz' 144;font-weight:500;color:var(--accent2)}
.rule,.takeaway{color:var(--accent2)}.rule{border-top-color:var(--line)}
.status-strip{border-top-color:var(--line)}.status-strip b{color:var(--accent2)}
.product-loop em,.journey-map em,.bug-steps em,.feature-number{font:500 16px var(--mono);letter-spacing:.5px;text-transform:uppercase;color:var(--accent2)}
.product-loop div,.journey-map div{background:rgba(255,255,255,.62);border-radius:24px;padding:22px 24px;box-shadow:inset 0 1px 1px #fff,0 14px 30px -18px rgba(160,90,40,.3)}
button,.feature-control button{font-family:var(--sans);border-radius:999px;border:0;background:rgba(255,255,255,.75);color:#2a1a10;
 box-shadow:inset 0 1px 1px #fff,inset 0 0 0 1px rgba(255,255,255,.8),0 6px 16px -10px rgba(150,80,30,.4)}
button:hover{background:#fff}
.feature-control button[data-action=play]{background:var(--peach);box-shadow:0 10px 22px -12px rgba(224,112,58,.8)}
.badge{font-family:var(--sans);border-radius:999px}
.badge.gate{background:#A84A1A;color:#fff}.badge.main{background:#FBE6D4;color:#7A3512;border:1px solid #E8BE9C}
.badge.manual{background:#fff;color:#5E4D43;border:1px solid #DCC3AE}.badge.report{background:#FFF8EE;color:#7A4510;border:1px solid #E4C59A}
.regression span:last-child b,.pass{color:#2F6B45}
.run-clock b{font-family:var(--mono);color:var(--accent2)}
.clip .cb{background:#FF9F6B}
.iphone-shell{background:#F6EDE3}
.feature-notes>p{color:var(--ink)}.feature-notes>p b{color:var(--muted);font-family:var(--sans)}
.foot{border-top:0}
#ov .th{background:var(--bg)}
#notes{font-family:var(--sans)}
/* Full-slide UML and charts stay on white. */
.slide.figure-slide,.slide.chart-slide{background:#fff}
.slide.figure-slide>h1,.slide.chart-slide>h1{font-family:var(--serif);font-weight:560;color:var(--accent2)}
/* Cover: app home on an iPhone 15 Pro beside the title. */
.slide.cover{background:radial-gradient(60% 75% at 72% 48%,rgba(255,207,150,.75),rgba(255,168,110,.28) 45%,transparent 72%),var(--bg);color:var(--ink);padding:0}
.slide.cover::before{display:none}
.cover>.kicker,.cover>h1{position:absolute!important;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}
.cover>.body{position:absolute;inset:0;margin:0;display:block}
.cover-grid{display:grid;grid-template-columns:1fr 360px;gap:40px;height:100%;padding:0 96px 0 84px;align-items:center}
.cover-text .cover-kicker{font:600 16px var(--sans);letter-spacing:2px;text-transform:uppercase;color:var(--accent2)}
.cover-word{font-family:var(--serif);font-variation-settings:'SOFT' 100,'opsz' 144;font-weight:520;font-size:132px;letter-spacing:-4px;line-height:1;margin:18px 0 8px;color:var(--ink)}
.cover-word span{display:none}
.cover-tag{font-family:var(--serif);font-variation-settings:'SOFT' 100;font-size:38px;line-height:1.15;margin:6px 0 14px;color:var(--ink)}
.cover-sub{font-size:24px;line-height:1.4;color:var(--muted);margin:0 0 26px;max-width:600px}
.cover-loop{display:flex;gap:10px;align-items:center;font:500 18px var(--sans);color:#2a1a10;margin:0}
.cover-loop span{background:rgba(255,255,255,.7);border-radius:999px;padding:9px 16px;box-shadow:inset 0 1px 1px #fff,0 6px 16px -10px rgba(150,80,30,.45)}
.cover-loop span:last-of-type{background:var(--peach)}
.cover-loop i{font-style:normal;color:#C0703F;font-size:20px}
.cover-meta{font:500 17px/1.7 var(--sans);margin-top:40px;color:var(--muted)}
.cover-meta b{color:var(--ink);font-weight:600}
.cover .foot{display:none}.cover .section-progress span{background:#EADBCB}
.cover-phone{display:flex;justify-content:center;align-items:center;height:100%}
.phone15{position:relative;width:310px;height:640px;border-radius:56px;background:#1c1c1e;padding:11px;box-sizing:border-box;
 box-shadow:0 0 0 2px #a49b92,0 0 0 4px #6f6861,inset 0 0 0 2px #3a3a3c,0 40px 70px -30px rgba(120,60,20,.55),0 12px 24px -12px rgba(60,30,10,.35)}
.phone15 .key{position:absolute;width:4px;background:linear-gradient(90deg,#8d857d,#b8afa6);border-radius:2px}
.phone15 .k1{left:-6px;top:118px;height:26px}.phone15 .k2{left:-6px;top:166px;height:50px}.phone15 .k3{left:-6px;top:226px;height:50px}.phone15 .k4{right:-6px;top:190px;height:78px}
.phone-screen{position:relative;width:100%;height:100%;border-radius:45px;overflow:hidden;background:#F6EDE3}
.phone-status{height:40px;display:flex;align-items:center;justify-content:space-between;padding:0 26px 0 30px;font:600 14px -apple-system,"SF Pro Text",var(--sans);color:#000}
.phone-status .di{position:absolute;left:50%;top:9px;transform:translateX(-50%);width:92px;height:27px;border-radius:20px;background:#000}
.phone-status .sys{display:flex;gap:5px;align-items:center}
.phone-status .bat{width:24px;height:11px;border:1.5px solid #000;border-radius:3.5px;position:relative;opacity:.9}
.phone-status .bat:after{content:'';position:absolute;inset:1.5px;right:4px;background:#000;border-radius:1.5px}
.phone-status .bars{display:flex;gap:1.5px;align-items:flex-end;height:11px}.phone-status .bars i{width:3px;background:#000;border-radius:1px}
.phone-screen img{display:block;width:100%;height:calc(100% - 40px);object-fit:cover;object-position:top}
.phone-screen:after{content:'';position:absolute;bottom:7px;left:50%;transform:translateX(-50%);width:104px;height:4px;border-radius:3px;background:#1b120d}
@media print{.slide{background:var(--bg)}.slide.cover{background:radial-gradient(60% 75% at 72% 48%,rgba(255,207,150,.75),rgba(255,168,110,.28) 45%,transparent 72%),#F6EDE3!important}
.cover .foot{display:none!important}.slide.figure-slide,.slide.chart-slide{background:#fff}}
'''

COVER_BODY = (
    '<div class="cover-grid"><div class="cover-text">'
    '<div class="cover-kicker">SWE5006 · Team 14</div>'
    '<div class="cover-word">Rewind</div>'
    '<p class="cover-tag">A month of moments. One film.</p>'
    '<p class="cover-sub">Small private groups. Sealed moments. A shared reveal.</p>'
    '<div class="cover-loop"><span>Contribute</span><i>→</i><span>Seal</span><i>→</i><span>Compile</span><i>→</i><span>Watch</span></div>'
    '<div class="cover-meta">27 October 2026</div>'
    '</div><div class="cover-phone"><div class="phone15" role="img" aria-label="Rewind Home on iPhone: group Sunday table, week 3 of 4, three of five moments sealed">'
    '<span class="key k1"></span><span class="key k2"></span><span class="key k3"></span><span class="key k4"></span>'
    '<div class="phone-screen"><div class="phone-status"><span>9:41</span><span class="di"></span>'
    '<span class="sys"><span class="bars"><i style="height:4px"></i><i style="height:6px"></i><i style="height:8px"></i><i style="height:10px"></i></span>'
    '<span class="bat"></span></span></div>'
    '<img src="assets/cover-home.png" alt="Rewind Home screen"></div></div></div></div>'
)


def apply_colors(document):
    for a, b in COLOR_MAP.items():
        document = document.replace(a, b)
    return document
