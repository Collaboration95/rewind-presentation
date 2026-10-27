# Rewind deck

Run `./serve.sh` and open `http://127.0.0.1:8778/deck/deck.html`. The server serves presentation-prep so the sibling videos directory is reachable. Arrow keys navigate; N notes; O overview; F fullscreen; B blackout; P clip playback; C command cards; Z full-size figure; digits + Enter jump. Named hashes include #s9, #F5 and #B7.

Twenty main narrative frames, twelve feature inserts, twenty-five Q&A backups. SCRIPT.md totals 38 minutes. OUTLINE.md maps the brief to frames. PLACEHOLDERS.md lists current parallel-agent asset slots.

`python3 build_deck.py` rebuilds the HTML and script, refreshes final-clip posters, and discovers every SVG in uml/. It reads shared records but writes only inside deck/. It does not edit diagram or video sources. Keep the final clips in ../videos/clips/ and the pipeline recording in clips/ci-cd-40344230832.mp4.

Framework fork: CSS and JS copied from dc2-rescue/project-documentation/presentation/site/deck.html, with the PDF palette and layout applied as overrides. Counters and five-section progress are generated. The overview supports clickable frames; videos load on activation and pause when leaving the frame. PDF uses a 1280×720 print stage and includes every split diagram and agile chart.

Export with `./export.sh`. The PDF and 60-dpi page rasterisations are under out/.
