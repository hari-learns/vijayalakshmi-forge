/* Vijayalakshmi Forge & Stamping. One IIFE; every feature is guarded so the
   same file loads safely on every page. */
(function () {
  "use strict";

  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) {
    return Array.prototype.slice.call((r || document).querySelectorAll(s));
  };

  /* ---------------------------------------------------- sticky header --- */
  var hdr = $("[data-header]");
  if (hdr) {
    var ticking = false;
    var lastY = window.scrollY;
    var onScroll = function () {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(function () {
        var y = window.scrollY;
        hdr.classList.toggle("is-stuck", y > 40);
        // Reading down, the page links fold into the Contact button; any move
        // back up unfolds them. The bar itself stays.
        var dr = $("[data-drawer]");
        var open = dr && dr.classList.contains("is-open");
        if (y < 120 || open) hdr.classList.remove("is-tucked");
        else if (y > lastY + 6) hdr.classList.add("is-tucked");
        else if (y < lastY - 6) hdr.classList.remove("is-tucked");
        if (Math.abs(y - lastY) > 6 || y < 120) lastY = y;
        ticking = false;
      });
    };
    window.addEventListener("scroll", onScroll, { passive: true });
    hdr.addEventListener("focusin", function () { hdr.classList.remove("is-tucked"); });
    onScroll();
  }

  /* ---------------------------------------------------- mobile drawer --- */
  var drawer = $("[data-drawer]");
  var burger = $("[data-burger]");
  if (drawer && burger) {
    var setDrawer = function (open) {
      drawer.classList.toggle("is-open", open);
      burger.setAttribute("aria-expanded", String(open));
      document.documentElement.style.overflow = open ? "hidden" : "";
      if (open) { var f = $("a", drawer); if (f) f.focus(); }
      else burger.focus();
    };
    burger.addEventListener("click", function () {
      setDrawer(!drawer.classList.contains("is-open"));
    });
    var x = $("[data-drawer-close]", drawer);
    if (x) x.addEventListener("click", function () { setDrawer(false); });
    $$("a", drawer).forEach(function (a) {
      a.addEventListener("click", function () { setDrawer(false); });
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && drawer.classList.contains("is-open")) setDrawer(false);
    });
  }

  /* ---------------------------------------------------------- reveals --- */
  var reveals = $$("[data-reveal]");
  if (reveals.length) {
    var activate = function (el) { el.classList.add("is-in"); };
    if (reduced || !("IntersectionObserver" in window)) {
      reveals.forEach(activate);
    } else {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          if (en.isIntersecting) { activate(en.target); io.unobserve(en.target); }
        });
      }, { threshold: 0.1, rootMargin: "0px 0px -8% 0px" });
      reveals.forEach(function (el) { io.observe(el); });

      /* Safety net: an IntersectionObserver that never fires (hidden tab,
         anchor jump, restored scroll) must not strand content at opacity 0. */
      var sweep = function () {
        var h = window.innerHeight || document.documentElement.clientHeight;
        reveals.forEach(function (el) {
          if (el.classList.contains("is-in")) return;
          if (el.getBoundingClientRect().top < h * 0.96) activate(el);
        });
      };
      ["load", "scroll", "resize", "pageshow"].forEach(function (ev) {
        window.addEventListener(ev, sweep, { passive: true });
      });
      setTimeout(sweep, 350);
      sweep();
    }
  }


  /* ------------------------------------------------ route chart, on scroll --- */
  /* The line and the steps fill as the section scrolls into view. Progress is
     measured from the element's own position, so it runs backwards too. */
  $$("[data-route]").forEach(function (route) {
    var steps = $$(".rstep", route);
    var update = function () {
      var r = route.getBoundingClientRect();
      var vh = window.innerHeight || document.documentElement.clientHeight;
      var span = Math.max(r.height, vh * 0.4);
      var p = reduced ? 1 : Math.min(1, Math.max(0, (vh * 0.72 - r.top) / span));
      route.style.setProperty("--p", p.toFixed(3));
      var a = steps[0].getBoundingClientRect(), b = steps[steps.length - 1].getBoundingClientRect();
      var vertical = Math.abs(b.top - a.top) > Math.abs(b.left - a.left);
      steps.forEach(function (s) {
        var n = $(".rstep__node", s).getBoundingClientRect();
        var f = vertical ? (n.top + n.height / 2 - (a.top + 28)) / Math.max(1, b.top - a.top)
                         : (n.left + n.width / 2 - (a.left + a.width / 2)) / Math.max(1, b.left - a.left);
        s.classList.toggle("is-on", p >= f - 0.001 && p > 0);
      });
    };
    // cheap enough to run on every scroll event; no frame callback, which a
    // background tab would never deliver
    var tick = update;
    ["scroll", "resize", "load", "pageshow"].forEach(function (ev) {
      window.addEventListener(ev, tick, { passive: true });
    });
    update();
  });

  /* --------------------------------------------- loader and page change --- */
  /* The loader is a CSS timeline (styles.css); this only tidies it away.
     Leaving for another page of the site, the press shutter closes, and the
     next page opens it (html.pt-in, set in <head>). */
  var root = document.documentElement;
  if (root.classList.contains("ld")) {
    setTimeout(function () { var l = $("#ld"); if (l) l.remove(); }, 4100);
  }
  var pt = $("#pt");
  var internal = function (a) {
    if (!a || a.target === "_blank" || a.hasAttribute("download")) return false;
    var href = a.getAttribute("href") || "";
    if (!href || href.charAt(0) === "#" || /^(mailto|tel):/.test(href)) return false;
    var u;
    try { u = new URL(a.href, location.href); } catch (e) { return false; }
    if (u.origin !== location.origin) return false;
    if (u.pathname === location.pathname && u.search === location.search) return false;
    return true;
  };
  if (pt && !reduced) {
    document.addEventListener("click", function (e) {
      if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
      var a = e.target.closest && e.target.closest("a");
      if (!internal(a)) return;
      e.preventDefault();
      try { sessionStorage.setItem("vlf-pt", "1"); } catch (x) { /* private mode */ }
      pt.classList.add("go");
      setTimeout(function () { location.href = a.href; }, 620);
    });
  }
  /* Back and forward restore the page from memory: open the shutter again */
  window.addEventListener("pageshow", function (e) {
    if (e.persisted && pt) pt.classList.remove("go");
  });
  /* fetch a page as soon as the pointer or a finger heads for its link, so it
     is ready when the shutter opens (browsers without speculation rules) */
  var warmed = {};
  var warm = function (e) {
    var a = e.target.closest && e.target.closest("a");
    if (!internal(a) || warmed[a.href]) return;
    warmed[a.href] = 1;
    var l = document.createElement("link");
    l.rel = "prefetch"; l.href = a.href;
    document.head.appendChild(l);
  };
  document.addEventListener("pointerover", warm, { passive: true });
  document.addEventListener("touchstart", warm, { passive: true });

  /* ------------------------------------------------------------ finder --- */
  /* The buyer describes the part in their own words; the page names the
     families that make it, says why, and writes the quote message. Nothing
     is sent from here: the buttons open WhatsApp or the quote form. */
  var fform = $("[data-finder]");
  var fdata = $("#vlf-finder");
  if (fform && fdata) {
    var F = JSON.parse(fdata.textContent);
    var said = $("[data-fsaid]"), res = $("[data-fres]"), sum = $("[data-fsum]");
    var txt = $("[data-ftxt]"), fwa = $("[data-fwa]"), fto = $("[data-fform]");
    var escH = function (t) {
      return String(t).replace(/[&<>"]/g, function (c) {
        return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
      });
    };
    var norm = function (t) { return " " + t.toLowerCase().replace(/[^a-z0-9]+/g, " ") + " "; };
    var vals = function () {
      var d = new FormData(fform), o = {};
      ["free", "use", "material", "have"].forEach(function (k) { o[k] = (d.get(k) || "").toString().trim(); });
      return o;
    };
    var useName = function (slug) {
      var opt = $('select[name="use"] option[value="' + slug + '"]', fform);
      return opt ? opt.textContent : "";
    };
    var match = function (v) {
      var words = norm(v.free);
      var scored = F.families.map(function (f) {
        var hits = f.words.filter(function (w) { return words.indexOf(" " + w + " ") > -1 || words.indexOf(" " + w + "s ") > -1; });
        var score = hits.length * 2 + (v.use === f.slug ? 3 : 0);
        return { f: f, hits: hits, score: score };
      }).filter(function (r) { return r.score > 0; });
      scored.sort(function (a, b) { return b.score - a.score; });
      return scored;
    };
    var message = function (v, list) {
      var L = F.labels, lines = [F.intro];
      if (v.free) lines.push(L.free + ": " + v.free);
      if (v.use) lines.push(L.use + ": " + useName(v.use));
      if (list.length) lines.push(L.range + ": " + list.map(function (r) { return r.f.name; }).join(", "));
      if (v.material && v.material !== "Not sure yet") lines.push(L.material + ": " + v.material);
      if (v.have) lines.push(L.have + ": " + v.have);
      return lines.filter(Boolean).join("\n");
    };
    var formLink = function (v, slug) {
      var q = new URLSearchParams();
      if (slug) q.set("family", slug);
      if (v.free) q.set("part", v.free);
      if (v.material && v.material !== "Not sure yet") q.set("material", v.material);
      if (v.have) q.set("have", v.have);
      return fto.getAttribute("href").split("?")[0].split("#")[0] + "?" + q.toString() + "#enquire";
    };
    var card = function (r, i, v) {
      var f = r.f, why = r.hits.length ? "Fits: " + r.hits.slice(0, 3).join(", ") : (v.use === f.slug ? "Fits: " + useName(f.slug).toLowerCase() : "");
      return '<article class="fcard" style="--i:' + i + '">' +
        '<h3 class="fcard__t">' + escH(f.name) + "</h3>" +
        (why ? '<p class="fcard__why">' + escH(why) + "</p>" : "") +
        '<dl class="fcard__facts">' +
        "<div><dt>" + F.facts[0] + "</dt><dd>" + escH(f.points.map(function (t, k) {
          return k ? t.charAt(0).toLowerCase() + t.slice(1) : t;
        }).join(", ")) + "</dd></div>" +
        "<div><dt>" + F.facts[1] + "</dt><dd>" + escH(F.made) + "</dd></div>" +
        "<div><dt>" + F.facts[2] + "</dt><dd>" + escH(v.material && v.material !== "Not sure yet" ? v.material : F.steel) + "</dd></div>" +
        "<div><dt>" + F.facts[3] + "</dt><dd>" + escH(v.have || F.from) + "</dd></div></dl>" +
        '<div class="fcard__img"><img src="' + f.img + '" alt="' + escH(f.name) + '" loading="lazy"></div>' +
        '<div class="fcard__act"><a class="btn btn--sm" href="' + formLink(v, f.slug) + '">' + F.quote + "</a>" +
        '<a class="link" href="products.html#' + f.slug + '">' + F.details + "</a></div></article>";
    };
    var run = function (force) {
      var v = vals();
      var active = force || v.free || v.use;
      if (!active) { res.innerHTML = ""; sum.hidden = true; said.textContent = ""; return; }
      var list = match(v);
      var loose = !list.length;
      if (loose) list = F.families.map(function (f) { return { f: f, hits: [], score: 0 }; });
      var bits = [];
      if (v.free) bits.push("<b>" + escH(v.free) + "</b>");
      if (v.use) bits.push("for <b>" + escH(useName(v.use).toLowerCase()) + "</b>");
      if (v.material && v.material !== "Not sure yet" && v.free.toLowerCase().indexOf(v.material.toLowerCase()) < 0) {
        bits.push("in <b>" + escH(v.material.toLowerCase()) + "</b>");
      }
      said.innerHTML = loose ? escH(F.none) :
        "Looking for " + bits.join(" ") + ". " + (list.length === 1 ? "One line makes this." : list.length + " lines make parts like this.");
      res.innerHTML = list.map(function (r, i) { return card(r, i, v); }).join("");
      var msg = message(v, loose ? [] : list);
      txt.textContent = msg;
      fwa.href = "https://wa.me/" + F.wa + "?text=" + encodeURIComponent(msg);
      fto.href = formLink(v, list.length === 1 ? list[0].f.slug : "");
      sum.hidden = false;
    };
    var timer = 0;
    fform.addEventListener("input", function () { clearTimeout(timer); timer = setTimeout(run, 260); });
    fform.addEventListener("change", function () { run(); });
    fform.addEventListener("submit", function (e) {
      e.preventDefault();
      run(true);
      res.scrollIntoView({ behavior: reduced ? "auto" : "smooth", block: "nearest" });
    });
  }

  /* ------------------------------------- quote form, filled from the finder --- */
  var qf = $("[data-enquiry]");
  if (qf && location.search) {
    var q = new URLSearchParams(location.search);
    var sel = $('select[name="product"]', qf), fam = q.get("family");
    var opt = sel && fam && sel.querySelector('option[data-slug="' + fam.replace(/[^a-z-]/g, "") + '"]');
    if (opt) opt.selected = true;
    var mat = $('input[name="material"]', qf);
    if (mat && q.get("material")) mat.value = q.get("material");
    var msgEl = $('textarea[name="message"]', qf);
    var parts = [];
    if (q.get("part")) parts.push(q.get("part"));
    if (q.get("have")) parts.push("I can send: " + q.get("have"));
    if (msgEl && parts.length && !msgEl.value) msgEl.value = parts.join("\n");
  }

  /* -------------------------------------------------------- validation --- */
  /* Indian numbers may be 10 digits, +91 and 10 digits, or 0 and 10 digits
     for a landline with its STD code; a leading + with another country code
     needs 8 to 15 digits. Only digits, spaces, + and - can be typed. */
  var phoneOk = function (v) {
    v = v.trim();
    if (!/^\+?[\d\s-]+$/.test(v)) return false;
    var d = v.replace(/\D/g, "");
    if (v.charAt(0) === "+" && d.slice(0, 2) !== "91") return d.length >= 8 && d.length <= 15;
    if (d.length === 12 && d.slice(0, 2) === "91") d = d.slice(2);
    else if (d.length === 11 && d.charAt(0) === "0") d = d.slice(1);
    return d.length === 10 && /^[2-9]/.test(d) && !/^(\d)\1{9}$/.test(d);
  };
  var emailOk = function (v) {
    return /^[^\s@]+@[^\s@.]+(\.[^\s@.]+)+$/.test(v.trim()) && !/\.\./.test(v);
  };
  var nameOk = function (v) { return (v.match(/[A-Za-z஀-௿]/g) || []).length >= 2; };
  var RULES = {
    phone: [phoneOk, "Enter a valid phone number, e.g. 98400 12345 or +91 98400 12345."],
    email: [emailOk, "Enter a valid email address, e.g. name@company.com."],
    name: [nameOk, "Enter your name."]
  };
  var errFor = function (input) {
    var host = input.closest("label") || input.parentNode;
    var e = host.querySelector(".field__err");
    if (!e) {
      e = document.createElement("span");
      e.className = "field__err";
      e.id = "err-" + Math.random().toString(36).slice(2);
      e.setAttribute("role", "alert");
      host.appendChild(e);
      input.setAttribute("aria-describedby", e.id);
    }
    return e;
  };
  var check = function (input, loud) {
    var rule = RULES[input.name];
    var v = input.value;
    var bad = "";
    if (!v.trim()) { if (input.required) bad = rule ? rule[1] : "This field is required."; }
    else if (rule && !rule[0](v)) bad = rule[1];
    input.setCustomValidity(bad);
    input.classList.toggle("is-bad", !!bad && loud);
    input.setAttribute("aria-invalid", bad && loud ? "true" : "false");
    var e = errFor(input);
    e.textContent = loud ? bad : "";
    e.hidden = !(bad && loud);
    return !bad;
  };
  var FIELDS = 'input[name="phone"],input[name="email"],input[name="name"]';
  var guard = function (root) {
    $$(FIELDS, root).forEach(function (input) {
      if (input.name === "phone") {
        input.addEventListener("input", function () {
          var c = input.value.replace(/[^\d\s+-]/g, "").replace(/(?!^)\+/g, "");
          if (c !== input.value) input.value = c;
        });
      }
      input.addEventListener("blur", function () { if (input.value) check(input, true); });
      input.addEventListener("input", function () {
        if (input.classList.contains("is-bad")) check(input, true);
      });
    });
  };
  var validate = function (root) {
    var first = null;
    $$(FIELDS, root).forEach(function (input) {
      if (!check(input, true) && !first) first = input;
    });
    if (first) first.focus();
    return !first;
  };

  /* --------------------------------------------------------- delivery --- */
  /* An email through FormSubmit to the company inbox, copied to the second
     inbox. Resolves true when FormSubmit confirms it, false otherwise. */
  var LABELS = {
    name: "Name", company: "Company", phone: "Phone", email: "Email",
    product: "Product", material: "Material", quantity: "Quantity",
    message: "Details", page: "Sent from"
  };
  function deliver(payload, opts) {
    opts = opts || {};
    if (!opts.endpoint) return Promise.resolve(false);
    var fd = new FormData();
    var who = payload.name || payload.phone || "website visitor";
    fd.append("_subject", "Enquiry from " + who + (payload.company ? ", " + payload.company : ""));
    fd.append("_template", "table");
    fd.append("_captcha", "false");
    if (opts.cc) fd.append("_cc", opts.cc);
    if (payload.email) fd.append("_replyto", payload.email);
    Object.keys(LABELS).forEach(function (k) {
      var v = (payload[k] || "").toString().trim();
      if (v) fd.append(LABELS[k], v);
    });
    if (opts.file) fd.append("attachment", opts.file, opts.file.name);
    return fetch(opts.endpoint, {
      method: "POST", headers: { "Accept": "application/json" }, body: fd
    }).then(function (r) { return r.json(); })
      .then(function (j) { return j && (j.success === true || j.success === "true"); })
      .catch(function () { return false; });
  }

  /* ----------------------------------------------------------- lightbox --- */
  (function () {
    var links = $$("[data-lightbox]");
    if (!links.length) return;
    var box = document.createElement("div");
    box.className = "lb";
    box.hidden = true;
    box.setAttribute("role", "dialog");
    box.setAttribute("aria-modal", "true");
    box.setAttribute("aria-label", "Image viewer");
    box.innerHTML =
      '<figure class="lb__fig"><img class="lb__img" alt=""><figcaption class="lb__cap"></figcaption></figure>' +
      '<button class="lb__btn lb__x" type="button" aria-label="Close">&times;</button>' +
      '<button class="lb__btn lb__prev" type="button" aria-label="Previous">&lsaquo;</button>' +
      '<button class="lb__btn lb__next" type="button" aria-label="Next">&rsaquo;</button>' +
      '<p class="lb__n" aria-live="polite"></p>';
    document.body.appendChild(box);
    var im = $(".lb__img", box), cap = $(".lb__cap", box), num = $(".lb__n", box);
    var at = 0, back = null;
    var show = function (i) {
      at = (i + links.length) % links.length;
      var a = links[at], pic = $("img", a);
      im.src = a.getAttribute("href");
      im.alt = pic ? pic.alt : "";
      var fc = a.parentNode.querySelector("figcaption");
      cap.textContent = fc ? fc.textContent : (pic ? pic.alt : "");
      num.textContent = (at + 1) + " / " + links.length;
    };
    var open = function (i) {
      back = document.activeElement;
      show(i);
      box.hidden = false;
      document.documentElement.classList.add("lb-open");
      $(".lb__x", box).focus();
    };
    var close = function () {
      box.hidden = true;
      document.documentElement.classList.remove("lb-open");
      im.removeAttribute("src");
      if (back) back.focus();
    };
    links.forEach(function (a, i) {
      a.addEventListener("click", function (e) { e.preventDefault(); open(i); });
    });
    $(".lb__x", box).addEventListener("click", close);
    $(".lb__prev", box).addEventListener("click", function () { show(at - 1); });
    $(".lb__next", box).addEventListener("click", function () { show(at + 1); });
    box.addEventListener("click", function (e) {
      if (e.target === box || e.target.classList.contains("lb__fig")) close();
    });
    document.addEventListener("keydown", function (e) {
      if (box.hidden) return;
      if (e.key === "Escape") close();
      else if (e.key === "ArrowLeft") show(at - 1);
      else if (e.key === "ArrowRight") show(at + 1);
    });
    var x0 = null;
    box.addEventListener("touchstart", function (e) { x0 = e.touches[0].clientX; }, { passive: true });
    box.addEventListener("touchend", function (e) {
      if (x0 === null) return;
      var dx = e.changedTouches[0].clientX - x0;
      if (Math.abs(dx) > 50) show(at + (dx < 0 ? 1 : -1));
      x0 = null;
    });
  })();

  /* ------------------------------------------------ enquiry -> email --- */
  var form = $("[data-enquiry]");
  if (form) {
    var send = $("[data-send]", form), status = $("[data-status]", form);
    guard(form);
    var thanks = $("[data-thanks]");
    $("[data-again]", thanks).addEventListener("click", function () {
      thanks.hidden = true;
      thanks.classList.remove("is-on");
      status.hidden = true;
      form.hidden = false;
      var n = $('input[name="name"]', form);
      if (n) n.focus();
    });
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!validate(form)) return;
      var d = new FormData(form);
      var payload = { page: location.href };
      ["name", "company", "phone", "email", "product", "material",
       "quantity", "message"].forEach(function (k) {
        payload[k] = (d.get(k) || "").toString().trim();
      });
      var file = d.get("drawing");
      if (!(file && file.size)) file = null;
      send.disabled = true;
      send.textContent = "Sending…";
      status.hidden = true;
      deliver(payload, {
        endpoint: form.getAttribute("data-endpoint") || "",
        cc: form.getAttribute("data-cc") || "",
        file: file
      }).then(function (ok) {
        send.disabled = false;
        send.textContent = "Send enquiry";
        if (ok) {
          form.reset();
          form.hidden = true;
          thanks.hidden = false;
          thanks.classList.remove("is-on");
          void thanks.offsetWidth;
          thanks.classList.add("is-on");
          thanks.focus({ preventScroll: true });
          var top = thanks.getBoundingClientRect().top;
          if (top < 80 || top > window.innerHeight - 200) {
            thanks.scrollIntoView({ behavior: reduced ? "auto" : "smooth", block: "center" });
          }
          return;
        }
        status.textContent = form.getAttribute("data-fail");
        status.classList.add("is-fail");
        status.hidden = false;
      });
    });
  }
})();
