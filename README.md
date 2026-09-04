# omarchy-lumon-screensaver

<!-- lumon-set:start -->
> **Part of [Omarchy · Lumon Industries](https://github.com/KaiCryan/omarchy-lumon)** — a whole-system *Severance* theme for Omarchy.

<details><summary><strong>The full set</strong></summary>

| Repo | |
|---|---|
| [omarchy-lumon](https://github.com/KaiCryan/omarchy-lumon) | **the hub** — install everything, screenshots, the whole pitch |
| [omarchy-lumon-boot](https://github.com/KaiCryan/omarchy-lumon-boot) | Plymouth boot splash — Lumon globe, matching LUKS prompt |
| [omarchy-lumon-lock](https://github.com/KaiCryan/omarchy-lumon-lock) | lock screen — prompts *“Enter your access code”* |
| [omarchy-lumon-greeting](https://github.com/KaiCryan/omarchy-lumon-greeting) | terminal greeting — 19 animations, then `fastfetch` |
| [omarchy-lumon-wallpapers](https://github.com/KaiCryan/omarchy-lumon-wallpapers) | ASCII crew portraits + 4K brand set, hourly cycler |
| **omarchy-lumon-screensaver** | capped-fps `ttfx` effects + an ambient scene reel &nbsp;·&nbsp; ← you are here |
| [omarchy-lumon-theme](https://github.com/KaiCryan/omarchy-lumon-theme) | colour scheme, Hyprland look’n’feel, `fastfetch` + about branding |
| [omarchy-desktop-quote](https://github.com/KaiCryan/omarchy-desktop-quote) | a rotating quote placard over the wallpaper |
| [omarchy-lumon-assets](https://github.com/KaiCryan/omarchy-lumon-assets) | shared ASCII art, fonts and build tools |

</details>
<!-- lumon-set:end -->

*Severance* / Lumon Industries screensavers for [Omarchy](https://omarchy.org).

Two idle-screen "bodies", picked at random each time you go idle:

| Body | What it is |
|---|---|
| `omarchy-lumon-screensaver` | Omarchy's stock `ttfx` effects, but the frame rate is capped (stock runs at 120 fps and pins a CPU core per monitor). Banner text from `screensaver.txt`. |
| `omarchy-lumon-scenes-screensaver` | An ambient reel — eight looping Severance scenes (a refinement grid filling with numbers, the corridor, the wireframe globe, the descent, drifting motes, aphorisms, the wordmark, a clock). CPU-cheap on purpose. |

`omarchy-lumon-screensaver-launch` is the picker. Force one:

```sh
LUMON_SCREENSAVER=ttfx    omarchy-lumon-screensaver-launch force
LUMON_SCREENSAVER=scenes  omarchy-lumon-screensaver-launch force
```

## Doesn't cover the screen while media is playing

`patch-idle.sh` also teaches the idle service to **hold the screensaver back
while any MPRIS player is "Playing"** — so it won't drop over a YouTube video or
a film just because you haven't touched the mouse. It polls every ~10s; when
playback stops, the screensaver comes up on the next tick.

`omarchy-lumon-media-playing` is the check (uses `playerctl` if present, else
`busctl`). Exempt specific players so background music doesn't count:

```sh
# in the idle plugin's environment, or your shell
LUMON_IDLE_IGNORE_PLAYERS="spotify,mpd"
```

Auto-**lock** still fires on its own timer regardless of media — this only
defers the screensaver.

## Install

```sh
git clone https://github.com/KaiCryan/omarchy-lumon-screensaver
cd omarchy-lumon-screensaver
./install.sh          # copies the bodies + the media check
./patch-idle.sh       # wires the idle service to use them + media gating
```

`patch-idle.sh` clones Omarchy's idle plugin and applies
`idle-patch/Service.qml.patch` on top of a pristine copy, so it's safe to re-run
after `omarchy update`.

## Tuning

- `LUMON_SCREENSAVER_FRAME_RATE` — ttfx fps (default 20)
- `LUMON_SCENE_SECS` — seconds per ambient scene (default 45)
- `LUMON_SCENE_FPS` — fps for the grid scenes (default 11)
- `LUMON_SCENE` — force one scene: `numbers|corridor|globe|descent|motes|aphorisms|wordmark|clock`
- `LUMON_SPEED` — global speed multiplier
- `LUMON_IDLE_IGNORE_PLAYERS` — MPRIS players that don't defer the screensaver

## Uninstall

```sh
./uninstall.sh
omarchy plugin disable <yourname>.idle   # revert the idle wiring
```

## Notes

- `branding/lumon-anims/_lumon.py` is a shared helper, also shipped by
  [omarchy-lumon-greeting](https://github.com/KaiCryan/omarchy-lumon-greeting).
  Installing both is fine — the file is identical.
- `idle-patch/Service.qml.patch` is a diff against Omarchy's own `Service.qml`
  (that plugin is Omarchy's code) — `patch-idle.sh` applies it rather than
  vendoring a copy.
