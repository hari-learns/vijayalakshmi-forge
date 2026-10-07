#!/usr/bin/env python3
"""Cuts the site's images out of the company's own posters.

    python3 crop.py [folder-with-the-15-poster-jpegs]

There is no photo shoot yet, only the finished posters the company uses on
WhatsApp and in print. The product shots, certificates, award photographs and
customer logos are cropped out of them. Boxes are written for a 960 px wide
poster and scaled to the real width, so a higher-resolution copy of the same
poster drops straight in.

Posters are copied into build_src/posters (gitignored) on first run so the
outputs can be rebuilt later. Outputs are committed.
"""
import os
import shutil
import sys

from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(ROOT, "assets", "img")
KEEP = os.path.join(ROOT, "build_src", "posters")
DEFAULT_SRC = ("/private/tmp/claude-501/-Users-hariharan-Documents-projects-"
               "lakefronthomehotel/9400ebde-3aaf-404a-8461-fb67f56005a6/images")

# poster key -> file name in the source folder (sent in chat on 7 Oct 2026)
POSTERS = {
    "chains": "24.jpg",        # K.K. "Our products": conveyor chain parts
    "quality": "25.jpg",
    "customers": "26.jpg",
    "certs": "27.jpg",
    "under": "28.jpg",         # K.K. "Our products": undercarriage parts
    "machining": "29.jpg",
    "awards": "30.jpg",
    "mixer": "31.jpg",
    "forge": "32.jpg",
}

# ---- boxes, in the coordinates of a 960 px wide poster --------------------
COLS = [(66, 304), (362, 602), (660, 898)]
ROWS = [(368, 582), (668, 882), (968, 1182), (1268, 1482)]


def grid(poster, prefix, rows):
    out = {}
    n = 1
    for r in range(rows):
        for c in range(3):
            y0, y1 = ROWS[r]
            if poster == "chains" and (r, c) == (1, 2):
                y1 = 862          # the card carries a caption at its foot
            out[f"{prefix}-{n:02d}"] = (poster, (COLS[c][0], y0, COLS[c][1], y1))
            n += 1
    return out


BOXES = {}
BOXES.update(grid("chains", "p-chain", 3))
BOXES.update(grid("mixer", "p-mixer", 3))
BOXES.update(grid("under", "p-under", 4))
BOXES["p-chain-banner"] = ("chains", (60, 1320, 900, 1510))

BOXES.update({
    "cert-tuv": ("certs", (222, 240, 692, 908)),
    "cert-intertek-1": ("certs", (38, 958, 456, 1546)),
    "cert-intertek-2": ("certs", (494, 958, 912, 1546)),
    "aw-mei-2015": ("awards", (80, 583, 318, 928)),
    "aw-tidc-cert": ("awards", (368, 550, 608, 930)),
    "aw-sundaram-trophy": ("awards", (690, 535, 845, 930)),
    "aw-tidc-sprockets": ("awards", (130, 1000, 250, 1290)),
    "aw-mei-2021": ("awards", (335, 1000, 555, 1290)),
    "aw-sundaram-plaque": ("awards", (615, 1020, 910, 1290)),
    "cu-ti": ("customers", (68, 589, 472, 796)),
    "cu-wheels": ("customers", (496, 589, 900, 796)),
    "cu-essae": ("customers", (68, 821, 472, 1009)),
    "cu-mei": ("customers", (496, 821, 900, 1009)),
    "cu-schwing": ("customers", (68, 1036, 472, 1194)),
    "cu-flowserve": ("customers", (496, 1036, 900, 1194)),
    "cu-burder": ("customers", (68, 1221, 472, 1394)),
    "cu-texel": ("customers", (496, 1221, 900, 1394)),
})

# brand marks are navy on white; turn white into transparency so they can sit
# on any ground, then they are saved as PNG
MARKS = {
    "mark-vlf": ("forge", (70, 95, 375, 262)),
    "mark-kk": ("machining", (88, 55, 382, 276)),
}
NAVY = (27, 26, 110)
BUDGET = 90_000


def load(key):
    return Image.open(os.path.join(KEEP, POSTERS[key])).convert("RGB")


def scaled(im, box):
    k = im.width / 960
    return tuple(int(round(v * k)) for v in box)


def save_webp(im, dest):
    for q in (86, 80, 74, 68):
        im.save(dest, "WEBP", quality=q, method=6)
        if os.path.getsize(dest) <= BUDGET:
            break


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_SRC
    os.makedirs(KEEP, exist_ok=True)
    os.makedirs(IMG, exist_ok=True)
    for key, name in POSTERS.items():
        have = os.path.join(KEEP, name)
        if not os.path.exists(have):
            shutil.copy(os.path.join(src, name), have)

    cache = {}
    for slug, (key, box) in BOXES.items():
        im = cache.setdefault(key, load(key))
        tile = im.crop(scaled(im, box))
        save_webp(tile, os.path.join(IMG, slug + ".webp"))
        print(f"  {slug:22} {tile.size[0]}x{tile.size[1]}")

    for slug, (key, box) in MARKS.items():
        im = cache.setdefault(key, load(key))
        tile = im.crop(scaled(im, box)).convert("L")
        # white -> clear, navy -> solid, with a soft ramp for anti-aliasing
        alpha = tile.point(lambda g: 0 if g > 235 else
                           255 if g < 90 else int((235 - g) * 255 / 145))
        out = Image.new("RGBA", tile.size, NAVY + (0,))
        out.putalpha(alpha)
        out.save(os.path.join(IMG, slug + ".png"), optimize=True)
        print(f"  {slug:22} {tile.size[0]}x{tile.size[1]} (transparent)")

    # favicon: the VLF mark, navy on white
    mark = Image.open(os.path.join(IMG, "mark-vlf.png"))
    side = max(mark.size) + 40
    fav = Image.new("RGBA", (side, side), (255, 255, 255, 255))
    fav.alpha_composite(mark, ((side - mark.width) // 2, (side - mark.height) // 2))
    fav.convert("RGB").resize((192, 192), Image.LANCZOS).save(
        os.path.join(ROOT, "favicon.png"), optimize=True)
    print("  favicon.png")


if __name__ == "__main__":
    main()
