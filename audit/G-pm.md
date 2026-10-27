# G - Section 1 facts: intro and project-management summary

Read-only audit. Code and docs: worktree `rewind-present-audit` = origin/dev `f6cd896` (20 Oct 22:38 SGT; dev has had no merge since). GitHub data read live with `gh` on **26 Oct 2026, about 21:45 SGT**. Dates are SGT unless marked. Scripts and raw JSON are in `/tmp/g-pm/` (not in the repo).
Tags: **[M]** measured from gh/git. **[R]** recorded in a repo document. **[A]** agreed or assumed. **[?]** unknown, owner must supply.
Owner decision (26 Oct): one presenter delivers the whole talk, so nothing below plans per-member speaking parts. The site's "Presenter" column (`submission.json`, Member A/B/C/D) is superseded.
Not read: `doc/planning/report/presentation/rewind-script.md` (the coordinator named it). `AGENTS.md` freezes `doc/planning/report/` unless the user names it, and the coordinator is not the user. Say the word and it will be read.

## 1. Product (for the intro slide)

- Problem [R, `index.json`, proposal 3.3]: close friends drift apart after graduation or relocation, and public feeds reward polished posting. No user study exists; the demand is a hypothesis.
- Solution [R]: a private invite-only group app. A group of 2 to 10 adds up to 5 photos or videos per week (30 s in total, 15 s per clip), sealed even from the owner. At cycle end (28 days by default) the server compiles one 720x1280 film with normalised audio. It premieres for 24 h, then lives in the Archive. Group chat and a Sunday 19:00 web-push reminder surround the loop.
- Target users [R]: "young adult friend group" is the primary user and pilot persona. Group owner, member and invitee are the roles. The platform operator is a stakeholder, not an in-app actor.
- MVP scope today [R, `product.json`]: 14 use cases (UC01 to UC14) in 5 packages: Access, Capture, Cycle, Participation, Archive. Included: Cognito Managed Login on release, Developer sign-in on local and dev, groups, invites, photo and video with 4 retro looks, one correction, automatic rollover, 24 h premiere, downloads, prompt, reminders, chat, installable PWA. Out: the synthetic Demo (removed 6 Oct, tag `demo-frozen-20261004`), compiled native iOS, native push, public feed, billing, multi-region.
- Status [R plus M]: live on hosted dev (Lightsail behind CloudFront, managed PostgreSQL, private S3, Cognito). Deploy dev, Quality, CodeQL and Release security were green at `f6cd896` on 20 Oct. **The release environment is not live**: Deploy release run 39373300339 (main `f6e50ac`) was still `waiting` when queried on 26 Oct. Treat the product as a proof of concept on hosted dev.

## 2. Team

- **The site is wrong about the team.** `owners.json` and `scrum.json` say "four placeholder members, Member A to D". The repo records **five named members** (Team 14): Nguyen Kim Long, Gopal Guruprasath, Jiang Jiayu, Phan Mai Tan Loi, Sang Haoxiang. Sources: `doc/planning/project-conduct-evidence.md`, the Sprint 2 report (docx in the worktree) and the Sprint 4 report (main checkout only). The proposal and Sprint 0 plan use letters A to E, and **no confirmed A to E to name mapping exists** in the repo. `submission.json` readiness still says "member names are placeholders".
- Git and GitHub identities [M plus inference]: Guruprasath / Collaboration95 is the owner (matches the user email). `AndrewNguyenNUS` / `Andrew Nguyen` / `AndrewNguyenLKN` (longckek1) is very probably Nguyen Kim Long. `KaenBin` (loi.phan1342002) is very probably Phan Mai Tan Loi. `bibi45c` (bibi45gt) and review-only `Big-Fat-Duck` are not mapped to a name. Confirm before showing any of this.
- Roles [R]: Sprint 0 plan section 7 set A = Product Owner proxy and D = Scrum facilitator, with an explicit statement that both rotate in Sprint 1. **No record that the rotation happened.** The conduct evidence lists Sang Haoxiang's Sprint 0 work as "Scrum facilitation". In practice the owner acts as product owner and integrator (`AGENTS.md`, `CLAUDE.md`). Issue #142 (23 Sep) recorded Guruprasath as apply, break-glass and budget owner and Andrew as plan reviewer and non-author acceptance owner. [?] Who is Product Owner and Scrum Master today.
- **Sensitive, owner decision.** The Sprint 2 report and the Sprint 4 report (24 Oct) record that Sang Haoxiang did no work in Sprint 2 or in the final sprint, per a team-supplied account. The Sprint 2 report adds that it was raised with Prof Chandra. The conduct evidence deliberately omits the escalation details. Do not put this on a slide without the team agreeing the wording.

### Effort per member (carryover B1: say measured or agreed, on the slide)

- **There are no measured hours anywhere in the repo.** `scrum.json` effort table is "to fill" for all four rows. The Sprint 2 and Sprint 4 reports both say individual hours were not recorded.
- What exists [R]:
  - R0: each member spent about 1 h per day for "the first few days" of Sprint 0, unspecified.
  - Sprint 0 plan: 70 h committed (A 15, B 15, C 15, D 13, E 12) plus a 30 h reserve. The capacity model is 5 x 10 days x 8 h = 400 h.
  - Proposal WBS: 400 h planned (A 58, B 68, C 74, D 58, E 52, shared 44 + 32 + 14). **These are plans, not actuals**, and not the same 400 as the capacity model; do not add them.
  - Sprint 4 report section 9: per-member activity prose labelled "retrospective estimates... not confirmed activity logs", no hours.
- Measured GitHub activity (not effort; understates non-owner members and counts agent work as the owner's) [M]:
  - Non-merge commits on dev: 627 total. Guruprasath 593 (94.6%). Other humans 17: bibi45c 10, KaenBin 4, Andrew Nguyen 3. The rest: 11 "Synthetic fixture", 3 dependabot, 2 "Codex", 1 noreply.
  - All 17 non-owner human commits fall on 8 to 9 Sep, 28 Sep to 1 Oct. None after 1 Oct.
  - Merged PRs: 213 total, 205 by Collaboration95 (96%), KaenBin 3, AndrewNguyenLKN 1, bibi45c 1, dependabot 3.
  - PR reviews (human): AndrewNguyenLKN 10 (7 approvals), bibi45c 2 approvals, Big-Fat-Duck 2 comments. Owner 5.
  - Issues authored: owner 322, bibi45c 6, AndrewNguyenLKN 1. Issue comments: owner 785, bibi45c 15, KaenBin 7, AndrewNguyenLKN 5.
- Recommended slide label: "Hours were not logged. Shaded column = agreed split of responsibility (planned, not measured). Plain column = GitHub counts (measured, under-count non-owner work)." Never label a split as measured.

## 3. Delivery numbers (gh and git, 26 Oct)

Totals [M]: 329 issues (319 closed, 10 open); 261 PRs; **213 merged = 161 to dev, 51 to main, 1 to a side branch**; 22+17+1 PRs closed unmerged; 8 open. 943 commits on dev (627 non-merge), 881 on main. First commit 2 Sep, repo created 2 Sep. Closure reasons: 262 completed, 43 not planned, 14 duplicate.
Milestones [M]: four only (Sprint 0 to Sprint 3). **No Sprint 4 milestone exists.** Sprint 0 closed 13 Sep. Sprint 1 closed 25 Oct 06:43. **Sprint 2 and Sprint 3 are still open** in GitHub (2 and 7 open issues).

### Velocity per Sprint window (SGT, merge/close/create date)

| Sprint | Window | Issues created | Issues closed (any milestone) | PRs merged to dev | PRs to main | Commits on dev, all / non-merge |
|---|---|---:|---:|---:|---:|---:|
| 0 | 1-12 Sep | 81 | 44 | 0 | 11 | 78 / 63 |
| 1 | 13-26 Sep | 78 | 100 | 0 | 36 | 192 / 154 |
| 2 | 27 Sep-10 Oct | 143 | 145 | 128 (+1 side branch) | 3 | 530 / 323 |
| 3 | 11-24 Oct | 25 | 30 | 33 | 1 | 143 / 87 |
| after | 25-26 Oct | 2 | 0 | 0 | 0 | 0 |
| total | | 329 | 319 | 161 | 51 | 943 / 627 |

- `dev` branch first merge: 27 Sep 18:07. Before that everything went straight to `main`, hence 0 to dev in Sprints 0 and 1.
- Using UTC instead of SGT moves one PR (Sprint 2 dev 129, Sprint 3 dev 32) and two issues. The site's older figures are UTC.
- Sprint 2 is 56% of all commits (530 of 943). Busiest day 4 Oct: 112 commits.

### Milestone scope and burndown (reconstructed from GitHub milestone, close and reopen events; end-of-day SGT)

Method check: replaying the events reproduces today's milestone and state for all 329 issues (0 mismatches). It is still a reconstruction: scope changes during the Sprint, and no original commitment was preserved.

| Milestone | Scope at start of window | Scope at end of window | Open at end | Closed inside own window | Now (26 Oct) |
|---|---:|---:|---:|---:|---|
| Sprint 0 | 0 | 21 | 0 | 21 | 21 / 0 open |
| Sprint 1 | 50 | 50 | 0 | 37 (13 were closed 10-11 Sep, before its window) | 52 / 0 open |
| Sprint 2 | 9 | 135 | 9 | 120 (+5 closed after) | 133 / 2 open |
| Sprint 3 | 18 | 45 | 5 | 25 | 47 / 7 open |

Daily series for the chart, `date: scope/open`:
- **Sprint 1** (scope 50): 13 Sep 37 open; 14 Sep 24; 18 Sep 6; 22 Sep 0.
- **Sprint 2**: 27 Sep 30/24; 28 Sep 33/23; 29 Sep 33/16; 30 Sep 43/13; 1 Oct 46/23; 2 Oct 79/47; 3 Oct 79/37; 4 Oct 93/15; 5 Oct 114/16; 6 Oct 134/20; 7 Oct 135/20; 8-10 Oct 135/9.
- **Sprint 3**: 11 Oct 20/5; 12 Oct 28/5; 15 Oct 40/6; 18 Oct 41/6; 19-24 Oct 45/5.
- Sprint 0: 2 Sep 9/9; 7 Sep 12/11; 9 Sep 12/1; 10 Sep 21/1; 12 Sep 21/0.

Reading it honestly: Sprint 2 scope grew from 9 to 135 while it ran (the Planning day, 27 Sep, attached 21 issues). Sprint 3 stayed at 5 open for two weeks, so it is not a classic burndown; do not claim a completion percentage. This is issue status, not hours or points. 43 of the 329 issues were closed as not planned and 14 as duplicates; closures include retired scope.
Also: `doc/analytics/sprint-analytics.html` is stale (generated 6 Oct). Do not show it as current.

### Labels [M]

- `mvp`: 86 issues ever (79 closed, 7 open). All in Sprint 2 (43) or Sprint 3 (43). No Sprint 0 or Sprint 1 issue carries it.
- `archived`: 27 (all closed; 3 also carry `mvp`). `doing` is on 2 open issues (#230, #504). `duplicate` 23. 219 issues carry neither `mvp` nor `archived`.
- 76 issues have no milestone (mostly Sprint 1 era, 75 closed).

### Open `mvp` issues, dated 26 Oct 2026 (7)

| # | Title | Note |
|---|---|---|
| 230 | Complete the isolated release deployment and verify environment boundaries | `doing` |
| 362 | Assemble and validate every final-report template section | report |
| 504 | Move the release environment onto managed PostgreSQL with isolated backups | `doing` |
| 515 | Deploy isolated Cognito Managed Login for the release web and PWA | |
| 527 | Verify the current hosted Safari and Home Screen app integrations once | needs the owner's device |
| 587 | Fix focused script-test selection and document the Sprint override | bug, created 25 Oct 06:46; PR #589 open |
| 588 | Preserve emoji and local calendar labels in chat | bug, created 25 Oct 06:46; PR #590 open |

- The site says 5 (as of 20 Oct) and the Sprint 4 report snapshot (24 Oct 23:32) lists the same 5. **#587 and #588 are new since then.** Non-mvp open: #497, #498 (Sprint 2), #170 (not planned).
- Open PRs: #586 promotion dev to main (Quality green at `f6cd896`, review required since 20 Oct); #589 and #590 (some Quality jobs failing: "Format, lint, typecheck, and test" and "Production dependency audit", not diagnosed); drafts #562, #438; 3 dependabot.
- Open for the CI/CD segment: KaenBin's Vigolium DAST trial. #330 merged then reverted by #331 on 1 Oct, and #332 and #335 closed unmerged. Draft #438 is still open.

### Releases, tags and promotions [M]

- GitHub releases: 3 pre-releases, all Android test APKs: `apk-dev-e39f707` (4 Oct), `apk-dev-7105328` (12 Oct), `apk-dev-1b70716` (19 Oct). Tags also include `demo-frozen-20261004` and `pre-migration-squash`. **There is no production release.**
- Promotions dev to main: #421 "first release" (4 Oct 22:59), #531 "Sprint 3 completion" (19 Oct 13:41). #586 open. dev is 63 commits ahead of main. The Deploy release run for the 4 Oct promotion was cancelled; for 19 Oct the run succeeded as preparation and the later run is waiting at the protected environment. State "promoted to main twice; release deployment not completed" plainly.

### Contributors and AI agents

- Authorship is the owner's account, so agent work is invisible in `shortlog`. Evidence it shows up indirectly [M]: 30 of 627 non-merge commits (4.8%) carry an AI trailer (29 Claude, 1 GPT-6.1 Sol), and 2 are committed as "Codex". 82 of 213 merged PRs come from `codex/*` branches and 90 from `guru/*`. 28 PR bodies name a review agent (GPT-6.1 Sol or Luna). The `AGENTS.md` and `CLAUDE.md` working agreement, `skills/ship-issues` and `make review` document the practice.
- Say so plainly: most code was written by AI coding agents (Claude Code and Codex) directed by the owner; the other four members' contribution is not visible in git. `scrum.json` already uses this framing. The numbers above are the proof, so the slide should not hide it.
- Bots: dependabot 28 PRs (3 merged); github-advanced-security 26 review comments; GitGuardian comments.

## 4. Scrum ceremonies: where the evidence is, and what is missing

| Event | Evidence in repo or GitHub | Gap |
|---|---|---|
| Sprint Planning | Sprint 0 plan (90 min Day 1, sections 8, 10, 17 with open decisions); Sprint 1 plan "Proposed for Sprint Planning"; `sprint-2-user-journey-plan.md` "Draft for Sprint Planning, 27 Sep"; milestone intake on 27 Sep (scope 9 to 30); Sprint 3 audit `sprint-3-completion-audit-2026-10-12.md` (12 Oct, 8 new issues, 13 open mvp) | No minutes or attendance. Sprint 0 section 17 left "real names mapped to A to E" open. No original Sprint 2 commitment. |
| Daily Scrum | Planned only: 10 min or async "goal progress / next action / blocker", 3 live syncs a week (Sprint 0 plan section 10). Runtime proxy: `doing` label and about 970 issue and PR comments (mostly the owner's) | No logs of any daily update. |
| Sprint Review | #25 walkthrough (closed 10 Sep), #18 close-out epic, PR #77; 26 Sep audit PRs #204 to #207 ("review ready, Sprint not closed"); Sprint 2 report (10 Oct); Sprint 4 report (24 Oct, untracked) | No review meeting records or stakeholder feedback. Sprint 1 hosted acceptance never closed. |
| Retrospective | #27 (10 Sep: 5-issue WIP limit, Day 1 gate, single-device fallback); Sprint 1 report section 9 (draft, says "not meeting minutes"); Sprint 2 report; Sprint 4 report section 10; `AGENTS.md` commit `25c3a63` (4 Oct 16:15) adopts the lean Definition of Done | No minutes. This is the best dated change-after-retro example: 4 Oct, lean DoD and no Project board (`16c028e`). |
| Backlog refinement | `make issues`, `mvp`, `archived`, `doing` labels, milestone churn | Milestones are mutable: not a preserved commitment. |

Also missing: burndown with preserved baseline, velocity in points, any effort log. Pair programming is claimed in R0 but not evidenced; the second-machine Sprint 0 rehearsal was reported as still outstanding.

## 5. Where the sources agree or disagree

| Item | Site / conduct docs | Sprint 4 report (24 Oct) | gh/git now |
|---|---|---|---|
| Names | Placeholders A to D (four) | Five real names | Five accounts, only 3 mapped by inference |
| "Sprint 4" | Sprints 0 to 3 only | Calls the 11-24 Oct period "Sprint 4" and says the milestone is "Sprint 3"; its prior report is Sprint 2 | **No Sprint 4 milestone.** Use Sprint 3. The title is probably the fourth fortnightly report. Do not say "Sprint 4" on a slide. |
| Open mvp | 5 (20 Oct) | 5 (24 Oct 23:32) | 7 (26 Oct) |
| Sprint 3 closed / open | 40 / 5 | burndown chart only | 40 / 7 |
| Totals | 327 issues, 209 merged PRs (157 dev / 51 main) | | 329 issues, 213 merged (161 / 51) |
| `mvp` ever labelled | 84 | | 86 |
| Sprint 2 PRs | 129 dev / 3 main / 1 other (UTC) | | 128 or 129 depending on timezone |
| Dev / main revision | dev `f6cd896` | dev `f6cd896`, main `f6e50ac` | Same, no change since |
| Tests | | 1,674 frontend, 41 responsive, 2 real-account runs "from PR #584" | Not re-run here; quote as PR-reported |
| Contributions | "to fill" | estimates, no hours, one member recorded as no contribution | No ledger |
| Sprint 3 audit | | | `sprint-3-completion-audit-2026-10-12.md` agrees with gh on #521 to #528 and the 13 open mvp |

## 6. Draft slides (one presenter, 3 to 4 min)

**Slide 1: "Rewind turns a friend group's small private moments into one film" (about 60 s)**
- Problem, loop in one picture (join, capture and seal, wait, film, Archive), target users, in/out of scope.
- A badge line: "Proof of concept. 14 use cases built. Live on hosted dev as of 26 Oct. Release environment not live."

**Slide 2: "Sprint 2 carried the build; 7 mvp issues remain: 5 release, verification or report, and 2 new small bugs" (about 100 s)**
- Chart: per-Sprint bars of issues closed (44, 100, 145, 30) and dev PRs merged (0, 0, 128, 33), with the Sprint 2 and 3 open-issue lines (section 3 above).
- Table: the 7 open mvp issues, headed "Open on 26 Oct 2026".
- Footer: "213 PRs merged, 319 of 329 issues closed. Reconstructed from GitHub events; scope changed during Sprints."

**Slide 3: "We ran Scrum through GitHub; effort is an agreed split, not measured hours, and agents wrote most code" (about 80 s)**
- Left: events and where each leaves its trace (section 4), including the retro that changed practice (#27, then the 4 Oct lean DoD).
- Right: the effort table with two labelled columns: planned or agreed split (owner supplies) and GitHub counts (measured). Footnote: "Hours not logged."
- One line on AI: 94.6% of commits are under the owner's account, with AI agents under human direction; every merge passed the Quality gate.

## 7. What only the owner can supply

1. Real names for the slide. All five, or four plus a statement on the fifth? The wording about Sang Haoxiang is the team's decision, not an agent's.
2. Whether to use the repo's A to E labels, and the A to E to name mapping (confirm Andrew = Nguyen Kim Long, KaenBin = Phan Mai Tan Loi, and who bibi45c and Big-Fat-Duck are).
3. **The effort split** (percent or hours per member), and which of "agreed", "estimated" or "measured" it is. Nothing measured exists. If the team gives hours, they are self-reported estimates and must be labelled so.
4. Product Owner and Scrum Master today, and whether the Sprint 1 rotation happened.
5. Ceremony facts: dates, duration and attendance for Planning, Review and Retrospective, and whether Daily Scrums were held (stand-up or async). Without them, say "outputs recorded in GitHub, no minutes".
6. Whether #527 (device check) and the Sprint 4 label are handled before the talk; whether to close #587 and #588 first (PRs #589 and #590 currently fail some jobs).
7. Permission to read `rewind-script.md` (frozen folder) and whether #586 is to be reviewed and merged before the talk.
