# -*- coding: utf-8 -*-
"""Génère index.html et les pages activites/*.html à partir de content.py.
Usage : python3 _build/build.py  (depuis la racine du dépôt)"""
import os, json, html, datetime, sys
sys.path.insert(0, os.path.dirname(__file__))
from content import *

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TODAY = datetime.date.today().isoformat()
e = html.escape
WA = f"https://wa.me/{PHONE_INTL}"

def head(title, desc, path, image="assets/og-image.png", extra=""):
    url = SITE + path
    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="TDJ Consulting">
<meta property="og:locale" content="fr_FR">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/{image}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{SITE}/{image}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="author" content="Tsontsozara Dominique Jorondraza">
<meta name="geo.region" content="MG">
<meta name="theme-color" content="#08090A">
<link rel="canonical" href="{url}">
{extra}<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/styles.css">
<link rel="icon" type="image/png" href="/assets/favicon.png">
</head>
<body>
<a class="skip" href="#contenu">Aller au contenu</a>
"""

def header(active=None):
    items = "\n".join(
        f'          <li><a href="/activites/{a["slug"]}"{" aria-current=\"page\"" if active == a["slug"] else ""}><span class="ref">{a["ref"]}</span>{e(a["title"])}</a></li>'
        for a in ACTIVITIES)
    act_cur = ' aria-current="true"' if active else ""
    home_cur = ' aria-current="page"' if active is None else ""
    return f"""<header class="site-header">
  <a href="/" class="brand" aria-label="TDJ Consulting, accueil">
    <img src="/assets/img/logo-240.webp" alt="TDJ Consulting" width="54" height="51" class="brand-logo">
    <span class="brand-line">Bureau d'études<br>électricité &amp; énergie</span>
  </a>
  <button class="nav-toggle" aria-expanded="false" aria-controls="main-nav">Menu</button>
  <nav class="main-nav" id="main-nav" aria-label="Navigation principale">
    <ul class="nav-list">
      <li><a href="/"{home_cur}>Accueil</a></li>
      <li class="has-menu">
        <button class="menu-btn" aria-expanded="false" aria-controls="menu-activites"{act_cur}>Activités</button>
        <ul class="mega" id="menu-activites" hidden>
{items}
        </ul>
      </li>
      <li><a href="/#methode">Méthode</a></li>
      <li><a href="/#apropos">À propos</a></li>
      <li><a href="/#contact">Contact</a></li>
    </ul>
    <a class="btn btn-gold nav-cta" href="{WA}" target="_blank" rel="noopener">WhatsApp</a>
  </nav>
</header>
"""

def footer():
    links = "\n".join(f'      <li><a href="/activites/{a["slug"]}">{e(a["title"])}</a></li>' for a in ACTIVITIES)
    return f"""<footer class="site-footer">
  <div class="footer-grid">
    <div class="footer-brand">
      <img src="/assets/img/logo-240.webp" alt="TDJ Consulting" width="96" height="90" loading="lazy">
      <p>Bureau d'études en ingénierie électrique et conseil énergie, Antananarivo.</p>
    </div>
    <nav aria-label="Activités">
      <h2 class="footer-h">Activités</h2>
      <ul>
{links}
      </ul>
    </nav>
    <div>
      <h2 class="footer-h">Contact</h2>
      <ul>
        <li><a href="{WA}" target="_blank" rel="noopener">{PHONE_DISPLAY} (WhatsApp)</a></li>
        <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
        <li>Antananarivo, Madagascar</li>
      </ul>
    </div>
  </div>
  <div class="footer-legal">
    <p>© <span class="year">{TODAY[:4]}</span> TDJ Consulting · Propriété exclusive · Reproduction interdite sans autorisation écrite</p>
    <p>Éditeur : TDJ Consulting, Tsontsozara Dominique Jorondraza, Antananarivo. Hébergement : Vercel Inc., 340 S Lemon Ave, Walnut, CA 91789, États-Unis. Les informations transmises par le formulaire ne servent qu'à répondre à votre demande.</p>
  </div>
</footer>
<script src="/script.js" defer></script>
</body>
</html>
"""

def cartouche(cells):
    out = "\n".join(f'    <div class="cell"><span class="cell-k">{e(k)}</span><span class="cell-v">{v}</span></div>' for k, v in cells)
    return f'<div class="cartouche" role="group" aria-label="Fiche signalétique">\n{out}\n  </div>'

# ------------------------------------------------------------------ accueil
def build_index():
    ld = {
        "@context": "https://schema.org", "@type": "ProfessionalService",
        "name": "TDJ Consulting",
        "description": "Bureau d'études en ingénierie électrique à Madagascar : dimensionnement électrique, réseaux et distribution, coffrets et protections, APS/APD/DOE, notes de calcul, audit énergétique, études financières, AMO et formation.",
        "url": SITE + "/", "logo": SITE + "/assets/logo.png", "image": SITE + "/assets/img/hero.jpg",
        "email": EMAIL, "telephone": "+" + PHONE_INTL,
        "areaServed": {"@type": "Country", "name": "Madagascar"},
        "address": {"@type": "PostalAddress", "addressLocality": "Antananarivo", "addressCountry": "MG"},
        "founder": {"@type": "Person", "name": "Tsontsozara Dominique Jorondraza", "jobTitle": "Ingénieur en énergie"},
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Activités",
            "itemListElement": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": a["title"], "url": f'{SITE}/activites/{a["slug"]}'}} for a in ACTIVITIES]},
    }
    faq = [
        ("Comment obtenir un devis ?", "Envoyez votre demande par le formulaire ou sur WhatsApp. Le devis est établi après un échange sur le périmètre de la mission, puis transmis par e-mail."),
        ("Quels documents dois-je fournir pour démarrer ?", "Selon la mission : plans existants, schéma actuel, puissances installées ou prévues, factures d'électricité, devis à analyser. Un premier échange permet de lister l'essentiel."),
        ("Quels livrables recevrai-je ?", "Notes de calcul justificatives, schémas unifilaires et multifilaires, plans d'aménagement de tableaux, nomenclatures et rapport de synthèse. Les plans sont remis en PDF et en DXF."),
        ("Intervenez-vous partout à Madagascar ?", "Les études se mènent depuis Antananarivo. Les déplacements sur site sont prévus au cas par cas, selon la mission."),
        ("Mes informations restent-elles confidentielles ?", "Oui. Les documents et données transmis ne servent qu'à la mission et ne sont communiqués à aucun tiers sans votre accord."),
    ]
    ld_faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": r}} for q, r in faq]}
    extra = f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>\n<script type="application/ld+json">{json.dumps(ld_faq, ensure_ascii=False)}</script>\n<link rel="preload" as="image" href="/assets/img/hero.webp">\n'

    tabs = "\n".join(
        f'''        <li role="presentation"><button role="tab" id="tab-{a["slug"]}" aria-controls="panel-{a["slug"]}" aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}"><span class="ref">{a["ref"]}</span><span class="t">{e(a["title"])}</span></button></li>'''
        for i, a in enumerate(ACTIVITIES))
    panels = "\n".join(
        f'''      <div class="bus-panel" role="tabpanel" id="panel-{a["slug"]}" aria-labelledby="tab-{a["slug"]}"{"" if i == 0 else " hidden"}>
        <a class="bus-figure" href="/activites/{a["slug"]}" tabindex="-1" aria-hidden="true"><img src="/assets/img/{a["image"]}.webp" alt="" width="1400" height="933" loading="{"eager" if i == 0 else "lazy"}"></a>
        <div class="bus-text">
          <p class="bus-ref">Départ {a["ref"]} · {e(a["deliv_codes"])}</p>
          <h3>{e(a["title"])}</h3>
          <p>{e(a["short"])}</p>
          <a class="link-arrow" href="/activites/{a["slug"]}">Voir l'activité</a>
        </div>
      </div>'''
        for i, a in enumerate(ACTIVITIES))
    cards = "\n".join(
        f'''      <li><a class="m-card" href="/activites/{a["slug"]}"><img src="/assets/img/{a["image"]}.webp" alt="" width="1400" height="933" loading="lazy"><span class="ref">{a["ref"]}</span><span class="m-title">{e(a["title"])}</span><span class="m-short">{e(a["short"])}</span></a></li>'''
        for a in ACTIVITIES)
    segs = "\n".join(f'      <li><h3>{e(t)}</h3><p>{e(d)}</p></li>' for t, d in SEGMENTS)
    faq_html = "\n".join(f'      <details><summary>{e(q)}</summary><p>{e(r)}</p></details>' for q, r in faq)
    options = "\n".join(f'            <option value="{a["slug"]}">{e(a["title"])}</option>' for a in ACTIVITIES)

    body = f"""{header()}
<main id="contenu">

  <section class="hero" aria-labelledby="hero-title">
    <div class="hero-copy">
      <p class="kicker">Bureau d'études · Antananarivo, Madagascar</p>
      <h1 id="hero-title">Ingénierie électrique et conseil énergie, calcul par calcul.</h1>
      <p class="lede">Dimensionnement, réseaux et distribution, coffrets et protections, audit énergétique, études financières et assistance à maîtrise d'ouvrage. Plus de 8 ans d'études, de conception et de réalisation technique de projets.</p>
      <div class="actions">
        <a class="btn btn-gold" href="#contact">Demander un devis</a>
        <a class="btn btn-line" href="#activites">Voir les 9 activités</a>
      </div>
    </div>
    <figure class="hero-media">
      <picture>
        <source srcset="/assets/img/hero.webp" type="image/webp">
        <img src="/assets/img/hero.jpg" alt="Ingénieur au bureau d'études travaillant sur un schéma unifilaire et une note de calcul, vue sur Antananarivo à la tombée de la nuit" width="1536" height="864" fetchpriority="high">
      </picture>
    </figure>
  </section>

  {cartouche([
      ("Bureau", "TDJ Consulting"),
      ("Responsable", "T. D. Jorondraza, ingénieur en énergie"),
      ("Normes", "NF C 15-100 · CEI 60364 · UTE C 15-105"),
      ("Livrables", "Notes de calcul, schémas, plans PDF + DXF"),
      ("Devis", "Sur demande, sans engagement"),
  ])}

  <section id="activites" class="section bus" aria-labelledby="act-title">
    <div class="section-head">
      <h2 id="act-title">Neuf activités, un seul bureau d'études</h2>
      <p>Chaque activité est un départ du même tableau : une méthode commune, des calculs vérifiés, des livrables propres. Choisissez un départ pour en voir le détail.</p>
    </div>
    <div class="bus-wrap">
      <ul class="bus-list" role="tablist" aria-label="Activités" aria-orientation="vertical">
{tabs}
      </ul>
      <div class="bus-panels">
{panels}
      </div>
    </div>
    <ul class="m-cards">
{cards}
    </ul>
  </section>

  <section class="section secteurs" aria-labelledby="sect-title">
    <figure class="secteurs-media">
      <img src="/assets/img/tgbt.webp" alt="Salle TGBT : rangée d'armoires basse tension et ingénieur contrôlant une armoire avec une tablette" width="1400" height="933" loading="lazy">
    </figure>
    <div class="secteurs-copy">
      <h2 id="sect-title">Pour qui nous travaillons</h2>
      <ul class="seg-list">
{segs}
      </ul>
    </div>
  </section>

  <section id="methode" class="section methode" aria-labelledby="meth-title">
    <div class="section-head">
      <h2 id="meth-title">De la demande à la remise, quatre étapes</h2>
      <p>Le cadre est le même pour toutes les missions. Vous savez à chaque étape ce qui est fait et ce que vous recevrez.</p>
    </div>
    <ol class="steps">
      <li><span class="step-n">1</span><h3>Votre demande</h3><p>Vous décrivez le projet par le formulaire ou sur WhatsApp : nature de l'installation, site, échéance.</p></li>
      <li><span class="step-n">2</span><h3>Cadrage et devis</h3><p>Après échange sur le périmètre, un devis détaillé vous est adressé, sans engagement.</p></li>
      <li><span class="step-n">3</span><h3>Étude</h3><p>Calculs, schémas et plans selon les normes applicables, avec hypothèses écrites et vérifications chiffrées.</p></li>
      <li><span class="step-n">4</span><h3>Remise et suivi</h3><p>Livrables vérifiés et présentés, puis suivi technique si la mission l'inclut.</p></li>
    </ol>
  </section>

  <section id="apropos" class="section apropos" aria-labelledby="about-title">
    <div class="apropos-mark">
      <img src="/assets/img/logo-480.webp" alt="" width="480" height="451" loading="lazy">
    </div>
    <div class="apropos-copy">
      <h2 id="about-title">Tsontsozara Dominique Jorondraza</h2>
      <p class="lede">Ingénieur en énergie, fondateur de TDJ Consulting. Plus de 8 ans d'expérience en étude et conception de projet, gestion et réalisation technique.</p>
      <p>TDJ Consulting est un bureau d'études indépendant : pas de matériel à vendre, pas d'installateur à placer. Nos recommandations ne dépendent que de votre projet.</p>
      <dl class="facts">
        <div><dt>Spécialités</dt><dd>Dimensionnement électrique, réseaux et protections</dd></div>
        <div><dt>Énergie</dt><dd>Analyse, audit et optimisation énergétique</dd></div>
        <div><dt>Décision</dt><dd>Business plan, ROI et plan de trésorerie</dd></div>
        <div><dt>Outils</dt><dd>Notes de calcul, CAO, modèles Excel vérifiés</dd></div>
      </dl>
    </div>
  </section>

  <section id="faq" class="section faq" aria-labelledby="faq-title">
    <div class="section-head">
      <h2 id="faq-title">Questions fréquentes</h2>
    </div>
    <div class="faq-list">
{faq_html}
    </div>
  </section>

  <section id="contact" class="section contact" aria-labelledby="contact-title">
    <div class="section-head">
      <h2 id="contact-title">Un projet à dimensionner, un audit à mener ?</h2>
      <p>Décrivez votre besoin. Vous recevez une réponse et, si la mission est claire, un devis détaillé.</p>
    </div>
    <div class="contact-layout">
      <form class="contact-form" id="contact-form" novalidate>
        <div class="form-row"><label for="f-name">Nom</label><input type="text" id="f-name" name="name" autocomplete="name" required></div>
        <div class="form-row"><label for="f-email">E-mail</label><input type="email" id="f-email" name="email" autocomplete="email" required></div>
        <div class="form-row"><label for="f-phone">Téléphone <span class="opt">(facultatif)</span></label><input type="tel" id="f-phone" name="phone" autocomplete="tel"></div>
        <div class="form-row"><label for="f-subject">Activité concernée</label>
          <select id="f-subject" name="subject">
{options}
            <option value="autre">Autre demande</option>
          </select>
        </div>
        <div class="form-row"><label for="f-lieu">Lieu du projet <span class="opt">(facultatif)</span></label><input type="text" id="f-lieu" name="lieu"></div>
        <div class="form-row"><label for="f-delai">Échéance souhaitée <span class="opt">(facultatif)</span></label><input type="text" id="f-delai" name="delai" placeholder="Ex. : fin janvier"></div>
        <div class="form-row full"><label for="f-message">Votre projet</label><textarea id="f-message" name="message" rows="5" required></textarea></div>
        <div class="form-foot full">
          <button type="submit" class="btn btn-gold">Envoyer la demande</button>
          <p class="form-note" id="form-note" role="status">Votre messagerie s'ouvre avec la demande pré-remplie. Il ne reste qu'à l'envoyer.</p>
        </div>
      </form>
      <aside class="contact-side" aria-label="Coordonnées">
        <div class="contact-block"><span class="cell-k">Téléphone / WhatsApp</span><a href="{WA}" target="_blank" rel="noopener">{PHONE_DISPLAY}</a></div>
        <div class="contact-block"><span class="cell-k">E-mail</span><a href="mailto:{EMAIL}">{EMAIL}</a></div>
        <div class="contact-block"><span class="cell-k">Bureau</span><span>Antananarivo, Madagascar</span></div>
        <a class="btn btn-line" href="{WA}" target="_blank" rel="noopener">Écrire sur WhatsApp</a>
      </aside>
    </div>
  </section>

</main>
"""
    page = head("TDJ Consulting · Bureau d'études en ingénierie électrique et énergie, Madagascar",
                "Bureau d'études à Antananarivo : dimensionnement électrique, réseaux et distribution, coffrets et protections, APS/APD/DOE, notes de calcul, audit énergétique, études financières, AMO et formation.",
                "/", "assets/img/hero.jpg", extra) + body + footer()
    open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8").write(page)

# ------------------------------------------------------------------ activités
def build_activity(i, a):
    n = len(ACTIVITIES)
    prev, nxt = ACTIVITIES[(i - 1) % n], ACTIVITIES[(i + 1) % n]
    strip = "\n".join(
        f'      <li><a href="/activites/{b["slug"]}"{" aria-current=\"page\"" if b is a else ""}><span class="ref">{b["ref"]}</span>{e(b["title"])}</a></li>'
        for b in ACTIVITIES)
    mission = "\n".join(f"        <li>{e(x)}</li>" for x in a["mission"])
    deliv = "\n".join(f"        <li>{e(x)}</li>" for x in a["deliverables"])
    cases = "\n".join(f'      <li><h3>{e(t)}</h3><p>{e(d)}</p></li>' for t, d in a["cases"])
    note = ("Plans et schémas remis en PDF et DXF. " if "PLN" in a["deliv_codes"] else "") + "Chaque document porte une référence, un indice de révision et une date."
    img2 = ""
    if a.get("image2"):
        img2 = f'''
  <figure class="wide-figure">
    <img src="/assets/img/{a["image2"]}.webp" alt="{e(a["alt2"])}" width="1400" height="933" loading="lazy">
  </figure>'''
    ld = {"@context": "https://schema.org", "@type": "Service", "name": a["title"], "description": a["short"],
          "provider": {"@type": "ProfessionalService", "name": "TDJ Consulting", "url": SITE + "/"},
          "areaServed": {"@type": "Country", "name": "Madagascar"}, "url": f'{SITE}/activites/{a["slug"]}'}
    bc = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Accueil", "item": SITE + "/"},
        {"@type": "ListItem", "position": 2, "name": a["title"], "item": f'{SITE}/activites/{a["slug"]}'}]}
    extra = f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>\n<script type="application/ld+json">{json.dumps(bc, ensure_ascii=False)}</script>\n<link rel="preload" as="image" href="/assets/img/{a["image"]}.webp">\n'

    body = f"""{header(a["slug"])}
<nav class="tab-strip" aria-label="Toutes les activités">
  <ul>
{strip}
  </ul>
</nav>
<main id="contenu">

  <section class="hero hero-act" aria-labelledby="act-h1">
    <div class="hero-copy">
      <p class="crumbs"><a href="/">Accueil</a> <span aria-hidden="true">/</span> <a href="/#activites">Activités</a></p>
      <h1 id="act-h1">{e(a["title"])}</h1>
      <p class="lede">{e(a["lede"])}</p>
      <div class="actions">
        <a class="btn btn-gold" href="/?sujet={a["slug"]}#contact">Demander un devis</a>
        <a class="btn btn-line" href="{WA}?text={e('Bonjour, je souhaite échanger sur une mission : ' + a['title'])}" target="_blank" rel="noopener">En parler sur WhatsApp</a>
      </div>
    </div>
    <figure class="hero-media">
      <img src="/assets/img/{a["image"]}.webp" alt="{e(a["alt"])}" width="1400" height="933" fetchpriority="high">
    </figure>
  </section>

  {cartouche([
      ("Repère", f'{a["ref"]} · {e(a["title"])}'),
      ("Pour qui", e(a["for"])),
      ("Références", e(a["norms"])),
      ("Livrables", e(a["deliv_codes"])),
      ("Devis", "Sur demande, sans engagement"),
  ])}

  <section class="section detail" aria-label="Contenu de la mission">
    <div class="detail-col">
      <h2>Ce que comprend la mission</h2>
      <ul class="sq-list">
{mission}
      </ul>
    </div>
    <div class="detail-col deliv">
      <h2>Ce que vous recevez</h2>
      <ul class="sq-list">
{deliv}
      </ul>
      <p class="note">{note}</p>
    </div>
  </section>
{img2}
  <section class="section cases" aria-labelledby="cases-title">
    <h2 id="cases-title">Situations où nous intervenons</h2>
    <ul class="case-list">
{cases}
    </ul>
  </section>

  <section class="cta-band" aria-labelledby="cta-title">
    <div>
      <h2 id="cta-title">Parlons de votre projet</h2>
      <p>Décrivez votre besoin en quelques lignes. Le devis est établi après un premier échange.</p>
    </div>
    <div class="actions">
      <a class="btn btn-gold" href="/?sujet={a["slug"]}#contact">Demander un devis</a>
      <a class="btn btn-ivory-line" href="{WA}" target="_blank" rel="noopener">WhatsApp {PHONE_DISPLAY}</a>
    </div>
  </section>

  <nav class="pager" aria-label="Activité précédente et suivante">
    <a class="pager-prev" href="/activites/{prev["slug"]}"><span class="cell-k">Précédente</span><span>{prev["ref"]} {e(prev["title"])}</span></a>
    <a class="pager-next" href="/activites/{nxt["slug"]}"><span class="cell-k">Suivante</span><span>{nxt["ref"]} {e(nxt["title"])}</span></a>
  </nav>

</main>
"""
    page = head(f'{a["title"]} · TDJ Consulting, bureau d\'études Madagascar', a["short"],
                f'/activites/{a["slug"]}', f'assets/img/{a["image"]}.webp', extra) + body + footer()
    os.makedirs(os.path.join(ROOT, "activites"), exist_ok=True)
    open(os.path.join(ROOT, "activites", a["slug"] + ".html"), "w", encoding="utf-8").write(page)

def build_sitemap():
    urls = [("/", "1.0")] + [(f'/activites/{a["slug"]}', "0.8") for a in ACTIVITIES]
    body = "\n".join(f"  <url><loc>{SITE}{u}</loc><lastmod>{TODAY}</lastmod><priority>{p}</priority></url>" for u, p in urls)
    open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{body}\n</urlset>\n')

if __name__ == "__main__":
    build_index()
    for i, a in enumerate(ACTIVITIES):
        build_activity(i, a)
    build_sitemap()
    print("OK :", 1 + len(ACTIVITIES), "pages")
