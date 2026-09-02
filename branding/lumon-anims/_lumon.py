"""Shared helpers for the Lumon terminal greeting animations.

Every animation script in this directory imports this. Palette, speed and the
employee name arrive as environment variables set by ../lumon-greeting; running
a script directly still works (sensible defaults, and a static frame when stdout
is not a terminal).
"""
import os
import re
import sys
import time

_ANSI = re.compile(r"\033\[[0-9;?]*[A-Za-z]")

SPEED = float(os.environ.get("LUMON_SPEED", "1") or 1)
COLOR = os.environ.get("LUMON_COLOR", "158;204;228")   # primary line work
DIM = os.environ.get("LUMON_DIM", "74;107;128")        # faint / background
HOT = os.environ.get("LUMON_HOT", "242;252;255")       # highlights
NAME = os.environ.get("LUMON_NAME") or os.environ.get("USER") or "employee"
TTY = sys.stdout.isatty()

RESET = "\033[0m"
BOLD = "\033[1m"


def fg(rgb):
    return f"\033[38;2;{rgb}m"


def paint(text, rgb=COLOR, bold=False):
    return f"{BOLD if bold else ''}{fg(rgb)}{text}{RESET}"


def term_size():
    try:
        t = os.get_terminal_size()
        return max(20, t.columns), max(8, t.lines)
    except OSError:
        return 80, 24


def nap(seconds):
    time.sleep(max(0.0, seconds / SPEED))


def hide_cursor():
    sys.stdout.write("\033[?25l")


def show_cursor():
    sys.stdout.write("\033[?25h")


def clear():
    sys.stdout.write("\033[2J\033[H")


def home():
    sys.stdout.write("\033[H")


def write(s):
    sys.stdout.write(s)
    sys.stdout.flush()


def visible_width(text):
    return len(_ANSI.sub("", text))


def center(text, width, visible_len=None):
    n = visible_len if visible_len is not None else visible_width(text)
    left = max(0, (width - n) // 2)
    right = max(0, width - n - left)
    return " " * left + text + " " * right


def bar(frac, width, fill="█", empty="░"):
    frac = 0.0 if frac < 0 else 1.0 if frac > 1 else frac
    k = round(frac * width)
    return fill * k + empty * (width - k)


def load_art(name):
    """Read an ASCII-art file from ../ (the branding dir) or lumon-assets/ascii."""
    here = os.path.dirname(os.path.abspath(__file__))
    for path in (
        os.path.join(here, "..", name),
        os.path.join(os.path.expanduser("~/lumon-assets/ascii"), name),
    ):
        try:
            with open(path, encoding="utf-8") as fh:
                return fh.read().rstrip("\n").split("\n")
        except OSError:
            continue
    return []


def run(main):
    """Wrap an animation entrypoint with cursor-safe teardown."""
    try:
        if TTY:
            hide_cursor()
        main()
    except KeyboardInterrupt:
        pass
    finally:
        if TTY:
            show_cursor()
        sys.stdout.write(RESET + "\n")
        sys.stdout.flush()
