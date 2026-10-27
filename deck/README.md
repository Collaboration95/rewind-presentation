# Rewind deck

Run `./serve.sh` and open `http://127.0.0.1:8778/deck/deck.html`. The server serves presentation-prep so the sibling videos directory is reachable. Arrow keys navigate; N notes; O overview; F fullscreen; B blackout; Space / P clip playback; M sound; R restart; C command cards; Z full-size figure; digits + Enter jump. Named hashes include #s9, #F5 and #B7.

The main path follows CUT-PLAN.md (cutplan.py): the main slides (narrative frames and 8 feature clips, numbered 1–N) in 33:00 of content within a 35:00 hard limit. Section 2 ends with the cycle statechart D1 and the full-bleed UI flow page D2 (uiflow/index.html#3-1); storyboards U1–U4 (S) and the CI/CD detail frames C5, C7, C15 and C11 (V opens and returns) sit after the main path with the other backups. Main slides carry 'n / N' and backups their own label (pageno.py); typing n + Enter jumps to main slide n. SCRIPT.md has a per-slide clock. OUTLINE.md maps the brief to frames. PLACEHOLDERS.md lists the completed asset check.

`python3 build_deck.py` rebuilds the HTML and script, refreshes final-clip posters, and discovers every SVG in uml/. It reads shared records but writes only inside deck/. It does not edit diagram or video sources. Stage features use clips/device/ and clips/hosted-device/; the pipeline uses clips/ci-cd-40344230832.mp4. Keep ../videos/ for the original recordings and installation/sign-in backups.

Framework fork: CSS and JS copied from dc2-rescue/project-documentation/presentation/site/deck.html, with the Rewind app's Warm Glass identity (appvibe.py: cream #f6ede3, peach accents, glass cards, the app's own Fraunces/Geist/DM Mono fonts) layered over restyle.py. The cover shows the hosted app's Home on an iPhone 15 Pro frame (assets/cover-home.png). Testing slides live in testing_slides.py. Counters and five-section progress are generated. The overview supports clickable frames; videos load paused and muted on activation; Space or a click controls playback, and leaving pauses them. PDF uses a 1280×720 print stage and includes every split diagram and agile chart.

Export with `./export.sh`. The PDF and 60-dpi page rasterisations are under out/.
