"""Every human-readable string on the Vijayalakshmi Forge & Stamping site.

build.py is a generator and holds no copy. Every fact here comes from the
company's own posters (products, quality, customers, certificates, awards,
infrastructure, about). Nothing is invented; what is missing is listed in
TODO_CLIENT.md.
"""

# ------------------------------------------------------------------ brand ----
NAME = "Vijayalakshmi Forge & Stamping"
SHORT = "VLF"
TAB_NAME = "Vijayalakshmi Forge & Stamping"
DOMAIN = "vijlakforge.com"
SITE_URL = "https://vijlakforge.com"
SINCE = 1988
CERT = "ISO 9001:2015"
BRAND_SUB = "Ambattur, Chennai · Since 1988"
TAGLINE = "Forged by trust. Stamped with excellence."
GROUP_TAG = "Precision | Performance | Perfection"

# False until the domain is live and the owner approves; true keeps it out of
# search engines while it is still a preview.
NOINDEX = True

# --------------------------------------------------------------- contacts ----
# Phones and emails exactly as printed on the company's own poster.
PHONES = [("98404 07255", "+919840407255"), ("98403 24470", "+919840324470")]
PHONE, PHONE_LINK = PHONES[0]
WHATSAPP = "919840407255"
ENQUIRY_TO = "vijakunit2@gmail.com"
ENQUIRY_CC = ["kkindustries.58@gmail.com"]
EMAILS = [ENQUIRY_TO] + ENQUIRY_CC
FORM_ENDPOINT = "https://formsubmit.co/ajax/" + ENQUIRY_TO
MAILTO = ("mailto:" + ",".join(EMAILS)
          + "?subject=Enquiry%20from%20the%20website")
WHATSAPP_TEXT = ("Hello Vijayalakshmi Forge & Stamping, I would like to "
                 "enquire about forged and machined components. Please let me "
                 "know a convenient time to discuss.")

# name, role, display phone, tel link
LEADERS = [
    ("Mr. A. Kumar", "Managing Director and founder, 1988"),
    ("Mr. R. Ganesh", "GM, Operations"),
]

# slug, name, role, address lines, scope, certificate, map query
PLANTS = [
    ("plant-1", "Plant I", "Forging and machining",
     ["No. 18, 2nd Street", "TASS Industrial Estate", "Ambattur, Chennai 600 098",
      "Tamil Nadu"],
     "Manufacture and supply of hot forged and machined steel components.",
     "Intertek ISO 9001:2015, certificate ICH-0246.12",
     "Valid to 21 August 2027",
     "18 2nd Street TASS Industrial Estate Ambattur Chennai 600098"),
    ("plant-2", "Plant II", "Hot forging",
     ["G-50, SIDCO Industrial Estate", "Kakkalur", "Thiruvallur 602 003",
      "Tamil Nadu"],
     "Hot forged components for automobile and other engineering industries.",
     "Intertek ISO 9001:2015, certificate 0007923",
     "Valid to 24 November 2028",
     "G-50 SIDCO Industrial Estate Kakkalur Thiruvallur 602003"),
    ("kk", "K.K. Industries", "Precision machining, our sister concern",
     ["SP 48, 3rd Main Road", "Ambattur Industrial Estate",
      "Chennai 600 058", "Tamil Nadu"],
     "Manufacture and supply of machined metal components.",
     "TUV SUD ISO 9001:2015, registration 99 100 03387",
     "Valid 16 December 2025 to 15 December 2028",
     "SP 48 3rd Main Road Ambattur Industrial Estate Chennai 600058"),
]

NAV = [
    ("products.html", "Products"),
    ("capabilities.html", "Capabilities"),
    ("customers.html", "Customers"),
    ("about.html", "About"),
    ("gallery.html", "Gallery"),
]
CONTACT_PAGE = ("contact.html", "Contact")

# ------------------------------------------------------------------- home ----
HERO_EYEBROW = "Ambattur, Chennai · ISO 9001:2015 · Since 1988"
HERO_TITLE_A = "The best forge and stamping"
HERO_TITLE_B = "works in Ambattur."
HERO_PROOF = ["3 ISO 9001:2015 certificates", "Supplier awards from MEI, TIDC and Sundram", "Forging since 1988"]
HERO_TEXT = ("Vijayalakshmi Forge and Stamping forges carbon, alloy and "
             "stainless steel into heavy conveyor chains, earth-moving spares "
             "and concrete-mixer parts. Hot forged at two plants, machined and "
             "inspected before it ships.")
HERO_IMAGES = ["p-chain-02", "p-under-05", "p-mixer-08", "p-under-01"]

STATS = [
    ("1988", "", "Founded in Chennai"),
    ("3.5", " ton", "Forging hammer"),
    ("3", "", "Works across two districts"),
    ("2015", "", "ISO 9001 certified"),
]

H_PRODUCTS = "What we forge"
PRODUCTS_HOME_INTRO = ("Four product families, forged and machined to the "
                       "customer's drawing.")
H_CAPS_HOME = "From billet to finished part"
CAPS_HOME_INTRO = ("Cutting, hot forging, machining and inspection run "
                   "under the same management.")
H_CUSTOMERS = "Trusted by industry names"
CUSTOMERS_INTRO = ("Chain, valve, wheel and equipment makers we supply "
                   "forged and machined parts to.")
H_PLANTS_HOME = "Three works, one standard"

# ---------------------------------------------------------------- products ----
# slug, name, one-liner, long text, image prefix, count, alt
PRODUCTS = [
    {"slug": "conveyor-chains", "name": "Heavy conveyor chains",
     "short": "Industrial chains engineered for long-lasting performance.",
     "body": ["Vijayalakshmi Forge and Stamping is a trusted manufacturer of "
              "superior-quality industrial heavy conveyor chains.",
              "Forged block-type chains, drag and scraper links, attachment "
              "links and side bars, made to run in the dust, load and impact "
              "of cement, mining and bulk-handling lines."],
     "images": [f"p-chain-{i:02d}" for i in range(1, 10)],
     "alt": "Forged conveyor chain component",
     "points": ["Forged block-type chains", "Drag and scraper chain links",
                "Attachment links and side bars", "Made to the customer's drawing"]},
    {"slug": "mixer-spares", "name": "Concrete mixer spares",
     "short": "Machinery spares that meet industry standards and performance requirements.",
     "body": ["We specialise in high-quality manufacturing of concrete mixer "
              "machinery spares that meet industry standards and performance "
              "requirements.",
              "Rollers, eye bolts, wear plates, rings and pump clamps and "
              "couplings, supplied to builders of truck mixers and concrete "
              "pumps."],
     "images": [f"p-mixer-{i:02d}" for i in range(1, 10)],
     "alt": "Forged concrete mixer spare",
     "points": ["Rollers and rings", "Eye bolts and wear plates",
                "Pump clamps and couplings", "Supplied to Schwing Stetter"]},
    {"slug": "undercarriage", "name": "Excavator and loader undercarriage",
     "short": "Unmatched quality in undercarriage parts for excavators and loaders.",
     "body": ["Explore unmatched quality in undercarriage parts for "
              "excavators and loaders.",
              "Hydraulic cylinders, rod ends and clevis ends, bushes and "
              "sprockets in many sizes, forged, machined and checked "
              "dimension by dimension."],
     "images": [f"p-under-{i:02d}" for i in range(1, 13)],
     "alt": "Forged and machined undercarriage part",
     "points": ["Hydraulic cylinders", "Rod ends, eyes and clevis ends",
                "Bushes and housings", "Sprockets in many sizes"]},
    {"slug": "earth-moving", "name": "Earth-moving replacement spares",
     "short": "All kinds of heavy earth-moving equipment replacement spares under one roof.",
     "body": ["One source for the replacement spares a heavy earth-moving "
              "fleet keeps asking for: sprockets, idlers, rings and the "
              "forged parts around them.",
              "Built to the original drawing, machined to size, and "
              "inspected before dispatch."],
     "images": ["p-under-04", "p-under-06", "p-under-12", "p-mixer-06"],
     "alt": "Replacement spare for heavy earth-moving equipment",
     "points": ["Sprockets and idlers", "Rings and discs",
                "Built to the original drawing", "Machined and inspected"]},
]
PRODUCTS_PAGE_INTRO = ("Four families of forged and machined parts. Send a "
                       "drawing, a sample or a part number and we will quote.")
H_PRODUCTS_PAGE = "Products"

# -------------------------------------------------------------- capability ----
CHAIN = [
    # step, what happens, the figure that goes with it
    ("Raw material", "Carbon, alloy and stainless steel, carefully selected for reliable component performance.", "3 steel families"),
    ("Cutting", "Bandsaw cutting and shearing bring bar down to forging size.", "Up to 350 mm"),
    ("Hot forging", "Hammer forging with controlled processes for strength, accuracy and consistency.", "Up to 3.5 ton hammer"),
    ("Machining", "CNC and VMC machining to meet critical dimensional requirements.", "CNC and VMC"),
    ("Inspection", "Systematic inspection at every critical stage, backed by an in-house lab and MPI.", "MPI and lab"),
    ("Dispatch", "Reliable components manufactured to customer specifications, delivered on time.", "To your drawing"),
]
EQUIPMENT = [
    ("Bandsaw cutting", "Up to 350 mm", "Cuts bar and billet to forging weight"),
    ("Shearing", "Up to 125 mm", "Fast cutting of smaller sections"),
    ("Forging hammer", "Up to 3.5 ton", "Hot forging of heavy components"),
    ("Bogie and bell furnace", "Heat", "Heating and thermal processing of forgings"),
    ("Shotblasting", "Finish", "Cleans scale from forged parts"),
    ("CNC and VMC", "Machining", "Turning and milling to drawing"),
    ("MPI", "Inspection", "Magnetic particle inspection for surface defects"),
    ("Lab facility", "Testing", "Hardness testing and metallurgical microscope"),
]
H_CAPS = "Capabilities"
CAPS_INTRO = ("Forging, machining and inspection under one management, so a "
              "part does not change hands between steps.")
CAPS_NOTE = ("Photographs of our own plant are on their way. Until then this "
             "page lists what we run, in words.")
H_CHAIN = "The route a part takes"
H_EQUIP = "Equipment and facilities"

# ----------------------------------------------------------------- quality ----
QUALITY_POINTS = [
    ("Quality raw material", "Carefully selected materials for reliable component performance."),
    ("Precision forging", "Controlled forging processes for strength, accuracy and consistency."),
    ("Accurate machining", "Precision machining to meet critical dimensional requirements."),
    ("Strict inspection", "Systematic inspection at every critical stage of production."),
    ("Consistent quality", "Reliable components manufactured to customer specifications."),
]
QUALITY_HOME = [
    ("ISO 9001:2015", "Certified at all three works"),
    ("Inspected", "At every critical stage"),
    ("Awarded", "Supplier awards since 2007"),
]
H_QUALITY = "Quality is our standard"
H_QUALITY_GLIMPSE = "A glimpse of how we hold quality"
QUALITY_GLIMPSE_INTRO = "Five standards on every order, and the certificates to show for it."
H_ABOUT_CUSTOMERS = "Where our parts go"
ABOUT_CUSTOMERS_INTRO = "The makers of chains, wheels, valves and equipment that fit our forged and machined parts."
H_ABOUT_ROUTE = "How a part is made"
ABOUT_ROUTE_INTRO = "From bar to finished part, under one management."
QUALITY_INTRO = ("Three works, three ISO 9001:2015 certificates, and the "
                 "awards our customers have given us.")
H_CERTS = "Certified for quality"
CERTS = [
    # image slug, title, number, body, scope, dates
    ("cert-intertek-1", "Vijayalakshmi Forge & Stamping, Plant I", "ICH-0246.12",
     "Intertek, UKAS accredited",
     "Manufacture and supply of hot forged and machined steel components",
     "First certified 11 August 2006. Valid to 21 August 2027"),
    ("cert-intertek-2", "Vijayalakshmi Forge & Stamping, Plant II", "0007923",
     "Intertek, UKAS accredited",
     "Manufacturing of hot forged component for automobile and other engineering industries",
     "First certified 25 November 2013. Valid to 24 November 2028"),
    ("cert-tuv", "K.K. Industries", "99 100 03387",
     "TUV SUD South Asia, NABCB accredited",
     "Manufacture and supply of machined metal components",
     "First certified 28 December 2007. Valid 16 December 2025 to 15 December 2028"),
]

# ---------------------------------------------------------------- customers ----
# name, logo file in assets/img
CUSTOMERS = [
    ("TI India", "cu-ti"), ("Wheels India Limited", "cu-wheels"),
    ("Essae", "cu-essae"), ("MEI", "cu-mei"),
    ("Schwing Stetter", "cu-schwing"), ("Flowserve", "cu-flowserve"),
    ("Burder AG Attachments", "cu-burder"), ("Texel", "cu-texel"),
]
H_AWARDS = "Recognition from our customers"
AWARDS_INTRO = "Awards given to us for quality and supply."
# image, title, giver, year
AWARDS = [
    ("aw-mei-2015", "Quality Excellence Award", "Madras Engineering Industries Pvt. Ltd.", "2015",
     "For achieving a low defect rate, as per MEIL norms"),
    ("aw-sundaram-trophy", "Best Supplier of the Year", "Sundaram Fasteners Ltd.", "2007",
     "In two categories: forged components"),
    ("aw-sundaram-plaque", "Best Supplier of the Year", "Sundram Fasteners Ltd.", "2007",
     "In recognition of quality and delivery performance"),
    ("aw-tidc-sprockets", "Best Supplier for Sprockets", "TIDC India", "",
     "Trophy"),
    ("aw-tidc-cert", "Best Supplier Award", "TIDC India", "2020-21",
     "Sprockets supplied to Industrial Chains, Plant 3"),
    ("aw-mei-2021", "Supplier Quality Excellence Award", "Madras Engineering Industries Pvt. Ltd.", "2021-22",
     "Best supplier for the year"),
]

# -------------------------------------------------------------------- about ----
H_ABOUT = "About us"
ABOUT_LEAD = ("Vijayalakshmi Forge and Stamping is an ISO 9001:2015 certified "
              "Chennai company that forges carbon, alloy and stainless steel.")
ABOUT_BODY = [
    "It was established by Mr. A. Kumar in 1988 and has grown into a well "
    "known name for precision, perfection and performance.",
    "Today the company is led by Mr. A. Kumar, Managing Director, with the "
    "support of experienced operational leadership, including Mr. R. Ganesh, "
    "GM, Operations.",
    "Alongside the two forging plants, our sister concern K.K. Industries "
    "machines components in Ambattur, so forged parts can be finished and "
    "inspected close by.",
]
H_PLANTS = "Our works"
PLANTS_INTRO = "Two forging plants and a machining unit, all certified to ISO 9001:2015."
PILLARS = [
    ("Strength", "Components engineered for strength, durability and dimensional precision."),
    ("End to end", "From hot forging to precision machining, solutions tailored to your requirement."),
    ("Dependable", "Consistent quality across a wide range of industrial applications."),
]
H_PILLARS = "What we hold to"

# Dates are the ones printed on the certificates, awards and posters.
H_TIMELINE = "Our timeline"
TIMELINE = [
    ("1988", "Founded in Chennai by Mr. A. Kumar"),
    ("2006", "Plant I first certified to ISO 9001"),
    ("2007", "K.K. Industries certified. Best Supplier of the Year, Sundaram Fasteners"),
    ("2013", "Plant II first certified to ISO 9001"),
    ("2015", "Quality Excellence Award, Madras Engineering Industries"),
    ("2020", "Best Supplier Award, TIDC India"),
    ("2022", "Supplier Quality Excellence Award, Madras Engineering Industries"),
]

# ------------------------------------------------------------------ gallery ----
H_GALLERY = "Gallery"
GALLERY_INTRO = "Photographs of our plants and our work."
GALLERY_EMPTY_TITLE = "Plant photographs are on their way"
GALLERY_EMPTY_TEXT = ("We are gathering photographs of the forging shop, the "
                      "machining floor and the lab. They will appear here. "
                      "Meanwhile, see the parts we make.")
# (slug, caption) once real photographs arrive. See media.py.
GALLERY = []
GALLERY_PLACEHOLDERS = ["Forging shop", "Hammer line", "Machining floor",
                        "Inspection and lab", "Furnace", "Dispatch"]

# ------------------------------------------------------------------ contact ----
H_CONTACT = "Contact"
CONTACT_INTRO = "Send a drawing, a sample or a part number. We will reply with a quote."
CTA_TITLE = "Have a drawing or a part number?"
CTA_TEXT = "Send it across. We will quote against your drawing."
RFQ_NOTE = "Send a drawing or a photograph of the part and we will quote."
THANKS_TITLE = "Thanks for reaching out"
THANKS_TEXT = ("We have your details and will get back to you soon. For "
               "anything urgent, call +91 98404 07255.")
THANKS_AGAIN = "Send another enquiry"
SENT_TEXT = "Thanks. We have your enquiry and will call you soon."
FAIL_TEXT = ("We could not send that just now. Please call or WhatsApp us "
             "on +91 98404 07255.")
FOOTER_NOTE = "Preview build. Not yet public."
SHOW_PREVIEW_NOTE = True

META = {
    "index": 'Hot forged and machined steel components from Ambattur, Chennai: heavy conveyor chains, earth-moving spares and concrete mixer parts. ISO 9001:2015, since 1988.',
    "products": 'Heavy conveyor chains, concrete mixer spares, excavator and loader undercarriage parts and earth-moving replacement spares, forged in Chennai.',
    "capabilities": 'Bandsaw cutting to 350 mm, hammer forging to 3.5 ton, CNC and VMC machining, MPI and an in-house lab.',
    "customers": 'Customers include TI India, Wheels India, MEI, Schwing Stetter and Flowserve, with supplier awards since 2007.',
    "about": 'A Chennai forging company founded in 1988 by Mr. A. Kumar, with two forging plants and a machining sister concern in Ambattur.',
    "gallery": 'Photographs of the forging shop, machining floor and lab.',
    "contact": 'Send a drawing or a part number to Vijayalakshmi Forge and Stamping and get a quote.',
    "404": 'Page not found.',
}
