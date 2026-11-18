#!/usr/bin/env python3
"""Poster variant: a drawn scene of the day's lead story with the three top stories under it."""
import math
import os
import random
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W = H = 1024
F = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = F + "DejaVuSerif-Bold.ttf"
SERIF = F + "DejaVuSerif.ttf"
SANS_B = F + "DejaVuSans-Bold.ttf"
SANS = F + "DejaVuSans.ttf"
MONO = F + "DejaVuSansMono.ttf"

INK = (12, 14, 20)
CREAM = (246, 242, 233)
ACCENT = (214, 62, 38)


def fnt(p, s):
    return ImageFont.truetype(p, s)


def sky(d, top, bottom, height=700):
    for y in range(height):
        t = y / max(1, height - 1)
        # horizon glow near 55% height
        glow = math.exp(-((t - 0.52) ** 2) / 0.010)
        r = int(top[0] * (1 - t) + bottom[0] * t + 120 * glow)
        g = int(top[1] * (1 - t) + bottom[1] * t + 46 * glow)
        b = int(top[2] * (1 - t) + bottom[2] * t + 10 * glow)
        d.line([(0, y), (W, y)], fill=(min(255, r), min(255, g), min(255, b)))


def water(d, y0):
    for y in range(y0, H):
        t = (y - y0) / max(1, H - y0)
        r = int(46 * (1 - t) + 8 * t)
        g = int(24 * (1 - t) + 10 * t)
        b = int(28 * (1 - t) + 16 * t)
        d.line([(0, y), (W, y)], fill=(r, g, b))


def cables(d, x0, x1, deck_y, tower_top, color):
    towers = [x0 + (x1 - x0) * f for f in (0.22, 0.78)]
    for tx in towers:
        d.line([(tx, tower_top), (tx, deck_y + 30)], fill=color, width=7)
        d.line([(tx - 16, tower_top + 10), (tx + 16, tower_top + 10)], fill=color, width=5)
    # main cables and hangers
    for tx in towers:
        for side, end in ((0, x0), (1, x1)):
            steps = 9
            for i in range(1, steps + 1):
                f = i / steps
                cx = tx + (end - tx) * f
                cy = tower_top + 14 + (deck_y + 6 - tower_top - 14) * (f ** 1.7)
                d.line([(tx, tower_top + 12), (cx, cy)], fill=color, width=2)
    d.line([(x0, deck_y), (x1, deck_y)], fill=color, width=12)
    d.line([(x0, deck_y + 22), (x1, deck_y + 22)], fill=color, width=4)


def smoke(d, x, y, scale, seed):
    rnd = random.Random(seed)
    for i in range(26):
        t = i / 26
        cx = x + rnd.uniform(-40, 40) * scale + 90 * t * scale
        cy = y - 210 * t * scale + rnd.uniform(-14, 14)
        r = (26 + 54 * t) * scale * rnd.uniform(0.75, 1.15)
        shade = int(70 + 60 * t)
        d.ellipse([cx - r, cy - r, cx + r, cy + r],
                  fill=(shade, shade - 4, shade - 6))


def drones(d, pts, color=(255, 190, 140)):
    for (x, y, s) in pts:
        d.polygon([(x, y - 5 * s), (x + 9 * s, y + 4 * s), (x - 9 * s, y + 4 * s)], fill=color)
        d.line([(x - 10 * s, y + 4 * s), (x + 10 * s, y + 4 * s)], fill=color, width=max(1, int(s)))
        d.line([(x, y - 5 * s), (x - 40 * s, y - 22 * s)], fill=(255, 120, 70), width=1)


def main(out):
    img = Image.new("RGB", (W, H), INK)
    d = ImageDraw.Draw(img)
    sky(d, (10, 12, 26), (54, 26, 22))
    water(d, 700)
    # distant city silhouette
    rnd = random.Random(7)
    x = -20
    while x < W + 40:
        bw = rnd.randint(26, 74)
        bh = rnd.randint(30, 120)
        d.rectangle([x, 700 - bh, x + bw, 700], fill=(18, 16, 22))
        for wy in range(700 - bh + 12, 690, 16):
            for wx in range(x + 6, x + bw - 6, 12):
                if rnd.random() < 0.28:
                    d.point((wx, wy), fill=(220, 170, 90))
        x += bw + rnd.randint(6, 18)
    # fire glow behind the bridge
    glow = Image.new("RGB", (W, H), (0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([300, 470, 760, 700], fill=(150, 60, 20))
    glow = glow.filter(ImageFilter.GaussianBlur(70))
    img = Image.blend(img, Image.blend(img, glow, 0.55), 0.55)
    d = ImageDraw.Draw(img)
    # bridge + smoke + drones
    cables(d, 60, 964, 620, 330, (14, 12, 16))
    smoke(d, 470, 600, 1.25, 3)
    smoke(d, 610, 612, 0.85, 11)
    drones(d, [(180, 300, 1.5), (330, 240, 1.2), (700, 270, 1.4), (830, 340, 1.1)])
    # dark scrim at the bottom for the text band
    band = Image.new("RGBA", (W, 420), (8, 8, 12, 238))
    img.paste(Image.alpha_composite(img.crop((0, 604, W, H)).convert("RGBA"), band).convert("RGB"), (0, 604))
    d = ImageDraw.Draw(img)

    # top label
    d.text((44, 40), "THE WORLD IN ONE DAY", font=fnt(SERIF_B, 30), fill=CREAM)
    d.text((44, 82), "TUESDAY, 17 NOVEMBER 2026", font=fnt(SANS_B, 15), fill=(230, 200, 180))
    d.rectangle([44, 108, 240, 112], fill=ACCENT)

    # headline over the image
    d.text((44, 420), "Ukraine strikes", font=fnt(SERIF_B, 64), fill=CREAM)
    d.text((44, 492), "the Kerch Bridge", font=fnt(SERIF_B, 64), fill=CREAM)
    d.text((46, 572), "Zelenskyy calls it \u201cunprecedented\u201d  \u00b7  a record number of drones downed",
           font=fnt(SANS, 17), fill=(240, 214, 196))

    # bottom: three leads, a numbers strip, and four briefs
    y = 620
    d.rectangle([44, y, 168, y + 4], fill=ACCENT)
    y += 16
    d.text((44, y), "ALSO TODAY", font=fnt(SANS_B, 12), fill=(232, 120, 96))
    y += 20
    leads = [("IRAN \u00b7 BAHRAIN", "Third drone attack on a US radar site; Washington fires back"),
             ("ASIA", "Trump in Manila, then Shenzhen for talks with Xi and Putin"),
             ("MARKETS", "S&P 500 \u22121.1%  \u00b7  Dow \u2212779  \u00b7  Nasdaq \u22121.5%")]
    for label, line in leads:
        d.text((44, y), label, font=fnt(SANS_B, 11), fill=(210, 132, 108))
        d.text((168, y - 2), line, font=fnt(SERIF, 15), fill=CREAM)
        y += 30
    y += 6
    d.rectangle([44, y, W - 44, y + 1], fill=(70, 62, 58))
    y += 12
    nums = [("11,000+", "Ebola cases, DR Congo"), ("7th", "day of strikes on Bahrain"),
            ("$200m", "pledged at COP31"), ("3rd", "US measles-free status lost")]
    cw = (W - 88) // 4
    for i, (num, cap) in enumerate(nums):
        cx = 44 + i * cw
        d.text((cx, y), num, font=fnt(SERIF_B, 22), fill=(226, 96, 68))
        d.text((cx, y + 30), cap, font=fnt(SANS, 11), fill=(198, 188, 178))
    y += 62
    briefs = [("Measles-free status lost", "The US, Mexico and Bolivia lose elimination status."),
              ("Ebola doubles in DR Congo", "11,000 cases and 5,400 deaths, the WHO says."),
              ("COP31 presses on in Antalya", "Four nations pledge $200m as tipping points near."),
              ("A hub in Rwanda", "Five European countries plan a return hub next year.")]
    col_w = (W - 88 - 24) // 2
    for i, (head, body) in enumerate(briefs):
        cx = 44 + (i % 2) * (col_w + 24)
        cy = y + (i // 2) * 56
        d.text((cx, cy), head, font=fnt(SANS_B, 12), fill=(232, 120, 96))
        para = body
        d.text((cx, cy + 16), para, font=fnt(SERIF, 11), fill=(198, 190, 182))
    d.text((44, 982), "ONE DAY \u00b7 ONE PAGE", font=fnt(MONO, 11), fill=(150, 140, 132))

    img.save(out, "PNG", optimize=True)
    return out


if __name__ == "__main__":
    import sys
    o = sys.argv[1] if len(sys.argv) > 1 else "poster.png"
    print(main(o), os.path.getsize(o), "bytes")
