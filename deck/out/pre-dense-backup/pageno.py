"""Physical page badge on every slide (owner request, 27 Oct ~12:00).

The number is the physical page used for jumps (type the number + Enter), so it
is written statically at build time and survives PDF export. Bottom-right by
default; on full-bleed figure/chart slides it moves to the right end of the
title strip when the figure would reach the bottom-right corner, so it never
covers a diagram.
"""
import re
import struct
from pathlib import Path

D = Path(__file__).resolve().parent
BOX_W, BOX_H = 1280, 688          # full-bleed figure area (inset 32px 0 0)
NEED_BOTTOM, NEED_RIGHT = 34, 150  # free strip the badge needs


def _dims(path):
    try:
        if path.suffix == '.svg':
            head = path.read_text(errors='ignore')[:3000]
            m = re.search(r'viewBox="[\d.\-]+ [\d.\-]+ ([\d.]+) ([\d.]+)"', head)
            if m:
                return float(m.group(1)), float(m.group(2))
            w, h = re.search(r'width="([\d.]+)', head), re.search(r'height="([\d.]+)', head)
            return float(w.group(1)), float(h.group(1))
        if path.suffix == '.png':
            b = path.read_bytes()[:24]
            return struct.unpack('>II', b[16:24])
    except Exception:
        return None
    return None


def corner_free(body):
    m = re.search(r'<img[^>]+src="([^"]+)"', body)
    if not m or m.group(1).startswith('data:'):
        return False
    dims = _dims(D / m.group(1))
    if not dims:
        return False
    w, h = dims
    if w / h >= BOX_W / BOX_H:   # width-bound: whitespace below
        return (BOX_H - BOX_W * h / w) / 2 >= NEED_BOTTOM
    return (BOX_W - BOX_H * w / h) / 2 >= NEED_RIGHT


def badge(s, index, total):
    if s['id'] == 's1':
        return ''
    label = f'{index} / {total}' + ('' if s['kind'] == 'main' else ' · ' + s['id'])
    extra = s.get('extra', '')
    top = ('pipeline-slide' in extra or
           (('figure-slide' in extra or 'chart-slide' in extra) and not corner_free(s['body'])))
    return f'<div class="pageno{" top" if top else ""}" aria-label="Page {index} of {total}">{label}</div>'


PAGENO_CSS = r'''
.foot .counter{display:none}
.pageno{position:absolute;right:16px;bottom:9px;z-index:40;font:500 14px/1 var(--mono);letter-spacing:.2px;color:#5E4D43;
 background:rgba(255,255,255,.82);padding:5px 10px;border-radius:999px;box-shadow:0 0 0 1px #EADBCB;white-space:nowrap;pointer-events:none}
.pageno.top{top:4px;bottom:auto}
.slide:has(.pageno.top)>h1{right:170px!important;overflow:hidden;text-overflow:ellipsis}
@media print{.pageno{display:block!important}}
'''
