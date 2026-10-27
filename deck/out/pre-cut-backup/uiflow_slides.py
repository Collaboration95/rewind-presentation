"""A&D: cycle statechart promoted to the main path (D1), the interactive UI flow
page embedded full slide (D2), and one static storyboard per flow (U1..Un) as
fallback frames directly after it. Arrow keys skip the fallback frames unless the
presenter presses S (or is already on one); the PDF keeps them in order.

Section 2 stays at 5:00: s4 28 + s5 32 + s6 38 + s7 48 + s8 50 + s9 44 + D1 25 + D2 35.
"""
import html
import json
import re
from pathlib import Path

D = Path(__file__).resolve().parent
UI = D / 'uiflow'

SECS = {'s4': 28, 's5': 32, 's6': 38, 's7': 48, 's8': 50, 's9': 44, 'D1': 25, 'D2': 35}

SCRIPTS = {
    's4': ('The use case view starts with user goals. Members join a private group, contribute, chat and watch; '
           'the owner also manages membership and settings. The boundary makes the secondary systems explicit: '
           'identity, object storage, web push and scheduled time. For detailed design I follow CU-B: close the cycle, '
           'compile the film and release it, which joins UC07 and UC08.'),
    's5': ('The main architecture decision is a modular monolith. Splitting membership, contributions and cycles into '
           'services would add coordination without helping this workflow; keeping the rules beside one transaction makes '
           'acceptance and cycle transitions easier to reason about. Hosted PostgreSQL holds durable relational state, '
           'private S3 holds media, and Cognito supplies web identity. Adapters keep those protocols out of the domain decisions.'),
    's6': ('The left side is analysis: a boundary receives interaction, a control coordinates the use case, and entities hold '
           'the state the business must retain. On the right we refine those responsibilities into real names. The scheduler '
           'finds work, lifecycle owns the cycle transition, compilation prepares and finalises the film, and the database keeps '
           'cycles, jobs and frozen inputs. A collection of functions is drawn as a module; a class symbol is reserved for a real '
           'class, so the model stays traceable to the code.'),
    's9': ('This is the database schema for the same use case. Membership relates an account to a group and its role, and every '
           'access decision uses it. A group has cycles; a cycle has contributions; media jobs retain processing state. '
           'Compilation inputs freeze exactly which media belongs to a film, so a retry cannot reinterpret a changing collection. '
           'Primary keys, foreign keys and uniqueness enforce those rules. We chose PostgreSQL because this path depends on joins '
           'and transactions across related records; the server suite runs on both SQLite and PostgreSQL. '
           'Before the screens, one more model: the cycle’s states.'),
    'D1': ('We planned this statechart before any screen. A cycle is collecting until its end time; advance closes it, queues the '
           'film job and opens the successor. It stays revealing and unpublished until a ready proof exists, then publishes for the '
           'twenty-four-hour premiere, and finally archives. The server owns every transition, so the client only ever renders a state.'),
}

D2_SCRIPT_DEFAULT = (
    '[Click inside the page to step through a flow; Esc returns to the slides. If the page does not load, press S for the storyboards.]\n\n'
    'The screens came second, and each one maps to a state. While the cycle is collecting, Home shows the countdown, the week and the '
    'member’s allowance, and capture is offered. When the cycle closes, Home shows the film developing. Once it is published, the '
    'premiere card opens the film for twenty-four hours, and after that the film lives in Archive. Every screen reads the server’s '
    'state instead of keeping its own, so a refresh or a second device always agrees.')


def storyboards():
    folder = UI / 'storyboards'
    return sorted(p for p in folder.glob('*.png')) if folder.exists() else []


def _title(path):
    name = re.sub(r'^\d+[-_ ]*', '', path.stem).replace('-', ' ').replace('_', ' ').strip()
    return name[:1].upper() + name[1:]


def integrate(slides, add_titles=None):
    by_id = {s['id']: s for s in slides}
    for key, secs in SECS.items():
        if key in by_id:
            by_id[key]['secs'] = secs
    for key, text in SCRIPTS.items():
        if key in by_id:
            by_id[key]['script'] = text
    by_id['s8']['script'] = by_id['s8']['script'].replace('57-second allocation', '50-second allocation')
    by_id['s9']['transition'] = 'The cycle statechart came before the screens.'

    # D1: the statechart moves from backup B2 into the main A&D path.
    st = by_id['B2']
    st.update(id='D1', kind='main', secs=SECS['D1'], title='The cycle’s states were fixed before any screen',
              say=['Collecting → revealing (unpublished) → published premiere → archived; the server owns every transition.'],
              transition='Each screen then maps to one of these states.', refs=['B16', 'B17'])
    for s in slides:
        s['refs'] = ['D1' if r == 'B2' else r for r in s['refs']]

    boards = storyboards()
    titles = add_titles or {}
    poster = ('uiflow/storyboards/' + boards[0].name) if boards else ''
    body = ('<div class="uiflow-frame">'
            '<iframe class="uiflow" data-src="uiflow/index.html" title="Rewind UI flow · screens mapped to cycle states" '
            'tabindex="0" allow="fullscreen"></iframe>'
            + (f'<img class="uiflow-poster" src="{poster}" alt="UI flow storyboard">' if poster else '') +
            '</div><div class="uiflow-bar"><span>Click inside to explore · Esc returns to slides</span>'
            '<a href="uiflow/index.html" target="_blank" rel="noopener">Open full screen ↗</a>'
            + (f'<button data-action="storyboards">S · storyboards ({len(boards)})</button>' if boards else '') + '</div>')
    ui = dict(id='D2', sec=2, tag='SAD', title='Each screen renders one state of the cycle', body=body, secs=SECS['D2'],
              say=['Home, capture, developing, premiere and Archive each render one server state.'],
              transition='Testing checks those states through their real boundaries.', refs=['D1'] + [f'U{i}' for i in range(1, len(boards) + 1)],
              source='uiflow/index.html', script=D2_SCRIPT_DEFAULT, kind='main', extra='uiflow-slide')
    frames = []
    for i, p in enumerate(boards, 1):
        t = titles.get(p.name, _title(p))
        frames.append(dict(id=f'U{i}', sec=2, tag='SAD', title=f'UI flow {i} · {t}',
                           body=f'<figure class="figure chart"><figcaption>Storyboard · {html.escape(t)}</figcaption>'
                                f'<img src="uiflow/storyboards/{p.name}" alt="{html.escape(t)} storyboard"></figure>',
                           secs=0, say=[t], transition='Continue the storyboards, or move on to Testing.', refs=['D1', 'D2'],
                           source='uiflow/storyboards/' + p.name,
                           script=f'Storyboard for the {t} flow: each frame is labelled with the cycle state it renders. '
                                  'Use these if the interactive page is unavailable.',
                           kind='back', extra='chart-slide fallback'))
    slides.remove(st)
    at = slides.index(by_id['s9']) + 1
    slides[at:at] = [st, ui] + frames


UIFLOW_CSS = r'''
.uiflow-slide{padding:0}
.uiflow-slide>.kicker,.uiflow-slide>.foot,.uiflow-slide>.section-progress{display:none!important}
.uiflow-slide::before{display:none}
.uiflow-slide>h1{position:absolute;top:6px;left:18px;right:420px;font-size:20px;line-height:26px;min-height:0;margin:0;letter-spacing:-.2px;white-space:nowrap}
.uiflow-slide>.body{position:absolute;inset:38px 0 0;margin:0;display:block}
.uiflow-frame{position:absolute;inset:0;background:#fff;overflow:hidden}
.uiflow-frame iframe{width:100%;height:100%;border:0;display:block;background:#F6EDE3}
.uiflow-poster{display:none}
.uiflow-bar{position:absolute;top:-31px;right:14px;display:flex;gap:14px;align-items:center;font:500 14px var(--sans);color:var(--muted)}
.uiflow-bar a{color:#A84A1A;font-weight:600;text-decoration:none}
.uiflow-bar button{font-size:14px;padding:5px 12px}
@media print{.uiflow-frame iframe{display:none!important}.uiflow-poster{display:block!important;width:100%;height:100%;object-fit:contain;background:#fff}.uiflow-bar{display:none!important}}
'''


def uiflow_js(js):
    js = re.sub(r"function next\(\)\{if\(cur<N-1\)go\(cur\+1\)\}",
                "function next(){if(cur>=N-1)return;var j=cur+1;if(!slides[cur].classList.contains('fallback'))while(j<N-1&&slides[j].classList.contains('fallback'))j++;go(j)}", js)
    js = re.sub(r"function prev\(\)\{if\(cur>0\)go\(cur-1\)\}",
                "function prev(){if(cur<=0)return;var j=cur-1;if(!slides[cur].classList.contains('fallback'))while(j>0&&slides[j].classList.contains('fallback'))j--;go(j)}", js)
    assert 'fallback' in js, 'next/prev hook missing'
    js = js.replace("else if(k==='n'||k==='N')",
                    "else if(k==='s'||k==='S'){var f=slides.findIndex(function(x){return x.classList.contains('fallback')});if(f>=0)go(f)}\nelse if(k==='n'||k==='N')", 1)
    js = js.replace("function go(i,noHash){if(i<0||i>=N)return;",
                    "function go(i,noHash){if(i<0||i>=N)return;if(slides[i])loadFrame(slides[i]);", 1)
    js = js.replace("var cur=-1,buf='',hudT=0;", "var cur=-1,buf='',hudT=0;" + r'''
function loadFrame(s){var fr=s.querySelector('iframe[data-src]');if(!fr||fr.getAttribute('src'))return;fr.addEventListener('load',function(){try{fr.contentWindow.addEventListener('keydown',function(e){if(e.key==='Escape'){fr.blur();window.focus();document.body.focus&&document.body.focus()}})}catch(err){}});fr.src=fr.dataset.src}
document.addEventListener('click',function(e){var b=e.target.closest('button[data-action=storyboards]');if(!b)return;var f=slides.findIndex(function(x){return x.classList.contains('fallback')});if(f>=0)go(f)});
''', 1)
    return js
