#!/bin/zsh
set -eu
cd "${0:A:h}/.."
python3 -m http.server "${1:-8778}" --bind 127.0.0.1
