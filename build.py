#!/usr/bin/env python3
"""Generate the Vijayalakshmi Forge & Stamping site.

A generator only. Every human-readable string lives in content.py.

    python3 build.py

Writes .html into the repo root, which is what GitHub Pages serves.
"""
import datetime
import glob
import hashlib
import html
import json
import os
import random
import re
from urllib.parse import quote

import content as C
import mark as M

ROOT = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(ROOT, "assets", "img")

try:
    from PIL import Image
except ImportError:
    Image = None


def esc(s):
    return html.escape(str(s), quote=True)


def version(path):
    full = os.path.join(ROOT, path)
    if not os.path.exists(full):
        return "0"
    with open(full, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()[:12]


CSS_V = version("styles.css")
JS_V = version("script.js")
SKY_V = version("sky.js")
TODAY = datetime.date.today().isoformat()
_dims = {}
_urls = []   # (clean path, lastmod) for the sitemap


def find(slug):
    for ext in ("webp", "png"):
        if os.path.exists(os.path.join(IMG_DIR, f"{slug}.{ext}")):
            return f"assets/img/{slug}.{ext}", os.path.join(IMG_DIR, f"{slug}.{ext}")
    return None, None


def img(slug, alt, cls="", eager=False, sizes=""):
    """An <img>, or a quiet blue block if the asset is missing."""
    src, path = find(slug)
    if not src:
        return (f'<div class="img-fallback {cls}" role="img" '
                f'aria-label="{esc(alt)}"></div>')
    if slug not in _dims:
        _dims[slug] = None
        if Image:
            with Image.open(path) as im:
                _dims[slug] = im.size
    size = _dims[slug]
    wh = f' width="{size[0]}" height="{size[1]}"' if size else ""
    loading = "" if eager else ' loading="lazy" decoding="async"'
    sz = f' sizes="{sizes}"' if sizes else ""
    cls_attr = f' class="{cls}"' if cls else ""
    return f'<img src="{src}" alt="{esc(alt)}"{cls_attr}{wh}{loading}{sz}>'



STEP_ICONS = {
    "Raw material": '<path d="M3 16l9-4 9 4-9 4-9-4z"/><path d="M3 12l9-4 9 4"/><path d="M3 8l9-4 9 4"/>',
    "Cutting": '<circle cx="12" cy="12" r="4"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M5 5l2 2M17 17l2 2M19 5l-2 2M7 17l-2 2"/>',
    "Hot forging": '<path d="M3 8h14a4 4 0 0 1-4 4h-3l1 3h3v4H6v-4h2l1-3H7a4 4 0 0 1-4-4z"/><path d="M19 3l-1 2M22 6l-2 1M16 2l0 2"/>',
    "Machining": '<rect x="9" y="3" width="6" height="8" rx="1"/><path d="M12 11v6l-1.5 3h3L12 17"/><path d="M4 21h16"/>',
    "Inspection": '<circle cx="11" cy="11" r="6"/><path d="M21 21l-5-5M8.5 11l2 2 3.5-4"/>',
    "Dispatch": '<path d="M2 6h11v10H2zM13 9h4l3 3v4h-7"/><circle cx="6.5" cy="17.5" r="1.8"/><circle cx="16.5" cy="17.5" r="1.8"/>',
}


def route(vertical=False):
    """The billet-to-part route as a chart that fills as the page scrolls."""
    items = "".join(
        f'''<li class="rstep{" rstep--hot" if t == "Hot forging" else ""}">
  <span class="rstep__node"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{STEP_ICONS.get(t, "")}</svg></span>
  <span class="rstep__body"><b>{t}</b><span>{d}</span><em>{m}</em></span>
</li>'''
        for t, d, m in C.CHAIN)
    return f'<ol class="route{" route--v" if vertical else ""}" data-route>{items}</ol>'


WA_GLYPH = '<svg viewBox="0 0 24 24" aria-hidden="true" class="wa-g" width="22" height="22"><path fill="currentColor" d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.32 4.95L2 22l5.25-1.38a9.9 9.9 0 0 0 4.79 1.22h.01c5.46 0 9.91-4.45 9.91-9.91 0-2.65-1.03-5.14-2.9-7.01A9.82 9.82 0 0 0 12.04 2Zm0 18.15h-.01a8.2 8.2 0 0 1-4.19-1.15l-.3-.18-3.12.82.83-3.04-.2-.31a8.18 8.18 0 0 1-1.26-4.38c0-4.54 3.7-8.24 8.25-8.24 2.2 0 4.27.86 5.83 2.42a8.19 8.19 0 0 1 2.41 5.83c0 4.54-3.69 8.23-8.24 8.23Zm4.52-6.16c-.25-.12-1.47-.72-1.69-.81-.23-.08-.39-.12-.56.13-.16.24-.64.8-.78.97-.15.16-.29.18-.53.06-.25-.12-1.05-.39-1.99-1.23-.74-.66-1.23-1.47-1.38-1.72-.14-.25-.01-.38.11-.5.11-.11.25-.29.37-.43.12-.15.16-.25.25-.41.08-.17.04-.31-.02-.43-.06-.12-.56-1.34-.76-1.84-.2-.48-.4-.42-.56-.43h-.47c-.17 0-.43.06-.66.31-.22.25-.86.85-.86 2.07 0 1.22.89 2.4 1.01 2.56.12.17 1.75 2.67 4.23 3.74.59.26 1.05.41 1.41.52.59.19 1.13.16 1.56.1.47-.07 1.47-.6 1.67-1.18.21-.58.21-1.07.15-1.18-.06-.1-.22-.16-.47-.28Z"/></svg>'


# --------------------------------------------------------------- loader ----

def mark_parts(letter_cls="", ram_cls="ld-ram"):
    """The VLF mark from mark.py: the hammer group and the three letters."""
    bars = "".join(f'<rect x="{x}" y="{y}" width="{w}" height="{h}"/>' for x, y, w, h in M.RAM)
    tx, ty, tw, th, tr = M.TUP
    hammer = (f'<g class="{ram_cls}">{bars}<rect x="{tx}" y="{ty}" width="{tw}" height="{th}" rx="{tr}"/>'
              f'<path d="{M.ARCH}" fill="none" stroke="currentColor" stroke-width="{M.ARCH_W}" '
              f'stroke-linejoin="round" stroke-linecap="round"/></g>')
    letters = "".join(f'<path class="{letter_cls}" d="{d}"/>' for d in M.LETTERS.values())
    return hammer, letters


def mark_svg(cls):
    hammer, letters = mark_parts(ram_cls="")
    return (f'<svg class="{cls}" viewBox="0 0 1220 660" aria-hidden="true" focusable="false" '
            f'fill="currentColor">{hammer}{letters}</svg>')


def sparks(at, n, seed):
    """Small solid flakes thrown from the contact line at each blow."""
    rnd = random.Random(seed)
    out = []
    for _ in range(n):
        x = rnd.uniform(170, 1050)
        side = 1 if x > 610 else -1
        dx = side * rnd.uniform(60, 380) + rnd.uniform(-40, 40)
        dy = -rnd.uniform(50, 300)
        w = rnd.uniform(16, 38)
        hue = rnd.choice(["#ffd27a", "#ff9a2e", "#ff6a1a", "#ffffff"])
        out.append(f'<rect class="ld-spark" x="{x:.0f}" y="282" width="{w:.0f}" height="8" rx="4" '
                   f'fill="{hue}" style="--dx:{dx:.0f}px;--dy:{dy:.0f}px;--r:{rnd.uniform(-200, 200):.0f}deg;'
                   f'--t:{at}s;--j:{rnd.uniform(0, .06):.3f}s"/>')
    return "".join(out)


def bands(n=6):
    return '<div class="ld-bands">' + "".join(f'<i style="--i:{i}"></i>' for i in range(n)) + "</div>"


def loader():
    """First visit of a session: three hammer blows stamp the letters out of
    a hot billet, the letters cool to white and the name is stamped beneath.
    The whole timeline is CSS, so it cannot hang (styles.css, 'loader')."""
    hammer, _ = mark_parts()
    letters = "".join(f'<path d="{d}"/>' for d in M.LETTERS.values())
    words, i = [], 0
    for word in C.LOADER_NAME.split(" "):
        chars = ""
        for ch in word:
            chars += f'<span style="--i:{i}">{esc(ch)}</span>'
            i += 1
        words.append(f'<span class="ld-w">{chars}</span>')
        i += 1
    name = " ".join(words)
    return f'''<div id="ld" aria-hidden="true">
  {bands()}
  <div class="ld-in">
    <svg class="ld-svg" viewBox="0 0 1220 660" focusable="false">
      <defs>
        <linearGradient id="ld-heat" gradientUnits="userSpaceOnUse" x1="0" y1="290" x2="0" y2="655">
          <stop offset="0" stop-color="#ff7a1a"/><stop offset=".45" stop-color="#ffc35c"/><stop offset="1" stop-color="#e0441a"/>
        </linearGradient>
      </defs>
      <g class="ld-shake">
        <rect class="ld-billet" x="200" y="278" width="820" height="300" rx="52" fill="url(#ld-heat)"/>
        <g class="ld-hot" fill="url(#ld-heat)">{letters}</g>
        <g class="ld-cool" fill="#fff">{letters}</g>
        <g class="ld-sparks">{sparks(.72, 16, 1)}{sparks(1.16, 13, 2)}{sparks(1.48, 9, 3)}</g>
        <g class="ld-hammer" fill="#fff" color="#fff">{hammer}</g>
      </g>
    </svg>
    <p class="ld-name">{name}</p>
    <p class="ld-line">{C.LOADER_LINE}</p>
  </div>
</div>
<div id="pt" aria-hidden="true">{bands()}{mark_svg("pt-mark")}</div>'''


# --------------------------------------------------------------- chrome ----

def nav(current):
    return "\n        ".join(
        f'<a href="{h}" style="--n:{i}"{" aria-current=\"page\"" if h == current else ""}>{l}</a>'
        for i, (h, l) in enumerate(C.NAV))


def brand():
    return f'''<a class="brand" href="index.html">
      {img("mark-vlf", "", cls="brand__mark", eager=True)}
      <span class="brand__txt">
        <span class="brand__name">{C.NAME}</span>
        <span class="brand__sub">{C.BRAND_SUB}</span>
      </span>
    </a>'''


def header(current):
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="hdr" data-header>
  <div class="hdr__in">
    {brand()}
    <nav class="nav" aria-label="Primary" style="--cnt:{len(C.NAV)}">
        {nav(current)}
    </nav>
    <div class="hdr__act">
      <a class="btn btn--sm" href="contact.html"{" aria-current=\"page\"" if current == "contact.html" else ""}>Contact</a>
      <button class="burger" type="button" aria-label="Open menu"
              aria-expanded="false" aria-controls="drawer" data-burger>
        <svg viewBox="0 0 24 24" width="24" height="24" aria-hidden="true"
             fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
          <path d="M3 6h18M3 12h18M3 18h18"/>
        </svg>
      </button>
    </div>
  </div>
</header>
<div class="drawer" id="drawer" data-drawer hidden>
  <button class="drawer__x" type="button" aria-label="Close menu" data-drawer-close>
    <svg viewBox="0 0 24 24" width="26" height="26" fill="none"
         stroke="currentColor" stroke-width="2" stroke-linecap="round">
      <path d="M5 5l14 14M19 5L5 19"/>
    </svg>
  </button>
  <nav class="drawer__nav" aria-label="Mobile">
        {nav(current)}
  </nav>
  <a class="btn btn--block" href="contact.html">Contact</a>
  <div class="drawer__meta">
    <a href="tel:{C.PHONE_LINK}">+91 {C.PHONE}</a>
    <a href="{esc(C.MAILTO)}">{C.ENQUIRY_TO}</a>
  </div>
</div>'''


def footer():
    links = "".join(f'<li><a href="{h}">{l}</a></li>'
                    for h, l in C.NAV + [C.CONTACT_PAGE])
    works = "".join(
        f'<li><a href="about.html#{p[0]}">{p[1]}</a></li>' for p in C.PLANTS)
    phones = "".join(f'<p><a href="tel:{tl}">+91 {ph}</a></p>' for ph, tl in C.PHONES)
    emails = "".join(f'<p><a href="mailto:{e}">{e}</a></p>' for e in C.EMAILS)
    note = (f'<p class="foot__note">{C.FOOTER_NOTE}</p>'
            if C.SHOW_PREVIEW_NOTE else "")
    return f'''
<footer class="foot">
  <div class="wrap foot__in">
    <div class="foot__brand">
      {mark_svg("foot__mark")}
      <p class="foot__name">{C.NAME}</p>
      <p class="foot__tag">{C.TAGLINE}</p>
      <p class="foot__cert">{C.CERT} · Ambattur, Chennai · Since {C.SINCE}</p>
    </div>
    <div class="foot__col">
      <h2 class="foot__h">Works</h2>
      <ul>{works}</ul>
    </div>
    <div class="foot__col">
      <h2 class="foot__h">Contact</h2>
      {phones}
      {emails}
    </div>
    <div class="foot__col">
      <h2 class="foot__h">Site</h2>
      <ul>{links}</ul>
    </div>
  </div>
  <div class="wrap foot__base">
    <p>&copy; 2026 {C.NAME}</p>
    {note}
  </div>
</footer>
<a class="wa" href="https://wa.me/{C.WHATSAPP}?text={quote(C.WHATSAPP_TEXT)}" target="_blank" rel="noopener"
   aria-label="Message us on WhatsApp">
  {WA_GLYPH}
</a>'''


def clean_urls(doc):
    """Link to /about rather than /about.html. GitHub Pages serves about.html
    for /about by itself; a local `python3 -m http.server` does not."""
    doc = re.sub(r'href="index\.html(?=[#"?])', 'href="./', doc)
    return re.sub(r'href="([a-z0-9-]+(?:/[a-z0-9-]+)?)\.html(?=[#"?])', r'href="\1', doc)


def clean_path(path):
    """about.html -> about, index.html -> '', blog/x.html -> blog/x."""
    p = path[:-5] if path.endswith(".html") else path
    return "" if p == "index" else p


def abs_url(path):
    return f"{C.SITE_URL}/{clean_path(path)}"


# ------------------------------------------------------------ structured data

def org_ld():
    p1, p2, kk = C.PLANTS
    def place(p, kind="LocalBusiness"):
        slug, name, role, addr, scope, *_ = p
        street, *rest = addr
        locality = "Thiruvallur" if "Thiruvallur" in " ".join(addr) else "Chennai"
        pin = re.search(r"\d{3} ?\d{3}", " ".join(addr)).group().replace(" ", "")
        return {"@type": kind, "@id": f"{C.SITE_URL}/#{slug}",
                "name": f"{C.NAME}, {name}" if slug != "kk" else name,
                "description": scope, "telephone": "+" + C.WHATSAPP,
                "url": f"{C.SITE_URL}/about#{slug}", "image": f"{C.SITE_URL}/{C.OG_IMAGE}",
                "address": {"@type": "PostalAddress", "streetAddress": ", ".join([street] + rest[:-2]),
                            "addressLocality": locality, "postalCode": pin,
                            "addressRegion": "Tamil Nadu", "addressCountry": "IN"},
                "parentOrganization": {"@id": f"{C.SITE_URL}/#org"}}
    org = {
        "@type": "Organization", "@id": f"{C.SITE_URL}/#org", "name": C.NAME,
        "alternateName": C.SHORT, "url": C.SITE_URL + "/",
        "logo": f"{C.SITE_URL}/assets/img/mark-vlf.png", "image": f"{C.SITE_URL}/{C.OG_IMAGE}",
        "description": C.LLMS_SUMMARY, "foundingDate": str(C.SINCE),
        "founder": {"@type": "Person", "name": C.LEADERS[0][0]},
        "slogan": C.TAGLINE, "email": C.ENQUIRY_TO,
        "telephone": "+" + C.WHATSAPP, "areaServed": "Worldwide",
        "knowsAbout": C.KNOWS_ABOUT,
        "hasCredential": [{"@type": "EducationalOccupationalCredential", "name": f"ISO 9001:2015, {t}",
                           "credentialCategory": "certification", "recognizedBy": {"@type": "Organization", "name": b.split(",")[0]}}
                          for _, t, _, b, *_ in C.CERTS],
        "award": [f"{t}, {g}" + (f", {y}" if y else "") for _, t, g, y, _ in C.AWARDS if y],
        "department": [{"@id": f"{C.SITE_URL}/#plant-1"}, {"@id": f"{C.SITE_URL}/#plant-2"}],
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Forged and machined components",
                            "itemListElement": [{"@type": "Offer", "itemOffered": {
                                "@type": "Product", "name": p["name"], "description": p["short"],
                                "url": f"{C.SITE_URL}/products#{p['slug']}",
                                "image": f"{C.SITE_URL}/assets/img/{p['images'][0]}.webp"}}
                                for p in C.PRODUCTS]},
        "contactPoint": {"@type": "ContactPoint", "contactType": "sales", "telephone": "+" + C.WHATSAPP,
                         "email": C.ENQUIRY_TO, "areaServed": "Worldwide", "availableLanguage": ["English", "Tamil"]},
    }
    site = {"@type": "WebSite", "@id": f"{C.SITE_URL}/#site", "url": C.SITE_URL + "/", "name": C.NAME,
            "publisher": {"@id": f"{C.SITE_URL}/#org"}, "inLanguage": "en-IN"}
    return [org, site, place(p1), place(p2), place(kk)]


def crumbs_ld(path, title):
    if clean_path(path) == "":
        return []
    items = [("Home", C.SITE_URL + "/")]
    if path.startswith("blog/"):
        items.append((C.H_BLOG, f"{C.SITE_URL}/blog"))
    items.append((title.split(" | ")[0], abs_url(path)))
    return [{"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(items)]}]


def json_ld(path, title, extra):
    graph = (org_ld() if path == "index.html" else
             [{"@type": "Organization", "@id": f"{C.SITE_URL}/#org", "name": C.NAME, "url": C.SITE_URL + "/"}])
    graph += crumbs_ld(path, title) + (extra or [])
    data = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":"))
    data = data.replace("</", "<\\/")
    return f'<script type="application/ld+json">{data}</script>'


HEAD_JS = ("(function(){var d=document.documentElement;d.className+=' js';try{"
           "if(matchMedia('(prefers-reduced-motion: reduce)').matches)return;var s=sessionStorage;"
           "if(!s.getItem('vlf-seen')){s.setItem('vlf-seen','1');d.className+=' ld'}"
           "else if(s.getItem('vlf-pt')){s.removeItem('vlf-pt');d.className+=' pt-in'}}catch(e){}})();")


def depth_fix(doc, path):
    """Pages in a folder (blog/x.html) reach the site root through ../"""
    depth = path.count("/")
    if not depth:
        return doc
    up = "../" * depth
    return re.sub(r'((?:href|src)=")(?!https?:|mailto:|tel:|#|data:|/|\.\./)', r"\1" + up, doc)


def page(path, title, description, body, current="", noindex=False, ld=None,
         og_type="website", image=None, sky=True):
    robots = "noindex, nofollow" if (C.NOINDEX or noindex) else "index, follow, max-image-preview:large"
    image = image or C.OG_IMAGE
    if not noindex:
        _urls.append((clean_path(path), TODAY))
    sky_js = f'<script src="sky.js?v={SKY_V}" defer></script>' if sky else ""
    doc = f'''<!doctype html>
<html lang="en-IN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<script>{HEAD_JS}</script>
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{abs_url(path)}">
<meta property="og:site_name" content="{esc(C.NAME)}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:type" content="{og_type}">
<meta property="og:url" content="{abs_url(path)}">
<meta property="og:image" content="{C.SITE_URL}/{image}">
<meta property="og:locale" content="en_IN">
<meta name="twitter:card" content="summary_large_image">
<meta name="geo.region" content="IN-TN">
<meta name="geo.placename" content="Ambattur, Chennai">
<meta name="theme-color" content="#1B1A6E">
<link rel="icon" href="favicon.png" type="image/png">
<link rel="apple-touch-icon" href="favicon.png">
<link rel="alternate" type="text/plain" href="llms.txt" title="Site summary for AI assistants">
<link rel="sitemap" type="application/xml" href="sitemap.xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@600;700;800&family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,600;9..40,700&display=swap">
<link rel="stylesheet" href="styles.css?v={CSS_V}">
<script type="speculationrules">{{"prefetch":[{{"where":{{"and":[{{"href_matches":"/*"}},{{"not":{{"selector_matches":"[target=_blank]"}}}}]}},"eagerness":"moderate"}}]}}</script>
{json_ld(path, title, ld)}
</head>
<body>
{loader()}
{header(current)}
<main id="main">
{body}
</main>
{footer()}
<script src="script.js?v={JS_V}" defer></script>
{sky_js}
</body>
</html>'''
    doc = depth_fix(clean_urls(doc), path)
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as fh:
        fh.write(doc)
    return path


# -------------------------------------------------------------- helpers ----

def sec_head(eyebrow, title, text="", mid=False):
    t = f'<p class="lede">{text}</p>' if text else ""
    # the eyebrow argument names the section in the code; it is not shown
    return f'''<div class="sec__head{" sec__head--mid" if mid else ""}" data-reveal>
  <h2 class="h2">{title}</h2>
  {t}
</div>'''


def cta():
    return f'''
<section class="band">
  <canvas class="sky" data-base="#1b1a6e" data-tint="#2c2ea0" data-amt=".9" data-scale="1.3" aria-hidden="true"></canvas>
  <div class="wrap band__in" data-reveal>
    <h2 class="h2">{C.CTA_TITLE}</h2>
    <p class="lede">{C.CTA_TEXT}</p>
    <div class="band__act">
      <a class="btn btn--light" href="contact.html#enquire">Send an enquiry</a>
      <a class="btn btn--ghost-light" href="https://wa.me/{C.WHATSAPP}?text={quote(C.WHATSAPP_TEXT)}"
         target="_blank" rel="noopener">{WA_GLYPH}WhatsApp +91 {C.PHONE}</a>
    </div>
  </div>
</section>'''


def subhero(eyebrow, title, text):
    return f'''
<section class="subhero">
  <div class="wrap subhero__in">
    <h1 class="h1">{title}</h1>
    <p class="lede">{text}</p>
  </div>
</section>'''


def plant_card(p, full=False):
    slug, name, role, addr, scope, cert, valid, q = p
    map_url = "https://www.google.com/maps/search/?api=1&query=" + quote(q)
    return f'''<article class="plant" id="{slug}" data-reveal>
  <p class="plant__role">{role}</p>
  <h3 class="plant__name">{name}</h3>
  <address class="plant__addr">{"<br>".join(addr)}</address>
  <dl class="plant__spec">
    <div><dt>Scope</dt><dd>{scope}</dd></div>
    <div><dt>Certified</dt><dd>{cert}<br><span>{valid}</span></dd></div>
  </dl>
  <a class="link" href="{map_url}" target="_blank" rel="noopener">Open in Maps</a>
</article>'''


def enquiry_form():
    opts = "".join(f'<option data-slug="{p["slug"]}">{p["name"]}</option>' for p in C.PRODUCTS)
    return f'''<div class="enq" data-enq>
<form class="form" data-enquiry data-wa="{C.WHATSAPP}"
      data-endpoint="{esc(C.FORM_ENDPOINT)}" data-cc="{esc(",".join(C.ENQUIRY_CC))}"
      data-sent="{esc(C.SENT_TEXT)}" data-fail="{esc(C.FAIL_TEXT)}" id="enquire" novalidate>
  <div class="form__row">
    <label><span class="form__lbl">Your name <i class="req">required</i></span><input type="text" name="name" required autocomplete="name" maxlength="80"></label>
    <label><span class="form__lbl">Company</span><input type="text" name="company" autocomplete="organization"></label>
  </div>
  <div class="form__row">
    <label><span class="form__lbl">Phone <i class="req">required</i></span><input type="tel" name="phone" required autocomplete="tel" inputmode="tel" maxlength="20" placeholder="e.g. 98400 12345"></label>
    <label><span class="form__lbl">Email</span><input type="email" name="email" autocomplete="email" maxlength="120" placeholder="name@company.com"></label>
  </div>
  <div class="form__row">
    <label><span class="form__lbl">Product</span><select name="product">
      <option>Not sure yet</option>{opts}<option>Something else</option></select></label>
    <label><span class="form__lbl">Material</span><input type="text" name="material" placeholder="Carbon, alloy, stainless, grade&hellip;"></label>
  </div>
  <div class="form__row">
    <label><span class="form__lbl">Quantity</span><input type="text" name="quantity" placeholder="e.g. 500 pieces a month"></label>
    <label class="file"><span class="form__lbl">Drawing <i class="opt">PDF, image or DWG</i></span><input type="file" name="drawing"
      accept=".pdf,.png,.jpg,.jpeg,.webp,.dwg,.dxf"></label>
  </div>
  <label><span class="form__lbl">Part description</span><textarea name="message" rows="4"
    placeholder="What the part does, the drawing or part number, any special requirement&hellip;"></textarea></label>
  <button class="btn btn--block" type="submit" data-send>Send enquiry</button>
  <p class="form__status" data-status role="status" aria-live="polite" hidden></p>
  <p class="form__note">Name and phone are all we need. Everything else is optional. {C.RFQ_NOTE}</p>
</form>
<div class="thanks" data-thanks hidden tabindex="-1">
  <svg class="thanks__tick" viewBox="0 0 96 96" aria-hidden="true">
    <circle class="thanks__glow" cx="48" cy="48" r="40"/>
    <circle class="thanks__ring" cx="48" cy="48" r="40" pathLength="1"/>
    <path class="thanks__check" d="M30 49 L43 62 L67 36" pathLength="1"/>
  </svg>
  <h3 class="thanks__h">{C.THANKS_TITLE}</h3>
  <p class="thanks__p">{C.THANKS_TEXT}</p>
  <button class="link thanks__again" type="button" data-again>{C.THANKS_AGAIN}</button>
</div>
</div>'''


def product_tile(p, image, i):
    return f'''<a class="ptile" href="products.html#{p["slug"]}" data-reveal style="--i:{i}">
  <span class="ptile__img">{img(image, p["alt"], sizes="(max-width:700px) 50vw, 25vw")}</span>
  <h3 class="ptile__name">{p["name"]}</h3>
  <p class="ptile__short">{p["short"]}</p>
  <span class="ptile__go">See the range</span>
</a>'''


def product_section(p, i):
    prose = "".join(f"<p>{x}</p>" for x in p["body"])
    pts = "".join(f"<li>{x}</li>" for x in p["points"])
    shots = "".join(
        f'<figure class="pshot" data-reveal style="--i:{n % 6}">'
        f'{img(s, p["alt"], sizes="(max-width:700px) 50vw, 25vw")}</figure>'
        for n, s in enumerate(p["images"]))
    banner = (f'<figure class="pbanner" data-reveal>{img("p-chain-banner", "A forged conveyor chain with its attachments", sizes="100vw")}</figure>'
              if p["slug"] == "conveyor-chains" else "")
    return f'''<section class="psec{" psec--alt" if i % 2 else ""}" id="{p["slug"]}">
  <div class="wrap">
    <div class="psec__head" data-reveal>
      <h2 class="h2">{p["name"]}</h2>
      <p class="lede">{p["short"]}</p>
    </div>
    <div class="psec__body">
      <div class="prose" data-reveal>{prose}<ul class="ticks">{pts}</ul></div>
    </div>
    <div class="pgrid{" pgrid--4" if len(p["images"]) == 4 else ""}">{shots}</div>
    {banner}
  </div>
</section>'''


def cert_card(c, i):
    slug, title, number, body, scope, dates = c
    return f'''<article class="cert" data-reveal style="--i:{i}">
  <a class="cert__img" href="assets/img/{slug}.webp" data-lightbox aria-label="Open certificate: {esc(title)}">{img(slug, f"ISO 9001:2015 certificate, {title}", sizes="(max-width:800px) 100vw, 30vw")}</a>
  <h3 class="cert__t">{title}</h3>
  <p class="cert__no">No. {number}</p>
  <p class="cert__scope">{scope}</p>
  <p class="cert__meta">{body}<br>{dates}</p>
</article>'''


def award_card(a, i):
    slug, title, giver, year, note = a
    return f'''<article class="award" data-reveal style="--i:{i % 3}">
  <div class="award__img">{img(slug, f"{title}, {giver}", sizes="(max-width:700px) 50vw, 25vw")}</div>
  <p class="award__year">{year or "&nbsp;"}</p>
  <h3 class="award__t">{title}</h3>
  <p class="award__by">{giver}</p>
  <p class="award__note">{note}</p>
</article>'''


def customer_grid():
    return "".join(
        f'<li class="cust" data-reveal style="--i:{i % 4}">'
        f'<span class="cust__plate">{img(f, n + " logo", sizes="200px")}</span>'
        f'<span class="cust__name">{n}</span></li>'
        for i, (n, f) in enumerate(C.CUSTOMERS))



# --------------------------------------------------------------- finder ----

def finder():
    """The row under the hero: the buyer describes the part, the page points
    to the family that makes it and prepares the quote message."""
    L = C.FINDER_LABELS
    opt = lambda xs: "".join(f'<option value="{esc(v)}">{esc(t)}</option>' for v, t in xs)
    data = {
        "families": [{"slug": p["slug"], "name": p["name"], "short": p["short"],
                      "points": p["points"][:3], "img": find(p["images"][0])[0],
                      "words": C.FINDER_KEYWORDS.get(p["slug"], [])} for p in C.PRODUCTS],
        "facts": C.FINDER_FACT_LABELS, "made": C.FINDER_FACT_MADE, "steel": C.FINDER_FACT_STEEL,
        "from": C.FINDER_FACT_FROM, "none": C.FINDER_NONE, "quote": C.FINDER_QUOTE,
        "details": C.FINDER_DETAILS, "intro": C.FINDER_WA_INTRO, "wa": C.WHATSAPP,
        "labels": C.FINDER_MSG, "sum": C.FINDER_SUM,
    }
    blob = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    return f'''<section class="finder" id="find" aria-labelledby="find-h">
  <div class="wrap">
    <h2 class="finder__h" id="find-h">{C.FINDER_TITLE}</h2>
    <form class="fbar" data-finder role="search" action="contact.html#enquire">
      <label class="fbar__f fbar__f--free"><span>{L["free"]}</span>
        <input name="free" type="text" autocomplete="off" placeholder="{esc(C.FINDER_PLACEHOLDER)}"></label>
      <label class="fbar__f"><span>{L["use"]}</span><select name="use">{opt(C.FINDER_USE)}</select></label>
      <label class="fbar__f"><span>{L["material"]}</span><select name="material">{opt((m, m) for m in C.FINDER_MATERIALS)}</select></label>
      <label class="fbar__f"><span>{L["have"]}</span><select name="have">{opt((h, h) for h in C.FINDER_HAVE)}</select></label>
      <button class="btn fbar__go" type="submit" data-fgo>Find the line</button>
    </form>
    <p class="finder__said" data-fsaid aria-live="polite"></p>
    <div class="fres" data-fres></div>
    <div class="fsum" data-fsum hidden>
      <div class="fsum__msg"><p class="fsum__h">{C.FINDER_SUM}</p><pre class="fsum__txt" data-ftxt></pre></div>
      <div class="fsum__act">
        <a class="btn btn--light" data-fwa href="https://wa.me/{C.WHATSAPP}" target="_blank" rel="noopener">{WA_GLYPH}WhatsApp this</a>
        <a class="btn btn--ghost-light" data-fform href="contact.html#enquire">Open the quote form</a>
      </div>
      <p class="fsum__note">{C.FINDER_NOTE}</p>
    </div>
    <script type="application/json" id="vlf-finder">{blob}</script>
  </div>
</section>'''


# ----------------------------------------------------------------- blog ----

def md(text):
    """Enough Markdown for the posts: ## headings, paragraphs, - and 1. lists,
    **bold** and [links](url)."""
    def inline(t):
        t = esc(t)
        t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
        return re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", r'<a href="\2">\1</a>', t)
    out = []
    for block in re.split(r"\n\s*\n", text.strip()):
        lines = block.strip().splitlines()
        if lines[0].startswith("### "):
            out.append(f"<h3>{inline(lines[0][4:])}</h3>")
        elif lines[0].startswith("## "):
            out.append(f"<h2>{inline(lines[0][3:])}</h2>")
        elif all(l.startswith("- ") for l in lines):
            out.append("<ul>" + "".join(f"<li>{inline(l[2:])}</li>" for l in lines) + "</ul>")
        elif all(re.match(r"\d+\. ", l) for l in lines):
            out.append("<ol>" + "".join(f"<li>{inline(re.sub(r'^\d+\. ', '', l))}</li>" for l in lines) + "</ol>")
        else:
            out.append(f"<p>{inline(' '.join(lines))}</p>")
    return "\n".join(out)


def posts():
    found = []
    for f in sorted(glob.glob(os.path.join(ROOT, "posts", "*.md"))):
        raw = open(f, encoding="utf-8").read()
        m = re.match(r"---\n(.*?)\n---\n(.*)", raw, re.S)
        meta = dict(re.findall(r"^(\w+):\s*(.+)$", m.group(1), re.M))
        meta["slug"] = os.path.basename(f)[:-3]
        meta["body"] = m.group(2)
        meta["words"] = len(m.group(2).split())
        found.append(meta)
    return sorted(found, key=lambda p: (p["date"], p["title"]), reverse=True)


def nice_date(iso):
    d = datetime.date.fromisoformat(iso)
    return f"{d.day} {d.strftime('%B %Y')}"


def read_time(p):
    return f"{max(1, round(p['words'] / 200))} min read"


def post_card(p, i):
    return f'''<a class="pcard" href="blog/{p["slug"]}.html" data-reveal style="--i:{i % 3}">
  <span class="pcard__img">{img(p.get("image", ""), "", sizes="(max-width:700px) 100vw, 33vw")}</span>
  <span class="pcard__date">{nice_date(p["date"])} · {read_time(p)}</span>
  <h3 class="pcard__t">{esc(p["title"])}</h3>
  <span class="pcard__d">{esc(p["description"])}</span>
</a>'''


def blog_teaser():
    ps = posts()[:3]
    if not ps:
        return ""
    cards = "".join(post_card(p, i) for i, p in enumerate(ps))
    return f'''<section class="sec">
  <div class="wrap">
    {sec_head("Blog", C.H_BLOG_HOME, C.BLOG_HOME_INTRO)}
    <div class="pcards">{cards}</div>
  </div>
</section>'''


def build_blog():
    ps = posts()
    cards = "".join(post_card(p, i) for i, p in enumerate(ps))
    body = f'''{subhero("Blog", C.H_BLOG, C.BLOG_INTRO)}
<section class="sec"><div class="wrap"><div class="pcards">{cards}</div></div></section>
{cta()}'''
    ld = [{"@type": "Blog", "@id": f"{C.SITE_URL}/blog#blog", "name": f"{C.H_BLOG} | {C.NAME}",
           "publisher": {"@id": f"{C.SITE_URL}/#org"},
           "blogPost": [{"@type": "BlogPosting", "headline": p["title"], "url": f"{C.SITE_URL}/blog/{p['slug']}",
                         "datePublished": p["date"]} for p in ps]}]
    page("blog.html", f"{C.H_BLOG} | {C.NAME}", C.META["blog"], body, "blog.html", ld=ld)
    for p in ps:
        path = f"blog/{p['slug']}.html"
        more = "".join(post_card(q, i) for i, q in enumerate(x for x in ps if x is not p))
        hero_img = img(p.get("image", ""), p["title"], cls="post__img", eager=True,
                       sizes="(max-width:900px) 100vw, 760px")
        body = f'''<article class="post">
  <header class="post__head">
    <div class="wrap post__wrap">
      <a class="post__back" href="blog.html">{C.BLOG_BACK}</a>
      <h1 class="h1">{esc(p["title"])}</h1>
      <p class="post__meta">{C.BLOG_BY} · <time datetime="{p["date"]}">{nice_date(p["date"])}</time> · {read_time(p)}</p>
    </div>
  </header>
  <div class="wrap post__wrap">
    <figure class="post__fig">{hero_img}</figure>
    <div class="prose post__body">{md(p["body"])}</div>
  </div>
</article>
<section class="sec sec--alt"><div class="wrap">
  {sec_head("More", C.BLOG_BACK)}
  <div class="pcards">{more}</div>
</div></section>
{cta()}'''
        image = find(p.get("image", ""))[0] or C.OG_IMAGE
        ld = [{"@type": "BlogPosting", "headline": p["title"], "description": p["description"],
               "datePublished": p["date"], "dateModified": p.get("updated", p["date"]),
               "image": f"{C.SITE_URL}/{image}", "url": abs_url(path), "mainEntityOfPage": abs_url(path),
               "author": {"@id": f"{C.SITE_URL}/#org"}, "publisher": {"@id": f"{C.SITE_URL}/#org"},
               "wordCount": p["words"], "inLanguage": "en-IN"}]
        page(path, f"{p.get('seo_title', p['title'])} | {C.SHORT}", p["description"], body, "blog.html",
             ld=ld, og_type="article", image=image)
    return f"blog.html + {len(ps)} posts"


# ------------------------------------------------- search engines and AI ----

def build_discovery():
    """robots.txt, sitemap.xml, llms.txt and the IndexNow key file."""
    pages_ = sorted(set(_urls), key=lambda u: (u[0] != "", u[0]))
    urls = "".join(f"  <url><loc>{C.SITE_URL}/{u}</loc><lastmod>{d}</lastmod></url>\n" for u, d in pages_)
    with open(os.path.join(ROOT, "sitemap.xml"), "w") as fh:
        fh.write('<?xml version="1.0" encoding="UTF-8"?>\n'
                 '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + "</urlset>\n")
    # Search and AI crawlers are named to make the welcome explicit. While the
    # site is a preview, every page carries a noindex tag rather than a block
    # here, because a crawler has to read a page to see its noindex tag.
    bots = ["Googlebot", "Bingbot", "OAI-SearchBot", "ChatGPT-User", "GPTBot", "PerplexityBot",
            "Perplexity-User", "Claude-SearchBot", "Claude-User", "ClaudeBot", "Applebot", "DuckDuckBot"]
    robots = "".join(f"User-agent: {b}\nAllow: /\n\n" for b in bots)
    with open(os.path.join(ROOT, "robots.txt"), "w") as fh:
        fh.write(robots + "User-agent: *\nAllow: /\n\n" + f"Sitemap: {C.SITE_URL}/sitemap.xml\n")
    nav = [("Products", "products", C.META["products"]), ("Capabilities", "capabilities", C.META["capabilities"]),
           ("Customers and awards", "customers", C.META["customers"]), ("About", "about", C.META["about"]),
           ("Contact and quotes", "contact", C.META["contact"]), (C.H_BLOG, "blog", C.META["blog"])]
    lines = [f"# {C.NAME}", "", f"> {C.LLMS_SUMMARY}", "", "## Facts", ""]
    lines += [f"- {f}" for f in C.LLMS_FACTS]
    lines += ["", "## Pages", ""] + [f"- [{t}]({C.SITE_URL}/{u}): {d}" for t, u, d in nav]
    lines += ["", "## Articles", ""] + [f"- [{p['title']}]({C.SITE_URL}/blog/{p['slug']}): {p['description']}"
                                        for p in posts()]
    with open(os.path.join(ROOT, "llms.txt"), "w") as fh:
        fh.write("\n".join(lines) + "\n")
    with open(os.path.join(ROOT, f"{C.INDEXNOW_KEY}.txt"), "w") as fh:
        fh.write(C.INDEXNOW_KEY)
    return f"robots.txt, sitemap.xml ({len(pages_)} urls), llms.txt, IndexNow key"


# ---------------------------------------------------------------- pages ----


def quality_glimpse():
    pts = "".join(f'<li data-reveal style="--i:{i}"><b>{t}</b><span>{d}</span></li>'
                  for i, (t, d) in enumerate(C.QUALITY_POINTS))
    certs = "".join(cert_card(c, i) for i, c in enumerate(C.CERTS))
    return f'''<section class="sec" id="quality">
  <div class="wrap">
    {sec_head("Quality", C.H_QUALITY_GLIMPSE, C.QUALITY_GLIMPSE_INTRO)}
    <ul class="qfive">{pts}</ul>
    <div class="certs certs--sm">{certs}</div>
  </div>
</section>'''


def build_home():
    stats = "".join(
        f'<div class="stat" data-reveal style="--i:{i}"><b>{v}<i>{u}</i></b>'
        f'<span>{l}</span></div>'
        for i, (v, u, l) in enumerate(C.STATS))
    hero_shots = "".join(
        f'<figure class="hshot hshot--{i + 1}">{img(s, "", eager=True, sizes="(max-width:900px) 40vw, 18vw")}</figure>'
        for i, s in enumerate(C.HERO_IMAGES))
    tiles = "".join(
        product_tile(p, p["images"][0], i)
        for i, p in enumerate(C.PRODUCTS))
    qual = "".join(
        f'<li data-reveal style="--i:{i}"><b>{t}</b><span>{d}</span></li>'
        for i, (t, d) in enumerate(C.QUALITY_HOME))
    awards = "".join(award_card(a, i) for i, a in enumerate(C.AWARDS[:3]))
    plants = "".join(plant_card(p) for p in C.PLANTS)

    body = f'''
<section class="hero">
  <canvas class="sky" data-base="#eef2fc" data-tint="#d3ddf7" data-amt=".95" data-scale="1.25" aria-hidden="true"></canvas>
  <div class="wrap hero__in">
    <div class="hero__copy">
      <p class="hero__eyebrow hin" style="--i:0">{C.HERO_EYEBROW}</p>
      <h1 class="hero__title hin" style="--i:1"><span>{C.HERO_TITLE_A}</span> <em>{C.HERO_TITLE_B}</em></h1>
      <p class="hero__text hin" style="--i:2">{C.HERO_TEXT}</p>
      <div class="hero__act hin" style="--i:3">
        <a class="btn" href="contact.html#enquire">Send an enquiry</a>
        <a class="btn btn--ghost" href="products.html">See our products</a>
      </div>
      <ul class="hero__proof hin" style="--i:4">{"".join(f"<li>{x}</li>" for x in C.HERO_PROOF)}</ul>
    </div>
    <div class="hero__shots" aria-hidden="true">{hero_shots}</div>
  </div>
</section>

{finder()}

<section class="stats-band"><div class="wrap stats">{stats}</div></section>

<section class="sec">
  <div class="wrap">
    {sec_head("Products", C.H_PRODUCTS, C.PRODUCTS_HOME_INTRO)}
    <div class="ptiles">{tiles}</div>
  </div>
</section>

<section class="sec sec--alt">
  <div class="wrap">
    {sec_head("Capabilities", C.H_CAPS_HOME, C.CAPS_HOME_INTRO)}
    {route()}
    <div class="sec__more" data-reveal><a class="btn btn--ghost" href="capabilities.html">Equipment and facilities</a></div>
  </div>
</section>

<section class="sec sec--navy">
  <div class="wrap">
    {sec_head("Quality", C.H_QUALITY, C.QUALITY_INTRO, mid=True)}
    <ul class="qstrip">{qual}</ul>
    <div class="sec__more" data-reveal><a class="btn btn--light" href="about.html#quality">Certificates and standards</a></div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    {sec_head("Customers", C.H_CUSTOMERS, C.CUSTOMERS_INTRO)}
    <ul class="custs">{customer_grid()}</ul>
  </div>
</section>

<section class="sec sec--alt">
  <div class="wrap">
    {sec_head("Recognition", C.H_AWARDS, C.AWARDS_INTRO)}
    <div class="awards">{awards}</div>
    <div class="sec__more" data-reveal><a class="btn btn--ghost" href="customers.html#awards">All awards</a></div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    {sec_head("Our works", C.H_PLANTS_HOME, C.PLANTS_INTRO)}
    <div class="plants">{plants}</div>
  </div>
</section>
{blog_teaser()}
{cta()}'''
    return page("index.html", C.TAB_NAME,
                C.META["index"], body)


def build_products():
    secs = "".join(product_section(p, i) for i, p in enumerate(C.PRODUCTS))
    jump = "".join(f'<a class="chip chip--link" href="#{p["slug"]}">{p["name"]}</a>'
                   for p in C.PRODUCTS)
    body = f'''{subhero("Products", C.H_PRODUCTS_PAGE, C.PRODUCTS_PAGE_INTRO)}
<div class="wrap"><div class="chips chips--jump" data-reveal>{jump}</div></div>
{secs}
{cta()}'''
    return page("products.html", f"Products | {C.NAME}",
                C.META["products"],
                body, "products.html")


def build_capabilities():
    rows = "".join(
        f'<tr><th scope="row">{n}</th><td class="fig">{s}</td><td>{d}</td></tr>'
        for n, s, d in C.EQUIPMENT)
    body = f'''{subhero("Capabilities", C.H_CAPS, C.CAPS_INTRO)}
<section class="sec">
  <div class="wrap">
    {sec_head("Process", C.H_CHAIN)}
    {route(True)}
  </div>
</section>
<section class="sec sec--alt">
  <div class="wrap">
    {sec_head("Plant", C.H_EQUIP, C.CAPS_NOTE)}
    <div class="tablewrap" data-reveal>
      <table class="spec">
        <thead><tr><th>Equipment</th><th>Capacity</th><th>Used for</th></tr></thead>
        <tbody>{rows}</tbody>
      </table>
    </div>
  </div>
</section>
{cta()}'''
    return page("capabilities.html", f"Capabilities | {C.NAME}",
                C.META["capabilities"], body, "capabilities.html")



def build_customers():
    awards = "".join(award_card(a, i) for i, a in enumerate(C.AWARDS))
    body = f'''{subhero("Customers", C.H_CUSTOMERS, C.CUSTOMERS_INTRO)}
<section class="sec">
  <div class="wrap"><ul class="custs">{customer_grid()}</ul></div>
</section>
<section class="sec sec--navy" id="awards">
  <div class="wrap">
    {sec_head("Recognition", C.H_AWARDS, C.AWARDS_INTRO)}
    <div class="awards awards--on-navy">{awards}</div>
  </div>
</section>
{cta()}'''
    return page("customers.html", f"Customers | {C.NAME}",
                C.META["customers"], body, "customers.html")


def build_about():
    leaders = "".join(
        f'<div class="person"><p class="person__name">{n}</p><p class="person__role">{r}</p></div>'
        for n, r in C.LEADERS)
    pillars = "".join(
        f'<li data-reveal style="--i:{i}"><b>{t}</b><span>{d}</span></li>'
        for i, (t, d) in enumerate(C.PILLARS))
    plants = "".join(plant_card(p) for p in C.PLANTS)
    tl = "".join(f'<li data-reveal style="--i:{i % 3}"><b>{y}</b><span>{t}</span></li>'
                 for i, (y, t) in enumerate(C.TIMELINE))
    prose = "".join(f"<p>{x}</p>" for x in C.ABOUT_BODY)
    body = f'''{subhero("About", C.H_ABOUT, C.ABOUT_LEAD)}
<section class="sec">
  <div class="wrap about">
    <div class="prose" data-reveal>{prose}</div>
    <div class="people" data-reveal>{leaders}</div>
  </div>
</section>
<section class="sec sec--alt">
  <div class="wrap">
    {sec_head("Process", C.H_ABOUT_ROUTE, C.ABOUT_ROUTE_INTRO)}
    {route()}
  </div>
</section>
<section class="sec">
  <div class="wrap">
    {sec_head("Customers", C.H_ABOUT_CUSTOMERS, C.ABOUT_CUSTOMERS_INTRO)}
    <ul class="custs">{customer_grid()}</ul>
    <div class="sec__more" data-reveal><a class="btn btn--ghost" href="customers.html#awards">Awards from our customers</a></div>
  </div>
</section>
{quality_glimpse()}
<section class="sec sec--alt">
  <div class="wrap">
    {sec_head("Principles", C.H_PILLARS)}
    <ul class="pillars">{pillars}</ul>
  </div>
</section>
<section class="sec">
  <div class="wrap">
    {sec_head("History", C.H_TIMELINE)}
    <ol class="tl">{tl}</ol>
  </div>
</section>
<section class="sec sec--alt" id="works">
  <div class="wrap">
    {sec_head("Our works", C.H_PLANTS, C.PLANTS_INTRO)}
    <div class="plants">{plants}</div>
  </div>
</section>
{cta()}'''
    return page("about.html", f"About | {C.NAME}",
                C.META["about"],
                body, "about.html")


def build_gallery():
    if C.GALLERY:
        shots = "".join(
            f'<figure class="shot" data-reveal><a href="assets/img/{s}.webp" data-lightbox>'
            f'{img(s, cap)}</a><figcaption>{cap}</figcaption></figure>'
            for s, cap in C.GALLERY)
        inner = f'<div class="masonry">{shots}</div>'
    else:
        frames = "".join(
            f'<figure class="frame" data-reveal style="--i:{i % 3}"><span>{t}</span></figure>'
            for i, t in enumerate(C.GALLERY_PLACEHOLDERS))
        inner = f'''<div class="empty" data-reveal>
  <h2 class="h3">{C.GALLERY_EMPTY_TITLE}</h2>
  <p>{C.GALLERY_EMPTY_TEXT}</p>
  <a class="btn btn--ghost" href="products.html">See our products</a>
</div>
<div class="frames">{frames}</div>'''
    body = f'''{subhero("Gallery", C.H_GALLERY, C.GALLERY_INTRO)}
<section class="sec"><div class="wrap">{inner}</div></section>
{cta()}'''
    return page("gallery.html", f"Gallery | {C.NAME}",
                C.META["gallery"],
                body, "gallery.html")


def build_contact():
    phones = "".join(f'<a class="link" href="tel:{tl}">+91 {ph}</a>' for ph, tl in C.PHONES)
    emails = "".join(f'<a class="link" href="mailto:{e}">{e}</a>' for e in C.EMAILS)
    plants = "".join(plant_card(p) for p in C.PLANTS)
    body = f'''{subhero("Contact", C.H_CONTACT, C.CONTACT_INTRO)}
<section class="sec">
  <div class="wrap contact">
    <div class="contact__form" data-reveal>{enquiry_form()}</div>
    <aside class="contact__side" data-reveal>
      <h2 class="h3">Talk to us</h2>
      <div class="contact__list">{phones}{emails}</div>
      <div class="contact__act">
        <a class="btn" href="https://wa.me/{C.WHATSAPP}?text={quote(C.WHATSAPP_TEXT)}" target="_blank" rel="noopener">{WA_GLYPH}WhatsApp us</a>
        <a class="btn btn--ghost" href="{esc(C.MAILTO)}">Email both inboxes</a>
      </div>
    </aside>
  </div>
</section>
<section class="sec sec--alt">
  <div class="wrap">
    {sec_head("Our works", C.H_PLANTS, C.PLANTS_INTRO)}
    <div class="plants">{plants}</div>
  </div>
</section>'''
    return page("contact.html", f"Contact | {C.NAME}",
                C.META["contact"], body, "contact.html")


def build_404():
    body = f'''{subhero("404", "That page is not here", "Try the products or send us your drawing.")}
<section class="sec"><div class="wrap"><a class="btn" href="index.html">Back to home</a></div></section>'''
    return page("404.html", f"Not found | {C.NAME}", C.META["404"], body, noindex=True)


if __name__ == "__main__":
    for fn in (build_home, build_products, build_capabilities,
               build_customers, build_about, build_gallery, build_contact, build_blog,
               build_404, build_discovery):
        print("wrote", fn())
