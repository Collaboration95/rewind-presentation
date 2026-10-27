"""Small-multiple charts drawn as inline SVG from the retained records, so related
charts share one slide and every label stays >= 14 px at 1280x720 (the viewBox
equals the rendered size)."""
import csv
import json
from datetime import date
from pathlib import Path

P = Path(__file__).resolve().parent.parent
INK, MUTED, LINE, ACC, PEACH, BLUE, GREY = '#33231A', '#5E4D43', '#E6D5C3', '#A84A1A', '#F0A06C', '#2B5C86', '#8C7B6E'
FONT = 'font-family="Geist,-apple-system,Arial,sans-serif"'


def _svg(w, h, inner, label):
    return (f'<svg class="mchart" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{label}" {FONT}>'
            + inner + '</svg>')


def _t(x, y, s, size=14, fill=MUTED, anchor='start', weight=400):
    return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{weight}">{s}</text>'


def burndown(n, w=350, h=232):
    rows = list(csv.DictReader(open(P / f'records/data/burndown-sprint-{n}.csv')))
    days = [date.fromisoformat(r['date_sgt']) for r in rows]
    scope = [int(r['scope_issues']) for r in rows]
    open_ = [int(r['open_issues']) for r in rows]
    top = max(scope) or 1
    L, R, T, B = 38, 10, 46, 30
    X = lambda i: L + (w - L - R) * i / max(1, len(rows) - 1)
    Y = lambda v: T + (h - T - B) * (1 - v / top)
    def step(vals):
        d = f'M{X(0):.1f},{Y(vals[0]):.1f}'
        for i in range(1, len(vals)):
            d += f' H{X(i):.1f} V{Y(vals[i]):.1f}'
        return d
    area = step(open_) + f' V{Y(0):.1f} H{X(0):.1f} Z'
    span = f"{days[0].day} {days[0]:%b}–{days[-1].day} {days[-1]:%b}"
    inner = (_t(0, 17, f'Sprint {n}', 16, INK, weight=650) + _t(70, 17, span, 14) +
             _t(0, 36, f'scope {scope[0]} → {scope[-1]} · open {open_[0]} → {open_[-1]}', 14, ACC, weight=600) +
             f'<line x1="{L}" x2="{w-R}" y1="{Y(0):.1f}" y2="{Y(0):.1f}" stroke="{LINE}"/>' +
             _t(L - 6, Y(top) + 5, str(top), 14, MUTED, 'end') + _t(L - 6, Y(0) + 5, '0', 14, MUTED, 'end') +
             f'<path d="{area}" fill="{PEACH}" opacity=".28"/>' +
             f'<path d="{step(scope)}" fill="none" stroke="{GREY}" stroke-width="2" stroke-dasharray="6 4"/>' +
             f'<path d="{step(open_)}" fill="none" stroke="{ACC}" stroke-width="3"/>' +
             _t(X(0), h - 8, f'{days[0].day} {days[0]:%b}', 14) + _t(X(len(rows) - 1), h - 8, f'{days[-1].day} {days[-1]:%b}', 14, anchor='end'))
    return _svg(w, h, inner, f'Sprint {n} burndown: scope {scope[0]} to {scope[-1]}, open {open_[0]} to {open_[-1]}')


def velocity(w=350, h=232):
    rows = list(csv.DictReader(open(P / 'records/data/velocity.csv')))
    closed = [int(r['closed_issues_all_milestones']) for r in rows]
    prs = [int(r['merged_prs_all_bases']) for r in rows]
    top = max(closed + prs)
    L, R, T, B = 10, 10, 64, 30
    gw = (w - L - R) / len(rows)
    Y = lambda v: T + (h - T - B) * (1 - v / top)
    inner = _t(0, 17, 'Velocity', 16, INK, weight=650) + _t(0, 36, '■ issues closed', 14, ACC, weight=600) + _t(118, 36, '■ PRs merged', 14, BLUE, weight=600)
    for i, (c, p) in enumerate(zip(closed, prs)):
        x = L + i * gw + gw * .14
        bw = gw * .34
        inner += f'<rect x="{x:.1f}" y="{Y(c):.1f}" width="{bw:.1f}" height="{Y(0)-Y(c):.1f}" fill="{ACC}" rx="3"/>'
        inner += f'<rect x="{x+bw+3:.1f}" y="{Y(p):.1f}" width="{bw:.1f}" height="{Y(0)-Y(p):.1f}" fill="{BLUE}" rx="3"/>'
        inner += _t(x + bw / 2, Y(c) - 4, str(c), 14, INK, 'middle') + _t(x + bw * 1.5 + 3, Y(p) - 4, str(p), 14, INK, 'middle')
        inner += _t(L + i * gw + gw / 2, h - 8, f'S{i}', 14, MUTED, 'middle')
    return _svg(w, h, inner, 'Velocity: issues closed 44, 100, 145, 30; PRs merged 11, 36, 132, 34')


def _stages():
    return json.loads((P / 'load-test/results/summary.json').read_text())['steadyStagesMeasured']


def _xy_chart(w, h, title, series, ymax, yticks, yfmt, target=None, xlabel='concurrent users', xs=None):
    L, R, T, B = 52, 16, 40, 44
    xs = xs or sorted({x for _, pts, _ in series for x, _ in pts})
    X = lambda x: L + (w - L - R) * xs.index(x) / (len(xs) - 1)
    Y = lambda v: T + (h - T - B) * (1 - v / ymax)
    inner = _t(0, 18, title, 16, INK, weight=650)
    for v in yticks:
        inner += f'<line x1="{L}" x2="{w-R}" y1="{Y(v):.1f}" y2="{Y(v):.1f}" stroke="{LINE}"/>' + _t(L - 8, Y(v) + 5, yfmt(v), 14, MUTED, 'end')
    if target:
        inner += f'<line x1="{L}" x2="{w-R}" y1="{Y(target[0]):.1f}" y2="{Y(target[0]):.1f}" stroke="#B3261E" stroke-dasharray="6 4" stroke-width="2"/>'
        inner += _t(L + 6, Y(target[0]) - 6, target[1], 14, '#B3261E', 'start', 600)
    for name, pts, color in series:
        inner += '<polyline fill="none" stroke="' + color + '" stroke-width="3" points="' + ' '.join(f'{X(x):.1f},{Y(y):.1f}' for x, y in pts) + '"/>'
        inner += ''.join(f'<circle cx="{X(x):.1f}" cy="{Y(y):.1f}" r="4" fill="{color}"/>' for x, y in pts)
        lx, ly = pts[-1]
        inner += _t(X(lx) - 8, Y(ly) - 10, name, 14, color, 'end', 650)
    for x in xs:
        inner += _t(X(x), h - 22, str(x), 14, MUTED, 'middle')
    inner += _t((L + w - R) / 2, h - 4, xlabel, 14, MUTED, 'middle')
    return _svg(w, h, inner, title)


def latency(w=560, h=330, stages=None):
    st = stages or _stages()
    ser = [(k, [(s['vus'], s[f'{k}Ms'] / 1000) for s in st], c) for k, c in (('p99', GREY), ('p95', ACC), ('p50', BLUE))]
    top = max(2.2, max(y for _, p, _ in ser for _, y in p) * 1.1)
    ticks = [0, .5, 1, 1.5, 2] if top <= 2.6 else [0, 2, 4, 6, 8, 10][: int(top // 2) + 1]
    return _xy_chart(w, h, 'Latency by stage · seconds', ser, top, ticks, lambda v: f'{v:g}', (2, '2 s target'))


def throughput(w=560, h=330, stages=None):
    st = stages or _stages()
    pts = [(s['vus'], s['throughputRps']) for s in st]
    top = max(y for _, y in pts) * 1.15
    step = 5 if top <= 25 else 10
    return _xy_chart(w, h, 'Throughput · requests per second', [('req/s', pts, ACC)], top,
                     list(range(0, int(top) + 1, step)), lambda v: f'{v:g}')


CHART_CSS = r'''
.mgrid{display:grid;gap:14px;height:100%}
.mgrid.pm{grid-template-columns:repeat(3,1fr);grid-template-rows:1fr 1fr}
.mgrid .cell{background:rgba(255,255,255,.72);border:1px solid rgba(255,255,255,.9);border-radius:18px;padding:8px 10px;display:flex;align-items:center;justify-content:center;
 box-shadow:inset 0 1px 1px #fff,0 14px 30px -20px rgba(160,90,40,.35);overflow:hidden}
.mgrid .cell.text{display:block;padding:14px 18px}.mgrid .cell.text p{font-size:16px;line-height:1.32;margin:0 0 8px;color:#5E4D43}.mgrid .cell.text b{color:#33231A}
.mgrid.two{grid-template-columns:1fr 1fr}
.mchart{display:block;max-width:100%;height:auto}
'''


# API-mix stages, load-test/RESULTS.md "Stress / breakpoint" (27 Oct): 1-100 from the
# 26 Oct 180 s run, 150-300 from the 27 Oct 60 s stress stages.
STRESS = [
    # users, p50, p95, p99 (ms), req/s, errors %, verdict
    (1, 765, 1058, 1238, 0.21, 0.0, 'PASS'), (10, 390, 663, 827, 1.83, 0.0, 'PASS'), (25, 379, 675, 944, 4.59, 0.0, 'PASS'),
    (50, 432, 842, 1106, 9.06, 0.0, 'PASS'), (100, 496, 1336, 1636, 17.84, 0.0, 'PASS'), (150, 685, 1656, 2379, 25.7, 0.0, 'PASS'),
    (200, 1871, 3030, 3469, 29.0, 0.0, 'BREAKPOINT'), (300, 3080, 6798, 7299, 36.3, 0.0, 'STOPPED'),
]


def stress_latency(w=560, h=262):
    ser = [(k, [(r[0], r[i] / 1000) for r in STRESS], c) for k, i, c in (('p99', 3, GREY), ('p95', 2, ACC), ('p50', 1, BLUE))]
    svg = _xy_chart(w, h, 'Latency by users · seconds (API mix)', ser, 7.6, [0, 2, 4, 6], lambda v: f'{v:g}', (2, '2 s target'))
    xs = [r[0] for r in STRESS]
    L, R, T, B = 52, 16, 40, 44
    x = L + (w - L - R) * xs.index(200) / (len(xs) - 1)
    mark = (f'<line x1="{x:.1f}" x2="{x:.1f}" y1="{T}" y2="{h-B}" stroke="#B3261E" stroke-width="2" stroke-dasharray="3 3"/>'
            + _t(x - 6, T + 16, 'breakpoint 200', 14, '#B3261E', 'end', 650))
    return svg.replace('</svg>', mark + '</svg>')


def stress_throughput(w=560, h=262):
    pts = [(r[0], r[4]) for r in STRESS]
    lin = [(r[0], 17.84 * r[0] / 100) for r in STRESS if r[0] >= 100]
    svg = _xy_chart(w, h, 'Throughput · req/s vs linear from 100 users', [('linear', lin, GREY), ('measured', pts, ACC)], 58,
                    [0, 20, 40], lambda v: f'{v:g}', xs=[r[0] for r in STRESS])
    return svg
