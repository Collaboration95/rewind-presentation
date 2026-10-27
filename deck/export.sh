#!/bin/zsh
set -eu
cd "${0:A:h}"
python3 build_deck.py
profile=$(mktemp -d /tmp/rewind-deck-chrome.XXXXXX)
trap 'rm -rf "$profile"' EXIT
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu --allow-file-access-from-files --user-data-dir="$profile" --no-pdf-header-footer --print-to-pdf="$PWD/out/rewind-presentation.pdf" "file://$PWD/deck.html"
pdftoppm -r 60 -png out/rewind-presentation.pdf out/page
