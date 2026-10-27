# Data and reproduction

All GitHub access used authenticated, read-only `gh`; git commands were read-only. No repository file, issue, label, board, PR or workflow was changed. Output is confined to this records folder. Saved data reflects retrieval on 26 October 2026, approximately 22:25–22:30 SGT, not a prediction of tomorrow’s state.

- `gh issue list -R Collaboration95/rewind-app --state all --limit 1000 --json number,title,body,state,stateReason,createdAt,closedAt,milestone,labels,url`
- `gh pr list -R Collaboration95/rewind-app --state all --limit 1000 --json number,title,body,state,createdAt,closedAt,mergedAt,baseRefName,milestone,url`
- `gh issue list -R Collaboration95/rewind-app --label mvp --state open --limit 1000 --json number,title,state,milestone,labels,url`
- `gh api repos/Collaboration95/rewind-app/milestones?state=all&per_page=100`
- Read-only `gh api graphql` query: repository issues, 50/page with cursor pagination, collecting current state/milestone, creation/closure dates, and milestone/demilestone/close/reopen events. All issue pages fetched; no issue exceeded the 100-event page. Raw results: `data/issue-timeline.json`.
- Supplemental read-only `gh pr view`, `gh run list` and `gh run view --log` established the dependency and build repair and the 8 October setup-delay context. Only relevant log extracts are retained, not credentials or full environment logs.

Rebuild with `python3 build_records.py` in an environment with matplotlib installed. This reads the saved JSON and source documents; it does not refresh GitHub. Temporary rendering dependencies were removed after verification; the script creates a local `.mplconfig` cache when run.

Burndown uses exact event timestamps in SGT, at the next midnight (exclusive), for each day. Only issues assigned to that sprint at that instant contribute. The opening snapshot is at day-one midnight. Reopen events restore open status; milestone changes alter scope. Replay was checked against all current timeline issue states and milestones (zero mismatches). A closed issue can move into a milestone later; therefore closed-in-scope is not necessarily work completed inside the sprint. No original commitment or ideal effort line is inferred.

Velocity uses each issue’s final `closedAt` and each PR’s `mergedAt` in half-open SGT sprint windows, independent of present milestone. It counts each issue once, not every historical close event. Sprint 0 uses 1–12 Sep (the first repository issues are 2 Sep); Sprint 1 13–26 Sep; Sprint 2 27 Sep–10 Oct; Sprint 3 11–24 Oct. Counts outside these windows remain in the raw census. PRs to main include promotions, so all-target throughput is not distinct feature delivery. Extra columns retain current own-milestone closure counts and closure reasons. State reasons and labels describe the saved current snapshot, not historic labels at closure.

CSV inventory: `burndown-sprint-0.csv` through `burndown-sprint-3.csv`; `velocity.csv`; `issues.csv`; `prs.csv`; `issue-events.csv`; `backlog-by-milestone.csv`; `backlog-by-label.csv`; `backlog-milestone-label.csv`. PNGs are exactly 1280×720 with a 100 dpi, 12.8×7.2-inch matplotlib canvas. No tests of the application were re-run; record QA checks only reconstruction, arithmetic, dimensions and readability.
