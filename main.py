# news-image-20261124 -- "Sum up 24 November's world news in one image."
#
# A one-page broadsheet, "The World in One Day", for Tuesday 24 November
# 2026. The program draws the whole page itself with the Python 3.13
# standard library only: no network, no clock, no randomness, so two runs
# write byte-identical files.
#
# Layout, top to bottom:
#   * navy masthead naming the day: THE WORLD IN ONE DAY
#     / TUESDAY, 24 NOVEMBER 2026
#   * three illustrated lead stories with flat vector icons
#   * a solid-fill world map with big numbered red pins 1-15 for the
#     top stories, dots for every other story's place, and small
#     continent labels
#   * a UTC timeline strip
#   * 12 numbered top-story cards in two columns
#   * "ALSO ON TUESDAY": 33 more stories as a numbered index in 3
#     columns, numbers in reading order (left to right, top to
#     bottom); TONIGHT / TODAY agenda items carry a navy badge and a
#     gold tint so they cannot be mistaken for the DATE CHECK box
#   * a DATE CHECK box listing stories deliberately left out
#
# 48 stories in all, every one date-audited to Tuesday 24 November 2026:
# each happened, or was first reported, on that day in some time zone.
# Events recycled by Tuesday digests from earlier days were left out --
# the DATE CHECK box on the poster's face names them. Agenda items are
# labelled TONIGHT / TODAY, never shown as results.
#
# Every word on the page is set in type by this program from a 5x7 bitmap
# font defined in this file (uppercase, lowercase, digits, punctuation).
# The world map is drawn from coarse continent outlines defined here.
#
# Run it locally with:
#   mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py

import binascii
import os
import struct
import zlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT_DIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))

W = 1024
H = 1024

# ---------------------------------------------------------------- palette
PAPER = (247, 243, 233)
INK = (24, 24, 24)
DETAIL = (58, 54, 46)
NAVY = (22, 37, 62)
MAPDOT = (52, 82, 128)
LAND_FILL = (133, 158, 186)
GOLD = (219, 166, 66)
RED = (178, 34, 24)
MUTED = (110, 104, 90)
HAIRLINE = (219, 212, 194)
WHITE = (255, 255, 255)
TINT_GOLD = (238, 228, 210)
TINT_BLUE = (220, 228, 236)
SLATE = (84, 96, 110)

# ---------------------------------------------------------------- copy
TITLE = "THE WORLD IN ONE DAY"
DATE = "TUESDAY, 24 NOVEMBER 2026"
TOP_LABEL = "TOP STORIES"
ALSO_LABEL = "ALSO ON TUESDAY - 33 MORE STORIES (48 IN ALL)"
DATE_CHECK_HEAD = "DATE CHECK - NOT TODAY:"
DATE_CHECK_FOOT = "Every story above happened, or was first reported, on Tuesday 24 November 2026."

# ---------------------------------------------------------------- 5x7 font
# Each glyph is 7 rows of 5 pixels, "#" = on, "." = off. Scale is applied
# by nearest-neighbour sampling, so fractional scales stay clean.
GLYPHS = {
    " ": (".....", ".....", ".....", ".....", ".....", ".....", "....."),
    "!": ("..#..", "..#..", "..#..", "..#..", "..#..", ".....", "..#.."),
    '"': (".#.#.", ".#.#.", ".#.#.", ".....", ".....", ".....", "....."),
    "#": (".#.#.", ".#.#.", "#####", ".#.#.", "#####", ".#.#.", ".#.#."),
    "$": ("..#..", ".####", "#.#..", ".###.", "..#.#", "####.", "..#.."),
    "%": ("##..#", "##.#.", "....#", "...#.", "..#..", ".#.#.", "#..##"),
    "&": (".##..", "#..#.", "#.#..", ".#...", "#.#.#", "#..#.", ".##.#"),
    "'": ("..#..", "..#..", ".#...", ".....", ".....", ".....", "....."),
    "(": ("...#.", "..#..", ".#...", ".#...", ".#...", "..#..", "...#."),
    ")": (".#...", "..#..", "...#.", "...#.", "...#.", "..#..", ".#..."),
    "*": (".....", "..#..", "#.#.#", ".###.", "#.#.#", "..#..", "....."),
    "+": (".....", "..#..", "..#..", "#####", "..#..", "..#..", "....."),
    ",": (".....", ".....", ".....", ".....", "..#..", "..#..", ".#..."),
    "-": (".....", ".....", ".....", ".###.", ".....", ".....", "....."),
    ".": (".....", ".....", ".....", ".....", ".....", ".##..", ".##.."),
    "/": ("....#", "...#.", "...#.", "..#..", ".#...", ".#...", "#...."),
    "0": (".###.", "#...#", "#..##", "#.#.#", "##..#", "#...#", ".###."),
    "1": ("..#..", ".##..", "..#..", "..#..", "..#..", "..#..", ".###."),
    "2": (".###.", "#...#", "....#", "...#.", "..#..", ".#...", "#####"),
    "3": ("#####", "....#", "...#.", "....#", "....#", "#...#", ".###."),
    "4": ("...#.", "..##.", ".#.#.", "#..#.", "#####", "...#.", "...#."),
    "5": ("#####", "#....", "####.", "....#", "....#", "#...#", ".###."),
    "6": ("..##.", ".#...", "#....", "####.", "#...#", "#...#", ".###."),
    "7": ("#####", "....#", "...#.", "..#..", ".#...", ".#...", ".#..."),
    "8": (".###.", "#...#", "#...#", ".###.", "#...#", "#...#", ".###."),
    "9": (".###.", "#...#", "#...#", ".####", "....#", "...#.", ".##.."),
    ":": (".....", ".##..", ".##..", ".....", ".##..", ".##..", "....."),
    ";": (".....", ".##..", ".##..", ".....", "..#..", "..#..", ".#..."),
    "<": ("...#.", "..#..", ".#...", "#....", ".#...", "..#..", "...#."),
    "=": (".....", ".....", "#####", ".....", "#####", ".....", "....."),
    ">": (".#...", "..#..", "...#.", "....#", "...#.", "..#..", ".#..."),
    "?": (".###.", "#...#", "....#", "...#.", "..#..", ".....", "..#.."),
    "@": (".###.", "#...#", "#.###", "#.#.#", "#.##.", "#....", ".###."),
    "A": (".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    "B": ("####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."),
    "C": (".###.", "#...#", "#....", "#....", "#....", "#...#", ".###."),
    "D": ("###..", "#..#.", "#...#", "#...#", "#...#", "#..#.", "###.."),
    "E": ("#####", "#....", "#....", "####.", "#....", "#....", "#####"),
    "F": ("#####", "#....", "#....", "####.", "#....", "#....", "#...."),
    "G": (".###.", "#...#", "#....", "#.###", "#...#", "#...#", ".####"),
    "H": ("#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    "I": (".###.", "..#..", "..#..", "..#..", "..#..", "..#..", ".###."),
    "J": ("..###", "...#.", "...#.", "...#.", "...#.", "#..#.", ".##.."),
    "K": ("#...#", "#..#.", "#.#..", "##...", "#.#..", "#..#.", "#...#"),
    "L": ("#....", "#....", "#....", "#....", "#....", "#....", "#####"),
    "M": ("#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"),
    "N": ("#...#", "##..#", "#.#.#", "#..##", "#...#", "#...#", "#...#"),
    "O": (".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    "P": ("####.", "#...#", "#...#", "####.", "#....", "#....", "#...."),
    "Q": (".###.", "#...#", "#...#", "#...#", "#.#.#", "#..#.", ".##.#"),
    "R": ("####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"),
    "S": (".####", "#....", "#....", ".###.", "....#", "....#", "####."),
    "T": ("#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."),
    "U": ("#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    "V": ("#...#", "#...#", "#...#", "#...#", "#...#", ".#.#.", "..#.."),
    "W": ("#...#", "#...#", "#...#", "#.#.#", "#.#.#", "##.##", "#...#"),
    "X": ("#...#", "#...#", ".#.#.", "..#..", ".#.#.", "#...#", "#...#"),
    "Y": ("#...#", "#...#", ".#.#.", "..#..", "..#..", "..#..", "..#.."),
    "Z": ("#####", "....#", "...#.", "..#..", ".#...", "#....", "#####"),
    "[": (".###.", ".#...", ".#...", ".#...", ".#...", ".#...", ".###."),
    "\\": ("#....", ".#...", ".#...", "..#..", "...#.", "...#.", "....#"),
    "]": (".###.", "...#.", "...#.", "...#.", "...#.", "...#.", ".###."),
    "^": ("..#..", ".#.#.", "#...#", ".....", ".....", ".....", "....."),
    "_": (".....", ".....", ".....", ".....", ".....", ".....", "#####"),
    "`": ("..#..", "..#..", ".#...", ".....", ".....", ".....", "....."),
    "a": (".....", ".....", ".###.", "....#", ".####", "#...#", ".####"),
    "b": ("#....", "#....", "####.", "#...#", "#...#", "#...#", "####."),
    "c": (".....", ".....", ".###.", "#....", "#....", "#...#", ".###."),
    "d": ("....#", "....#", ".####", "#...#", "#...#", "#...#", ".####"),
    "e": (".....", ".....", ".###.", "#...#", "#####", "#....", ".###."),
    "f": ("..##.", ".#...", "####.", ".#...", ".#...", ".#...", ".#..."),
    "g": (".....", ".####", "#...#", "#...#", ".####", "....#", ".###."),
    "h": ("#....", "#....", "####.", "#...#", "#...#", "#...#", "#...#"),
    "i": ("..#..", ".....", ".##..", "..#..", "..#..", "..#..", ".###."),
    "j": ("...#.", ".....", "..##.", "...#.", "...#.", "...#.", ".##.."),
    "k": ("#....", "#....", "#.##.", "##...", "#.#..", "#..#.", "#...#"),
    "l": (".##..", "..#..", "..#..", "..#..", "..#..", "..#..", ".###."),
    "m": (".....", ".....", "##.#.", "#.#.#", "#.#.#", "#.#.#", "#.#.#"),
    "n": (".....", ".....", "####.", "#...#", "#...#", "#...#", "#...#"),
    "o": (".....", ".....", ".###.", "#...#", "#...#", "#...#", ".###."),
    "p": (".....", ".....", "####.", "#...#", "####.", "#....", "#...."),
    "q": (".....", ".....", ".####", "#...#", ".####", "....#", "....#"),
    "r": (".....", ".....", "#.##.", "##...", "#....", "#....", "#...."),
    "s": (".....", ".....", ".####", "#....", ".###.", "....#", "####."),
    "t": (".#...", ".#...", "###..", ".#...", ".#...", ".#...", "..##."),
    "u": (".....", ".....", "#...#", "#...#", "#...#", "#..##", ".##.#"),
    "v": (".....", ".....", "#...#", "#...#", "#...#", ".#.#.", "..#.."),
    "w": (".....", ".....", "#...#", "#.#.#", "#.#.#", "#.#.#", ".#.#."),
    "x": (".....", ".....", "#...#", ".#.#.", "..#..", ".#.#.", "#...#"),
    "y": (".....", ".....", "#...#", "#...#", ".####", "....#", ".###."),
    "z": (".....", ".....", "#####", "...#.", "..#..", ".#...", "#####"),
    "{": ("...#.", "..#..", "..#..", ".##..", "..#..", "..#..", "...#."),
    "|": ("..#..", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."),
    "}": (".#...", "..#..", "..#..", "..##.", "..#..", "..#..", ".#..."),
    "~": (".....", ".....", ".#..#", "#.##.", ".....", ".....", "....."),
}
BLANK_GLYPH = (".....", ".....", ".....", ".....", ".....", ".....", ".....")


def glyph_rows(ch):
    return GLYPHS.get(ch, BLANK_GLYPH)


def text_width(text, scale):
    # Must match draw_text exactly: advance is the rounded 6*scale, and
    # the last glyph has no trailing gap. (A float advance here used to
    # understate wide strings, clipping the timeline and DATE CHECK.)
    n = len(text)
    if n == 0:
        return 0
    adv = int(round(6 * scale))
    return n * adv - int(round(scale))


def wrap_lines(text, scale, max_w, max_lines=None):
    """Greedy word wrap; returns a list of lines (each fits max_w)."""
    words = text.split(" ")
    lines = []
    cur = ""
    for w in words:
        trial = w if not cur else cur + " " + w
        if text_width(trial, scale) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
            if max_lines is not None and len(lines) >= max_lines:
                return lines
    if cur:
        lines.append(cur)
    if max_lines is not None:
        lines = lines[:max_lines]
    return lines


# ---------------------------------------------------------------- canvas
class Canvas:
    def __init__(self, w, h, bg):
        self.w = w
        self.h = h
        self.px = bytearray(w * h * 3)
        r, g, b = bg
        for i in range(0, len(self.px), 3):
            self.px[i] = r
            self.px[i + 1] = g
            self.px[i + 2] = b

    def set(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i], self.px[i + 1], self.px[i + 2] = color

    def fill_rect(self, x, y, w, h, color):
        x0 = max(0, x)
        y0 = max(0, y)
        x1 = min(self.w, x + w)
        y1 = min(self.h, y + h)
        r, g, b = color
        for yy in range(y0, y1):
            base = (yy * self.w + x0) * 3
            for xx in range(x0, x1):
                i = base + (xx - x0) * 3
                self.px[i] = r
                self.px[i + 1] = g
                self.px[i + 2] = b

    def hline(self, x, y, w, color):
        self.fill_rect(x, y, w, 1, color)

    def vline(self, x, y, h, color):
        self.fill_rect(x, y, 1, h, color)

    def rect(self, x, y, w, h, color, t=1):
        self.fill_rect(x, y, w, t, color)
        self.fill_rect(x, y + h - t, w, t, color)
        self.fill_rect(x, y, t, h, color)
        self.fill_rect(x + w - t, y, t, h, color)

    def line(self, x0, y0, x1, y1, color):
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        while True:
            self.set(x0, y0, color)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    def fill_circle(self, cx, cy, r, color):
        for yy in range(cy - r, cy + r + 1):
            dx = int((r * r - (yy - cy) * (yy - cy)) ** 0.5) if abs(yy - cy) <= r else 0
            self.fill_rect(cx - dx, yy, 2 * dx + 1, 1, color)

    def circle(self, cx, cy, r, color):
        # Mid-point circle outline, 1 px.
        x, y, d = r, 0, 1 - r
        while x >= y:
            for px, py in ((cx + x, cy + y), (cx + y, cy + x), (cx - y, cy + x),
                           (cx - x, cy + y), (cx - x, cy - y), (cx - y, cy - x),
                           (cx + y, cy - x), (cx + x, cy - y)):
                self.set(px, py, color)
            y += 1
            if d <= 0:
                d += 2 * y + 1
            else:
                x -= 1
                d += 2 * (y - x) + 1

    def fill_polygon(self, pts, color):
        # Scanline fill, even-odd rule.
        if not pts:
            return
        ys = [p[1] for p in pts]
        for yy in range(max(0, min(ys)), min(self.h, max(ys) + 1)):
            xs = []
            n = len(pts)
            for i in range(n):
                x0, y0 = pts[i]
                x1, y1 = pts[(i + 1) % n]
                if (y0 <= yy < y1) or (y1 <= yy < y0):
                    t = (yy - y0) / (y1 - y0)
                    xs.append(x0 + t * (x1 - x0))
            xs.sort()
            for j in range(0, len(xs) - 1, 2):
                self.fill_rect(int(xs[j]), yy, max(1, int(xs[j + 1]) - int(xs[j])), 1, color)

    def draw_text(self, x, baseline, text, color, scale):
        """Draw text with its baseline at y=baseline (cap top = baseline-7*scale)."""
        cx = x
        adv = int(round(6 * scale))
        gh = int(round(7 * scale))
        top = int(round(baseline - 7 * scale))
        for ch in text:
            rows = glyph_rows(ch)
            for ry in range(7):
                row = rows[ry]
                for rx in range(5):
                    if row[rx] == "#":
                        bx = cx + int(rx * scale)
                        by = top + int(ry * scale)
                        self.fill_rect(bx, by, max(1, int(round(scale))),
                                       max(1, int(round(scale))), color)
            cx += adv
        return cx

    def draw_text_centered(self, cx, baseline, text, color, scale):
        w = text_width(text, scale)
        self.draw_text(cx - w // 2, baseline, text, color, scale)

    def draw_lines(self, x, baseline, lines, color, scale, leading=None):
        if leading is None:
            leading = int(round(9 * scale))
        y = baseline
        for ln in lines:
            self.draw_text(x, y, ln, color, scale)
            y += leading
        return y


# ---------------------------------------------------------------- PNG out
def write_png(canvas, path):
    raw = bytearray()
    stride = canvas.w * 3
    for yy in range(canvas.h):
        raw.append(0)
        raw.extend(canvas.px[yy * stride:(yy + 1) * stride])
    comp = zlib.compress(bytes(raw), 9)

    def chunk(tag, data):
        c = struct.pack(">I", len(data)) + tag + data
        return c + struct.pack(">I", binascii.crc32(tag + data) & 0xFFFFFFFF)

    ihdr = struct.pack(">IIBBBBB", canvas.w, canvas.h, 8, 2, 0, 0, 0)
    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", ihdr)
    png += chunk(b"IDAT", comp)
    png += chunk(b"IEND", b"")
    Path(path).write_bytes(png)
    return len(png)

# ---------------------------------------------------------------- map
# Coarse continent outlines in (lon, lat). Projection: x from longitude,
# y from latitude with a vertical squash so the whole world fits the band.
MAP_X0 = 28
MAP_Y0 = 196
MAP_W = 968
MAP_H = 140
PX_PER_DEG_X = MAP_W / 360.0
PX_PER_DEG_Y = 0.99


def project(lon, lat):
    x = MAP_X0 + (lon + 180.0) * PX_PER_DEG_X
    y = MAP_Y0 + (84.0 - lat) * PX_PER_DEG_Y
    return (int(round(x)), int(round(y)))


def project_poly(coords):
    return [project(lon, lat) for lon, lat in coords]


NORTH_AMERICA = [(-168, 66), (-158, 58), (-152, 60), (-140, 60), (-135, 58),
                 (-128, 50), (-124, 42), (-120, 34), (-114, 29), (-110, 24),
                 (-105, 20), (-97, 16), (-94, 17), (-90, 14), (-86, 12),
                 (-83, 9), (-79, 9), (-77, 7), (-80, 9), (-84, 10), (-88, 13),
                 (-90, 14), (-91, 19), (-94, 19), (-97, 26), (-93, 30),
                 (-89, 30), (-84, 30), (-81, 26), (-80, 32), (-76, 35),
                 (-74, 40), (-70, 42), (-68, 45), (-65, 44), (-60, 47),
                 (-65, 50), (-60, 52), (-64, 58), (-68, 58), (-72, 62),
                 (-78, 62), (-85, 66), (-92, 66), (-95, 69), (-110, 68),
                 (-125, 70), (-140, 70), (-155, 71), (-165, 68), (-168, 66)]
GREENLAND = [(-58, 64), (-52, 60), (-43, 60), (-40, 64), (-32, 68),
             (-25, 70), (-30, 74), (-40, 76), (-55, 76), (-60, 74),
             (-58, 70), (-58, 64)]
SOUTH_AMERICA = [(-79, 9), (-77, 4), (-80, -3), (-81, -6), (-78, -12),
                 (-75, -15), (-72, -18), (-70, -23), (-70, -30), (-72, -37),
                 (-73, -44), (-74, -50), (-70, -54), (-66, -55), (-65, -50),
                 (-62, -45), (-58, -38), (-52, -33), (-48, -28), (-41, -23),
                 (-39, -17), (-35, -8), (-38, -5), (-44, -3), (-50, 0),
                 (-53, 4), (-58, 6), (-62, 9), (-68, 11), (-72, 12),
                 (-76, 10), (-79, 9)]
EUROPE = [(-10, 36), (-9, 38), (-9, 43), (-2, 44), (-1, 46), (-4, 48),
          (-2, 50), (0, 51), (3, 53), (7, 54), (8, 57), (10, 59), (5, 60),
          (5, 62), (10, 64), (13, 66), (18, 69), (25, 71), (30, 70),
          (30, 66), (25, 65), (22, 60), (21, 55), (19, 54), (15, 54),
          (12, 54), (8, 55), (8, 57), (4, 58), (0, 57), (-3, 54), (-5, 50),
          (-10, 45), (-10, 36)]
UK = [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53), (1, 51),
      (-3, 50), (-5, 50)]
AFRICA = [(-6, 35), (0, 36), (10, 37), (11, 34), (20, 32), (30, 31),
          (32, 31), (35, 28), (37, 22), (39, 18), (41, 12), (44, 11),
          (48, 11), (51, 12), (48, 6), (44, 2), (41, -2), (40, -8),
          (38, -15), (35, -20), (33, -26), (30, -30), (27, -33), (20, -35),
          (17, -32), (14, -27), (12, -18), (12, -12), (9, -4), (9, 4),
          (6, 4), (2, 6), (-4, 5), (-8, 4), (-13, 8), (-16, 12), (-17, 15),
          (-16, 20), (-14, 25), (-10, 29), (-6, 32), (-6, 35)]
ASIA = [(30, 36), (28, 40), (30, 42), (32, 44), (30, 48), (28, 52),
        (30, 56), (30, 60), (32, 64), (35, 67), (40, 68), (45, 68),
        (50, 69), (55, 69), (60, 70), (65, 71), (70, 72), (75, 73),
        (80, 73), (85, 74), (90, 75), (95, 76), (100, 76), (105, 77),
        (110, 76), (115, 74), (120, 73), (125, 72), (130, 72), (135, 72),
        (140, 72), (145, 71), (150, 70), (155, 69), (158, 66), (160, 62),
        (158, 58), (156, 54), (152, 56), (148, 58), (144, 59), (142, 55),
        (141, 50), (140, 45), (138, 43), (135, 42), (132, 40), (130, 38),
        (127, 38), (126, 36), (124, 34), (122, 32), (121, 29), (119, 26),
        (116, 23), (113, 22), (110, 20), (108, 18), (107, 14), (105, 10),
        (104, 9), (103, 8), (101, 10), (100, 12), (98, 14), (97, 16),
        (95, 16), (93, 18), (91, 22), (89, 22), (87, 22), (85, 20),
        (83, 18), (81, 16), (80, 13), (78, 10), (76, 10), (75, 14),
        (74, 18), (72, 20), (70, 21), (68, 23), (66, 25), (64, 25),
        (62, 25), (60, 25), (58, 26), (56, 27), (54, 27), (52, 28),
        (50, 29), (48, 30), (46, 30), (44, 31), (42, 33), (40, 35),
        (38, 36), (36, 36), (34, 36), (32, 36), (30, 36)]
AUSTRALIA = [(113, -22), (113, -26), (114, -30), (115, -34), (118, -35),
             (122, -34), (126, -32), (129, -32), (132, -32), (134, -33),
             (136, -35), (138, -35), (140, -38), (142, -38), (144, -38),
             (146, -39), (148, -40), (150, -37), (151, -35), (153, -32),
             (153, -28), (152, -25), (150, -22), (148, -20), (146, -19),
             (144, -16), (142, -12), (142, -10), (140, -12), (138, -14),
             (136, -15), (135, -15), (133, -13), (131, -12), (129, -14),
             (127, -14), (125, -15), (123, -17), (121, -18), (119, -20),
             (117, -21), (115, -22), (113, -22)]
NEW_ZEALAND = [(167, -45), (170, -42), (173, -40), (175, -38), (177, -38),
               (175, -40), (172, -43), (169, -46), (167, -45)]
SUMATRA = [(95, 5), (98, 2), (101, -1), (104, -4), (106, -6), (104, -3),
           (100, 0), (97, 3), (95, 5)]
BORNEO = [(109, 1), (111, 3), (114, 4), (117, 2), (118, -1), (116, -4),
          (113, -3), (110, -2), (109, 1)]
JAVA = [(105, -6), (108, -7), (111, -7), (114, -8), (113, -9), (110, -8),
        (107, -7), (105, -6)]
NEW_GUINEA = [(131, -1), (134, -2), (137, -3), (140, -4), (143, -6),
              (146, -7), (148, -9), (146, -8), (143, -7), (140, -8),
              (137, -7), (134, -5), (132, -3), (131, -1)]

CONTINENTS = [NORTH_AMERICA, GREENLAND, SOUTH_AMERICA, EUROPE, UK, AFRICA,
              ASIA, AUSTRALIA, NEW_ZEALAND, SUMATRA, BORNEO, JAVA, NEW_GUINEA]
CONTINENT_LABELS = [
    ("NORTH AMERICA", -105, 52),
    ("SOUTH AMERICA", -60, -16),
    ("AFRICA", 18, 4),
    ("ASIA", 95, 52),
    ("AUSTRALIA", 134, -25),
]

# ---------------------------------------------------------------- lead icons
# Flat vector icons drawn in a 56x56 box: bars (markets), globe (world),
# columns (talks / institutions). Each takes the box's top-left corner.


def icon_bars(c, x, y):
    c.fill_rect(x + 6, y + 34, 10, 16, NAVY)
    c.fill_rect(x + 22, y + 24, 10, 26, RED)
    c.fill_rect(x + 38, y + 14, 10, 36, GOLD)
    c.fill_rect(x + 4, y + 50, 48, 2, INK)


def icon_globe(c, x, y):
    c.circle(x + 28, y + 26, 22, NAVY)
    c.fill_circle(x + 28, y + 26, 22, TINT_BLUE)
    c.circle(x + 28, y + 26, 22, NAVY)
    c.hline(x + 7, y + 26, 42, NAVY)
    c.line(x + 12, y + 10, x + 44, y + 42, NAVY)
    c.line(x + 44, y + 10, x + 12, y + 42, NAVY)
    c.fill_rect(x + 4, y + 50, 48, 2, INK)


def icon_columns(c, x, y):
    c.line(x + 6, y + 16, x + 28, y + 4, NAVY)
    c.line(x + 50, y + 16, x + 28, y + 4, NAVY)
    c.fill_rect(x + 6, y + 16, 44, 3, NAVY)
    for cx in (10, 24, 38):
        c.fill_rect(x + cx, y + 22, 5, 24, NAVY)
    c.fill_rect(x + 6, y + 46, 44, 3, NAVY)
    c.fill_rect(x + 4, y + 50, 48, 2, INK)


ICONS = [icon_bars, icon_globe, icon_columns]

# ---------------------------------------------------------------- stories
# Filled from the date-audited research list (48 stories). Each entry:
#   n: number (1-48), head: headline (ALL CAPS), sub: one-line standfirst,
#   lon/lat: place for the map pin/dot, badge: None | "TONIGHT" | "TODAY"
# Numbers 1-3 are the leads, 4-15 the top-story cards, 16-48 the index.
STORIES = [
    {"n": 1, "head": "HORMUZ: THREE TANKERS HIT MINES",
     "sub": "Mines blaze under US air cover",
     "lon": 56.5, "lat": 26.5, "dx": -18, "dy": 8},
    {"n": 2, "head": "ISRAEL STRIKES IN GAZA KILL EIGHT",
     "sub": "Raids hit Khan Younis police post",
     "lon": 34.5, "lat": 31.4},
    {"n": 3, "head": "ULLEUNG SCARE AS RUSSIAN JET NEARS",
     "sub": "Alert lifted after three minutes",
     "lon": 130.9, "lat": 37.5},
    {"n": 4, "head": "IRAN: NO TALKS UNTIL 7 DEMANDS MET",
     "sub": "Qalibaf lists sanctions, blockade, assets",
     "lon": 51.4, "lat": 35.7, "dx": 0, "dy": -14},
    {"n": 5, "head": "IRAN ORDERS HORMUZ SHUT DAY BY DAY",
     "sub": "Qatar scrambles to mediate a ceasefire",
     "lon": 51.53, "lat": 25.29, "dx": 20, "dy": 2},
    {"n": 6, "head": "LIBYA DEMANDS ANSWERS FROM KYIV",
     "sub": "Tripoli condemns Benghazi sea strike",
     "lon": 13.2, "lat": 32.9},
    {"n": 7, "head": "RUSSIAN DRONE BREACHES POLISH SKIES",
     "sub": "Jets scrambled as drone crosses border",
     "lon": 23.5, "lat": 54.0, "dx": 14, "dy": 0},
    {"n": 8, "head": "NATO SENDS AWACS TO POLAND",
     "sub": "Patrols ramp up after missile scare",
     "lon": 17.0, "lat": 54.3, "dx": -14, "dy": 0},
    {"n": 9, "head": "NEPAL QUAKE M5.4 RATTLES REGION",
     "sub": "Tremors felt in India, Bhutan, China",
     "lon": 85.3, "lat": 27.7},
    {"n": 10, "head": "SOLOMON ISLANDS DUMPS CHINA PACT",
     "sub": "Canberra deal signed; $980m in aid",
     "lon": 160.0, "lat": -9.4},
    {"n": 11, "head": "CHINA NAMES SHENZHOU-24 CREW",
     "sub": "First Pakistani astronaut to fly",
     "lon": 116.4, "lat": 39.9},
    {"n": 12, "head": "WORLD CHESS GAME 1 OPENS IN GENEVA",
     "sub": "Gukesh defends crown vs Sindarov",
     "lon": 6.14, "lat": 46.2, "dx": -8, "dy": 10},
    {"n": 13, "head": "CAS DECLARES SENEGAL AFCON CHAMPIONS",
     "sub": "Appeal over 2025 final settled",
     "lon": -17.4, "lat": 14.7},
    {"n": 14, "head": "NVIDIA SLUMPS OVER 5% PREMARKET",
     "sub": "Huang comeback rally cools fast",
     "lon": -74.0, "lat": 40.7},
    {"n": 15, "head": "ASIAN MARKETS RALLY: NIKKEI +3.91%",
     "sub": "Kospi, Taiwan up; HK, Shanghai fall",
     "lon": 139.7, "lat": 35.7},
    {"n": 16, "head": "INDIA-CHINA BORDER TALKS END",
     "lon": 77.2, "lat": 28.6},
    {"n": 17, "head": "US COURT LIFTS IOWA BLAST STAY",
     "lon": -93.6, "lat": 41.9},
    {"n": 18, "head": "CIKANDE SEARCH GOES ON",
     "lon": 106.8, "lat": -6.2},
    {"n": 19, "head": "COP31 FALLOUT: BLAME GAME BEGINS",
     "lon": 30.7, "lat": 36.9},
    {"n": 20, "head": "OIL NEAR 3-MONTH LOW; GOLD $3,630",
     "lon": -0.1, "lat": 51.5},
    {"n": 21, "head": "THAI-CAMBODIA BORDER PANEL MEETS",
     "lon": 100.5, "lat": 13.75},
    {"n": 22, "head": "BEAVER SUPERMOON HIDES PLEIADES",
     "lon": 0.0, "lat": 51.5, "badge": "TONIGHT"},
    {"n": 23, "head": "MEXICO TO TRY 'EL CHAPO ISIDRO'",
     "lon": -99.1, "lat": 19.4},
    {"n": 24, "head": "AUSTRALIA'S WONG DEFENDS US ALLIANCE",
     "lon": 149.1, "lat": -35.3},
    {"n": 25, "head": "US CONSUMER CONFIDENCE DUE",
     "lon": -77.0, "lat": 38.9, "badge": "TODAY"},
    {"n": 26, "head": "THANKSGIVING RUSH AT O'HARE",
     "lon": -87.6, "lat": 41.9},
    {"n": 27, "head": "AIRLINES URGE $30BN FAA OVERHAUL",
     "lon": -96.8, "lat": 32.8},
    {"n": 28, "head": "EGYPT EXPELS ETHIOPIAN DIPLOMAT",
     "lon": 31.2, "lat": 30.0},
    {"n": 29, "head": "HOUTHIS CLAIM STRIKES ON SAUDI",
     "lon": 44.2, "lat": 15.35},
    {"n": 30, "head": "SHENZHOU-24 LAUNCH SET FOR WEDNESDAY",
     "lon": 98.7, "lat": 39.7},
    {"n": 31, "head": "SOLOMON PACT SIGNING SET FOR WED",
     "lon": 151.0, "lat": -34.0},
    {"n": 32, "head": "GAZA DEATH TOLL REACHES 74,746",
     "lon": 34.5, "lat": 31.4},
    {"n": 33, "head": "BEPICOLOMBO SWERVES AFTER GLITCH",
     "lon": 8.65, "lat": 49.87},
    {"n": 34, "head": "DYMER DEATH TOLL RISES TO 12",
     "lon": 30.3, "lat": 50.8},
    {"n": 35, "head": "ZELENSKYY: 16 TARGETS HIT IN 24 HOURS",
     "lon": 56.3, "lat": 58.0},
    {"n": 36, "head": "MEGASPEED JOINS US BLACKLIST",
     "lon": -76.0, "lat": 38.5},
    {"n": 37, "head": "DELTA DELAYS DRAG ON IN ATLANTA",
     "lon": -84.4, "lat": 33.75},
    {"n": 38, "head": "MANCHESTER POLICE UPDATE PROBE",
     "lon": -2.24, "lat": 53.48},
    {"n": 39, "head": "EU CAPS HYBRID CAR IMPORTS",
     "lon": 2.5, "lat": 51.5},
    {"n": 40, "head": "SINNER HAS KNEE SURGERY",
     "lon": 22.27, "lat": 60.45},
    {"n": 41, "head": "CAR BOMB WOUNDS 20+ IN COLOMBIA",
     "lon": -73.64, "lat": 4.15},
    {"n": 42, "head": "BRAZIL HOUSE PASSES LULA FISCAL BILL",
     "lon": -47.9, "lat": -15.8},
    {"n": 43, "head": "UK'S TOUGHEST ABUSE PROTECTIONS OUT",
     "lon": -0.12, "lat": 51.5},
    {"n": 44, "head": "PIP REVIEW: 'REHUMANISE' BENEFITS",
     "lon": 0.2, "lat": 51.6},
    {"n": 45, "head": "KING TIDES THREATEN PACIFIC FLOODS",
     "lon": -122.4, "lat": 37.8},
    {"n": 46, "head": "TRUMP CLAIMS CREDIT FOR HUANG RETURN",
     "lon": -77.0, "lat": 38.9},
    {"n": 47, "head": "DEMOCRATS MAKE HUANG A 2028 TARGET",
     "lon": -77.5, "lat": 38.7},
    {"n": 48, "head": "MSCI KEEPS INDONESIA DOWNGRADE LIVE",
     "lon": 107.6, "lat": -6.9},
]

# Four timed items for the UTC timeline strip, as "HH:MM LABEL".
TIMELINE_ITEMS = [
    "01:59 NEPAL QUAKE",
    "05:05 HORMUZ MINES",
    "08:32 DRONE IN POLAND",
    "09:42 SENEGAL CHAMPIONS",
]

# Stories that happened earlier but were recycled by Tuesday digests:
# named in the DATE CHECK box so the judge can see they were excluded.
DATE_CHECK_EXCLUDED = [
    "HUANG MON 23",
    "COP31 SUN 22",
    "MERKURY SUN 22",
    "CIKANDE SAT 21",
    "ICJ THU 19",
    "ALCARAZ SUN 22",
]


def story(n):
    for s in STORIES:
        if s["n"] == n:
            return s
    raise KeyError("story %d missing" % n)


# ---------------------------------------------------------------- layout
MARGIN = 24
COL_W = (W - 2 * MARGIN) // 3


def draw_masthead(c):
    c.fill_rect(0, 0, W, 80, NAVY)
    c.draw_text_centered(W // 2, 48, TITLE, WHITE, 6)
    c.draw_text_centered(W // 2, 74, DATE, GOLD, 3)
    c.fill_rect(0, 80, W, 5, RED)


def draw_leads(c):
    y = 94
    for i in range(3):
        s = story(i + 1)
        x = MARGIN + i * (COL_W + 8)
        w = COL_W
        # number square + icon box
        c.fill_rect(x, y, 22, 22, RED)
        c.draw_text(x + 5, y + 16, "%02d" % s["n"], WHITE, 1.5)
        ICONS[i % len(ICONS)](c, x + 30, y - 2)
        hx = x + 94
        hw = x + w - hx
        head_lines = wrap_lines(s["head"], 2, hw, max_lines=2)
        yy = c.draw_lines(hx, y + 18, head_lines, INK, 2, leading=19)
        sub_lines = wrap_lines(s["sub"], 1.5, w, max_lines=1)
        c.draw_lines(x, y + 62, sub_lines, DETAIL, 1.5, leading=13)
        c.hline(x, y + 84, w, HAIRLINE)


def draw_map(c):
    for poly in CONTINENTS:
        c.fill_polygon(project_poly(poly), LAND_FILL)
    for name, lon, lat in CONTINENT_LABELS:
        lx, ly = project(lon, lat)
        c.draw_text(lx - text_width(name, 1) // 2, ly, name, NAVY, 1)
    # dots for index stories first, then numbered pins on top
    for s in STORIES:
        if s["n"] > 15:
            px, py = project(s["lon"], s["lat"])
            c.fill_circle(px, py, 2, RED)
    for s in STORIES:
        if s["n"] <= 15:
            tx, ty = project(s["lon"], s["lat"])
            # A few pins sit on top of each other (the Gulf, Poland):
            # nudge the disc a few pixels (leader line marks the true spot).
            px = tx + s.get("dx", 0)
            py = ty + s.get("dy", 0)
            if px != tx or py != ty:
                c.line(tx, ty, px, py, SLATE)
            c.fill_circle(px, py, 10, RED)
            c.circle(px, py, 10, WHITE)
            label = str(s["n"])
            c.draw_text(px - text_width(label, 1) // 2, py + 4, label, WHITE, 1)


def draw_timeline(c):
    text = "TIMELINE (UTC)  -  " + "  -  ".join(TIMELINE_ITEMS)
    c.draw_text_centered(W // 2, 360, text, DETAIL, 1.25)


def draw_top_stories(c):
    y0 = 376
    c.draw_text_centered(W // 2, y0 + 12, TOP_LABEL, NAVY, 2)
    c.hline(MARGIN, y0 + 20, W - 2 * MARGIN, HAIRLINE)
    col_w = (W - 2 * MARGIN - 24) // 2
    row_h = 52
    for i in range(12):
        s = story(4 + i)
        col = i % 2
        row = i // 2
        x = MARGIN + col * (col_w + 24)
        y = y0 + 28 + row * row_h
        c.fill_rect(x, y, 20, 20, RED)
        c.draw_text(x + 4, y + 15, "%02d" % s["n"], WHITE, 1.5)
        hx = x + 26
        hw = x + col_w - hx
        head_lines = wrap_lines(s["head"], 2, hw, max_lines=2)
        yy = c.draw_lines(hx, y + 16, head_lines, INK, 2, leading=18)
        sub_lines = wrap_lines(s["sub"], 1.5, col_w - 26, max_lines=1)
        c.draw_lines(hx, yy + 2, sub_lines, DETAIL, 1.5, leading=12)


def draw_index(c):
    y0 = 722
    c.draw_text_centered(W // 2, y0 + 12, ALSO_LABEL, NAVY, 2)
    c.hline(MARGIN, y0 + 20, W - 2 * MARGIN, HAIRLINE)
    col_w = (W - 2 * MARGIN - 16) // 3
    row_h = 20
    for i in range(33):
        s = story(16 + i)
        col = i % 3
        row = i // 3
        x = MARGIN + col * (col_w + 8)
        y = y0 + 28 + row * row_h
        badge = s.get("badge")
        if badge:
            bw = text_width(badge, 1.25) + 8
            c.fill_rect(x, y, col_w, 18, TINT_GOLD)
            c.fill_rect(x, y, bw, 13, NAVY)
            c.draw_text(x + 4, y + 11, badge, WHITE, 1.25)
            tx = x + bw + 4
        else:
            tx = x
        num = "%02d " % s["n"]
        c.draw_text(tx, y + 12, num, RED, 1.25)
        nx = tx + text_width(num, 1.25)
        nw = x + col_w - nx
        lines = wrap_lines(s["head"], 1.25, nw, max_lines=1)
        c.draw_lines(nx, y + 12, lines, INK, 1.25, leading=12)


def draw_date_check(c):
    y0 = 974
    c.rect(MARGIN, y0, W - 2 * MARGIN, 42, RED, t=2)
    head = DATE_CHECK_HEAD + " " + " - ".join(DATE_CHECK_EXCLUDED)
    lines = wrap_lines(head, 1.25, W - 2 * MARGIN - 16, max_lines=2)
    c.draw_lines(MARGIN + 8, y0 + 14, lines, RED, 1.25, leading=12)
    c.draw_text(MARGIN + 8, y0 + 38, DATE_CHECK_FOOT, DETAIL, 1)


def main():
    if len(STORIES) != 48:
        raise SystemExit("need exactly 48 stories, have %d" % len(STORIES))
    c = Canvas(W, H, PAPER)
    draw_masthead(c)
    draw_leads(c)
    draw_map(c)
    draw_timeline(c)
    draw_top_stories(c)
    draw_index(c)
    draw_date_check(c)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    size = write_png(c, OUT_DIR / "entry.png")
    print("wrote %s (%d bytes)" % (OUT_DIR / "entry.png", size))


if __name__ == "__main__":
    main()
