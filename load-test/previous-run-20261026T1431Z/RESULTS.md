# Rewind load-test results

Hosted test: 2026-10-26T14:31:15.377Z to 2026-10-26T14:47:38.263Z (UTC). Target: https://d2m6kz76y4kuvm.cloudfront.net. Source baseline: origin/dev f6cd8969379ba720fc0508833f138e29475bc32a. Driver: plain Node v26.3.1 from this Mac.

## Measured hosted performance

Overall stage gate: **FAIL**. Each steady stage must meet p95 < 2 seconds and errors < 1%. Steady samples: 5967; errors: 339; overall p95: 1130.3 ms. The five steady windows total 900.2 seconds. Ramps are retained in raw JSON and excluded from this table.

| VUs | Requests measured | p50 ms measured | p95 ms measured | p99 ms measured | req/s measured | Errors measured | Result |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 1 | 38 | 706.6 | 907.3 | 997.7 | 0.21 | 0 (0.00%) | PASS |
| 10 | 334 | 369.4 | 537.0 | 1026.8 | 1.85 | 0 (0.00%) | PASS |
| 25 | 833 | 356.5 | 629.3 | 789.1 | 4.63 | 0 (0.00%) | PASS |
| 50 | 1645 | 392.7 | 859.1 | 1329.7 | 9.14 | 0 (0.00%) | PASS |
| 100 | 3117 | 489.3 | 1368.0 | 8266.4 | 17.31 | 339 (10.88%) | FAIL |

The highest passing tested stage is **50 VUs**. At 100 VUs, the error gate fails despite p95 meeting the latency target. Failures are clustered in a short upstream-error interval; acceptance keeps every failure. Host CPU: **unobserved**. The health endpoint reports PostgreSQL, ffmpeg configured and migration 31 ready. Status counts across ramps and steady windows: `{"200": 5744, "201": 316, "502": 115, "503": 178, "504": 46}`. CloudFront cache headers: `{"Error from cloudfront": 339, "Miss from cloudfront": 6060}`.

| Operation | Requests measured | p50 ms measured | p95 ms measured | p99 ms measured | Errors measured |
| --- | ---: | ---: | ---: | ---: | ---: |
| upload-source | 3 | 462.3 | 706.6 | 706.6 | 0 |
| upload-contribution | 3 | 478.5 | 755.1 | 755.1 | 0 |
| chat-read | 1789 | 503.2 | 1179.4 | 6972.2 | 98 |
| home | 1195 | 356.8 | 1072.7 | 8237.2 | 63 |
| archive | 892 | 357.0 | 992.6 | 6498.1 | 52 |
| contributions | 596 | 344.3 | 1030.2 | 6668.9 | 39 |
| groups | 894 | 341.1 | 1035.1 | 6925.5 | 55 |
| media-capability | 294 | 334.9 | 932.5 | 7498.8 | 20 |
| chat-send | 301 | 729.1 | 1375.2 | 5683.8 | 12 |

Uploads: 3 tiny photos attempted; source, contribution and processing results appear above. Capability requests returned 0 nonempty download paths and 293 empty collecting-state archives. Media transfer and a populated released Archive were not exercised. The maximum tested activity was 100 VUs sharing three accounts in one test group.

## Capacity model: projected

The repeating API journey is fitted separately from the three bounded uploads. Fit the sustained multi-user regime (10/25/50/100 VUs); retain 1 VU as a separately measured baseline. The 1-VU stage is sparse and uses a different pooled-connection cadence. Fit effective serialized demand **S = 51.039 ms/request** and fixed network/parallel delay **L = 341.8 ms**; four-level mean-response RMSE = 9.8 ms. S is an inferred service demand, not a measured CPU service time. The calibration includes failed requests: the short 100-VU upstream incident raises the fitted demand. Treat this as an incident-influenced operational projection, not proof that physical host saturation occurred. The input measurements and all model outputs are in `results/capacity-model.json`.

Use U = λS and R_queue = S/(1−U). Add fixed delay: R = L + R_queue. Users think for Z = 5 seconds, so λ = N/(Z+R). Solve these equations together; assuming λ=N/5 after saturation would overstate throughput. R is a mean. Do not compare this projected mean directly with the measured p95 acceptance target.

| Users | req/s measured | Mean ms measured | p95 ms measured | req/s projected | Mean ms projected | U projected | Mean ms projected, two hosts |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 100 | 17.31 | 779.5 | 1368.0 | 17.30 | 778.8 | 88.3% | 438.0 |
| 250 | — | — | — | 19.46 | 7847.0 | 99.3% | 1640.8 |
| 500 | — | — | — | 19.54 | 20583.8 | 99.7% | 7847.0 |
| 1000 | — | — | — | 19.57 | 46095.6 | 99.9% | 20583.8 |

Modeled single-center ceiling: **19.6 requests/second**. Practical saturation at U=90%: **17.6 requests/second**, approximately **103 active users** under this think-time model. This is a projected knee; the test establishes results only through 100 VUs. At the ceiling the open-queue formula diverges; in the closed user model throughput approaches the ceiling while latency rises. Saturation of physical CPU or PostgreSQL was not measured.

Sensitivity at 1,000 users: halving fitted S projects 39.1 req/s and 20552 ms mean; doubling S projects 9.8 req/s and 97185 ms mean. Higher populations use the same small group and response-size assumptions as calibration.

## Bottleneck and scale-out

| Component | Measured | Source evidence and projected implication |
| --- | --- | --- |
| Node event loop + PostgreSQL bridge | Hosted request latencies above; no event-loop counters | `server/src/postgres/database.ts` uses Atomics.wait; `server/src/postgres/sync-worker.ts` runs one pg Client. Main-thread requests serialize around synchronous database calls. This is the strongest source-supported API bottleneck candidate. |
| PostgreSQL connections and writes | PostgreSQL confirmed by health; no connection/CPU counters | There is no request-serving connection pool to exhaust here. One client serializes calls. The adapter's schema-wide advisory writer lock also serializes write transactions across hosts. A second API host adds another connection and overlapping reads but cannot double shared write throughput. |
| ffmpeg media processing | Three small photo processing requests; no film compilation | ffmpeg is a child process sharing the Lightsail CPU budget, rather than JavaScript executing on the event loop. Film compilation can compete for CPU and increase the effective S. This run does not establish film capacity or prove ffmpeg is the current bottleneck. |

A second API host behind a load balancer ideally halves the per-host arrival rate. The table models R = L + S/(1−λS/2) and uses the same user think time. Its service-center ceiling becomes 39.2 req/s if database time and fixed delay do not change. Balance authenticated requests across the hosts; shared durable sessions are in PostgreSQL, but media capabilities are in-memory and staged media is local, so routing affinity or shared state/storage is required. Multiple scheduler/worker instances also need coordinated job ownership. CloudFront remains the edge; PostgreSQL and S3 remain shared services.

Separate the media worker to reserve API CPU and isolate compilation bursts. Keep durable job claims and retry semantics. This reduces contention when films compile, but leaves synchronous database calls on the API path; converting that path to asynchronous persistence and an appropriately bounded connection pool addresses the serialization mechanism. No infrastructure or production configuration was changed for this test.

## Presentation assets and repeatability

- `charts/latency-vs-vus.png`: observed p50/p95/p99 against the two-second target.
- `charts/throughput-vs-vus.png`: observed request throughput.
- `charts/measured-vs-projected.png`: measured API means and projected one/two-host means.
- `results/hosted.json`: raw formal observations, setup health, stage and operation summaries.
- `results/capacity-model.json`: calibration points, fitted parameters, projections and sensitivity.
- `METHODOLOGY.md`: journeys, profile, acceptance rules and rerun command.

Regenerate charts and tables with `python scripts/load/analyze.py /absolute/path/to/load-test` after installing numpy and matplotlib. All chart files are 1280×720 PNGs. The PR adds a manual performance workflow; it does not deploy or merge anything.

## Deployment overlap

The initial run's 339 failures occurred from 2026-10-26T14:46:00.696Z to 2026-10-26T14:46:26.610Z. [Dev deployment 40341542790](https://github.com/Collaboration95/rewind-app/actions/runs/40341542790) installed the release from 14:45:06–14:46:30 UTC and passed public health at 14:46:30–14:46:31 UTC. The error interval falls within that installation step. Deployment interference is the leading explanation; the request timings alone do not establish CPU saturation. The original failed stage remains in every acceptance statistic and in the incident-influenced capacity scenario.

## Post-deployment read-only confirmation

A separate three-minute 100-VU confirmation reused the same sessions and group after deployment. It sent no chat writes or uploads; the chat-send slot became a chat read. Keep this read-only result separate from the initial 95% read / 5% chat-write mix.

| VUs | Requests measured | p50 ms measured | p95 ms measured | p99 ms measured | req/s measured | Errors measured | Result |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 100 | 3316 | 396.4 | 625.4 | 838.3 | 18.42 | 0 (0.00%) | PASS |

The initial mixed-workload run remains FAIL. This confirmation establishes the read-only result after deployment and does not validate the projected 250–1,000-user populations.
