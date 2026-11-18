#!/usr/bin/env python3
"""Draw the rebuilt news-image-20261118 front page: THE WORLD TODAY,
Wednesday 18 November 2026. Deterministic: same input -> same bytes.
Run: python3 draw.py  (writes entry.png, 1024x1024 PNG, next to this file)
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
M = 16                      # side margin
G = 12                      # gutter between columns
NAVY = (26, 35, 64)
RED = (176, 30, 36)
PAPER = (247, 243, 234)
INK = (17, 17, 17)
GREY = (102, 102, 102)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
NOTO_B = "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if fnt.getlength(trial) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_lines(d, x, y, lines, fnt, fill, spacing=1.18):
    """Draw lines of text; return y just below the last line."""
    lh = int(fnt.size * spacing)
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def headline_block(d, x, y, text, max_w, max_lines, start, fnt_path):
    """Headline, shrinking the font until it fits max_lines.
    Returns y just below the last line."""
    size = start
    while size > 14:
        fnt = font(fnt_path, size)
        if len(wrap(text, fnt, max_w)) <= max_lines:
            break
        size -= 1
    fnt = font(fnt_path, size)
    return draw_lines(d, x, y, wrap(text, fnt, max_w), fnt, INK, 1.08)


def kicker(d, x, y, text, size=16):
    fnt = font(SANS_B, size)
    d.text((x, y), text, font=fnt, fill=RED)
    return y + int(size * 1.25)


def body_block(d, x, y, text, max_w, size=14, max_lines=3):
    fnt = font(SANS, size)
    lines = wrap(text, fnt, max_w)[:max_lines]
    return draw_lines(d, x, y, lines, fnt, INK, 1.25)


def explosion(d, cx, cy, r):
    """Orange/yellow starburst + grey smoke."""
    for ang in range(0, 360, 30):
        a = math.radians(ang)
        d.line([(cx, cy), (cx + r * math.cos(a), cy + r * math.sin(a))],
               fill=(255, 140, 0), width=5)
    d.ellipse([cx - r * 0.45, cy - r * 0.45, cx + r * 0.45, cy + r * 0.45],
              fill=(255, 200, 40))
    d.ellipse([cx - r * 0.9, cy - r * 1.5, cx - r * 0.2, cy - r * 0.8],
              fill=(120, 120, 120))
    d.ellipse([cx + r * 0.1, cy - r * 1.7, cx + r * 0.8, cy - r * 1.0],
              fill=(150, 150, 150))


def tanker(d, x, y, w, h, hull=(52, 58, 64)):
    """Flat tanker silhouette: hull + deck + superstructure + funnel."""
    d.rectangle([x, y, x + w, y + h], fill=hull)
    d.rectangle([x + w * 0.62, y - h * 0.55, x + w * 0.78, y], fill=(230, 230, 225))
    d.rectangle([x + w * 0.80, y - h * 0.35, x + w * 0.86, y], fill=(176, 30, 36))
    d.rectangle([x + w * 0.10, y - h * 0.18, x + w * 0.55, y], fill=(90, 96, 102))


def snowflake(d, cx, cy, r, fill=(255, 255, 255), width=2):
    for ang in (0, 60, 120):
        a = math.radians(ang)
        d.line([(cx - r * math.cos(a), cy - r * math.sin(a)),
                (cx + r * math.cos(a), cy + r * math.sin(a))], fill=fill, width=width)


def story(d, x, y, col_w, ill_h, kicker_text, headline, head_size,
          head_lines, body_text, body_size=14, body_lines=3):
    """A column story: illustration box (caller draws into it), kicker,
    headline, body. Returns y just below the body. Caller must draw the
    illustration in the box (x, y, x+col_w, y+ill_h) before calling, or
    pass ill_h=0 for none. Here the illustration is drawn by the caller
    first; this lays out the text below it."""
    yy = y + ill_h + 6
    yy = kicker(d, x, yy, kicker_text)
    yy = headline_block(d, x, yy + 2, headline, col_w, head_lines,
                        head_size, NOTO_B)
    yy = body_block(d, x, yy + 2, body_text, col_w, body_size, body_lines)
    return yy


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    y = 0

    # ---- masthead ------------------------------------------------------
    d.rectangle([0, 0, W, 76], fill=NAVY)
    f = font(SERIF_B, 56)
    t = "THE WORLD TODAY"
    d.text(((W - f.getlength(t)) / 2, 4), t, font=f, fill=(255, 255, 255))
    f = font(SANS_B, 13)
    t = "O N E   D A Y ' S   N E W S   •   I N   O N E   P I C T U R E"
    d.text(((W - f.getlength(t)) / 2, 60), t, font=f, fill=(200, 205, 220))
    y = 76

    # ---- date band ------------------------------------------------------
    d.rectangle([0, y, W, y + 32], fill=RED)
    f = font(SANS_B, 21)
    t = "WEDNESDAY, 18 NOVEMBER 2026"
    d.text(((W - f.getlength(t)) / 2, y + 5), t, font=f, fill=(255, 255, 255))
    y += 32

    # ---- LEAD: U.S. sinks five Iranian tankers --------------------------
    lx, lw = M, W - 2 * M
    iy0 = y + 8
    iy1 = iy0 + 112
    d.rectangle([lx, iy0, lx + lw, iy1], fill=(176, 214, 235))
    d.rectangle([lx, iy1 - 56, lx + lw, iy1], fill=(38, 92, 140))
    d.rectangle([lx, iy1 - 56, lx + lw, iy1 - 52], fill=(120, 170, 210))
    tanker(d, lx + 60, iy1 - 42, 210, 24)
    tanker(d, lx + 360, iy1 - 48, 240, 28)
    tanker(d, lx + 700, iy1 - 40, 200, 22)
    explosion(d, lx + 300, iy1 - 72, 24)
    explosion(d, lx + 640, iy1 - 64, 20)
    d.line([(lx + 470, iy0 + 14), (lx + 520, iy0 + 56)], fill=(255, 255, 255), width=3)
    d.line([(lx + 830, iy0 + 20), (lx + 790, iy0 + 58)], fill=(255, 255, 255), width=3)
    yy = kicker(d, lx, iy1 + 8, "THE GULF  •  U.S. – IRAN")
    # two-line lead headline, drawn explicitly at 46 pt
    f = font(NOTO_B, 46)
    yy = draw_lines(d, lx, yy + 2, ["U.S. SINKS FIVE", "IRANIAN TANKERS"],
                    f, INK, 1.06)
    yy = body_block(d, lx, yy + 2,
                    "U.S. forces sank five Iranian oil tankers — Kaviz, Charminar, "
                    "Horizon 1 and Riesco in the Gulf of Oman, Derya near Kharg — "
                    "after the IRGC twice targeted U.S. warships. Iran hit 10 ships "
                    "near Hormuz and fired missiles at Al-Azraq in Jordan.",
                    lw, 15, 2)
    y = yy + 6
    d.line([M, y, W - M, y], fill=GREY, width=2)
    y += 8

    # ---- row 2: Bahrain | Gaza -------------------------------------------
    col_w = (W - 2 * M - G) // 2
    rx = M + col_w + G
    row_y = y
    ill_h = 64
    # Bahrain illustration: radar panel
    bx0, by0, bx1, by1 = M, row_y, M + col_w, row_y + ill_h
    d.rectangle([bx0, by0, bx1, by1], fill=(24, 42, 78))
    cx, cy = bx0 + 80, by0 + 32
    for r in (28, 20, 12):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(90, 180, 120), width=2)
    d.line([(cx, cy), (cx + 24, cy - 20)], fill=(140, 230, 160), width=3)
    d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=(140, 230, 160))
    for dx, dy in ((260, 18), (310, 40), (360, 22)):
        d.ellipse([bx0 + dx - 4, by0 + dy - 4, bx0 + dx + 4, by0 + dy + 4],
                  fill=(255, 255, 255))
        d.line([(bx0 + dx - 6, by0 + dy - 6), (bx0 + dx + 6, by0 + dy + 6)],
               fill=(255, 80, 60), width=3)
        d.line([(bx0 + dx - 6, by0 + dy + 6), (bx0 + dx + 6, by0 + dy - 6)],
               fill=(255, 80, 60), width=3)
    d.text((bx0 + 130, by0 + 42), "INTERCEPTED", font=font(SANS_B, 14),
           fill=(255, 200, 60))
    # Gaza illustration: tents + snow
    gx0, gy0, gx1, gy1 = rx, row_y, rx + col_w, row_y + ill_h
    d.rectangle([gx0, gy0, gx1, gy1], fill=(168, 196, 220))
    d.rectangle([gx0, gy1 - 14, gx1, gy1], fill=(240, 240, 235))
    for tx in (gx0 + 55, gx0 + 175, gx0 + 305):
        d.polygon([(tx, gy0 + 18), (tx + 46, gy1 - 14), (tx - 46, gy1 - 14)],
                  fill=(196, 178, 140))
        d.polygon([(tx, gy0 + 18), (tx + 46, gy1 - 14), (tx, gy1 - 14)],
                  fill=(170, 152, 116))
    snowflake(d, gx0 + 125, gy0 + 14, 8)
    snowflake(d, gx0 + 260, gy0 + 24, 6)
    snowflake(d, gx0 + 395, gy0 + 12, 8)
    y1 = story(d, M, row_y, col_w, ill_h, "THE GULF  •  BAHRAIN",
               "BAHRAIN INTERCEPTS THIRD IRANIAN DRONE ATTACK IN FIVE DAYS",
               25, 3,
               "Drones targeting Sheikh Isa Air Base were shot down on "
               "17 November — the third such attack in five days.", 14, 2)
    y2 = story(d, rx, row_y, col_w, ill_h, "GAZA  •  WINTER",
               "U.N. WARNS OF DEATHS FROM THE COLD", 27, 2,
               "Winter arrives with 1.7 million people still displaced and "
               "about 1.4 million in acute hunger. A 9-month-old baby died of "
               "the cold, and floods have swamped tens of thousands of tents.",
               14, 3)
    y = max(y1, y2) + 6
    d.line([M, y, W - M, y], fill=GREY, width=2)
    y += 8

    # ---- row 3: Kerch (follow-up) | Quad ---------------------------------
    row_y = y
    kx0, ky0, kx1, ky1 = M, row_y, M + col_w, row_y + ill_h
    d.rectangle([kx0, ky0, kx1, ky1], fill=(190, 220, 235))
    d.rectangle([kx0, ky1 - 22, kx1, ky1], fill=(52, 110, 160))
    d.rectangle([kx0, ky0 + 28, kx1, ky0 + 36], fill=(90, 96, 102))
    for tx in (kx0 + 80, kx0 + 350):
        d.rectangle([tx, ky0 + 4, tx + 9, ky0 + 36], fill=(70, 76, 82))
        d.line([(tx + 4, ky0 + 4), (tx - 30, ky0 + 28)], fill=(70, 76, 82), width=3)
        d.line([(tx + 4, ky0 + 4), (tx + 38, ky0 + 28)], fill=(70, 76, 82), width=3)
    d.arc([kx0 + 165, ky0 + 8, kx0 + 290, ky0 + 82], 0, 180,
          fill=(60, 66, 72), width=6)
    d.ellipse([kx0 + 205, ky0 + 44, kx0 + 233, ky0 + 62], fill=(120, 120, 120))
    d.ellipse([kx0 + 219, ky0 + 34, kx0 + 247, ky0 + 52], fill=(150, 150, 150))
    # Quad flags
    qx0, qy0, qx1, qy1 = rx, row_y, rx + col_w, row_y + ill_h
    d.rectangle([qx0, qy0, qx1, qy1], fill=(240, 236, 226))
    fw, fh, gap = 112, 46, 10
    fx, fy = qx0 + 8, qy0 + 6
    for i in range(7):
        d.rectangle([fx, fy + i * 6, fx + fw, fy + i * 6 + 6],
                    fill=(176, 30, 36) if i % 2 == 0 else (255, 255, 255))
    d.rectangle([fx, fy, fx + 46, fy + 24], fill=(26, 35, 64))
    for sx in range(3):
        for sy in range(2):
            d.ellipse([fx + 6 + sx * 14, fy + 5 + sy * 10,
                       fx + 10 + sx * 14, fy + 9 + sy * 10], fill=(255, 255, 255))
    d.text((fx + 18, fy + fh + 3), "USA", font=font(SANS_B, 13), fill=INK)
    fx += fw + gap
    d.rectangle([fx, fy, fx + fw, fy + fh], fill=(255, 255, 255), outline=GREY)
    d.ellipse([fx + fw // 2 - 13, fy + fh // 2 - 13, fx + fw // 2 + 13,
               fy + fh // 2 + 13], fill=(188, 0, 45))
    d.text((fx + 34, fy + fh + 3), "JAPAN", font=font(SANS_B, 13), fill=INK)
    fx += fw + gap
    d.rectangle([fx, fy, fx + fw, fy + 15], fill=(255, 153, 51))
    d.rectangle([fx, fy + 15, fx + fw, fy + 31], fill=(255, 255, 255))
    d.rectangle([fx, fy + 31, fx + fw, fy + fh], fill=(19, 136, 8))
    d.ellipse([fx + fw // 2 - 7, fy + fh // 2 - 7, fx + fw // 2 + 7,
               fy + fh // 2 + 7], outline=(0, 0, 128), width=2)
    d.text((fx + 36, fy + fh + 3), "INDIA", font=font(SANS_B, 13), fill=INK)
    fx += fw + gap
    d.rectangle([fx, fy, fx + fw, fy + fh], fill=(0, 40, 104))
    for sx, sy in ((18, 10), (38, 22), (58, 10), (78, 22), (94, 32)):
        d.ellipse([fx + sx - 3, fy + sy - 3, fx + sx + 3, fy + sy + 3],
                  fill=(255, 255, 255))
    d.text((fx + 14, fy + fh + 3), "AUSTRALIA", font=font(SANS_B, 13), fill=INK)
    y1 = story(d, M, row_y, col_w, ill_h, "UKRAINE  •  FOLLOW-UP — 16–17 NOV",
               "KERCH BRIDGE: ROAD ARCH COLLAPSES", 27, 2,
               "Ukraine's drones and missiles brought down the road arch in "
               "the second-night attack of 16–17 November; Russia answered "
               "by striking bridges in Kyiv.", 14, 3)
    y2 = story(d, rx, row_y, col_w, ill_h, "ASIA  •  MANILA",
               "QUAD MEETS IN MANILA", 30, 1,
               "Trump, Modi and the leaders of Japan and Australia agree "
               "critical-minerals deals and a first joint maritime patrol "
               "exercise in 2027, and warn against economic coercion.", 14, 3)
    y = max(y1, y2) + 6
    d.line([M, y, W - M, y], fill=GREY, width=2)
    y += 8

    # ---- row 4: Cyclone Akvan band -----------------------------------------
    ax0, ay0, ax1, ay1 = M, y, M + 190, y + 76
    d.rectangle([ax0, ay0, ax1, ay1], fill=(200, 216, 232))
    cx, cy = ax0 + 95, ay0 + 38
    for r, col in ((34, (30, 80, 140)), (26, (60, 120, 180)),
                   (18, (90, 150, 210)), (10, (30, 80, 140))):
        d.arc([cx - r, cy - r, cx + r, cy + r], 20, 300, fill=col, width=4)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(30, 80, 140))
    for dx in (ax0 + 18, ax0 + 168):
        for dy in (ay0 + 12, ay0 + 30, ay0 + 48):
            d.line([(dx, dy), (dx - 6, dy + 10)], fill=(120, 150, 190), width=2)
    tx = M + 206
    yy = kicker(d, tx, y + 2, "WEATHER  •  BAY OF BENGAL")
    yy = headline_block(d, tx, yy + 2, "CYCLONE AKVAN BEARS DOWN",
                        W - M - tx, 1, 28, NOTO_B)
    yy = body_block(d, tx, yy + 2,
                    "The storm strengthens over the Bay of Bengal and is forecast "
                    "to become a very severe cyclonic storm by 19 November, "
                    "crossing the Andhra coast on 20 November with winds to "
                    "145 km/h.", W - M - tx, 13, 2)
    y = max(yy, ay1) + 8

    # ---- footer ------------------------------------------------------------
    d.rectangle([0, y, W, H], fill=NAVY)
    f = font(SANS_B, 14)
    t = ("ALSO TODAY:  COP31 draft deal of 144 items under fire as ministers "
         "take over in Antalya  •  Robert Pattinson named the new James Bond")
    yy = y + 10
    for ln in wrap(t, f, W - 2 * M):
        d.text((M, yy), ln, font=f, fill=(255, 255, 255))
        yy += 18
    f = font(SANS, 12)
    t = "Sources: Reuters, AP, CNN, BBC — as reported on 18 November 2026"
    d.text(((W - f.getlength(t)) / 2, H - 22), t, font=f, fill=(170, 178, 200))

    img.save("entry.png", format="PNG", optimize=True)


if __name__ == "__main__":
    main()
