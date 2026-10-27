# Rewind hosted performance methodology

Prepared for 27 October 2026, 14:30 SGT. Test target: https://d2m6kz76y4kuvm.cloudfront.net.

## What the test exercises

A plain Node HTTP runner drives the real HTTPS API through CloudFront to the hosted Node server, PostgreSQL and the media processing path. It creates three synthetic accounts and one private test group, signs in once per account, and reuses the returned native bearer sessions across virtual users. No passwords, session tokens, invite codes or media capabilities are written to evidence. No existing group is modified. The fixture remains in hosted dev; there are no delete requests.

A virtual user represents an active session doing one action and then thinking for 3–7 seconds (approximately five seconds on average). Virtual users share three account identities and one group; VUs count concurrent activity, not unique accounts. Requests use persistent fetch connections. Timings include CloudFront, network, API execution and body consumption from this Mac; they are HTTP timings, not page rendering or browser interaction timings.

| Action | Share of scheduled requests | API |
| --- | ---: | --- |
| Open Home: selected group and cycle state | 20% | GET /api/real/groups/:id |
| List groups | 15% | GET /api/real/groups |
| Read recent chat | 30% | GET /api/realtime/groups/:id/messages?limit=30 |
| Read contribution budget/history | 10% | GET /api/contributions?groupId=:id&limit=5 |
| Open Archive | 15% | GET /api/archive?groupId=:id&limit=5 |
| Request media capabilities via Archive | 5% | Same Archive endpoint; count returned download paths |
| Send chat | 5% | POST /api/realtime/groups/:id/messages |

Offset the sequence per VU to avoid synchronized requests. The separate upload path contributes only nine requests: stage a PNG, submit its photo contribution and process it, once per account. Photos are one pixel, 68 bytes each, three seconds of generated output. Uploads occur during the first steady stage and are included in its percentiles and errors.

The new group's cycle ends on 23 November. Archive and capability requests exercise the collecting-state authorization path; no released clip exists, so no playable capability can be issued. This is recorded as an empty-capability count, not a successful media delivery. No video download, persistent SSE stream or group-film compilation is driven by this test.

## Ramp and acceptance

Use 1 → 10 → 25 → 50 → 100 VUs. Each level has a 15-second ramp and a 180-second steady window: 975 seconds (16 min 15 sec), plus setup and drain. The user think time is retained as load rises; VUs send one request at a time, so slower responses reduce throughput. Ramp observations are retained separately and excluded from the acceptance tables. A request is assigned to the phase in which it completes. Stage throughput is completed requests divided by wall-clock stage seconds. Per-operation throughput uses the total steady-window duration.

Every steady stage must have p95 < 2,000 ms and errors < 1%. Count unexpected status codes, HTTP 429, invalid/non-JSON responses, explicit API errors and 15-second timeouts as failures. Keep failures in latency distributions. Use nearest-rank p50, p95 and p99. Retain each observation's operation, UTC completion time, phase, VUs, milliseconds, status, validity, body length and CloudFront cache header. Aggregate and per-operation summaries are derived from those observations.

The public health endpoint confirms PostgreSQL and ffmpeg configuration. Host CPU, event-loop utilization, database execution time and active connections are not exposed by the endpoint. Record host CPU as unobserved. Source inspection identifies mechanisms; the queueing model estimates capacity rather than measuring these host counters.

## Reproduce

In the guru/load-test branch:

```sh
TARGET_URL=https://d2m6kz76y4kuvm.cloudfront.net \
MAX_VUS=100 OUTPUT=load-results/results.json \
node scripts/load/hosted.mjs
```

The workflow `.github/workflows/performance.yml` exposes `target_url` and `max_vus`, uses pinned actions and read-only repository permissions, and saves `results.json` plus `SUMMARY.md`. Each fresh run creates three synthetic accounts and uploads three tiny photos. A local `FIXTURE_FILE` can reuse private sessions; its target must match. Never upload that file as an artifact. Lower `MAX_VUS` for a shorter, smaller run. `STEADY_SECONDS` and `RAMP_SECONDS` exist for harness verification; the evidence run uses the full defaults.

One early pilot used incorrect photo metadata (`hasAudio: false`); the API correctly rejected it. The metadata was corrected to match Rewind's generated silent-track contract. The formal measurement reuses the same sessions and group, with three valid uploads. Pilot stage output is retained separately and does not enter the formal run's statistics.

## Capacity calculations

Fit the measured steady-window mean response times and throughputs to a single serialized service center plus a fixed network/parallel delay:

- Utilization law: U = λS.
- Queue response: R_queue = S / (1 − U).
- End-to-end mean: R = L + R_queue, where L is fitted fixed delay.
- Interactive throughput: λ = N / (Z + R), with mean think time Z = 5 seconds.

Fit S and L to the four sustained multi-user (10/25/50/100 VU) measured (λ, mean R) points, excluding the three bounded uploads. Retain the sparse 1-VU stage as a separate baseline because its pooled-connection cadence differs. Use least squares, requiring S > 0, L ≥ 0 and λS < 1. Solve the closed-loop equations for 100, 250, 500 and 1,000 users. Show measured results and projected results in separate columns. Model response times are means; measured p95 and p99 remain observed percentiles. Define practical saturation as 90% modeled utilization; 1/S is the asymptotic service ceiling, not an observed maximum. Also show half and double fitted service demand as sensitivity scenarios.

For two balanced API hosts, apply λS/2 to each host while holding fixed delay constant. This is an idealized comparison with unchanged database service times. The shared PostgreSQL writer advisory lock and local media/capability state prevent assuming perfect scaling. Separating the media worker removes ffmpeg contention from the API host; its numerical benefit requires a workload with compilation, so no measured film-throughput improvement is claimed.

## Deployment interference and separate confirmation

The dev deployment run 40341542790 installed a release from 14:45:06–14:46:30 UTC, overlapping the initial 100-VU error interval (14:46:00.696–14:46:26.610 UTC). Keep the initial failed acceptance result. Its model is an incident-influenced operational scenario, not evidence of physical host saturation.

Run a separate 15-second ramp and 180-second steady window at 100 VUs after deployment, reusing the fixture with `CONFIRMATION_ONLY=true`. This mode performs reads only: it replaces the 5% chat-send slot with chat reads and disables uploads and account setup. Save its JSON separately. The initial mixed run and the read-only confirmation together contain 19 minutes 30 seconds of ramp/steady measurement, plus setup and drain. Do not combine the two acceptance results or claim the same write workload was rerun.

## Headline rerun on a quiet host

On 26 Oct, 15:56:55–16:13:24 UTC, the identical default profile ran again. It started after Deploy dev 40350232534 had finished, and no workflow run overlapped it. It ran locally from `scripts/load/hosted.mjs`, byte-identical to `origin/dev`, because the `performance.yml` dispatch returned HTTP 404: the workflow is not on the default branch. The run used a fresh fixture, with three new accounts and a new group. All five stages passed with 0 errors. This run is the headline in `RESULTS.md`; the earlier run is kept in `previous-run-20261026T1431Z/`.

