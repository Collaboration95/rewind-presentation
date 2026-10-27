# Rewind load-test results

**Headline run:** 2026-10-26T15:56:55.909Z to 16:13:23.955Z UTC (26 Oct 23:56–27 Oct 00:13 SGT). Target: hosted dev, https://d2m6kz76y4kuvm.cloudfront.net. Deployed build: dev `2390589dbf1d731fba9810ac410f5b31ac1c23c4`, installed by [Deploy dev 40350232534](https://github.com/Collaboration95/rewind-app/actions/runs/40350232534), which finished successfully at 15:56:03Z.

**Source and command.** The default profile of `scripts/load/hosted.mjs` was run with Node v26.3.1 from the presenter's Mac. The script is byte-identical to `origin/dev`.

```sh
TARGET_URL=https://d2m6kz76y4kuvm.cloudfront.net MAX_VUS=100 \
OUTPUT=presentation-prep/load-test/rerun-local-20261026T155655Z/results.json \
node scripts/load/hosted.mjs
```

The GitHub `performance.yml` dispatch was attempted first, twice. Both attempts returned HTTP 404 because the workflow is on `dev` but not on the default branch `main`. No Actions run was created. The exact errors are in `rerun-local-20261026T155655Z/dispatch-attempts.txt`.

**Quiet host.** No GitHub Actions run was queued or in progress between 15:56:03Z and 16:13:24Z. The run started 52 s after the deploy finished.

## Measured hosted performance

Overall stage gate: **PASS**. Every steady stage meets p95 < 2 s and errors < 1%. Steady windows: 6,038 requests, **0 errors**, overall p95 1,163.6 ms, p99 1,520.1 ms, max 1,972.7 ms. Each stage has a 15 s ramp and a 180 s steady window; ramps are in the raw JSON and are left out of this table.

| VUs | Requests measured | p50 ms measured | p95 ms measured | p99 ms measured | req/s measured | Errors measured | Result |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 1 | 38 | 765.1 | 1057.7 | 1238.1 | 0.21 | 0 (0.00%) | PASS |
| 10 | 330 | 389.8 | 663.4 | 827.4 | 1.83 | 0 (0.00%) | PASS |
| 25 | 826 | 379.0 | 674.9 | 944.4 | 4.59 | 0 (0.00%) | PASS |
| 50 | 1632 | 432.2 | 842.4 | 1105.6 | 9.06 | 0 (0.00%) | PASS |
| 100 | 3212 | 496.0 | 1335.9 | 1635.9 | 17.84 | 0 (0.00%) | PASS |

At 100 VUs, p95 is 1.34 s, which leaves 0.66 s of headroom below the 2 s target. Throughput rises linearly with users, from 1.83 to 17.84 req/s. Status codes across setup, ramps and steady windows: `{"200": 6149, "201": 330}`; no 4xx or 5xx. CloudFront: every API request was a cache miss and reached the origin (6,479). Health at start: PostgreSQL, ffmpeg configured, schema migration 31 ready.

| Operation | Requests measured | p50 ms measured | p95 ms measured | p99 ms measured | Errors measured |
| --- | ---: | ---: | ---: | ---: | ---: |
| chat-read | 1816 | 523.5 | 1264.3 | 1612.8 | 0 |
| home | 1213 | 368.5 | 1112.8 | 1452.8 | 0 |
| archive | 906 | 367.0 | 1139.1 | 1466.3 | 0 |
| groups | 895 | 373.6 | 1014.6 | 1398.6 | 0 |
| contributions | 601 | 360.8 | 1016.5 | 1357.1 | 0 |
| chat-send | 304 | 774.3 | 1445.5 | 1752.8 | 0 |
| media-capability | 297 | 360.9 | 1089.2 | 1435.4 | 0 |
| upload-source | 3 | 670.5 | 819.0 | 819.0 | 0 |
| upload-contribution | 3 | 408.9 | 642.2 | 642.2 | 0 |

The workload is three synthetic accounts in one new private group. It is 95% reads and 5% chat writes, plus three photo uploads that were processed in the first steady window. Archive capability requests: 318, each returning an empty collecting-state Archive. The group was still collecting, so no film playback or compilation was in this workload.

## Capacity model: projected

The model is fitted to the measured means of the repeating API mix at 10, 25, 50 and 100 VUs. Uploads are excluded, and 1 VU is kept as a separate baseline.

- Serialized service demand: **S = 45.39 ms/request**, inferred from the measured means.
- Fixed network/parallel delay: **L = 377.9 ms**.
- Fit error (RMSE): 10.3 ms.
- Equations: U = λS, R = L + S/(1−U), λ = N/(Z+R), with think time Z = 5 s. They are solved together for each user count N.

| Users | req/s measured | Mean ms measured | p95 ms measured | req/s projected | Mean ms projected | U projected | req/s projected, two hosts | Mean ms projected, two hosts |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 250 | — | — | — | 21.87 | 6433.1 | 99.3% | 41.18 | 1071.2 |
| 500 | — | — | — | 21.97 | 17754.3 | 99.7% | 43.73 | 6433.1 |
| 1000 | — | — | — | 22.01 | 40441.2 | 99.9% | 43.95 | 17754.3 |

For comparison, the measured 100-VU point gives 17.84 req/s and a 615.4 ms mean. The model projects 17.81 req/s and a 614.8 ms mean at the same load.

- **Ceiling:** about **22.0 req/s** on one API host (projected).
- **Knee:** the projected knee (U = 90%) is **19.8 req/s**, at about **116 active users**.
- **Beyond the knee:** throughput flattens and the projected mean latency rises roughly linearly with users.
- **Two hosts:** two balanced API hosts double the projected ceiling to 44.1 req/s, keeping 250 users near a 1.07 s mean.
- **Sensitivity at 1,000 users:** half the fitted S projects 44.0 req/s with a 17.7 s mean; double S projects 11.0 req/s with an 85.9 s mean.

All inputs and outputs are in `results/capacity-model.json`.

## Bottleneck and scale-out

| Component | Measured | Source evidence and projected implication |
| --- | --- | --- |
| Node event loop + PostgreSQL bridge | Latencies above | `server/src/postgres/database.ts` uses Atomics.wait; `server/src/postgres/sync-worker.ts` runs one pg Client. Main-thread requests serialize around synchronous database calls, which matches the single serialized centre the model fits. |
| PostgreSQL connections and writes | PostgreSQL confirmed by health | One client serializes calls; there is no request-serving pool. The schema-wide advisory writer lock serializes write transactions across hosts, so a second API host adds read concurrency but not shared write throughput. |
| ffmpeg media processing | Three small photo jobs, 0 errors | ffmpeg is a child process sharing the Lightsail CPU. Film compilation competes for that CPU and raises the effective S. |

**Scale-out path:**

1. Put a second API host behind a load balancer. Sessions are already in PostgreSQL. Media capabilities and staged media are host-local, so this needs routing affinity or shared state. Scheduler jobs need coordinated ownership.
2. Move the media worker to its own host, so film compilation does not take API CPU.
3. Make persistence asynchronous with a bounded connection pool. This removes the serialization that sets S.

CloudFront stays the edge, and PostgreSQL and S3 stay shared. No infrastructure or configuration was changed for this test.

## Earlier run (superseded)

The first full run on 26 Oct, 14:31–14:47 UTC, overlapped [Deploy dev 40341542790](https://github.com/Collaboration95/rewind-app/actions/runs/40341542790). That deploy installed a release from 14:45:06 to 14:46:30 UTC. All 339 errors (502/503/504) fell between 14:46:00.7Z and 14:46:26.6Z, inside the install window. The 100-VU stage therefore failed its error gate, at 10.88%; stages 1 to 50 passed.

The headline run above replaces it: same profile, quiet host, 0 errors. The earlier data, charts and post-deploy read-only confirmation are kept in `previous-run-20261026T1431Z/`.

## Files

- `charts/latency-vs-vus.png`: measured p50/p95/p99 against the 2 s target (1280×720).
- `charts/throughput-vs-vus.png`: measured throughput (1280×720).
- `charts/measured-vs-projected.png`: measured means with projected one-host and two-host means up to 1,000 users (1280×720).
- `results/hosted.json`: the raw headline run, also at `rerun-local-20261026T155655Z/results.json`. It holds per-request observations and no credentials.
- `results/summary.json`: the machine-readable summary for the video, also in the rerun folder.
- `results/capacity-model.json`, `results/tables.md`, `results/runner-SUMMARY.md`.
- `tools/analyze_rerun.py`: a copy of `scripts/load/analyze.py` from `origin/dev`. It preserves the fit, projections and charts, updates the projection chart subtitle and limits the capacity table to 250/500/1000. Regenerate with `python -I tools/analyze_rerun.py "$PWD"` (needs numpy and matplotlib).

## Stress / breakpoint (27 Oct 2026)

**Run:** 2026-10-27 04:08:27–04:26:22 UTC (12:08–12:26 SGT) against hosted dev, https://d2m6kz76y4kuvm.cloudfront.net. All load stopped at 12:26:22 SGT. The host was confirmed healthy from 12:26:41 to 12:30:05 SGT. Raw data is in `stress-20261027T040827Z/`.

**Runner:** `tools/stress.mjs` reuses the request function, operation mix, 3–7 s think time, 15 s timeout and nearest-rank percentiles of `scripts/load/hosted.mjs` (`origin/dev`). That script caps `MAX_VUS` at 100, so `stress.mjs` adds:

- stages above 100 users, each with a 15 s ramp and a 60 s steady window;
- classification of every failure as 5xx, 429 (with the API error code), timeout or client socket error;
- a health poll every 5 s and a client CPU and event-loop monitor;
- stop conditions: a stage or rolling 15 s window with errors > 10% or p95 > 5 s, two consecutive health failures, or 13:00 SGT.

The fixture is three synthetic accounts and one new private group. No uploads ran. The breakpoint is the first stage with p95 ≥ 2 s or errors ≥ 1%. The saturation point is the first stage whose throughput falls below 85% of linear scaling from 100 users.

Two workloads were run:

- **API mix** is the same mix as the 1–100 run: 95% authenticated reads and 5% chat-send into the run's own group. Chat history fills, so chat-read returns 30 messages (median 11,380 B, as in the headline run).
- **Read-only mix** is the `CONFIRMATION_ONLY` profile: the chat-send slot reads chat instead. The group's chat stays empty, so chat-read returns 101 B and nothing is written. It measures the cheapest authenticated read path, not the product mix.

### API mix: breakpoint

| Users | Window | p50 ms | p95 ms | p99 ms | req/s | Errors | Error types | Verdict |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| 1 | 180 s (26 Oct) | 765 | 1,058 | 1,238 | 0.21 | 0.00% | none | PASS |
| 10 | 180 s (26 Oct) | 390 | 663 | 827 | 1.83 | 0.00% | none | PASS |
| 25 | 180 s (26 Oct) | 379 | 675 | 944 | 4.59 | 0.00% | none | PASS |
| 50 | 180 s (26 Oct) | 432 | 842 | 1,106 | 9.06 | 0.00% | none | PASS |
| 100 | 180 s (26 Oct) | 496 | 1,336 | 1,636 | 17.84 | 0.00% | none | PASS |
| 100 | 60 s | 459 | 990 | 1,550 | 18.1 | 0.00% | none | PASS |
| 150 | 60 s | 685 | 1,656 | 2,379 | 25.7 | 0.00% | none | PASS |
| **200** | 60 s | 1,871 | **3,030** | 3,469 | 29.0 | 0.00% | none | **FAIL: breakpoint** |
| 300 | 35 s, stopped | 3,080 | 6,798 | 7,299 | 36.3 | 0.00% | none | STOP: rolling p95 7.2 s > 5 s |

- **Breakpoint: 200 concurrent users.** p95 is 3.03 s, above the 2 s target, with 0 errors. The last passing stage is 150 users at p95 1.66 s.
- **Saturation: 200 users at 29.0 req/s,** which is 80% of linear scaling. At 300 users, throughput reaches 36.3 req/s (67% of linear) while p50 climbs to 3.1 s. Ramping stopped there.
- **How it fails:** latency rises through queueing, and nothing is rejected. All 7,223 API-mix requests returned 200 or 201. There were no 5xx, no 429s, no timeouts and no socket errors. The health endpoint answered 200 on 47/47 polls, but took up to 6.7 s, because it waits in the same queue.

### Read-only mix: read-path ceiling

| Users | p50 ms | p95 ms | p99 ms | req/s | Errors | Verdict |
| ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 100 | 299 | 430 | 529 | 18.8 | 0.00% | PASS |
| 150 | 297 | 434 | 676 | 28.0 | 0.00% | PASS |
| 200 | 299 | 438 | 764 | 37.5 | 0.00% | PASS |
| 300 | 300 | 427 | 693 | 56.3 | 0.00% | PASS |
| 500 | 307 | 475 | 1,037 | 93.7 | 0.00% | PASS |
| 750 | 316 | 577 | 1,718 | 139.6 | 0.00% | PASS |
| 1,000 | 330 | 578 | 1,066 | 186.4 | 0.00% | PASS |
| **1,500** | 374 | **4,550** | 5,489 | 262.6 | 0.00% | **FAIL**, stopped at 35 s (rolling p95 5.25 s > 5 s) |

On the read-only path, throughput scales linearly to 1,500 users (93% of linear, 262.6 req/s). The 1,500-user stage then breaks on a single stall of the whole server. At 04:20:01Z, completions fell from about 290/s to 43/s for 2 s. Queued requests then finished about 5 s late, and the health poll took 5.0 s. Service resumed at normal latency by 04:20:09Z. A smaller 1.1 s stall had already appeared at 750 users (04:15:02Z). All 67,195 read-only requests returned 200.

### Why the stress numbers differ from the 1–100 run

- **Workload.** Think time (3–7 s), timeout and operation shares match the 1–100 run. The read-only mix removes the 5% chat writes, and its empty chat makes chat-read 113× smaller (101 B against 11,380 B). Home (643 B), groups (646 B) and Archive (128 B) payloads are byte-identical to the headline run. The API mix restores the writes and the populated chat. Its 100-user p95 is 990 ms, against 1,336 ms for the headline run's 180 s window.
- **CloudFront.** Every request reached the origin: `x-cache: Miss from cloudfront` on 74,418 of 74,418. API responses carry `cache-control: no-store`.
- **Success accounting.** A request succeeds only on its expected status (200, or 201 for chat-send) and a JSON body without an `error` field. The only statuses seen were 200 and 201. There were no 304, 403 or 429 responses.
- **Authentication.** Every request carries a bearer session. An unauthenticated `GET /api/real/groups` returns 401, and the same request with the session returns 200 with the group JSON.

### Limiting factor

- **Not the load generator.** Client Node CPU peaked at 26% of one core (8% during the API mix), and event-loop p99 stayed ≤ 22 ms. `ulimit -n` was 65,536. There were no socket errors or client timeouts.
- **Not a rate limiter.** There were zero 429s. The server's limiters are per account, not per IP: chat-send allows 30 messages per minute per account, and Archive allows two concurrent requests. Neither limit was reached. CloudFront applied no throttling.
- **Not host CPU.** Lightsail `CPUUtilization` (2 vCPU, `micro_3_0`, 5-minute maximum) peaked at 25.2% during the read-only 1,000–1,500 stages. During the API-mix saturation it was at most 12.5%. Burst capacity stayed at or above 99.6%.
- **The server's serialized PostgreSQL bridge.** Requests run on one Node event loop, and every database call blocks it through `Atomics.wait` on a single `pg` client (`server/src/postgres/database.ts`, `sync-worker.ts`). Throughput therefore stops at 1 / (database time per request), while the CPU stays mostly idle. Every route, including `/api/health`, waits in the same queue.
  - The API mix costs more database time per request: its chat reads return 30 messages, and its writes take the schema-wide writer lock. It saturates at about 29–36 req/s, an effective serialized demand of about 28–34 ms per request.
  - The read-only mix costs under 4 ms per request. It scales past 260 req/s, until a single slow database round trip stalls every request at once.
- **Capacity model check.** The model fitted on 26 Oct (S = 45.4 ms, ceiling 22.0 req/s, knee about 116 users) has the same shape. It is about 1.4× conservative: the measured knee lies between 150 and 200 users, and saturation lies between 29 and 36 req/s.

### What would scale it

From the capacity model, in order of effect:

1. **Asynchronous persistence with a bounded connection pool.** This removes the serialization that sets S, which is the binding limit here because CPU sits at or below 25%.
2. **A second API host behind a load balancer.** The model doubles the ceiling, to 44.1 req/s, with 250 users near a 1.07 s mean. This needs routing affinity for host-local media state. Writes still serialize on the PostgreSQL advisory lock.
3. **A separate media worker.** This keeps film compilation off the API host. It has no effect on this workload, which runs no ffmpeg jobs.

A larger instance alone would add little, because the CPU is not saturated.

### Recovery

Load stopped at 04:26:22Z. From 04:26:41Z to 04:30:05Z, one request every 5 s showed:

- health: 30/30 returned 200, median 816 ms (856 ms before the test);
- home: median 298 ms;
- chat-read (11 KB): median 603 ms;
- app page `/`: 200.

The host returned to baseline within 20 s of the stop, with no restarts and no errors.

### Stress files

- `charts/stress-latency-vs-users.png` and `.svg`: API-mix p50/p95/p99 from 1 to 300 users (1–100 from the 26 Oct headline run), the read-only p95 to 1,500 users, the 2 s target and the breakpoint (1280×720).
- `charts/stress-throughput-vs-users.png` and `.svg`: completed and successful req/s for both mixes against linear scaling, with the saturation point marked (1280×720).
- `stress-20261027T040827Z/`:
  - `results.json`: read-only, 100–1,000 users;
  - `results-extension.json`: read-only, 1,000–1,500 users;
  - `results-fullmix.json`: API mix, 100–300 users;
  - `summary.json` and `tables.md`;
  - `recovery.json`, `host-metrics-lightsail.txt`;
  - `runner*.log`.

  The raw files hold per-request observations (operation, ms, status, error type, bytes, x-cache) and no credentials.
- `tools/stress.mjs`: the runner. `tools/analyze_stress.py`: summaries and charts. Regenerate with `python -I tools/analyze_stress.py "$PWD" "$PWD/stress-20261027T040827Z"` (needs matplotlib).
