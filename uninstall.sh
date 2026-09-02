#!/usr/bin/env bash
# Remove the Lumon screensaver bodies. Does NOT touch the idle plugin clone —
# disable that with:  omarchy plugin disable <yourname>.idle
set -euo pipefail

BIN="$HOME/.local/bin"
BRAND="$HOME/.config/omarchy/branding"

rm -f "$BIN"/omarchy-lumon-screensaver \
      "$BIN"/omarchy-lumon-screensaver-launch \
      "$BIN"/omarchy-lumon-scenes-screensaver \
      "$BRAND"/screensaver.txt \
      "$BRAND"/lumon-anims/_scenes.py
# _lumon.py is shared with omarchy-lumon-greeting — leave it if that dir has other files
[[ -d "$BRAND/lumon-anims" ]] && [[ -z $(ls -A "$BRAND/lumon-anims" 2>/dev/null) ]] && rmdir "$BRAND/lumon-anims"

echo "Done. If you patched the idle plugin:  omarchy plugin disable <yourname>.idle"
