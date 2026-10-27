# UI flow page: screens mapped to the cycle statechart

`index.html` is self-contained (relative `screens/`, `fonts/`; the statechart SVG from `../uml/state-cycle.svg` is inlined, title and legend cropped). It renders on a 1280×720 stage that scales to any window or iframe. All page text is ≥14 px at 1280×720.

## Views

- **Live view:** the real screen in an iPhone frame on the left. On the right are the statechart (current state filled peach, the transition that led here drawn in orange), and a step card: trigger (user action / system event / alt-error), screen title, the real state values (`cycles.status`, `release_status`, `media_jobs.status`, quota and invite columns) and the code name (component and testID, or server function). Below is a filmstrip of the flow's screens.
- **Storyboard view (S):** every screen of the flow in one or two rows, with labelled arrows (solid = user action, orange dashed = system event, red dashed = alt/error branch) and a state chip under each screen.

## Keyboard and mouse

| Key | Action |
|---|---|
| → / Space / PageDown | next screen (continues into the next flow) |
| ← / PageUp | previous screen |
| 1–4 | switch flow |
| S | toggle storyboard view (←/→ then switch flows) |
| Home / End | first / last screen of the flow |
| Click phone / thumbnail / tabs | next screen / jump / switch flow |

Deep links: `index.html#2-5` (flow 2, step 5), `index.html#story-3` (storyboard of flow 3). `?export` hides the tab bar (used for the PNGs).

## Flows

1. **Join** (UC02, UC03), 8 screens: no group → New group → `createRealGroup()` → Home collecting → Invite code (`real_group_invites.status = 'active'`) → Jun enters code → Joined (`'accepted'`) → Jun's Home → Members.
2. **Capture** (UC04, UC05, UC06a), 8 screens: Home 5 of 5 left → camera permission → look picker → Retake/Seal → Sealed 4 left → video Sealed 3 left → Home 2 of 5 → allowance used (grey shutter, "All 5 used"). The state stays Collecting throughout.
3. **Lifecycle** (UC07, UC08, UC12, UC13), 8 screens: Collecting → `advance` → Home "film developing" (Revealing/unpublished) → Archive developing → `publish` → "Your film is here" (Revealing/published) → Film → The end (Replay / Save film) → `advance` 24 h → Archive earlier films (Archived) → alt branch: "Taking a little longer" (`media_jobs.status = 'failed'`, state retained).
4. **Access** (UC03 guard, private media), 4 steps: Priya not in a group → reused code, "This invitation has already been used" (`'replayed'`) → direct film request, HTTP 403 `forbidden` → member Jun gets 200 and sees the film.

## Static storyboards (for the PDF)

`storyboards/1-join-a-private-group.png`, `2-contribute-within-the-allowance.png`, `3-cycle-lifecycle-to-archive.png` and `4-outsider-is-denied.png`, each 1280×720.

## Where it goes in the deck

- **A&D section**, right after the statechart slide (D1): embed `uiflow/index.html` full slide (D2), starting on flow 3 (`#3-1`), the cycle lifecycle. That flow is the one that shows the planned statechart driving the UI. Flows 1 and 4 also fit the system demo (UC02/UC03 and the privacy point); flow 2 fits the capture and allowance use cases.
- **Backup / PDF:** the four storyboard PNGs, one per slide, after D2.
- In a 1280×682 iframe the stage scales to 0.95. Give it the full 1280×720 when you can.

## Sources of the screens

Real app UI throughout. Home, Archive, invite, join, film, the end and access screens are Playwright captures (iPhone viewport 402×720 at 3×) of `origin/dev` 2390589, run locally with real 28-day cycles. Each lifecycle state was reached in the local database; the film is the real hosted-dev film. The camera, look, review and Sealed screens are frames from the iPhone simulator recordings in `videos/raw/` (05-photo, 06-video), cropped below the status bar and above the Safari toolbar. No screen shows a minutes countdown.
