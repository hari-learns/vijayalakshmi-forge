#!/usr/bin/env python3
"""Drop in high-resolution originals by file name.

    python3 hd.py ~/Desktop/hd-images [--dry]

Every file in the folder whose name (without extension) matches an image the
site already uses, for example p-chain-02.png or P-CHAIN-02.jpg, replaces that
image in assets/img/. Logos keep transparency (mark-*.png, favicon). Anything
that does not match is listed, never copied. Long edge is capped at 1600 px.
"""
import os
import sys

from PIL import Image, ImageOps

ROOT = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(ROOT, "assets", "img")
EDGE = 1600


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    dry = "--dry" in sys.argv
    if not args:
        sys.exit(__doc__)
    src = os.path.expanduser(args[0])
    known = {os.path.splitext(f)[0]: f for f in os.listdir(IMG)}
    known["favicon"] = "../../favicon.png"
    done, skipped = [], []
    for name in sorted(os.listdir(src)):
        stem, ext = os.path.splitext(name)
        key = stem.lower().strip().replace(" ", "-").replace("_", "-")
        if ext.lower() not in (".png", ".jpg", ".jpeg", ".webp") or key not in known:
            skipped.append(name)
            continue
        im = ImageOps.exif_transpose(Image.open(os.path.join(src, name)))
        keep_alpha = known[key].endswith(".png")
        im = im.convert("RGBA" if keep_alpha else "RGB")
        im.thumbnail((EDGE, EDGE), Image.LANCZOS)
        dest = os.path.normpath(os.path.join(IMG, known[key]))
        if not dry:
            if keep_alpha:
                im.save(dest, optimize=True)
            else:
                im.save(dest, "WEBP", quality=90, method=6)
        done.append(f"{key:22} {im.size[0]}x{im.size[1]}")
    print(("would replace" if dry else "replaced"), len(done))
    print("\n".join("  " + d for d in done))
    if skipped:
        print("not matched, ignored:\n" + "\n".join("  " + s for s in skipped))
    if done and not dry:
        print("now run: python3 build.py && python3 verify.py")


if __name__ == "__main__":
    main()
