## Stages

| VUs | Requests measured | p50 ms measured | p95 ms measured | p99 ms measured | req/s measured | Errors measured | Result |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 1 | 38 | 765.1 | 1057.7 | 1238.1 | 0.21 | 0 (0.00%) | PASS |
| 10 | 330 | 389.8 | 663.4 | 827.4 | 1.83 | 0 (0.00%) | PASS |
| 25 | 826 | 379.0 | 674.9 | 944.4 | 4.59 | 0 (0.00%) | PASS |
| 50 | 1632 | 432.2 | 842.4 | 1105.6 | 9.06 | 0 (0.00%) | PASS |
| 100 | 3212 | 496.0 | 1335.9 | 1635.9 | 17.84 | 0 (0.00%) | PASS |

## Operations

| Operation | Requests measured | p50 ms measured | p95 ms measured | p99 ms measured | Errors measured |
| --- | ---: | ---: | ---: | ---: | ---: |
| upload-source | 3 | 670.5 | 819.0 | 819.0 | 0 |
| upload-contribution | 3 | 408.9 | 642.2 | 642.2 | 0 |
| chat-read | 1816 | 523.5 | 1264.3 | 1612.8 | 0 |
| home | 1213 | 368.5 | 1112.8 | 1452.8 | 0 |
| archive | 906 | 367.0 | 1139.1 | 1466.3 | 0 |
| contributions | 601 | 360.8 | 1016.5 | 1357.1 | 0 |
| groups | 895 | 373.6 | 1014.6 | 1398.6 | 0 |
| media-capability | 297 | 360.9 | 1089.2 | 1435.4 | 0 |
| chat-send | 304 | 774.3 | 1445.5 | 1752.8 | 0 |

## Capacity

| Users | req/s measured | Mean ms measured | p95 ms measured | req/s projected | Mean ms projected | U projected | Mean ms projected, two hosts |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 250 | — | — | — | 21.87 | 6433.1 | 99.3% | 1071.2 |
| 500 | — | — | — | 21.97 | 17754.3 | 99.7% | 6433.1 |
| 1000 | — | — | — | 22.01 | 40441.2 | 99.9% | 17754.3 |

statuses: {"200": 6149, "201": 330}
cache: {"Miss from cloudfront": 6479}
media: {"uploadAttempts": 3, "capabilitiesIssued": 0, "capabilityEmpty": 318}
