# Rewind deck

Run `./serve.sh` and open `http://127.0.0.1:8778/deck/deck.html`. The server serves presentation-prep so the sibling videos directory is reachable. Arrow keys navigate; N notes; O overview; F fullscreen; B blackout; Space / P clip playback; M sound; R restart; C command cards; Z full-size figure; digits + Enter jump. Named hashes include #s9, #F5 and #B7.

Twenty-six narrative frames (Section 3 has one slide per test type), ten feature inserts, thirty-five Q&A backups. Installation and sign-in are backups B32 and B33. SCRIPT.md totals 38 minutes. OUTLINE.md maps the brief to frames. PLACEHOLDERS.md lists the completed asset check.

`python3 build_deck.py` rebuilds the HTML and script, refreshes final-clip posters, and discovers every SVG in uml/. It reads shared records but writes only inside deck/. It does not edit diagram or video sources. Stage features use clips/device/ and clips/hosted-device/; the pipeline uses clips/ci-cd-40344230832.mp4. Keep ../videos/ for the original recordings and installation/sign-in backups.

Framework fork: CSS and JS copied from dc2-rescue/project-documentation/presentation/site/deck.html, with a calm light-green palette (restyle.py) applied as overrides. Testing slides live in testing_slides.py. Counters and five-section progress are generated. The overview supports clickable frames; videos load paused and muted on activation; Space or a click controls playback, and leaving pauses them. PDF uses a 1280×720 print stage and includes every split diagram and agile chart.

Export with `./export.sh`. The PDF and 60-dpi page rasterisations are under out/.
