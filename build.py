#!/usr/bin/env python3
"""Generate the Vijayalakshmi Forge & Stamping site.

A generator only. Every human-readable string lives in content.py.

    python3 build.py

Writes .html into the repo root, which is what GitHub Pages serves.
"""
import hashlib
import html
import os
import re
from urllib.parse import quote

import content as C

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
_dims = {}


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
  <svg viewBox="0 0 24 24" aria-hidden="true" width="24" height="24"><path fill="currentColor" d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.32 4.95L2 22l5.25-1.38a9.9 9.9 0 0 0 4.79 1.22h.01c5.46 0 9.91-4.45 9.91-9.91 0-2.65-1.03-5.14-2.9-7.01A9.82 9.82 0 0 0 12.04 2Zm0 18.15h-.01a8.2 8.2 0 0 1-4.19-1.15l-.3-.18-3.12.82.83-3.04-.2-.31a8.18 8.18 0 0 1-1.26-4.38c0-4.54 3.7-8.24 8.25-8.24 2.2 0 4.27.86 5.83 2.42a8.19 8.19 0 0 1 2.41 5.83c0 4.54-3.69 8.23-8.24 8.23Zm4.52-6.16c-.25-.12-1.47-.72-1.69-.81-.23-.08-.39-.12-.56.13-.16.24-.64.8-.78.97-.15.16-.29.18-.53.06-.25-.12-1.05-.39-1.99-1.23-.74-.66-1.23-1.47-1.38-1.72-.14-.25-.01-.38.11-.5.11-.11.25-.29.37-.43.12-.15.16-.25.25-.41.08-.17.04-.31-.02-.43-.06-.12-.56-1.34-.76-1.84-.2-.48-.4-.42-.56-.43h-.47c-.17 0-.43.06-.66.31-.22.25-.86.85-.86 2.07 0 1.22.89 2.4 1.01 2.56.12.17 1.75 2.67 4.23 3.74.59.26 1.05.41 1.41.52.59.19 1.13.16 1.56.1.47-.07 1.47-.6 1.67-1.18.21-.58.21-1.07.15-1.18-.06-.1-.22-.16-.47-.28Z"/></svg>
</a>'''


def clean_urls(doc):
    """Link to /about rather than /about.html. GitHub Pages serves about.html
    for /about by itself; a local `python3 -m http.server` does not."""
    doc = re.sub(r'href="index\.html(?=[#"?])', 'href="./', doc)
    return re.sub(r'href="([a-z0-9-]+)\.html(?=[#"?])', r'href="\1', doc)


def page(path, title, description, body, current="", noindex=False):
    robots = "noindex, nofollow" if (C.NOINDEX or noindex) else "index, follow"
    doc = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<meta name="robots" content="{robots}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:type" content="website">
<meta name="theme-color" content="#1B1A6E">
<script>document.documentElement.classList.add("js")</script>
<link rel="icon" href="favicon.png" type="image/png">
<link rel="apple-touch-icon" href="favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@600;700;800&family=DM+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap">
<link rel="stylesheet" href="styles.css?v={CSS_V}">
</head>
<body>
{header(current)}
<main id="main">
{body}
</main>
{footer()}
<script src="script.js?v={JS_V}" defer></script>
</body>
</html>'''
    doc = clean_urls(doc)
    with open(os.path.join(ROOT, path), "w", encoding="utf-8") as fh:
        fh.write(doc)
    return path


# -------------------------------------------------------------- helpers ----

def sec_head(eyebrow, title, text="", mid=False):
    t = f'<p class="lede">{text}</p>' if text else ""
    return f'''<div class="sec__head{" sec__head--mid" if mid else ""}" data-reveal>
  <p class="eyebrow">{eyebrow}</p>
  <h2 class="h2">{title}</h2>
  {t}
</div>'''


def cta():
    return f'''
<section class="band">
  <div class="wrap band__in" data-reveal>
    <h2 class="h2">{C.CTA_TITLE}</h2>
    <p class="lede">{C.CTA_TEXT}</p>
    <div class="band__act">
      <a class="btn btn--light" href="contact.html#enquire">Send an enquiry</a>
      <a class="btn btn--ghost-light" href="https://wa.me/{C.WHATSAPP}?text={quote(C.WHATSAPP_TEXT)}"
         target="_blank" rel="noopener">WhatsApp +91 {C.PHONE}</a>
    </div>
  </div>
</section>'''


def subhero(eyebrow, title, text):
    return f'''
<section class="subhero">
  <div class="wrap subhero__in">
    <p class="eyebrow">{eyebrow}</p>
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
    opts = "".join(f'<option>{p["name"]}</option>' for p in C.PRODUCTS)
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
  <div class="wrap hero__in">
    <div class="hero__copy">
      <p class="hero__eyebrow">{C.HERO_EYEBROW}</p>
      <h1 class="hero__title"><span>{C.HERO_TITLE_A}</span> <em>{C.HERO_TITLE_B}</em></h1>
      <p class="hero__text">{C.HERO_TEXT}</p>
      <div class="hero__act">
        <a class="btn" href="contact.html#enquire">Send an enquiry</a>
        <a class="btn btn--ghost" href="products.html">See our products</a>
      </div>
      <ul class="hero__proof">{"".join(f"<li>{x}</li>" for x in C.HERO_PROOF)}</ul>
    </div>
    <div class="hero__shots" aria-hidden="true">{hero_shots}</div>
  </div>
</section>

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
        f'<tr><th scope="row">{n}</th><td class="mono">{s}</td><td>{d}</td></tr>'
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
        <a class="btn" href="https://wa.me/{C.WHATSAPP}?text={quote(C.WHATSAPP_TEXT)}" target="_blank" rel="noopener">WhatsApp us</a>
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
               build_customers, build_about, build_gallery, build_contact, build_404):
        print("wrote", fn())
