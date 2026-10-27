"""Build reproducible presentation tables and 1280x720 charts from hosted JSON.

Usage: python analyze_rerun.py /absolute/path/to/load-test
Copy of rewind-loadtest scripts/load/analyze.py (7d6ed1e): same fit, projections and charts;
chart subtitle without the incident wording, capacity table limited to 250/500/1000 users,
and tables written to results/tables.md instead of a full RESULTS.md.
Requires numpy and matplotlib. Never reads private authentication fixtures.
"""
import json
import math
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

root = Path(sys.argv[1])
report = json.loads((root / "results/hosted.json").read_text())
stages = [s for s in report["stages"] if s["phase"] == "steady"]
if len(stages) != 5 or [s["vus"] for s in stages] != [1, 10, 25, 50, 100]:
    raise ValueError("Expected complete five-stage evidence")
# Fit only the repeating journey. The three bounded uploads are retained in
# acceptance statistics, but are not a sustained upload arrival process.
points = []
for stage in stages:
    rows = [s for s in report["samples"] if s["phase"] == "steady" and s["stage"] == stage["vus"] and not (s["operation"].startswith("upload-") or s["operation"] == "process-contribution")]
    points.append({"vus": stage["vus"], "rps": len(rows)/stage["elapsedSeconds"], "meanSeconds": sum(s["ms"] for s in rows)/len(rows)/1000})
calibration = points[1:]  # Use the sustained multi-user regime; retain 1 VU as baseline.
x = np.array([p["rps"] for p in calibration])
y = np.array([p["meanSeconds"] for p in calibration])
# One-dimensional grid with the least-squares optimum L at each S.
# Equal weights per load level avoid letting the busiest stage dominate.
ceiling = min(.999/x.max(), y.min())
grid = np.geomspace(1e-5, ceiling, 100000)
queue = grid[:, None] / (1 - grid[:, None] * x)
fixed = np.maximum(0, np.mean(y - queue, axis=1))
loss = np.mean((fixed[:, None] + queue - y)**2, axis=1)
best = int(np.argmin(loss))
S, L = float(grid[best]), float(fixed[best])
Z = 5.0

def project(n, demand=S, hosts=1):
    low, high = 0.0, hosts / demand * (1 - 1e-10)
    for _ in range(100):
        rate = (low + high)/2
        utilization = rate*demand/hosts
        response = L + demand/(1-utilization)
        if rate*(Z+response) > n:
            high = rate
        else:
            low = rate
    rate = (low+high)/2
    u = rate*demand/hosts
    return {"users": n, "throughputRps": rate, "utilization": u, "meanMs": 1000*(L+demand/(1-u))}

projections = [project(n) for n in [100,250,500,1000]]
practical_rate = .9/S
practical_users = practical_rate*(Z+L+S/.1)
model = {"model": "single serialized M/M/1 center plus fixed delay; closed-loop think time", "serviceDemandSecondsProjected": S, "fixedDelaySecondsProjected": L, "thinkTimeSeconds": Z, "rmseMs": 1000*math.sqrt(float(loss[best])), "calibrationMeasured": calibration, "baselineMeasured": points[0], "ceilingRpsProjected": 1/S, "practicalSaturationUsersProjected": practical_users, "practicalSaturationRpsProjected": practical_rate, "projections": projections, "twoHostsIdealizedProjected": [project(n, hosts=2) for n in [100,250,500,1000]], "serviceDemandSensitivityProjected": [{"demandMultiplier": multiplier, "projections": [project(n, demand=S*multiplier) for n in [100,250,500,1000]]} for multiplier in [.5,2]]}
(root/"results/capacity-model.json").write_text(json.dumps(model,indent=2)+"\n")

plt.rcParams.update({"font.size":17,"axes.titlesize":23,"axes.labelsize":18,"legend.fontsize":15,"xtick.labelsize":16,"ytick.labelsize":16,"figure.facecolor":"white","axes.spines.top":False,"axes.spines.right":False})

def figure():
    fig, ax = plt.subplots(figsize=(12.8,7.2),dpi=100)
    fig.subplots_adjust(left=.12,right=.96,bottom=.15,top=.83)
    ax.grid(axis='y',alpha=.22)
    return fig, ax

vus = [s["vus"] for s in stages]
fig, ax = figure()
for key,label,color in [("p50Ms","Measured p50","#2563eb"),("p95Ms","Measured p95","#d97706"),("p99Ms","Measured p99","#9333ea")]:
    ax.plot(vus,[s[key]/1000 for s in stages],marker='o',linewidth=2.5,label=label,color=color)
ax.axhline(2,color='#dc2626',linestyle='--',label='p95 target: 2 s')
ax.set(xlabel='Concurrent virtual users (VUs)',ylabel='End-to-end latency (seconds)',title='Rewind hosted dev: latency under load',xticks=vus)
ax.legend(loc='upper left')
fig.text(.12,.9,'CloudFront → Node → PostgreSQL • 3-minute steady windows',fontsize=14,color='#475569')
fig.savefig(root/'charts/latency-vs-vus.png');plt.close(fig)

fig, ax = figure()
ax.plot(vus,[s['throughputRps'] for s in stages],marker='o',linewidth=3,color='#059669',label='Measured completed requests/s')
ax.plot(vus,[(s['requests']-s['errors'])/s['elapsedSeconds'] for s in stages],marker='s',linewidth=2.5,color='#2563eb',label='Measured successful requests/s')
ax.set(xlabel='Concurrent virtual users (VUs)',ylabel='Throughput (requests/second)',title='Rewind hosted dev: achieved throughput',xticks=vus,ylim=(0,None))
ax.legend(loc='upper left')
fig.text(.12,.9,'Read-heavy closed loop • approximately 5 seconds think time per user',fontsize=14,color='#475569')
fig.savefig(root/'charts/throughput-vs-vus.png');plt.close(fig)

fig, ax = figure()
users=np.linspace(1,1000,300)
ax.plot(users,[project(float(n))['meanMs']/1000 for n in users],linewidth=3,color='#d97706',linestyle='--',label='Projected mean: one API host')
ax.plot(users,[project(float(n),hosts=2)['meanMs']/1000 for n in users],linewidth=2.5,color='#059669',linestyle='--',label='Projected mean: two balanced hosts')
ax.scatter(vus,[p['meanSeconds'] for p in points],s=75,color='#2563eb',zorder=4,label='Measured mean: repeating API mix')
ax.set(xlabel='Concurrent active users (5 s mean think time)',ylabel='Mean end-to-end latency (seconds)',title='Rewind capacity: measured vs projected',xlim=(0,1020),ylim=(0,None),xticks=[1,100,250,500,1000])
ax.legend(loc='upper left')
fig.text(.12,.9,f'Fitted serial demand {S*1000:.1f} ms/request • fixed delay {L*1000:.0f} ms • think time 5 s',fontsize=14,color='#475569')
fig.savefig(root/'charts/measured-vs-projected.png');plt.close(fig)

stage_table='| VUs | Requests measured | p50 ms measured | p95 ms measured | p99 ms measured | req/s measured | Errors measured | Result |\n| ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |\n'
for s in stages:
    stage_table+=f"| {s['vus']} | {s['requests']} | {s['p50Ms']:.1f} | {s['p95Ms']:.1f} | {s['p99Ms']:.1f} | {s['throughputRps']:.2f} | {s['errors']} ({s['errorRate']*100:.2f}%) | {'PASS' if s['p95Ms']<2000 and s['errorRate']<.01 else 'FAIL'} |\n"
capacity_table='| Users | req/s measured | Mean ms measured | p95 ms measured | req/s projected | Mean ms projected | U projected | Mean ms projected, two hosts |\n| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |\n'
for p,two in [(p,t) for p,t in zip(projections,model['twoHostsIdealizedProjected']) if p['users'] in (250,500,1000)]:
    measured=next((s for s in stages if s['vus']==p['users']),None)
    measured_text=f"{measured['throughputRps']:.2f} | {measured['meanMs']:.1f} | {measured['p95Ms']:.1f}" if measured else '— | — | —'
    capacity_table+=f"| {p['users']} | {measured_text} | {p['throughputRps']:.2f} | {p['meanMs']:.1f} | {p['utilization']*100:.1f}% | {two['meanMs']:.1f} |\n"
operations='| Operation | Requests measured | p50 ms measured | p95 ms measured | p99 ms measured | Errors measured |\n| --- | ---: | ---: | ---: | ---: | ---: |\n'
for op,s in report['operations'].items():
    operations+=f"| {op} | {s['requests']} | {s['p50Ms']:.1f} | {s['p95Ms']:.1f} | {s['p99Ms']:.1f} | {s['errors']} |\n"
cache={}; statuses={}
for sample in report['samples']:
    cache[sample['cache'] or 'none']=cache.get(sample['cache'] or 'none',0)+1
    statuses[str(sample['status'])]=statuses.get(str(sample['status']),0)+1
(root/'results/tables.md').write_text(f"## Stages\n\n{stage_table}\n## Operations\n\n{operations}\n## Capacity\n\n{capacity_table}\nstatuses: {json.dumps(statuses,sort_keys=True)}\ncache: {json.dumps(cache,sort_keys=True)}\nmedia: {json.dumps(report['fixture']['media'])}\n")
print(json.dumps({"passed":report['passed'],"serviceDemandMsProjected":S*1000,"fixedDelayMsProjected":L*1000,"rmseMs":model['rmseMs'],"ceilingRpsProjected":1/S,"kneeUsersProjected":practical_users,"kneeRps":practical_rate,"projections":projections,"twoHosts":model['twoHostsIdealizedProjected'],"sens":model['serviceDemandSensitivityProjected']},indent=2))
