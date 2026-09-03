#!/usr/bin/env bash
# Wire Omarchy's idle service to the Lumon screensavers + media-aware gating.
#
# Clones Omarchy's idle plugin (so `omarchy update` can't revert it) and applies
# idle-patch/Service.qml.patch, which:
#   - launches omarchy-lumon-screensaver-launch instead of omarchy-launch-screensaver
#   - holds the screensaver back while any MPRIS player is "Playing" (so it
#     doesn't cover the screen while you watch YouTube / a film), retrying once
#     playback stops
#
# Idempotent: patches a pristine copy each run, so it's safe after an update.
set -euo pipefail
cd "$(dirname "$0")"

PLUGINS="$HOME/.config/omarchy/plugins"
STOCK=/usr/share/omarchy/shell/plugins/services/idle

clone=$(find "$PLUGINS" -maxdepth 1 -type d -name '*.idle' 2>/dev/null | head -1 || true)
if [[ -z $clone ]]; then
  echo ":: cloning omarchy.idle"
  omarchy plugin clone omarchy.idle
  clone=$(find "$PLUGINS" -maxdepth 1 -type d -name '*.idle' | head -1)
fi
[[ -n $clone && -d $STOCK ]] || { echo "idle plugin not found" >&2; exit 1; }

cp "$STOCK/Service.qml" "$clone/Service.qml"           # start pristine
patch -s -p1 -d "$clone" < idle-patch/Service.qml.patch
grep -q 'omarchy-lumon-screensaver-launch' "$clone/Service.qml" \
  || { echo "patch did not apply cleanly — upstream Service.qml may have changed" >&2; exit 1; }

omarchy restart shell 2>/dev/null || true
echo "Done. Revert with:  omarchy plugin disable $(basename "$clone")"
