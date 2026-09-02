#!/usr/bin/env bash
# Point Omarchy's idle service at the Lumon screensaver launcher.
#
# Omarchy's stock idle plugin runs `omarchy-launch-screensaver` when you go
# idle. This clones that plugin (so `omarchy update` can't revert it) and
# swaps in `omarchy-lumon-screensaver-launch`, which randomly picks one of the
# Lumon screensaver bodies.
#
# Idempotent: if you already have an idle clone, it just re-patches it.
set -euo pipefail

LAUNCH='"$HOME/.local/bin/omarchy-lumon-screensaver-launch"'
PLUGINS="$HOME/.config/omarchy/plugins"

# find an existing idle clone, or make one
clone=$(find "$PLUGINS" -maxdepth 1 -type d -name '*.idle' 2>/dev/null | head -1 || true)
if [[ -z $clone ]]; then
  echo ":: cloning omarchy.idle"
  omarchy plugin clone omarchy.idle
  clone=$(find "$PLUGINS" -maxdepth 1 -type d -name '*.idle' | head -1)
fi
[[ -n $clone && -f "$clone/Service.qml" ]] || { echo "no idle plugin clone found" >&2; exit 1; }

echo ":: patching $clone/Service.qml"
sed -i "s#|| omarchy-launch-screensaver\"#|| $LAUNCH\"#" "$clone/Service.qml"
grep -q "omarchy-lumon-screensaver-launch" "$clone/Service.qml" \
  || { echo "patch did not apply (already patched, or upstream changed)" >&2; }

omarchy restart shell 2>/dev/null || true
echo "Done. Idle now launches the Lumon screensaver. Revert: omarchy plugin disable $(basename "$clone")"
