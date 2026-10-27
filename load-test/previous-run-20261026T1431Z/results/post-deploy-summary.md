# Hosted load test

Target: https://d2m6kz76y4kuvm.cloudfront.net

Result: PASS (p95 < 2000 ms, errors < 1%, every steady stage)

| VUs | Phase | Requests | p50 ms | p95 ms | p99 ms | req/s | Errors % |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 100 | ramp | 184 | 362.8 | 649.6 | 914.6 | 12.19 | 0.00 |
| 100 | steady | 3316 | 396.4 | 625.4 | 838.3 | 18.42 | 0.00 |
