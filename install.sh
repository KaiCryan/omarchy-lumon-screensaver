#!/usr/bin/env bash
# Install the Lumon screensaver bodies into Omarchy.
set -euo pipefail
cd "$(dirname "$0")"

BIN="$HOME/.local/bin"
BRAND="$HOME/.config/omarchy/branding"

echo ":: installing screensaver bodies -> $BIN"
mkdir -p "$BIN"
install -m 755 bin/omarchy-lumon-screensaver         "$BIN/"
install -m 755 bin/omarchy-lumon-screensaver-launch  "$BIN/"
install -m 755 bin/omarchy-lumon-scenes-screensaver  "$BIN/"

echo ":: installing assets -> $BRAND"
mkdir -p "$BRAND/lumon-anims"
cp branding/screensaver.txt        "$BRAND/screensaver.txt"
cp branding/lumon-anims/_lumon.py  "$BRAND/lumon-anims/_lumon.py"
cp branding/lumon-anims/_scenes.py "$BRAND/lumon-anims/_scenes.py"

echo
echo "Bodies installed. To make idle actually use them:  ./patch-idle.sh"
echo "Or test one now:  LUMON_SCREENSAVER=scenes omarchy-lumon-screensaver-launch force"
