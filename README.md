# omarchy-lumon-screensaver

*Severance* / Lumon Industries screensavers for [Omarchy](https://omarchy.org).

Three idle-screen "bodies", picked at random each time you go idle:

| Body | What it is |
|---|---|
| `omarchy-lumon-screensaver` | Omarchy's stock `ttfx` effects, but the frame rate is capped (stock runs at 120 fps and pins a CPU core per monitor). Banner text from `screensaver.txt`. |
| `omarchy-lumon-scenes-screensaver` | An ambient reel — eight looping Severance scenes (a refinement grid filling with numbers, the corridor, the wireframe globe, the descent, drifting motes, aphorisms, the wordmark, a clock). CPU-cheap on purpose. |

`omarchy-lumon-screensaver-launch` is the picker. Force one:

```sh
LUMON_SCREENSAVER=ttfx    omarchy-lumon-screensaver-launch force
LUMON_SCREENSAVER=scenes  omarchy-lumon-screensaver-launch force
```

## Install

```sh
git clone https://github.com/KaiCryan/omarchy-lumon-screensaver
cd omarchy-lumon-screensaver
./install.sh          # copies the bodies + assets
./patch-idle.sh       # makes the idle service actually use them
```

`patch-idle.sh` clones Omarchy's idle plugin (so `omarchy update` can't revert
it) and redirects its screensaver launch to `omarchy-lumon-screensaver-launch`.
It's idempotent.

## Tuning

Environment knobs (set in the launcher, your shell, or the idle plugin):

- `LUMON_SCREENSAVER_FRAME_RATE` — ttfx fps (default 20)
- `LUMON_SCENE_SECS` — seconds per ambient scene (default 45)
- `LUMON_SCENE_FPS` — fps for the grid scenes (default 11)
- `LUMON_SCENE` — force one scene: `numbers|corridor|globe|descent|motes|aphorisms|wordmark|clock`
- `LUMON_SPEED` — global speed multiplier

## Uninstall

```sh
./uninstall.sh
omarchy plugin disable <yourname>.idle   # revert the idle wiring
```

## Notes

- `branding/lumon-anims/_lumon.py` is a shared helper, also shipped by
  [omarchy-lumon-greeting](https://github.com/KaiCryan/omarchy-lumon-greeting).
  Installing both is fine — the file is identical.
- The idle plugin's `Service.qml` is Omarchy's own code; `patch-idle.sh` only
  changes the one line that names the launch command, rather than vendoring a
  copy here.
