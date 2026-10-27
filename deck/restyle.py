"""Calm light-green palette and quieter typography (27 Oct restyle)."""
RESTYLE_CSS = r'''
:root{--sans:-apple-system,BlinkMacSystemFont,"Helvetica Neue",Arial,sans-serif;--mono:Menlo,Consolas,monospace;
--bg:#EEF4EF;--cream:#EEF4EF;--navy:#163A2F;--ink:#15281F;--muted:#45594F;--line:#CADBCE;--card:#FFFFFF;
--accent2:#A5481B;--orange:#A5481B;--pm:#1F6B55;--sad:#1F6B55;--sdp:#1F6B55;--testing:#1F6B55;--devsecops:#1F6B55;--demo:#1F6B55}
html,body,#stage{background:var(--bg)}
#stage,.slide{background:var(--bg);color:var(--ink)}
.slide h1{color:var(--ink);font-weight:700;letter-spacing:-.5px}
.kicker{font:600 16px var(--sans);letter-spacing:0;text-transform:none;color:var(--accent)}
.foot{border-top:0;justify-content:flex-end}
.foot .source{display:none}
.counter{font:500 14px var(--sans);color:var(--muted)}
.section-progress span{background:#D3E2D7}
pre,code,.command,.commands pre,.figure-fallback code{font-family:var(--mono)}
code{font-size:.85em;color:#24483B}
.figure{background:var(--card);border-color:var(--line);border-radius:12px}
.figuretitle,figcaption{font:600 15px var(--sans);color:var(--muted);letter-spacing:0}
.explain{color:var(--muted)}.explain b{color:var(--ink)}
.data th{font:700 15px var(--sans);color:var(--muted);border-bottom:2px solid #A9C2B1;text-transform:none;letter-spacing:0}
.data td{border-bottom-color:var(--line)}
.rule{border-top-color:var(--line);color:var(--accent)}
.takeaway{color:var(--accent)}
.status-strip{border-top-color:var(--line)}.status-strip b{font:700 15px var(--sans);color:var(--accent2)}
.product-loop em,.journey-map em,.bug-steps em{font:700 17px var(--sans);color:var(--accent);text-transform:uppercase;letter-spacing:.6px}
.regression b{font-family:var(--sans)}.regression span:last-child b{color:#1F6B55}
.metric-row strong{color:var(--accent)}
.feature-number{font:700 17px var(--sans);color:var(--accent)}
.feature-notes>p b{color:var(--muted)}
.feature-control button,button{font-family:var(--sans);border-color:#B5CBBC;color:#22463A}
button:hover{background:#DDEBE1}
.clip-hint{font:15px/1.6 var(--sans);color:var(--muted)}
.run-clock b{font-family:var(--sans);color:var(--accent)}
.image-counts{font-family:var(--mono)}
.clip .cb{background:#7CC4A0}
/* Cover */
.slide.cover{background:var(--navy);color:#EEF4EF}
.cover .kicker{color:#A8DCC0}
.cover h1{color:#DCEAE1}
.cover-word span{color:#A8DCC0}
.cover-sub{color:#CFE1D6}
.cover-loop{font:500 22px var(--sans);color:#E6F1EA}.cover-loop i{color:#A8DCC0}
.cover-meta{font:17px/1.7 var(--sans);color:#B9CFC3}
.cover .section-progress span{background:#2B5546}
.cover .counter{color:#9DB8AA}
#ov .th{background:var(--bg)}
/* Full-slide figures stay on white so UML and charts keep their own backgrounds. */
.slide.figure-slide,.slide.chart-slide{background:#fff}
.slide.figure-slide>h1,.slide.chart-slide>h1{color:var(--accent);font-weight:650}
.pipeline-film video,.pipeline-film .poster{background:var(--bg)}
.playback-strip{background:var(--bg)}
/* Pipeline badges */
.badge{display:inline-block;padding:6px 12px;border-radius:999px;font:650 15px var(--sans);white-space:nowrap;line-height:1.2}
.badge.gate{background:#1F6B55;color:#fff}
.badge.main{background:#DCEBDD;color:#1E4D33;border:1px solid #93B89E}
.badge.manual{background:#fff;color:#3F5449;border:1px solid #9DB5A6}
.badge.deploy{background:#2B5C86;color:#fff}
.badge.report{background:#FFF8EE;color:#7A4510;border:1px solid #D9B98E}
/* Testing overview matrix */
.data.matrix{font-size:19px}.data.matrix td{padding:6px 10px;vertical-align:middle}.data.matrix th{padding:4px 10px 8px}
.data.matrix td:nth-child(3){font-weight:700;color:var(--accent);white-space:nowrap}
.data.matrix .badge{font-size:14px;padding:4px 10px}
/* One slide per test type */
.tt{display:grid;grid-template-columns:350px 1fr;gap:36px;height:100%;align-items:stretch;min-height:0}
.tt-left{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:26px 28px;display:flex;flex-direction:column;justify-content:center}
.tt-count{font-size:78px;font-weight:750;color:var(--accent);line-height:1;letter-spacing:-2px}
.tt-countlabel{font-size:20px;color:var(--muted);margin-top:10px;line-height:1.3}
.tt-tool{font-size:20px;line-height:1.38;color:var(--ink);margin-top:20px;padding-top:18px;border-top:1px solid var(--line)}
.tt-badges{display:flex;flex-direction:column;align-items:flex-start;gap:9px;margin-top:20px}
.tt-badges .badge{white-space:normal}
.tt-right{display:flex;flex-direction:column;justify-content:center;gap:26px;min-width:0}
.tt-what{font-size:25px;line-height:1.4;margin:0;color:var(--ink)}
.tt-example{background:var(--card);border:1px solid var(--line);border-left:6px solid var(--accent);border-radius:12px;padding:20px 26px}
.tt-label{font-size:15px;font-weight:700;color:var(--muted);text-transform:uppercase;letter-spacing:.7px;margin-bottom:8px}
.tt-example code{font-size:17px;color:#24483B;overflow-wrap:anywhere}
.tt-name{font-size:22px;line-height:1.38;margin:10px 0 12px;font-style:italic;color:var(--ink)}
.tt-name.plain{font-style:normal;font-size:19px;color:var(--muted)}
.tt-catch{font-size:21px;line-height:1.4;margin:0;color:var(--muted)}.tt-catch b{color:var(--ink)}
/* Security testing */
.sec-grid{display:grid;grid-template-columns:1.08fr 1fr;gap:34px;height:100%}
.sec-col h2{font-size:24px;margin:0 0 14px;color:var(--accent)}
.sec-col>p{font-size:20px;line-height:1.38;margin:0 0 14px;color:var(--muted)}.sec-col>p b{color:var(--ink)}
.sec-col>.badge{margin-top:4px}
.data.secscan{font-size:21px;background:var(--card);border-radius:12px}.data.secscan td{padding:10px 12px;vertical-align:middle}
/* Performance testing */
.perf-grid{display:grid;grid-template-columns:1fr 1fr;gap:34px;height:100%;min-height:0}
.perf-grid .figure{justify-content:flex-start;padding:16px 18px}
.perf-grid svg{width:100%;height:auto}.perf-grid svg text{font:19px var(--sans);fill:#45594F}
.perf-rule{font-size:22px;margin:18px 0 0;line-height:1.4}.perf-rule b{color:var(--accent)}
.perf-p{font-size:22px;line-height:1.4;margin:0 0 12px;color:var(--muted)}.perf-p b{color:var(--ink)}
.data.mix{font-size:21px;margin-top:10px}.data.mix td{padding:6px 10px}.data.mix td:last-child{text-align:right;font-weight:700;color:var(--accent)}
.perf-grid.results{grid-template-columns:.95fr 1.05fr}
.data.perfres{font-size:22px}.data.perfres td{padding:9px 10px}.data.perfres td:not(:first-child){text-align:right}.data.perfres th:not(:first-child){text-align:right}
.pass{color:#1F6B55;font-weight:750}
.perf-stats{display:flex;gap:18px;margin-top:22px}.perf-stats div{flex:1;background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px 16px}
.perf-stats strong{display:block;font-size:32px;color:var(--accent);line-height:1.1}.perf-stats span{font-size:16px;color:var(--muted)}
.perf-grid .chart{padding:12px}.perf-grid .chart img{height:calc(100% - 30px)}
/* System demo capacity slide */
.perf-layout.scale{grid-template-columns:1.25fr 1fr;align-items:center}
.perf-layout.scale .figure{padding:18px}
.perf-layout.scale svg{height:360px}
.perf-layout.scale .explain{font-size:22px;line-height:1.35}.perf-layout.scale .explain p{margin:0 0 16px}
.perf-grid.results .figure{justify-content:flex-start}#s11 .explain code{font-size:16px;display:inline-block;margin-top:6px}.perf-grid.results svg{width:100%;height:auto;max-height:470px}
.tt-left{justify-content:center}
@media print{.slide{background:var(--bg)}.cover{background:var(--navy)!important}.slide.figure-slide,.slide.chart-slide{background:#fff}}
'''
