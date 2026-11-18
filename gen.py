#!/usr/bin/env python3
"""Render a one-page newspaper front page for the world news of Tuesday 17 November 2026."""
import os
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (246, 242, 233)
INK = (18, 18, 18)
ACCENT = (163, 30, 24)
MUTED = (92, 88, 82)
HAIR = (160, 154, 144)

F = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = F + "DejaVuSerif-Bold.ttf"
SERIF_I = F + "DejaVuSerif.ttf"
SERIF = F + "DejaVuSerif.ttf"
SANS_B = F + "DejaVuSans-Bold.ttf"
SANS = F + "DejaVuSans.ttf"
MONO = F + "DejaVuSansMono.ttf"
M = 44


def fnt(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, f, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=f) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(d, xy, text, f, width, fill=INK, leading=1.24, max_lines=None):
    x, y = xy
    lines = wrap(d, text, f, width)
    if max_lines:
        lines = lines[:max_lines]
    lh = int(f.size * leading)
    for ln in lines:
        d.text((x, y), ln, font=f, fill=fill)
        y += lh
    return y


def rule(d, y, x0=M, x1=W - M, width=2, color=INK):
    d.rectangle([x0, y, x1, y + width - 1], fill=color)


def label(d, xy, text, color=ACCENT, size=14):
    x, y = xy
    d.text((x, y), " ".join(text.upper()), font=fnt(SANS_B, size), fill=color)
    return y + int(size * 1.55)


def main(out_path):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---------------- masthead ----------------
    y = 24
    d.text((M, y), "THE WORLD IN ONE DAY", font=fnt(SERIF_B, 50), fill=INK)
    d.text((W - M, y + 12), "No. 17 \u00b7 2026", font=fnt(MONO, 14), fill=MUTED, anchor="ra")
    y += 62
    d.text((M, y), "Tuesday, 17 November 2026  \u00b7  every story below broke in the last 24 hours",
           font=fnt(SANS, 14), fill=MUTED)
    y += 24
    rule(d, y, width=4)
    y += 14

    # ---------------- top: lead + right column ----------------
    left_w = 588
    x2 = M + left_w + 26
    right_w = W - M - x2
    d.rectangle([x2 - 13, y, x2 - 12, y + 300], fill=HAIR)

    ly = label(d, (M, y), "Ukraine \u00b7 Russia")
    ly = para(d, (M, ly - 2), "Ukraine strikes the Kerch Bridge", fnt(SERIF_B, 42), left_w, leading=1.08)
    ly += 6
    ly = para(d, (M, ly), "Drones and missiles hit Russia's only land link to Crimea. Zelenskyy called "
                          "the operation \u201cunprecedented\u201d; Moscow says it downed a record number "
                          "of Ukrainian drones for the second day running.",
              fnt(SERIF, 16), left_w, fill=(44, 42, 38), leading=1.26)
    ly += 12
    rule(d, ly, M, M + left_w, width=1, color=HAIR)
    ly += 10
    d.text((M, ly), "ALSO TODAY", font=fnt(SANS_B, 12), fill=MUTED)
    ly += 18
    ly = para(d, (M, ly), "Kyiv's forces also hit energy sites inside Russia overnight, while UN monitors "
                          "said civilian casualties in Ukraine this year already far exceed any year since "
                          "the invasion.", fnt(SERIF, 14), left_w, fill=(60, 57, 52), leading=1.2, max_lines=3)

    ry = label(d, (x2, y), "Iran \u00b7 United States")
    ry = para(d, (x2, ry - 2), "Iran strikes Bahrain; US fires back", fnt(SERIF_B, 25), right_w, leading=1.1)
    ry += 4
    ry = para(d, (x2, ry), "Drones hit a US radar site in the kingdom for the third time in days. "
                           "Washington answered against Iranian targets on a key shipping route.",
              fnt(SERIF, 15), right_w, fill=(44, 42, 38), leading=1.22)
    ry += 14
    rule(d, ry, x2, W - M, width=1, color=HAIR)
    ry += 12
    ry = label(d, (x2, ry), "Asia")
    ry = para(d, (x2, ry - 2), "Trump lands in Manila", fnt(SERIF_B, 25), right_w, leading=1.1)
    ry += 4
    ry = para(d, (x2, ry), "Trade deals in the Philippines, then Shenzhen: three-way nuclear talks "
                           "with Xi and Putin, and a possible meeting with Kim Jong Un.",
              fnt(SERIF, 15), right_w, fill=(44, 42, 38), leading=1.22)

    y = max(ly, ry) + 10

    # ---------------- pull quote ----------------
    rule(d, y, width=4)
    y += 14
    q = "\u201cUnprecedented.\u201d"
    d.text((M, y), q, font=fnt(SERIF_I, 46), fill=ACCENT)
    qw = d.textlength(q, font=fnt(SERIF_I, 46))
    d.text((M + qw + 14, y + 22), "Volodymyr Zelenskyy, on the strike against the bridge",
           font=fnt(SANS, 15), fill=MUTED)
    y += 62

    # ---------------- the day in numbers ----------------
    rule(d, y, width=1, color=HAIR)
    y += 12
    label(d, (M, y), "The day in numbers")
    y += 24
    stats = [("11,000+", "Ebola cases in DR Congo, with 5,400 deaths"),
             ("779", "points lost by the Dow as AI stocks swung"),
             ("$200m", "pledged to climate funds at COP31"),
             ("3rd", "Iranian drone attack on Bahrain in days")]
    cw = (W - 2 * M) // 4
    for i, (num, cap) in enumerate(stats):
        cx = M + i * cw
        d.text((cx, y), num, font=fnt(SERIF_B, 34), fill=ACCENT)
        para(d, (cx, y + 42), cap, fnt(SANS, 12), cw - 18, fill=(60, 58, 54), leading=1.18, max_lines=3)
    y += 108

    # ---------------- markets ----------------
    rule(d, y, width=1, color=HAIR)
    y += 12
    label(d, (M, y), "Markets")
    y += 24
    cells = [("S&P 500", "\u22121.1%"), ("DOW", "\u2212779 pts"), ("NASDAQ", "\u22121.5%")]
    for i, (name, val) in enumerate(cells):
        cx = M + i * cw
        d.text((cx, y), name, font=fnt(SANS_B, 13), fill=MUTED)
        d.text((cx, y + 17), val, font=fnt(SERIF_B, 28), fill=INK)
    y += 52
    d.text((M, y), "Manic swings in Nvidia and other AI stocks dragged the US market lower on Tuesday.",
           font=fnt(SERIF, 13), fill=(60, 58, 54))
    y += 30

    # ---------------- world in brief ----------------
    rule(d, y, width=4)
    y += 12
    label(d, (M, y), "The world in brief")
    y += 26
    briefs = [
        ("Measles-free status lost",
         "The US, Mexico and Bolivia have lost elimination status as the virus spreads fastest in 30 years."),
        ("Ebola doubles in DR Congo",
         "More than 11,000 cases and 5,400 deaths across 67 health zones in eight provinces, the WHO says."),
        ("COP31 presses on in Antalya",
         "Four nations pledged $200m as scientists warned of irreversible climate tipping points."),
        ("A hub in Rwanda for rejected asylum seekers",
         "Five European countries aim to open a \u201creturn hub\u201d next year to deter new arrivals."),
        ("Ukraine's civilian toll at a record",
         "Casualties in 2026 already far exceed any year since the invasion, UN monitors say."),
        ("Tiger Woods returns to competition",
         "He will play the Hero World Challenge he hosts in the Bahamas on 3\u20136 December."),
    ]
    col_w = (W - 2 * M - 30) // 2
    for i, (head, body) in enumerate(briefs):
        cx = M + (i % 2) * (col_w + 30)
        cy = y + (i // 2) * 68
        d.text((cx, cy), head, font=fnt(SANS_B, 14), fill=ACCENT)
        para(d, (cx, cy + 19), body, fnt(SERIF, 13), col_w, fill=(40, 38, 36), leading=1.18, max_lines=3)

    # ---------------- footer ----------------
    rule(d, H - 40, width=1, color=HAIR)
    d.text((M, H - 31), "Compiled from AP, NPR, IPS and Global Issues reports filed on 17 November 2026.",
           font=fnt(SANS, 11), fill=MUTED)
    d.text((W - M, H - 31), "ONE DAY \u00b7 ONE PAGE", font=fnt(MONO, 11), fill=MUTED, anchor="ra")

    img.save(out_path, "PNG", optimize=True)
    return out_path


if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    print(main(out), os.path.getsize(out), "bytes")
