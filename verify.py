#!/usr/bin/env python3
"""Static checks to pass after every build.

    python3 verify.py
"""
import glob
import os
import re
import sys
from html.parser import HTMLParser

import content as C

ROOT = os.path.dirname(os.path.abspath(__file__))
problems = []


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.assets, self.imgs, self.ids = [], [], [], set()
        self.h1 = 0
        self.title = self.desc = ""
        self._t = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get("id"):
            self.ids.add(a["id"])
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])
        elif tag == "img":
            self.imgs.append((a.get("src", ""), a.get("alt")))
            self.assets.append(a.get("src", ""))
        elif tag in ("link", "script") and (a.get("href") or a.get("src")):
            self.assets.append(a.get("href") or a.get("src"))
        elif tag == "h1":
            self.h1 += 1
        elif tag == "title":
            self._t = True
        elif tag == "meta" and a.get("name") == "description":
            self.desc = a.get("content", "")

    def handle_data(self, d):
        if self._t:
            self.title += d

    def handle_endtag(self, tag):
        if tag == "title":
            self._t = False


def lum(h):
    h = h.lstrip("#")
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    c = [x / 12.92 if x <= .03928 else ((x + .055) / 1.055) ** 2.4 for x in c]
    return .2126 * c[0] + .7152 * c[1] + .0722 * c[2]


def ratio(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + .05) / (lb + .05)


# --- contrast of the brand pairings, read from the stylesheet tokens ------
css = open(os.path.join(ROOT, "styles.css")).read()
tok = dict(re.findall(r"--([a-z0-9-]+):\s*(#[0-9a-fA-F]{6})", css))
tok["white"] = "#ffffff"
for fg, bg, floor in [("text", "white", 7), ("muted", "white", 4.5),
                      ("muted", "sky", 4.5), ("navy", "white", 7),
                      ("blue", "white", 4.5), ("red", "white", 4.5),
                      ("white", "navy", 7), ("on-navy", "navy", 4.5),
                      ("on-navy", "ink", 4.5), ("white", "blue", 4.5)]:
    r = ratio(tok[fg], tok[bg])
    if r < floor:
        problems.append(f"contrast {fg} on {bg} is {r:.2f}, wants {floor}")

# --- pages ------------------------------------------------------------
pages = {os.path.basename(p): p for p in glob.glob(os.path.join(ROOT, "*.html"))}
ids = {}
parsed = {}
for name, path in pages.items():
    p = Page()
    p.feed(open(path, encoding="utf-8").read())
    parsed[name] = p
    ids[name] = p.ids
    if p.h1 != 1:
        problems.append(f"{name}: {p.h1} h1 tags")
    if not p.title or not p.desc:
        problems.append(f"{name}: missing title or description")
    for src, alt in p.imgs:
        if alt is None:
            problems.append(f"{name}: img without alt: {src}")

for name, p in parsed.items():
    for a in p.assets:
        if a.startswith(("http", "data:", "//")) or not a:
            continue
        if not os.path.exists(os.path.join(ROOT, a.split("?")[0])):
            problems.append(f"{name}: missing asset {a}")
    for h in p.links:
        if h.startswith(("http", "mailto:", "tel:", "#")):
            if h.startswith("#") and h[1:] not in p.ids:
                problems.append(f"{name}: dead anchor {h}")
            continue
        target, _, frag = h.partition("#")
        target = target.split("?")[0]
        key = "index.html" if target in ("./", "") else target + ".html"
        if key not in pages and not os.path.exists(os.path.join(ROOT, target)):
            problems.append(f"{name}: dead link {h}")
        elif frag and key in ids and frag not in ids[key]:
            problems.append(f"{name}: {h} has no anchor {frag}")

# --- content --------------------------------------------------------------
for slug, *_ in C.PLANTS:
    pass
for p in C.PRODUCTS:
    for s in p["images"]:
        if not os.path.exists(os.path.join(ROOT, "assets", "img", s + ".webp")):
            problems.append(f"product image missing: {s}")
for slug, *_ in C.CERTS + C.AWARDS:
    if not os.path.exists(os.path.join(ROOT, "assets", "img", slug + ".webp")):
        problems.append(f"image missing: {slug}")
for _, f in C.CUSTOMERS:
    if not os.path.exists(os.path.join(ROOT, "assets", "img", f + ".webp")):
        problems.append(f"customer logo missing: {f}")

# the poster typo must never reach the site
for name, path in pages.items():
    if "vijlakforg." in open(path).read().replace("vijlakforge.", ""):
        problems.append(f"{name}: misspelt domain")

# build.py is a generator; copy lives in content.py
src = open(os.path.join(ROOT, "build.py")).read()
for needle in ("Ambattur Industrial Estate", "Mr. A. Kumar", "98404"):
    if needle in src:
        problems.append(f"build.py contains content: {needle}")

if problems:
    print("PROBLEMS")
    print("\n".join(" - " + p for p in problems))
    sys.exit(1)
print(f"ok: {len(pages)} pages, links, assets and contrast pass")
