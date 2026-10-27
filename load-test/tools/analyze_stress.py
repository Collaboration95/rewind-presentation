"""Summarise the stress-<ts>/ runs and draw the stress charts.

Series: "full" = results-fullmix.json (same 95/5 authenticated API mix as the
1-100 VU headline run, chat history populated by chat-send); "readonly" =
results.json + results-extension.json (chat-send slot reads chat; empty chat).
Usage: python -I analyze_stress.py <load-test dir> <stress dir>
"""
import json, math, sys
from collections import Counter
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

root = Path(sys.argv[1]); out = Path(sys.argv[2])
base = json.loads((root / "results/summary.json").read_text())["steadyStagesMeasured"]
model = json.loads((root / "results/capacity-model.json").read_text())

def load(files):
    runs = [json.loads((out / f).read_text()) for f in files if (out / f).exists()]
    steady, client, health, samples, stops = [], [], [], [], []
    for i, r in enumerate(runs):
        top = max([s["vus"] for s in steady], default=0)
        steady += [s | {"part": i} for s in r["stages"] if s["phase"] == "steady" and s["vus"] > top]
        client += [c | {"part": i} for c in r["client"]]; health += r["health"]; samples += r["samples"]; stops.append(r["stopReason"])
    return runs, steady, client, health, samples, stops

def verdict(s):
    if s["errorRate"] > 0.10 or s["p95Ms"] > 5000: return "STOP"
    if s["p95Ms"] >= 2000 or s["errorRate"] >= 0.01: return "FAIL"
    return "PASS"

def analyse(name, files):
    runs, steady, client, health, samples, stops = load(files)
    if not runs: return None
    def cstats(s):
        rows = [c for c in client if c["stage"] == s["vus"] and c["phase"] == "steady" and c["part"] == s["part"]]
        return {"cpuPercentMax": max(r["cpuPercent"] for r in rows), "loopP99MsMax": max(r["loopP99Ms"] for r in rows),
                "inflightMax": max(r["inflight"] for r in rows)} if rows else {}
    table = []
    for s in steady:
        rows = [x for x in samples if x["stage"] == s["vus"] and x["phase"] == "steady"]
        nonsend = [x for x in rows if x["operation"] != "chat-send"]
        table.append({k: s[k] for k in ["vus","elapsedSeconds","complete","requests","errors","errorRate","throughputRps","successRps","meanMs","p50Ms","p95Ms","p99Ms","maxMs","errorTypes"]}
                     | {"verdict": verdict(s), "client": cstats(s),
                        "errorsExcludingChatSendRateLimit": sum(1 for x in rows if not x["ok"] and not (x["operation"] == "chat-send" and (x["error"] or "").startswith("429"))),
                        "nonSendRequests": len(nonsend)})
    bp = next((t for t in table if t["verdict"] != "PASS"), None)
    # Saturation: first stage whose throughput falls below 85% of linear
    # scaling from the 100-VU stage (closed loop with no queueing).
    per_user = table[0]["successRps"] / table[0]["vus"]
    for t in table: t["linearEfficiency"] = t["successRps"] / (per_user * t["vus"])
    sat = next((t for t in table if t["linearEfficiency"] < 0.85), None)
    peak = max(table, key=lambda t: t["successRps"])
    hfail = [h for h in health if not h["ok"]]
    ops = {}
    for op in sorted({x["operation"] for x in samples if x["phase"] == "steady"}):
        rows = [x for x in samples if x["phase"] == "steady" and x["operation"] == op]
        b = sorted(x["bytes"] for x in rows)
        ops[op] = {"requests": len(rows), "medianBytes": b[len(b)//2], "errors": sum(not x["ok"] for x in rows),
                   "errorTypes": dict(Counter(x["error"] for x in rows if not x["ok"]))}
    return {"series": name, "files": [f for f in files if (out / f).exists()], "startedAt": runs[0]["startedAt"], "finishedAt": runs[-1]["finishedAt"],
            "profile": runs[0]["profile"] | {"levels": sorted({l for r in runs for l in r["profile"]["levels"]})},
            "stopReasons": stops, "steadyStages": table,
            "breakpoint": bp and {k: bp[k] for k in ["vus","p95Ms","errorRate","verdict","errorTypes"]},
            "lastPassingVus": next((t["vus"] for t in reversed(table) if t["verdict"] == "PASS" and (not bp or t["vus"] < bp["vus"])), None),
            "saturation": sat and {"vus": sat["vus"], "successRps": sat["successRps"], "linearEfficiency": sat["linearEfficiency"]},
            "peakSuccessRps": {"vus": peak["vus"], "successRps": peak["successRps"]},
            "operations": ops,
            "health": {"polls": len(health), "failures": len(hfail), "maxMs": max(h["ms"] for h in health) if health else None},
            "statusCodes": dict(Counter(str(x["status"]) for x in samples)),
            "cloudFront": dict(Counter(x["cache"] for x in samples))}

full = analyse("full", ["results-fullmix.json"])
ro = analyse("readonly", ["results.json", "results-extension.json"])
summary = {"target": "https://d2m6kz76y4kuvm.cloudfront.net", "modelCeilingRpsProjected": model["ceilingRpsProjected"], "full": full, "readonly": ro}
(out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")

# Charts ---------------------------------------------------------------
plt.rcParams.update({"font.size":17,"axes.titlesize":23,"axes.labelsize":18,"legend.fontsize":14,"xtick.labelsize":15,"ytick.labelsize":16,"figure.facecolor":"white","axes.spines.top":False,"axes.spines.right":False,"svg.fonttype":"none"})
def figure():
    fig, ax = plt.subplots(figsize=(12.8,7.2),dpi=100)
    fig.subplots_adjust(left=.12,right=.96,bottom=.15,top=.83)
    ax.grid(axis='y',alpha=.22)
    return fig, ax
main = full or ro
pts = [b for b in base] + [t for t in main["steadyStages"] if t["vus"] > 100]
for p in pts: p.setdefault("successRps", (p["requests"] - p["errors"]) / (p["requests"] / p["throughputRps"]))
pts.sort(key=lambda p: p["vus"])
vus = [p["vus"] for p in pts]
allv = sorted(set(vus) | {t["vus"] for t in ro["steadyStages"]}) if ro else vus
bp = main["breakpoint"]
per_user_main = main['steadyStages'][0]['successRps'] / main['steadyStages'][0]['vus']
def xaxis(ax, log=True):
    ticks = [v for v in allv if v not in (150, 750)] if log else [v for v in allv if v >= 100 and v not in (150,)]
    if log: ax.set_xscale("log")
    ax.set_xticks(ticks); ax.set_xticklabels([f"{v}" if log else f"{v:,}" for v in ticks]); ax.minorticks_off()
def mark_bp(ax, y, ha="right"):
    if bp:
        ax.axvline(bp["vus"], color="#475569", linestyle=":", linewidth=2)
        ax.annotate(f"Breakpoint: {bp['vus']:,} users (API mix)", xy=(bp["vus"], y), xytext=(-8 if ha == "right" else 8, 0), textcoords="offset points",
                    fontsize=15, color="#0f172a", va="center", ha=ha)

fig, ax = figure()
for key,label,color in [("p50Ms","p50","#2563eb"),("p95Ms","p95","#d97706"),("p99Ms","p99","#9333ea")]:
    ax.plot(vus,[p[key]/1000 for p in pts],marker='o',linewidth=2.5,label=f'{label}: API mix (95% reads, 5% chat-send)',color=color)
if ro and full:
    ax.plot([t["vus"] for t in ro["steadyStages"]],[t["p95Ms"]/1000 for t in ro["steadyStages"]],marker='^',linewidth=2,linestyle='--',color='#94a3b8',label='p95: read-only mix, empty chat')
ax.axhline(2,color='#dc2626',linestyle='--',label='p95 target: 2 s')
if ro and full and ro["breakpoint"]:
    rb = ro["breakpoint"]
    ax.annotate(f"Read-only\nbreakpoint:\n{rb['vus']:,} users", xy=(rb["vus"], rb["p95Ms"]/1000), xytext=(-50, -140), textcoords="offset points",
                fontsize=13, color="#475569", ha="right", va="center", arrowprops={"arrowstyle":"->","color":"#94a3b8"})
ymax = max([p["p99Ms"] for p in pts] + ([t["p95Ms"] for t in ro["steadyStages"]] if ro else []))/1000
xaxis(ax); ax.set(xlabel='Concurrent users (VUs, log scale)',ylabel='End-to-end latency (seconds)',title='Rewind hosted dev: latency to the breakpoint',ylim=(0, ymax*1.12))
mark_bp(ax, ymax*0.97)
ax.legend(loc='center left', bbox_to_anchor=(0, .62))
fig.text(.12,.9,'CloudFront → Node → PostgreSQL • 1–100 VUs: 3-min windows • 150+ VUs: 60 s steps',fontsize=14,color='#475569')
for ext in ("png","svg"): fig.savefig(root/f'charts/stress-latency-vs-users.{ext}')
plt.close(fig)

fig, ax = figure()
ax.plot(vus,[p['throughputRps'] for p in pts],marker='o',linewidth=3,color='#059669',label='Completed requests/s: API mix')
ax.plot(vus,[p['successRps'] for p in pts],marker='s',linewidth=2.5,color='#2563eb',label='Successful requests/s: API mix')
if ro and full:
    ax.plot([t["vus"] for t in ro["steadyStages"]],[t["throughputRps"] for t in ro["steadyStages"]],marker='^',linewidth=2,linestyle='--',color='#94a3b8',label='Completed requests/s: read-only mix')
ytop = max([p['throughputRps'] for p in pts] + ([t["throughputRps"] for t in ro["steadyStages"]] if ro else []))
xaxis(ax, log=False); ax.set(xlabel='Concurrent users (VUs)',ylabel='Throughput (requests/second)',title='Rewind hosted dev: throughput to saturation',ylim=(0,ytop*1.2),xlim=(0,max(allv)*1.04))
mark_bp(ax, ytop*0.6, ha="left")
sat = main["saturation"] or main["peakSuccessRps"]
if main["saturation"]:
    lx = [0, max(allv)]
    ax.plot(lx,[x * per_user_main for x in lx],linestyle=':',linewidth=2,color='#059669',alpha=.7,label='Linear scaling from 100 users (no queueing)')
    ax.annotate(f"Saturation: {main['saturation']['vus']:,} users, {main['saturation']['successRps']:.0f} req/s", xy=(main['saturation']["vus"], main['saturation']["successRps"]),
                xytext=(60, -10), textcoords="offset points", fontsize=15, ha="left", va="center", arrowprops={"arrowstyle":"->","color":"#0f172a"})
ax.legend(loc='upper left')
fig.text(.12,.9,'Closed loop • approximately 5 seconds think time per user',fontsize=14,color='#475569')
for ext in ("png","svg"): fig.savefig(root/f'charts/stress-throughput-vs-users.{ext}')
plt.close(fig)

# Markdown tables ------------------------------------------------------
def fmt_err(t): return ", ".join(f"{k} {v}" for k, v in sorted(t["errorTypes"].items(), key=lambda kv: -kv[1])) or "none"
def md(series):
    lines = ["| Users | Requests | p50 ms | p95 ms | p99 ms | req/s | OK req/s | Errors | Error types | Linear % | Client CPU max | Verdict |",
             "| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: | --- |"]
    for t in series["steadyStages"]:
        c = t["client"]
        lines.append(f"| {t['vus']:,} | {t['requests']:,} | {t['p50Ms']:.0f} | {t['p95Ms']:.0f} | {t['p99Ms']:.0f} | {t['throughputRps']:.1f} | {t['successRps']:.1f} | "
                     f"{t['errors']:,} ({t['errorRate']*100:.2f}%) | {fmt_err(t)} | {t['linearEfficiency']*100:.0f}% | {c.get('cpuPercentMax', 0):.0f}% | {t['verdict']}{'' if t['complete'] else ' (stopped at ' + format(t['elapsedSeconds'], '.0f') + ' s)'} |")
    return "\n".join(lines) + "\n"
txt = "".join(f"## {s['series']}\n\n{md(s)}\n" for s in (full, ro) if s)
(out / "tables.md").write_text(txt); print(txt)
for s in (full, ro):
    if s: print(s["series"], json.dumps({k: s[k] for k in ["stopReasons","breakpoint","lastPassingVus","saturation","peakSuccessRps","health","statusCodes","cloudFront"]}))
