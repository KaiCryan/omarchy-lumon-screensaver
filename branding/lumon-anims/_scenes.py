#!/usr/bin/env python3
"""Lumon ambient screensaver reel -- cycles full-screen Severance scenes forever.

Launched by ~/.local/bin/omarchy-lumon-scenes-screensaver (which, like the stock
saver wrapper, also watches the keyboard and kills this on input). Loops until
SIGTERM/SIGINT. Deliberately CPU-cheap: grid scenes run ~11fps, text scenes
redraw a line or two a second.

Knobs (env): LUMON_SCENE_SECS (per scene, default 45), LUMON_SCENE_FPS (grid
scenes, default 11), LUMON_SCENE (force one: numbers|corridor|globe|descent|
motes|aphorisms|wordmark|clock), LUMON_SPEED.
"""
import math
import os
import random
import signal
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lumon import COLOR, DIM, HOT, RESET, fg, load_art, term_size  # noqa: E402

SPEED = float(os.environ.get("LUMON_SPEED", "1") or 1)
SCENE_SECS = float(os.environ.get("LUMON_SCENE_SECS", "45") or 45)
GRID_NAP = max(0.03, 1.0 / float(os.environ.get("LUMON_SCENE_FPS", "11") or 11))
ONLY = os.environ.get("LUMON_SCENE", "").strip()

_run = True


def _stop(*_a):
    global _run
    _run = False


for _s in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP, signal.SIGQUIT):
    signal.signal(_s, _stop)


def emit(s):
    sys.stdout.write(s)
    sys.stdout.flush()


def nap(t):
    end = time.time() + t / SPEED
    while _run and time.time() < end:
        time.sleep(min(0.05, max(0.0, end - time.time())))


def paint_rows(rows):
    emit("\033[H" + "".join(r + "\033[K\r\n" for r in rows) + "\033[J")


def center_plain(text, width, rgb):
    return " " * max(0, (width - len(text)) // 2) + fg(rgb) + text + RESET


def wrap(text, width):
    line, out = "", []
    for word in text.split():
        if len(line) + len(word) + 1 > width:
            out.append(line)
            line = word
        else:
            line = (line + " " + word).strip()
    if line:
        out.append(line)
    return out


def dissolve():
    cols, lines = term_size()
    cells = [(y, x) for y in range(1, lines + 1) for x in range(1, cols)]
    random.shuffle(cells)
    step = max(1, len(cells) // 12)
    for k in range(0, len(cells), step):
        if not _run:
            break
        emit("".join(f"\033[{y};{x}H " for (y, x) in cells[k:k + step]))
        nap(0.014)
    emit("\033[2J\033[H")


FALLBACK_WORDMARK = [
    "██╗     ██╗   ██╗ ███╗   ███╗  ██████╗  ███╗   ██╗",
    "██║     ██║   ██║ ████╗ ████║ ██╔═══██╗ ████╗  ██║",
    "██║     ██║   ██║ ██╔████╔██║ ██║   ██║ ██╔██╗ ██║",
    "██║     ██║   ██║ ██║╚██╔╝██║ ██║   ██║ ██║╚██╗██║",
    "███████╗╚██████╔╝ ██║ ╚═╝ ██║ ╚██████╔╝ ██║ ╚████║",
    "╚══════╝ ╚═════╝  ╚═╝     ╚═╝  ╚═════╝  ╚═╝  ╚═══╝",
]

KIER_LINES = [
    "The remembered are never truly gone.",
    "Keep a merry humor ever in your heart.",
    "Let not weakness live in your veins.",
    "Be ever merry.",
    "A handshake is available upon request.",
    "Tame in me the tempers four that seek to make my soul impure.",
    "The surest way to tame a prisoner is to let him believe he is free.",
    "Industry is the flower of which commerce is the fruit.",
    "Bring me your bloodied and weak, and I shall exalt them.",
    "The work is mysterious and important.",
    "A good person will follow the rules. A great person will follow herself.",
]

CLOCK_FONT = {
    "0": ["╭─╮", "│ │", "│ │", "│ │", "╰─╯"],
    "1": ["  ╷", "  │", "  │", "  │", "  ╵"],
    "2": ["╭─╮", "  │", "╭─╯", "│  ", "╰─╯"],
    "3": ["╭─╮", "  │", "╶─┤", "  │", "╰─╯"],
    "4": ["╷ ╷", "│ │", "╰─┤", "  │", "  ╵"],
    "5": ["╭─╮", "│  ", "╰─╮", "  │", "╰─╯"],
    "6": ["╭─╮", "│  ", "├─╮", "│ │", "╰─╯"],
    "7": ["╭─╮", "  │", "  │", " │ ", " ╵ "],
    "8": ["╭─╮", "│ │", "├─┤", "│ │", "╰─╯"],
    "9": ["╭─╮", "│ │", "╰─┤", "  │", "╰─╯"],
    ":": ["   ", " • ", "   ", " • ", "   "],
    " ": ["   ", "   ", "   ", "   ", "   "],
}


def scene_numbers(deadline):
    cols, lines = term_size()
    gw, gh = cols - 1, lines - 1
    rnd = random.Random()
    data = [[rnd.randrange(10) for _ in range(gh)] for _ in range(gw)]
    offs = [0.0] * gw
    spd = [rnd.uniform(0.015, 0.14) for _ in range(gw)]
    flare = {}
    f = 0
    while _run and time.time() < deadline:
        f += 1
        for x in range(gw):
            prev = offs[x]
            offs[x] += spd[x]
            if int(offs[x]) > int(prev):
                data[x].insert(0, rnd.randrange(10))
                data[x].pop()
        if rnd.random() < 0.16:
            fx = rnd.randrange(max(1, gw - 5))
            fy = rnd.randrange(max(1, gh - 3))
            for dx in range(rnd.randint(2, 5)):
                for dy in range(rnd.randint(1, 3)):
                    flare[(fx + dx, fy + dy)] = rnd.randint(6, 14)
        rows = []
        for y in range(gh):
            row = []
            for x in range(gw):
                d = data[x][y]
                key = (x, y)
                if key in flare:
                    row.append(fg(HOT) + str(d) + RESET)
                    flare[key] -= 1
                    if flare[key] <= 0:
                        del flare[key]
                else:
                    wave = math.sin(x * 0.10 + y * 0.07 + f * 0.05)
                    row.append((fg(COLOR) if wave > 0.62 else fg(DIM)) + str(d) + RESET)
            rows.append("".join(row))
        paint_rows(rows)
        nap(GRID_NAP)


def scene_corridor(deadline):
    cols, lines = term_size()
    w, h = cols - 1, lines - 1
    cx, cy = w / 2, h / 2
    rings = 7
    f = 0
    while _run and time.time() < deadline:
        f += 1
        cell = [[None] * w for _ in range(h)]
        for t in range(70):
            tt = t / 70
            for sx, sy in ((0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)):
                x, y = int(sx + (cx - sx) * tt), int(sy + (cy - sy) * tt)
                if 0 <= y < h and 0 <= x < w and cell[y][x] is None:
                    cell[y][x] = ("·", DIM)
        for k in range(rings):
            d = ((k / rings) + f * 0.011) % 1.0
            scale = d ** 2.0
            hw = max(1, int(scale * (cx - 1)))
            hh = max(1, int(scale * (cy - 1)))
            rgb = HOT if d > 0.85 else COLOR if d > 0.45 else DIM
            x0, x1 = int(cx - hw), int(cx + hw)
            y0, y1 = int(cy - hh), int(cy + hh)
            for x in range(max(0, x0), min(w, x1 + 1)):
                for y in (y0, y1):
                    if 0 <= y < h:
                        cell[y][x] = ("─", rgb)
            for y in range(max(0, y0), min(h, y1 + 1)):
                for x in (x0, x1):
                    if 0 <= x < w:
                        cell[y][x] = ("│", rgb)
            for x, y, ch in ((x0, y0, "┌"), (x1, y0, "┐"), (x0, y1, "└"), (x1, y1, "┘")):
                if 0 <= y < h and 0 <= x < w:
                    cell[y][x] = (ch, rgb)
        rows = []
        for y in range(h):
            rr = []
            for x in range(w):
                c = cell[y][x]
                rr.append(" " if c is None else fg(c[1]) + c[0] + RESET)
            rows.append("".join(rr))
        paint_rows(rows)
        nap(GRID_NAP)


def scene_globe(deadline):
    cols, lines = term_size()
    gw, gh = 46, 23
    ox, oy = (gw - 1) / 2, (gh - 1) / 2
    rx, ry = 20.0, 10.0
    top = max(1, lines // 2 - gh // 2)
    left = max(0, cols // 2 - gw // 2)
    lons = [i * math.pi / 6 for i in range(6)]
    lats = [-0.9, -0.45, 0.0, 0.45, 0.9]
    emit("\033[2J")
    rot = 0.0
    while _run and time.time() < deadline:
        rot += 0.035
        grid = [[" "] * gw for _ in range(gh)]
        for lon in lons:
            for i in range(150):
                a = math.pi * i / 149 - math.pi / 2
                x = math.cos(a) * math.sin(lon + rot)
                z = math.cos(a) * math.cos(lon + rot)
                yv = math.sin(a)
                if z < 0:
                    continue
                px, py = int(round(ox + x * rx)), int(round(oy - yv * ry))
                if 0 <= py < gh and 0 <= px < gw:
                    grid[py][px] = "|" if abs(x) < 0.35 else ("/" if (x > 0) == (yv > 0) else "\\")
        for lat in lats:
            for i in range(150):
                lon = 2 * math.pi * i / 149
                x = math.cos(lat) * math.sin(lon + rot)
                z = math.cos(lat) * math.cos(lon + rot)
                if z < 0:
                    continue
                px, py = int(round(ox + x * rx)), int(round(oy - math.sin(lat) * ry))
                if 0 <= py < gh and 0 <= px < gw:
                    grid[py][px] = "-"
        for i in range(220):
            a = 2 * math.pi * i / 220
            px, py = int(round(ox + math.cos(a) * rx)), int(round(oy + math.sin(a) * ry))
            if 0 <= py < gh and 0 <= px < gw:
                grid[py][px] = "(" if math.cos(a) < -0.5 else ")" if math.cos(a) > 0.5 else "-"
        buf = []
        for i, rowl in enumerate(grid):
            buf.append(f"\033[{top + i};{left + 1}H" + fg(COLOR) + "".join(rowl) + RESET)
        cap = "L U M O N"
        buf.append(f"\033[{top + gh + 1};{cols // 2 - len(cap) // 2 + 1}H" + fg(HOT) + cap + RESET)
        emit("".join(buf))
        nap(max(GRID_NAP, 0.06))


def scene_descent(deadline):
    cols, lines = term_size()
    w, h = cols - 1, lines - 1
    rail_l = max(2, w // 2 - 22)
    rail_r = min(w - 2, w // 2 + 22)
    tube = 0.0
    floor = 0
    while _run and time.time() < deadline:
        tube += 0.5
        if tube > h:
            tube -= h
            floor += 1
        ty = int(tube)
        ly = h // 2
        lbl = f"SUBLEVEL  B{floor + 1}"
        rows = []
        for y in range(h):
            line = [" "] * w
            line[rail_l] = "│"
            line[rail_r] = "│"
            if y % 4 == 0:
                for x in range(rail_l + 1, rail_r):
                    line[x] = "·"
            s = "".join(line)
            if y == ty:
                s = " " * rail_l + "█" * (rail_r - rail_l + 1) + " " * (w - rail_r - 1)
                rows.append(fg(HOT) + s + RESET)
            elif y == ly:
                mid = w // 2 - len(lbl) // 2
                s = s[:mid] + lbl + s[mid + len(lbl):]
                rows.append(fg(COLOR) + s + RESET)
            else:
                rows.append(fg(DIM) + s + RESET)
        paint_rows(rows)
        nap(GRID_NAP)


def scene_motes(deadline):
    cols, lines = term_size()
    w, h = cols - 1, lines - 1
    rnd = random.Random()
    n = max(20, (w * h) // 80)
    motes = [[rnd.uniform(0, w), rnd.uniform(0, h),
              rnd.uniform(-0.14, 0.14), rnd.uniform(-0.05, 0.05),
              rnd.choice("0123456789"), rnd.random()] for _ in range(n)]
    emit("\033[2J")
    while _run and time.time() < deadline:
        grid = [[None] * w for _ in range(h)]
        for m in motes:
            m[0] = (m[0] + m[2]) % w
            m[1] = (m[1] + m[3]) % h
            if rnd.random() < 0.004:
                m[4] = rnd.choice("0123456789")
            m[5] = max(0.0, min(1.0, m[5] + (rnd.random() - 0.5) * 0.12))
            ix, iy = int(m[0]), int(m[1])
            if 0 <= iy < h and 0 <= ix < w:
                rgb = HOT if m[5] > 0.86 else COLOR if m[5] > 0.42 else DIM
                grid[iy][ix] = (m[4], rgb)
        rows = ["".join(" " if c is None else fg(c[1]) + c[0] + RESET for c in r) for r in grid]
        paint_rows(rows)
        nap(GRID_NAP)


def scene_aphorisms(deadline):
    cols, lines = term_size()
    rnd = random.Random()
    pool = []
    while _run and time.time() < deadline:
        if not pool:
            pool = KIER_LINES[:]
            rnd.shuffle(pool)
        q = pool.pop()
        wrapped = wrap(q, min(cols - 8, 54))
        row0 = lines // 2 - len(wrapped) // 2
        emit("\033[2J")
        for phase, (shade, hold) in enumerate(((DIM, 0.5), (COLOR, 3.4), (DIM, 0.6))):
            for i, ln in enumerate(wrapped):
                emit(f"\033[{row0 + i};1H\033[2K" + center_plain(ln, cols, shade))
            if phase == 1:
                emit(f"\033[{row0 + len(wrapped) + 2};1H\033[2K"
                     + center_plain("— Kier Eagan", cols, DIM))
            nap(hold)
            if not _run:
                return
        emit("\033[2J")
        nap(0.5)


def scene_wordmark(deadline):
    cols, lines = term_size()
    art = load_art("lumon-wordmark-ascii.txt")
    if not art or max(len(x) for x in art) > cols - 2:
        art = FALLBACK_WORDMARK
    ah = len(art)
    aw = max(len(x) for x in art)
    top = max(1, lines // 2 - ah // 2 - 1)
    left = max(0, cols // 2 - aw // 2)
    emit("\033[2J")
    band = 0.0
    while _run and time.time() < deadline:
        band = (band + 0.3) % (ah + 10)
        buf = []
        for i, ln in enumerate(art):
            dist = abs(i - band)
            rgb = HOT if dist < 1.3 else COLOR if dist < 3.2 else DIM
            buf.append(f"\033[{top + i};{left + 1}H" + fg(rgb) + ln + RESET)
        cap = "U N I T E D   I N   S E V E R A N C E"
        buf.append(f"\033[{top + ah + 2};{cols // 2 - len(cap) // 2 + 1}H" + fg(DIM) + cap + RESET)
        emit("".join(buf))
        nap(0.11)


def scene_clock(deadline):
    cols, lines = term_size()
    emit("\033[2J")
    last = None
    while _run and time.time() < deadline:
        now = time.localtime()
        hhmm = time.strftime("%H:%M", now)
        top = lines // 2 - 4
        if hhmm != last:
            last = hhmm
            emit("\033[2J")
            rows = ["", "", "", "", ""]
            for ch in hhmm:
                g = CLOCK_FONT.get(ch, CLOCK_FONT[" "])
                for r in range(5):
                    rows[r] += g[r] + " "
            cw = max(len(r) for r in rows)
            left = cols // 2 - cw // 2
            for r in range(5):
                emit(f"\033[{top + r};{left + 1}H" + fg(COLOR) + rows[r] + RESET)
            emit(f"\033[{top + 7};1H\033[2K" + center_plain("SEVERED FLOOR", cols, DIM))
            emit(f"\033[{top + 9};1H\033[2K"
                 + center_plain(time.strftime("%A, %B %d", now).upper(), cols, DIM))
        secs = time.localtime().tm_sec
        barw = 40
        filled = int(barw * secs / 60)
        emit(f"\033[{top + 11};1H\033[2K"
             + center_plain("▏" + "─" * filled + " " * (barw - filled) + "▕", cols, DIM))
        nap(0.5)


SCENES = {
    "numbers": scene_numbers,
    "corridor": scene_corridor,
    "globe": scene_globe,
    "descent": scene_descent,
    "motes": scene_motes,
    "aphorisms": scene_aphorisms,
    "wordmark": scene_wordmark,
    "clock": scene_clock,
}


def main():
    emit("\033[?25l\033[2J\033[H")
    forced = ONLY if ONLY in SCENES else ""
    order = []
    try:
        while _run:
            if forced:
                name = forced
            else:
                if not order:
                    order = list(SCENES)
                    random.shuffle(order)
                name = order.pop()
            try:
                SCENES[name](time.time() + SCENE_SECS)
            except Exception:
                nap(1.0)
            if _run and not forced:
                dissolve()
    finally:
        emit(RESET + "\033[?25h\033[2J\033[H")


main()
