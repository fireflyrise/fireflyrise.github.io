# -*- coding: utf-8 -*-
"""
Firefly Rise — Site Builder
Generates all 27 HTML pages from site_data + faqs_data.
Run from project root:   python scripts/build_site.py
"""
import os
import sys
import datetime
from pathlib import Path

# Make sibling modules importable
sys.path.insert(0, str(Path(__file__).parent))
from site_data import (
    BUSINESS, SERVICES, SERVICE_BY_SLUG_EN, SERVICE_BY_SLUG_ES,
    HOME_EN_FILE, HOME_ES_FILE, HOME_EN_PATH, HOME_ES_PATH, HOME_ES_SLUG,
    REVIEWS_EN, REVIEWS_ES, WHY_US_ICONS, STEP_ICONS,
)


def clean_url(slug):
    """/slug/ — the public URL for a service or legal page."""
    return "/" + slug + "/"


def clean_file(slug):
    """slug/index.html — the filesystem output path."""
    return slug + "/index.html"


def h1_from_title(title):
    """Strip the business name from an SEO <title> so the on-page h1 shows
    only the distinctive part. Keeps the <title> intact for SEO while the
    on-page heading stays clean. Handles both 'BRAND | X' and 'X | BRAND'."""
    prefix = BUSINESS["name"] + " | "
    suffix = " | " + BUSINESS["name"]
    if title.startswith(prefix):
        return title[len(prefix):]
    if title.endswith(suffix):
        return title[:-len(suffix)]
    return title
from faqs_data import FAQS_EN, FAQS_ES

ROOT = Path(__file__).resolve().parent.parent
os.chdir(ROOT)

BUILD_DATE = datetime.date.today().strftime("%B %d, %Y")
YEAR = datetime.date.today().year
DOMAIN = BUSINESS["domain"]
PHONE_TEL = BUSINESS["phone_tel"]
PHONE_DISPLAY = BUSINESS["phone_display"]
EMAIL = BUSINESS["email"]
BUSINESS_NAME = BUSINESS["name"]

# ── Localized labels ─────────────────────────────────────────────────────────
LABELS = {
    "en": {
        "nav_home": "Home",
        "nav_services": "Services",
        "nav_about": "About Us",
        "nav_privacy": "Privacy Policy",
        "nav_terms": "Terms & Conditions",
        "lang_toggle": "ESPAÑOL",
        "lang_aria": "Ver en Español",
        "call_cta": "Call " + PHONE_DISPLAY,
        "quote_cta": "Get My Free Quote",
        "call_cta_short": "Call Now",
        "footer_rights": "All rights reserved.",
        "footer_tagline": BUSINESS["tagline_en"],
        "mobile_call": "📞 Call Now",
        "mobile_quote": "Free Quote",
        "modal_step1_q": "What marketing service are you interested in?",
        "modal_step1_sub": "Pick the one closest to where you need help most.",
        "modal_step2_q": "What type of home service business do you run?",
        "modal_step2_sub": "This helps us tailor the conversation around your trade.",
        "modal_step3_q": "Where should we send your free strategy call details?",
        "modal_step3_sub": "A real human will reach out within one business hour.",
        "modal_name": "Full Name",
        "modal_phone": "Phone Number",
        "modal_email": "Email Address",
        "modal_back": "Back",
        "modal_next": "Next",
        "modal_submit": "Get My Free Strategy Call",
        "modal_success_title": "Thanks, %s!",
        "modal_success_body": "Your request is in. A real human will reach out within one business hour. Talk soon.",
        "modal_error_title": "Something went wrong",
        "modal_error_body": "Please try again in a moment, or use the Call button to reach us directly.",
        "modal_close": "Close",
    },
    "es": {
        "nav_home": "Inicio",
        "nav_services": "Servicios",
        "nav_about": "Quiénes Somos",
        "nav_privacy": "Política de Privacidad",
        "nav_terms": "Términos y Condiciones",
        "lang_toggle": "ENGLISH",
        "lang_aria": "View in English",
        "call_cta": "Llama " + PHONE_DISPLAY,
        "quote_cta": "Obtén Tu Cotización Gratis",
        "call_cta_short": "Llama Ahora",
        "footer_rights": "Todos los derechos reservados.",
        "footer_tagline": BUSINESS["tagline_es"],
        "mobile_call": "📞 Llama Ahora",
        "mobile_quote": "Cotización",
        "modal_step1_q": "¿Qué servicio de marketing te interesa?",
        "modal_step1_sub": "Elige el más cercano a donde más necesitas ayuda.",
        "modal_step2_q": "¿Qué tipo de negocio de servicios del hogar manejas?",
        "modal_step2_sub": "Esto nos ayuda a enfocar la conversación en tu oficio.",
        "modal_step3_q": "¿A dónde te enviamos los detalles de tu llamada de estrategia?",
        "modal_step3_sub": "Una persona real te contactará en una hora hábil.",
        "modal_name": "Nombre Completo",
        "modal_phone": "Número de Teléfono",
        "modal_email": "Correo Electrónico",
        "modal_back": "Atrás",
        "modal_next": "Siguiente",
        "modal_submit": "Obtener Mi Llamada Gratis",
        "modal_success_title": "¡Gracias, %s!",
        "modal_success_body": "Tu solicitud está lista. Una persona real te contactará en una hora hábil. Hablamos pronto.",
        "modal_error_title": "Algo salió mal",
        "modal_error_body": "Por favor intenta de nuevo en un momento, o usa el botón de llamada para contactarnos directamente.",
        "modal_close": "Cerrar",
    },
}

MODAL_STEP1_OPTIONS = {
    "en": [
        "Google Ads Management",
        "Facebook & Social Media Ads",
        "Website Design",
        "Lead Generation",
        "Reputation Management",
        "Other",
    ],
    "es": [
        "Administración de Google Ads",
        "Anuncios en Facebook y Redes Sociales",
        "Diseño Web",
        "Generación de Leads",
        "Manejo de Reputación",
        "Otro",
    ],
}
MODAL_STEP2_OPTIONS = {
    "en": [
        "Plumbing",
        "HVAC / Air Conditioning",
        "Electrical",
        "Roofing",
        "Landscaping / Lawn Care",
        "General Contractor",
        "Other",
    ],
    "es": [
        "Plomería",
        "HVAC / Aire Acondicionado",
        "Eléctrico",
        "Techado",
        "Jardinería",
        "Contratista General",
        "Otro",
    ],
}

SECTION_HEADINGS = {
    "en": {
        "why_title": "Why Home Service Contractors Choose Firefly Rise",
        "why_intro": "You've been burned by agencies that overpromise and underdeliver. Here's what makes working with a team that lives and breathes home services different — starting with the fact that every campaign is engineered to make your phone ring, not pad our billable hours.",
        "about_title": "Your Marketing Agency Should Speak Your Language",
        "reviews_title": "Real Wins From Real Home Service Contractors",
        "reviews_intro": "Contractors just like you were stuck with the same problems you're facing right now. Here's what changed when they stopped trusting generalists and started working with specialists who understand the home services grind.",
        "banner_text": "Every day your competitor's ads run and yours don't, another homeowner calls them instead of you. Don't wait another week. Start winning today.",
        "services_title": "Marketing Services Built For Home Service Contractors",
        "services_intro": "Every service offered here exists for one reason — to make your phone ring with real homeowners ready to book. No vanity metrics, no long contracts, no black boxes. Just marketing built by people who understand what it takes to run a home services business.",
        "steps_title": "Three Simple Steps To More Calls",
        "steps_intro": "You don't need to figure any of this out yourself. One short call and a real strategist will tell you exactly where your marketing is leaking jobs and what to do about it. Simple, direct, no pressure.",
        "step1_t": "Call Or Fill Out The Form — No Pressure, No Pitch Deck",
        "step1_b": "Reach out and a real strategist will get on the phone with you within one business hour. You'll have a short, honest conversation about your business, your goals, and where you feel stuck. If this isn't a fit, you'll be told directly.",
        "step2_t": "Get A Clear Strategy Built Around Your Business",
        "step2_b": "You'll get a plain-English plan that shows exactly what needs to change, what it will cost, and what you can expect in return. No long slide decks, no jargon, no commitment to sign anything on the spot.",
        "step3_t": "Watch Your Phone Start Ringing — And Stay Ringing",
        "step3_b": "Campaigns go live fast, every dollar is tracked from the first click to the booked job, and you get transparent weekly reports. Adjustments happen every week so the system keeps getting better, not stale.",
        "faqs_title": "Straight Answers To The Questions You're Already Asking",
        "faqs_intro": "It's smart to do your homework before handing your marketing to anyone. The answers below are direct — not sales fluff. If what you need isn't here, reach out using the buttons on this page and get a straight answer from a real human.",
        "service_card_link": "See the details →",
        "hero_cta1": "Call " + PHONE_DISPLAY,
        "hero_cta2": "Get My Free Strategy Call",
    },
    "es": {
        "why_title": "Por Qué Los Contratistas Eligen Firefly Rise",
        "why_intro": "Ya te quemaste con agencias que prometen mucho y entregan poco. Esto es lo que hace diferente trabajar con un equipo que vive y respira servicios del hogar — empezando por el hecho de que cada campaña está diseñada para hacer sonar tu teléfono, no para inflar nuestras horas facturables.",
        "about_title": "Tu Agencia De Marketing Debería Hablar Tu Idioma",
        "reviews_title": "Victorias Reales De Contratistas Reales",
        "reviews_intro": "Contratistas como tú estaban atorados con los mismos problemas que enfrentas ahora. Esto es lo que cambió cuando dejaron de confiar en generalistas y empezaron a trabajar con especialistas que entienden el esfuerzo diario de los servicios del hogar.",
        "banner_text": "Cada día que los anuncios de tu competidor corren y los tuyos no, otro dueño de casa les llama a ellos en vez de a ti. No esperes otra semana. Empieza a ganar hoy.",
        "services_title": "Servicios De Marketing Creados Para Contratistas",
        "services_intro": "Cada servicio que ofrecemos existe por una razón — hacer sonar tu teléfono con dueños reales listos para agendar. Sin métricas vacías, sin contratos largos, sin cajas negras. Solo marketing hecho por gente que entiende lo que toma manejar un negocio de servicios del hogar.",
        "steps_title": "Tres Pasos Simples A Más Llamadas",
        "steps_intro": "No necesitas descifrar nada por ti mismo. Una llamada corta y un estratega real te dirá exactamente dónde tu marketing está dejando trabajos y qué hacer al respecto. Simple, directo, sin presión.",
        "step1_t": "Llama O Llena El Formulario — Sin Presión, Sin Presentación",
        "step1_b": "Comunícate y un estratega real se pondrá en el teléfono contigo en una hora hábil. Tendrás una conversación corta y honesta sobre tu negocio, metas, y dónde te sientes atorado. Si no encaja, te lo diremos directamente.",
        "step2_t": "Recibe Una Estrategia Clara Creada Para Tu Negocio",
        "step2_b": "Recibirás un plan en lenguaje sencillo que muestra exactamente qué necesita cambiar, cuánto costará, y qué esperar a cambio. Sin presentaciones largas, sin jerga, sin compromiso de firmar nada en el momento.",
        "step3_t": "Observa Cómo Empieza A Sonar Tu Teléfono — Y Sigue Sonando",
        "step3_b": "Las campañas se lanzan rápido, cada dólar se rastrea desde el primer clic hasta el trabajo agendado, y recibes reportes semanales transparentes. Los ajustes pasan cada semana para que el sistema mejore, no se estanque.",
        "faqs_title": "Respuestas Directas A Las Preguntas Que Ya Te Estás Haciendo",
        "faqs_intro": "Es inteligente hacer tu tarea antes de entregar tu marketing a alguien. Las respuestas de abajo son directas — sin relleno de ventas. Si lo que necesitas no está aquí, usa los botones en esta página y recibe una respuesta directa de una persona real.",
        "service_card_link": "Ver los detalles →",
        "hero_cta1": "Llama " + PHONE_DISPLAY,
        "hero_cta2": "Obtén Tu Llamada Gratis",
    },
}

ABOUT_US_COPY = {
    "en": {
        "home": [
            "If you run a home service business, you already know marketing agencies rarely understand the difference between a lead and a booked job. You've probably been burned at least once — locked into a long contract, handed vanity reports full of impressions, and left wondering why your phone isn't ringing.",
            "Firefly Rise was built exclusively for home service contractors — plumbers, HVAC techs, roofers, electricians, landscapers, and every trade that sends a truck to a homeowner's door. Every campaign is engineered to produce phone calls. Every report is tied to revenue. And every contract is month-to-month because the work has to earn its place every single month. Your success is the only metric that matters.",
        ],
        "service_default": [
            "You didn't go into the trades to become a marketing expert. You're great at what you do — fixing things, installing things, building things, making homeowners' lives better. Marketing shouldn't be a second job you're bad at.",
            "Firefly Rise takes marketing off your plate completely, handled by a team that works only with home service contractors. Your campaigns are built by specialists who understand what a qualified lead looks like, how to talk to homeowners, and what it takes to turn a click into a booked job. Your job is to run your business. Ours is to keep the phone ringing.",
        ],
    },
    "es": {
        "home": [
            "Si manejas un negocio de servicios del hogar, ya sabes que las agencias de marketing rara vez entienden la diferencia entre un lead y un trabajo agendado. Probablemente te has quemado al menos una vez — atrapado en un contrato largo, entregado reportes vacíos llenos de impresiones, y dejado preguntándote por qué no suena tu teléfono.",
            "Firefly Rise fue creado exclusivamente para contratistas de servicios del hogar — plomeros, técnicos HVAC, techadores, electricistas, jardineros, y cada oficio que envía un camión a la casa de un dueño. Cada campaña está diseñada para producir llamadas. Cada reporte está ligado a ingresos. Y cada contrato es mes a mes porque el trabajo tiene que ganarse su lugar cada mes. Tu éxito es la única métrica que importa.",
        ],
        "service_default": [
            "No te metiste al oficio para convertirte en experto en marketing. Eres bueno en lo que haces — arreglando cosas, instalando cosas, construyendo cosas, mejorando la vida de los dueños. El marketing no debería ser un segundo trabajo en el que eres malo.",
            "Firefly Rise se encarga del marketing por completo, manejado por un equipo que solo trabaja con contratistas de servicios del hogar. Tus campañas se construyen por especialistas que entienden cómo luce un lead calificado, cómo hablar con dueños de casa, y qué toma convertir un clic en un trabajo agendado. Tu trabajo es dirigir tu negocio. El nuestro es mantener el teléfono sonando.",
        ],
    },
}

WHY_US_CARDS = {
    "en": [
        {
            "icon": "fa-solid fa-bullseye",
            "h3": "Built Exclusively For Home Service Contractors",
            "p": "You don't need a generalist agency juggling restaurants and real estate between your campaigns. Every strategist, every campaign, every dollar goes into serving home service trades — which means faster wins, sharper campaigns, and zero learning curve on your industry.",
        },
        {
            "icon": "fa-solid fa-chart-line",
            "h3": "Transparent Reporting Tied To Real Phone Calls",
            "p": "No vanity metrics, no black boxes. You see every ad, every keyword, every dollar, and every call that it produced. Weekly updates land in your inbox like clockwork so you always know what's working, what's being killed, and what's being scaled.",
        },
        {
            "icon": "fa-solid fa-handshake",
            "h3": "No Long-Term Contracts — The Work Earns Its Keep",
            "p": "Every engagement is month-to-month after setup, and you keep every asset if you ever decide to leave. That means the only way this relationship continues is if the phone keeps ringing. Incentives aligned, no handcuffs.",
        },
    ],
    "es": [
        {
            "icon": "fa-solid fa-bullseye",
            "h3": "Creado Exclusivamente Para Contratistas De Servicios Del Hogar",
            "p": "No necesitas una agencia generalista malabareando restaurantes y bienes raíces entre tus campañas. Cada estratega, cada campaña, cada dólar va a servir a los oficios de servicios del hogar — lo que significa victorias más rápidas, campañas más afiladas, y cero curva de aprendizaje sobre tu industria.",
        },
        {
            "icon": "fa-solid fa-chart-line",
            "h3": "Reportes Transparentes Ligados A Llamadas Reales",
            "p": "Sin métricas vacías, sin cajas negras. Ves cada anuncio, cada palabra clave, cada dólar, y cada llamada que produjo. Actualizaciones semanales llegan a tu bandeja como reloj para que siempre sepas qué funciona, qué se está matando, y qué se está escalando.",
        },
        {
            "icon": "fa-solid fa-handshake",
            "h3": "Sin Contratos Largos — El Trabajo Se Gana Su Lugar",
            "p": "Cada compromiso es mes a mes después de la configuración, y te quedas con todos los activos si decides irte. Eso significa que la única forma en que continúa esta relación es si el teléfono sigue sonando. Incentivos alineados, sin esposas.",
        },
    ],
}

# ── Helpers ──────────────────────────────────────────────────────────────────

def html_escape(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace('"', "&quot;").replace("'", "&#39;"))


def canonical(path, lang):
    return "https://" + DOMAIN + path


def render_head(page, lang, title, description, og_image, canonical_path, alt_path):
    """Render the <head> block. canonical_path + alt_path are root-relative, leading slash."""
    L = LABELS[lang]
    lang_attr = "en" if lang == "en" else "es"
    og_locale = "en_US" if lang == "en" else "es_US"
    alt_hreflang = "es-US" if lang == "en" else "en"
    self_hreflang = "en" if lang == "en" else "es-US"
    return f"""<!DOCTYPE html>
<html lang="{lang_attr}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">

  <title>{html_escape(title)}</title>
  <meta name="description" content="{html_escape(description)}">
  <meta name="keywords" content="home services marketing, digital marketing agency, Google Ads, Facebook Ads, lead generation, {html_escape(BUSINESS_NAME)}">
  <link rel="canonical" href="https://{DOMAIN}{canonical_path}">
  <meta name="robots" content="index, follow">

  <!-- Favicon — light bg default; dark-bg swap via media query -->
  <link rel="icon" type="image/png" href="/images/favicon-light-background.png" media="(prefers-color-scheme: light)">
  <link rel="icon" type="image/png" href="/images/favicon-dark-background.png" media="(prefers-color-scheme: dark)">
  <link rel="icon" type="image/png" href="/images/favicon-light-background.png">
  <link rel="apple-touch-icon" href="/images/favicon-light-background.png">

  <!-- hreflang cross-references (English ↔ Spanish) -->
  <link rel="alternate" hreflang="{self_hreflang}" href="https://{DOMAIN}{canonical_path}">
  <link rel="alternate" hreflang="{alt_hreflang}" href="https://{DOMAIN}{alt_path}">
  <link rel="alternate" hreflang="x-default" href="https://{DOMAIN}/">

  <!-- Open Graph -->
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="{html_escape(BUSINESS_NAME)}">
  <meta property="og:title" content="{html_escape(title)}">
  <meta property="og:description" content="{html_escape(description)}">
  <meta property="og:url" content="https://{DOMAIN}{canonical_path}">
  <meta property="og:image" content="https://{DOMAIN}/images/{og_image}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="{html_escape(BUSINESS_NAME)} — {html_escape(title)}">
  <meta property="og:locale" content="{og_locale}">

  <!-- Twitter / X -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{html_escape(title)}">
  <meta name="twitter:description" content="{html_escape(description)}">
  <meta name="twitter:image" content="https://{DOMAIN}/images/{og_image}">
  <meta name="twitter:image:alt" content="{html_escape(BUSINESS_NAME)} — {html_escape(title)}">

  <!-- Geo / National -->
  <meta name="geo.region" content="US">
  <meta name="geo.placename" content="United States">

  <!-- Preconnect -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="preconnect" href="https://cdnjs.cloudflare.com">

  <!-- Font Awesome 7 -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/7.0.1/css/all.min.css">

  <!-- Site CSS -->
  <link rel="stylesheet" href="/css/styles.css">

  <!-- JSON-LD LocalBusiness -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "ProfessionalService",
    "name": "{BUSINESS_NAME}",
    "url": "https://{DOMAIN}{canonical_path}",
    "telephone": "{PHONE_DISPLAY}",
    "email": "{EMAIL}",
    "areaServed": {{"@type": "Country", "name": "United States"}},
    "description": "{BUSINESS['tagline_en'] if lang == 'en' else BUSINESS['tagline_es']}",
    "image": "https://{DOMAIN}/images/{og_image}",
    "priceRange": "$$"
  }}
  </script>
</head>
"""


def render_nav(lang, current_path):
    L = LABELS[lang]
    # Service links
    service_links = []
    for s in SERVICES:
        slug = s["slug_en"] if lang == "en" else s["slug_es"]
        name = s["name_en"] if lang == "en" else s["name_es"]
        service_links.append(f'            <li><a href="{clean_url(slug)}">{html_escape(name)}</a></li>')
    service_links_html = "\n".join(service_links)

    # About anchor
    if lang == "en":
        about_anchor = "/#about-us"
        lang_toggle_href = HOME_ES_PATH
    else:
        about_anchor = HOME_ES_PATH + "#about-us"
        lang_toggle_href = "/"

    privacy_path = clean_url("privacy-policy") if lang == "en" else clean_url("politica-de-privacidad")
    terms_path = clean_url("terms-and-conditions") if lang == "en" else clean_url("terminos-y-condiciones")

    logo_light = "/images/logo-light-backgrounds.png"

    return f"""<nav class="site-nav" role="navigation">
  <div class="nav-inner">
    <a href="/" class="nav-brand" aria-label="{html_escape(BUSINESS_NAME)}">
      <img src="{logo_light}" alt="{html_escape(BUSINESS_NAME)} logo">
    </a>
    <button class="hamburger" id="hamburger" aria-label="Toggle menu" aria-expanded="false">&#9776;</button>
    <ul class="nav-menu" id="nav-menu">
      <li><a href="/">{L['nav_home']}</a></li>
      <li>
        <button class="nav-parent" aria-haspopup="true" aria-expanded="false">
          {L['nav_services']} <span class="chevron">&#9662;</span>
        </button>
        <ul class="dropdown" role="menu">
{service_links_html}
        </ul>
      </li>
      <li>
        <button class="nav-parent" aria-haspopup="true" aria-expanded="false">
          {L['nav_about']} <span class="chevron">&#9662;</span>
        </button>
        <ul class="dropdown" role="menu">
          <li><a href="{about_anchor}">{L['nav_about']}</a></li>
          <li><a href="{privacy_path}">{L['nav_privacy']}</a></li>
          <li><a href="{terms_path}">{L['nav_terms']}</a></li>
        </ul>
      </li>
      <li><a href="{lang_toggle_href}" class="lang-toggle" aria-label="{L['lang_aria']}">🌐 {L['lang_toggle']}</a></li>
    </ul>
  </div>
</nav>
"""


def render_hero(lang, seo_title, headline, body, bg_image):
    """seo_title is the exact <title> content. The on-page h1 drops the
    business-name portion (kept only in the <title> tag for SEO)."""
    L = LABELS[lang]
    SH = SECTION_HEADINGS[lang]
    h1_text = h1_from_title(seo_title)
    return f"""<section class="hero" style="background-image: linear-gradient(rgba(0,0,0,0.15), rgba(0,0,0,0.15)), url('/images/{bg_image}');">
  <div class="container">
    <div class="hero-content">
      <h1 class="hero-title">{html_escape(h1_text)}</h1>
      <h2 class="hero-headline">{html_escape(headline)}</h2>
      <p class="hero-body">{html_escape(body)}</p>
      <div class="hero-ctas">
        <a href="tel:{PHONE_TEL}" class="btn-primary">{L['call_cta']}</a>
        <button class="btn-secondary" data-modal="hero-modal" type="button">{SH['hero_cta2']}</button>
      </div>
    </div>
  </div>
</section>
"""


def render_why_us(lang):
    SH = SECTION_HEADINGS[lang]
    cards = WHY_US_CARDS[lang]
    cards_html = ""
    for c in cards:
        cards_html += f"""        <div class="why-us-card fade-in">
          <i class="{c['icon']}"></i>
          <h3>{html_escape(c['h3'])}</h3>
          <p>{html_escape(c['p'])}</p>
        </div>
"""
    return f"""<section class="why-us">
  <div class="container">
    <h2 class="section-title">{html_escape(SH['why_title'])}</h2>
    <p class="section-intro">{html_escape(SH['why_intro'])}</p>
    <div class="why-us-grid">
{cards_html}    </div>
  </div>
</section>
"""


def render_about_us(lang, page_type="home"):
    SH = SECTION_HEADINGS[lang]
    paragraphs = ABOUT_US_COPY[lang].get(page_type, ABOUT_US_COPY[lang]["service_default"])
    paras_html = "\n".join(f"          <p>{html_escape(p)}</p>" for p in paragraphs)
    # Contextual link back to homepage on service pages
    home_link_html = ""
    if page_type != "home":
        home_href = "/" if lang == "en" else HOME_ES_PATH
        if lang == "en":
            home_link_html = f'\n          <p>Want the full picture? See every marketing service for home service contractors on our <a href="{home_href}">home services marketing agency</a> homepage.</p>'
        else:
            home_link_html = f'\n          <p>¿Quieres el panorama completo? Mira todos nuestros servicios de marketing en la <a href="{home_href}">agencia de marketing digital para servicios del hogar</a>.</p>'
    return f"""<section class="about-us" id="about-us">
  <div class="container">
    <div class="about-us-grid">
        <div class="about-us-text fade-in">
          <h2 class="section-title">{html_escape(SH['about_title'])}</h2>
{paras_html}{home_link_html}
        </div>
        <div class="about-us-image fade-in">
          <img src="/images/about-us.webp" alt="{html_escape(BUSINESS_NAME)} strategy team reviewing home services marketing campaigns" loading="lazy" width="600" height="600">
        </div>
    </div>
  </div>
</section>
"""


def render_reviews(lang, page_slug):
    """page_slug is either 'home' or a service slug (in the page's language)."""
    SH = SECTION_HEADINGS[lang]
    reviews_pool = REVIEWS_EN if lang == "en" else REVIEWS_ES

    if page_slug == "home":
        # Homepage: curated top 3 (google ads, facebook, websites)
        wanted_en = ["google-ads-management", "facebook-meta-ads", "website-design-development"]
        wanted_es = ["administracion-de-google-ads", "anuncios-en-facebook-y-meta", "diseno-y-desarrollo-web"]
        wanted = wanted_en if lang == "en" else wanted_es
        chosen = [r for r in reviews_pool if r["service"] in wanted]
    else:
        # Service page: matching review first, then 2 adjacent
        matching = [r for r in reviews_pool if r["service"] == page_slug]
        others = [r for r in reviews_pool if r["service"] != page_slug]
        chosen = matching[:1] + others[:2]

    cards_html = ""
    for r in chosen:
        cards_html += f"""        <div class="review-card fade-in">
          <!-- Placeholder review — replace with real customer testimonial -->
          <i class="fa-solid fa-quote-left review-icon"></i>
          <h3 class="review-title">{html_escape(r['title'])}</h3>
          <p class="review-body">{html_escape(r['body'])}</p>
          <p class="review-name">— {html_escape(r['name'])}</p>
        </div>
"""
    return f"""<section class="reviews">
  <div class="container">
    <h2 class="section-title">{html_escape(SH['reviews_title'])}</h2>
    <p class="section-intro">{html_escape(SH['reviews_intro'])}</p>
    <div class="reviews-grid">
{cards_html}    </div>
  </div>
</section>
"""


def render_banner(lang):
    L = LABELS[lang]
    SH = SECTION_HEADINGS[lang]
    return f"""<section class="banner">
  <div class="container">
    <p class="banner-text">{html_escape(SH['banner_text'])}</p>
    <div class="banner-ctas">
      <a href="tel:{PHONE_TEL}" class="btn-banner-primary">{L['call_cta']}</a>
      <button class="btn-banner-secondary" data-modal="hero-modal" type="button">{SH['hero_cta2']}</button>
    </div>
  </div>
</section>
"""


def render_services(lang, exclude_slug=None, count=4):
    SH = SECTION_HEADINGS[lang]
    lang_key_slug = "slug_en" if lang == "en" else "slug_es"
    lang_key_title = "card_title_en" if lang == "en" else "card_title_es"
    lang_key_text = "card_text_en" if lang == "en" else "card_text_es"
    lang_key_name = "name_en" if lang == "en" else "name_es"

    services = [s for s in SERVICES if s[lang_key_slug] != exclude_slug]
    # Homepage: show 4 highest-impact. Service page: show 4 related.
    featured_slugs = ["google-ads-management", "facebook-meta-ads", "website-design-development", "lead-generation"]
    if exclude_slug is None:
        ordered = [s for s in services if s["slug_en"] in featured_slugs]
        # ensure 4
        others = [s for s in services if s["slug_en"] not in featured_slugs]
        ordered.extend(others)
    else:
        # Service page — show 4 sibling services (skip current)
        ordered = services[:count]

    cards_html = ""
    for s in ordered[:count]:
        slug = s[lang_key_slug]
        cards_html += f"""        <a href="{clean_url(slug)}" class="service-card fade-in">
          <div class="service-card-image">
            <img src="/images/service-{s['slug_en']}.webp" alt="{html_escape(s[lang_key_name])} for home service contractors" loading="lazy" width="600" height="600">
          </div>
          <div class="service-card-body">
            <h3 class="service-card-title">{html_escape(s[lang_key_title])}</h3>
            <p class="service-card-text">{html_escape(s[lang_key_text])}</p>
            <span class="service-card-link">{SH['service_card_link']}</span>
          </div>
        </a>
"""
    return f"""<section class="services-section" id="services">
  <div class="container">
    <h2 class="section-title">{html_escape(SH['services_title'])}</h2>
    <p class="section-intro">{html_escape(SH['services_intro'])}</p>
    <div class="services-grid">
{cards_html}    </div>
  </div>
</section>
"""


def render_steps(lang):
    SH = SECTION_HEADINGS[lang]
    steps = [
        (STEP_ICONS[0], SH['step1_t'], SH['step1_b']),
        (STEP_ICONS[1], SH['step2_t'], SH['step2_b']),
        (STEP_ICONS[2], SH['step3_t'], SH['step3_b']),
    ]
    cards_html = ""
    for icon, title, body in steps:
        cards_html += f"""        <div class="step-card fade-in">
          <i class="{icon} step-icon"></i>
          <h3 class="step-title">{html_escape(title)}</h3>
          <p class="step-body">{html_escape(body)}</p>
        </div>
"""
    return f"""<section class="steps-section">
  <div class="container">
    <h2 class="section-title">{html_escape(SH['steps_title'])}</h2>
    <p class="section-intro">{html_escape(SH['steps_intro'])}</p>
    <div class="steps-grid">
{cards_html}    </div>
  </div>
</section>
"""


def render_faqs(lang, page_key):
    SH = SECTION_HEADINGS[lang]
    faqs_source = FAQS_EN if lang == "en" else FAQS_ES
    faqs = faqs_source.get(page_key, faqs_source["home"])

    items_html = ""
    for f in faqs:
        items_html += f"""      <div class="faq-item">
        <button class="faq-question" aria-expanded="false" type="button">
          <h3>{html_escape(f['q'])}</h3>
          <i class="fa-solid fa-chevron-down faq-chevron"></i>
        </button>
        <div class="faq-answer" hidden>
          <p>{html_escape(f['a'])}</p>
        </div>
      </div>
"""
    return f"""<section class="faqs-section">
  <div class="container">
    <h2 class="section-title">{html_escape(SH['faqs_title'])}</h2>
    <p class="section-intro">{html_escape(SH['faqs_intro'])}</p>
    <div class="faqs-accordion">
{items_html}    </div>
  </div>
</section>
"""


def render_footer(lang):
    L = LABELS[lang]
    SH = SECTION_HEADINGS[lang]
    logo_dark = "/images/logo-dark-backgrounds.png"
    privacy_path = clean_url("privacy-policy") if lang == "en" else clean_url("politica-de-privacidad")
    terms_path = clean_url("terms-and-conditions") if lang == "en" else clean_url("terminos-y-condiciones")
    home_href = "/" if lang == "en" else HOME_ES_PATH

    # Footer service list
    svc_links = []
    for s in SERVICES:
        slug = s["slug_en"] if lang == "en" else s["slug_es"]
        name = s["name_en"] if lang == "en" else s["name_es"]
        svc_links.append(f'    <a href="{clean_url(slug)}">{html_escape(name)}</a>')
    svc_links_html = "\n".join(svc_links)

    return f"""<footer class="footer">
  <div class="container footer-inner-solo">
    <a href="{home_href}" class="footer-brand">
      <img src="{logo_dark}" alt="{html_escape(BUSINESS_NAME)} logo" width="160">
      <span class="footer-company-name">{html_escape(BUSINESS_NAME)}</span>
    </a>
    <p class="footer-tagline">{html_escape(L['footer_tagline'])}</p>
    <div class="footer-ctas">
      <a href="tel:{PHONE_TEL}" class="btn-primary">{L['call_cta']}</a>
      <button class="btn-secondary" data-modal="hero-modal" type="button">{SH['hero_cta2']}</button>
    </div>
    <nav class="footer-nav" aria-label="Footer navigation">
{svc_links_html}
    </nav>
    <nav class="footer-nav" aria-label="Legal">
      <a href="{privacy_path}">{L['nav_privacy']}</a>
      <a href="{terms_path}">{L['nav_terms']}</a>
    </nav>
  </div>
  <div class="footer-bottom">
    <p>&copy; <span id="footer-year">{YEAR}</span> {html_escape(BUSINESS_NAME)}. {L['footer_rights']}</p>
  </div>
</footer>
"""


def render_modal(lang):
    L = LABELS[lang]
    step1_opts = MODAL_STEP1_OPTIONS[lang]
    step2_opts = MODAL_STEP2_OPTIONS[lang]
    step1_choices = "\n".join(
        f'''            <label class="choice-label">
              <input type="radio" name="step1" value="{html_escape(o)}">
              <span>{html_escape(o)}</span>
            </label>''' for o in step1_opts
    )
    step2_choices = "\n".join(
        f'''            <label class="choice-label">
              <input type="radio" name="step2" value="{html_escape(o)}">
              <span>{html_escape(o)}</span>
            </label>''' for o in step2_opts
    )
    dots_html = '<span class="active"></span><span></span><span></span>'

    return f"""<div class="modal-overlay" id="hero-modal"
     data-lang="{lang}"
     data-spanish-region="{BUSINESS['spanish_region']}"
     data-webhook="{BUSINESS['webhook_placeholder']}"
     data-business="{html_escape(BUSINESS_NAME)}"
     data-step1-q="{html_escape(L['modal_step1_q'])}"
     data-step2-q="{html_escape(L['modal_step2_q'])}"
     aria-hidden="true" role="dialog" aria-modal="true">
  <div class="modal-box">
    <button class="modal-close" aria-label="{L['modal_close']}" type="button">&times;</button>

    <div class="modal-form">
      <div class="modal-progress">
        <div class="modal-progress-dots">{dots_html}</div>
        <span class="modal-progress-label">Step 1 of 3</span>
      </div>

      <div class="modal-step active" data-step="1">
        <h3>{html_escape(L['modal_step1_q'])}</h3>
        <p class="step-subtitle">{html_escape(L['modal_step1_sub'])}</p>
        <div class="choice-grid">
{step1_choices}
        </div>
        <div class="modal-error" role="alert"></div>
        <div class="modal-nav">
          <span></span>
          <button class="btn-primary" data-action="next" type="button">{L['modal_next']} →</button>
        </div>
      </div>

      <div class="modal-step" data-step="2">
        <h3>{html_escape(L['modal_step2_q'])}</h3>
        <p class="step-subtitle">{html_escape(L['modal_step2_sub'])}</p>
        <div class="choice-grid">
{step2_choices}
        </div>
        <div class="modal-error" role="alert"></div>
        <div class="modal-nav">
          <button class="btn-secondary" data-action="back" type="button">← {L['modal_back']}</button>
          <button class="btn-primary" data-action="next" type="button">{L['modal_next']} →</button>
        </div>
      </div>

      <div class="modal-step" data-step="3">
        <h3>{html_escape(L['modal_step3_q'])}</h3>
        <p class="step-subtitle">{html_escape(L['modal_step3_sub'])}</p>
        <div class="modal-input-group">
          <label for="modal-name">{L['modal_name']}</label>
          <input type="text" id="modal-name" name="name" autocomplete="name" required>
        </div>
        <div class="modal-input-group">
          <label for="modal-phone">{L['modal_phone']}</label>
          <input type="tel" id="modal-phone" name="phone" autocomplete="tel" required>
        </div>
        <div class="modal-input-group">
          <label for="modal-email">{L['modal_email']}</label>
          <input type="email" id="modal-email" name="email" autocomplete="email" required>
        </div>
        <div class="modal-error" role="alert"></div>
        <div class="modal-nav">
          <button class="btn-secondary" data-action="back" type="button">← {L['modal_back']}</button>
          <button class="btn-primary" data-action="submit" type="button">{L['modal_submit']}</button>
        </div>
      </div>
    </div>

    <div class="modal-success">
      <div class="success-icon"><i class="fa-solid fa-circle-check"></i></div>
      <h3>{L['modal_success_title'] % ''}<span class="success-name"></span>!</h3>
      <p>{L['modal_success_body']}</p>
    </div>

    <div class="modal-error-state">
      <div class="error-icon"><i class="fa-solid fa-triangle-exclamation"></i></div>
      <h3>{L['modal_error_title']}</h3>
      <p>{L['modal_error_body']}</p>
    </div>
  </div>
</div>
"""


def render_mobile_cta(lang):
    L = LABELS[lang]
    return f"""<div class="mobile-cta-bar" role="complementary">
  <a href="tel:{PHONE_TEL}" class="btn-call">{L['mobile_call']}</a>
  <button class="btn-quote" data-modal="hero-modal" type="button">{L['mobile_quote']}</button>
</div>
"""


def render_body_close(lang):
    return """<script src="/js/main.js" defer></script>
</body>
</html>
"""


def render_full_page(lang, title, description, og_image, canonical_path, alt_path,
                    hero_headline, hero_body, hero_bg,
                    page_type, page_slug_for_reviews_and_faqs, exclude_service_slug=None):
    head = render_head(None, lang, title, description, og_image, canonical_path, alt_path)
    nav = render_nav(lang, canonical_path)
    # h1 on every page is the exact <title> content
    hero = render_hero(lang, title, hero_headline, hero_body, hero_bg)
    why = render_why_us(lang)
    about = render_about_us(lang, page_type)
    reviews = render_reviews(lang, page_slug_for_reviews_and_faqs)
    banner = render_banner(lang)
    services = render_services(lang, exclude_slug=exclude_service_slug)
    steps = render_steps(lang)
    faqs = render_faqs(lang, page_slug_for_reviews_and_faqs)
    footer = render_footer(lang)
    modal = render_modal(lang)
    mobile_cta = render_mobile_cta(lang)

    return head + "<body>\n" + nav + hero + why + about + reviews + banner + services + steps + faqs + footer + modal + mobile_cta + render_body_close(lang)


def write_file(rel_path, content):
    p = ROOT / rel_path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    print("wrote", rel_path, "(" + str(len(content)) + " chars)")


# ── Build: Homepages ─────────────────────────────────────────────────────────

def build_homepage(lang):
    if lang == "en":
        title = BUSINESS_NAME + " | Home Services Digital Marketing Agency"
        description = "Home services digital marketing agency built exclusively for contractors. Google Ads, Facebook Ads, websites, and lead gen that make your phone ring. Call (602) 829-0009."
        hero_headline = "Stop Losing Jobs To Contractors Who Just Out-Market You"
        hero_body = "You're great at your trade. Your marketing shouldn't be a second job you're bad at. Get Google Ads, Facebook campaigns, websites, and lead generation engineered exclusively for home service contractors — and watch the phone start ringing like it should."
        out_path = HOME_EN_FILE
        canon = "/"
        alt = HOME_ES_PATH
    else:
        title = BUSINESS_NAME + " | Agencia de Marketing Digital para Servicios del Hogar"
        description = "Agencia de marketing digital creada exclusivamente para contratistas de servicios del hogar. Google Ads, Facebook Ads, sitios web y generación de leads. Llama al (602) 829-0009."
        hero_headline = "Deja De Perder Trabajos Con Contratistas Que Simplemente Se Venden Mejor"
        hero_body = "Eres bueno en tu oficio. El marketing no debería ser un segundo trabajo en el que eres malo. Obtén Google Ads, campañas de Facebook, sitios web, y generación de leads creados exclusivamente para contratistas — y mira cómo empieza a sonar tu teléfono."
        out_path = HOME_ES_FILE
        canon = HOME_ES_PATH
        alt = "/"

    html = render_full_page(
        lang=lang,
        title=title,
        description=description,
        og_image="og-image.webp",
        canonical_path=canon,
        alt_path=alt,
        hero_headline=hero_headline,
        hero_body=hero_body,
        hero_bg="hero-bg.webp",
        page_type="home",
        page_slug_for_reviews_and_faqs="home",
        exclude_service_slug=None,
    )
    write_file(out_path, html)


# ── Build: Service pages ─────────────────────────────────────────────────────

def build_service_pages(lang):
    for s in SERVICES:
        slug = s["slug_en"] if lang == "en" else s["slug_es"]
        title = s["title_en"] if lang == "en" else s["title_es"]
        description = s["meta_desc_en"] if lang == "en" else s["meta_desc_es"]
        hero_headline = s["hero_headline_en"] if lang == "en" else s["hero_headline_es"]
        hero_body = s["hero_body_en"] if lang == "en" else s["hero_body_es"]
        hero_bg = "hero-" + s["slug_en"] + ".webp"  # images only exist in English slug naming
        og_image = "og-" + s["slug_en"] + ".webp"

        alt_slug = s["slug_es"] if lang == "en" else s["slug_en"]
        canon = clean_url(slug)
        alt = clean_url(alt_slug)

        # FAQs key: always keyed by English slug for EN, Spanish slug for ES
        faqs_key = s["slug_en"] if lang == "en" else s["slug_es"]

        html = render_full_page(
            lang=lang,
            title=title,
            description=description,
            og_image=og_image,
            canonical_path=canon,
            alt_path=alt,
            hero_headline=hero_headline,
            hero_body=hero_body,
            hero_bg=hero_bg,
            page_type="service",
            page_slug_for_reviews_and_faqs=faqs_key,
            exclude_service_slug=slug,
        )
        write_file(clean_file(slug), html)


# ── Build: Legal pages ───────────────────────────────────────────────────────

LEGAL_SERVICES_LIST_EN = ", ".join(s["name_en"] for s in SERVICES)
LEGAL_SERVICES_LIST_ES = ", ".join(s["name_es"] for s in SERVICES)


def render_legal_page(lang, which, sections, title_txt):
    """which: 'privacy' or 'terms'. sections: list of (h2, [paragraphs])."""
    if lang == "en":
        if which == "privacy":
            canon = clean_url("privacy-policy")
            alt = clean_url("politica-de-privacidad")
        else:
            canon = clean_url("terms-and-conditions")
            alt = clean_url("terminos-y-condiciones")
    else:
        if which == "privacy":
            canon = clean_url("politica-de-privacidad")
            alt = clean_url("privacy-policy")
        else:
            canon = clean_url("terminos-y-condiciones")
            alt = clean_url("terms-and-conditions")

    description = (title_txt + " — " + BUSINESS_NAME)[:160]
    full_title = title_txt + " | " + BUSINESS_NAME

    head = render_head(None, lang, full_title, description,
                       "og-image.webp", canon, alt)
    nav = render_nav(lang, canon)
    footer = render_footer(lang)
    modal = render_modal(lang)
    mobile_cta = render_mobile_cta(lang)

    last_updated = "Last updated: " + BUILD_DATE if lang == "en" else "Última actualización: " + BUILD_DATE

    sections_html = ""
    for h2, paragraphs in sections:
        sections_html += f"          <h2>{html_escape(h2)}</h2>\n"
        for p in paragraphs:
            if isinstance(p, list):
                sections_html += "          <ul>\n"
                for li in p:
                    sections_html += f"            <li>{html_escape(li)}</li>\n"
                sections_html += "          </ul>\n"
            else:
                sections_html += f"          <p>{html_escape(p)}</p>\n"

    main_html = f"""<main class="legal-page">
  <div class="container">
    <div class="legal-content">
        <h1>{html_escape(title_txt)}</h1>
        <p class="legal-meta">{html_escape(last_updated)}</p>
{sections_html}    </div>
  </div>
</main>
"""
    return head + "<body>\n" + nav + main_html + footer + modal + mobile_cta + render_body_close(lang)


PRIVACY_EN_SECTIONS = [
    ("1. Introduction", [
        f"Welcome to {BUSINESS_NAME}. {BUSINESS_NAME} is a home services digital marketing agency that provides services across the United States, including {LEGAL_SERVICES_LIST_EN}. This Privacy Policy explains how we collect, use, and protect the information you share with us when you visit our website or request our services.",
        f"By using our website or contacting us through any form, email, or phone call, you agree to the practices described in this policy. If you have questions, contact us at {EMAIL}.",
    ]),
    ("2. Information We Collect", [
        "We collect two types of information:",
        "Information you provide directly:",
        [
            "Your name, phone number, and email address",
            "Your business name and industry (when you request services)",
            "Any messages, service requests, or details you share through our forms, modals, or communications",
        ],
        "Information collected automatically:",
        [
            "IP address and approximate geographic location",
            "Browser type, device type, and operating system",
            "Pages visited, time spent, and referring websites (via standard web analytics)",
        ],
    ]),
    ("3. How We Use Your Information", [
        f"We use the information we collect to respond to your inquiries and schedule consultations, deliver the {BUSINESS_NAME} marketing services you request, send follow-up communications related to your request, improve our website and service offerings, and comply with legal obligations.",
        f"{BUSINESS_NAME} does not sell, rent, or trade your personal information to third parties for marketing purposes.",
    ]),
    ("4. How We Share Your Information", [
        "We only share your information with trusted service providers who help us operate this website and deliver our services — such as hosting providers, email platforms, CRM systems, and analytics tools. These partners are contractually bound to protect your information.",
        "We may also disclose information when required by law, a court order, or a government request, or when necessary to protect our rights, safety, or property.",
    ]),
    ("5. Cookies & Tracking Technologies", [
        "Our website may use cookies, pixels, and similar technologies to understand how visitors interact with the site, improve performance, and measure marketing effectiveness. You can disable cookies in your browser settings; some site features may not work as intended if cookies are blocked.",
    ]),
    ("6. Data Security", [
        "We take reasonable administrative, technical, and physical measures to protect the information you share with us. However, no method of transmission over the internet or electronic storage is 100% secure, and we cannot guarantee absolute security.",
    ]),
    ("7. Third-Party Links", [
        "This website may contain links to third-party websites (such as Google, Facebook, or partner platforms). We are not responsible for the privacy practices or content of those sites. We encourage you to review their privacy policies before providing any information.",
    ]),
    ("8. Children's Privacy", [
        "Our services are directed at business owners and operators — not children. We do not knowingly collect personal information from individuals under the age of 13. If you believe a child has submitted information to us, please contact us at " + EMAIL + " and we will delete it promptly.",
    ]),
    ("9. Your Rights", [
        f"You have the right to request access to, correction of, or deletion of the personal information we hold about you. Depending on your state of residence, you may have additional rights under applicable privacy laws. To exercise these rights, contact us at {EMAIL}.",
    ]),
    ("10. Changes To This Policy", [
        "We may update this Privacy Policy from time to time to reflect changes in our practices, technology, or legal obligations. The \"Last updated\" date above will always reflect the most recent revision. Continued use of our website after changes means you accept the updated policy.",
    ]),
    ("11. Contact Us", [
        f"If you have any questions about this Privacy Policy or how we handle your information, please contact {BUSINESS_NAME} by phone at {PHONE_DISPLAY} or by email at {EMAIL}.",
    ]),
]

TERMS_EN_SECTIONS = [
    ("1. Acceptance Of Terms", [
        f"By accessing or using this website, requesting services, or communicating with {BUSINESS_NAME} in any way, you agree to these Terms and Conditions. If you do not agree, please do not use this site or engage our services.",
    ]),
    ("2. Services Offered", [
        f"{BUSINESS_NAME} provides digital marketing services exclusively for home service contractors across the United States, including {LEGAL_SERVICES_LIST_EN}. Service availability, scope, and deliverables are subject to the terms of each engagement agreement.",
    ]),
    ("3. Quotes And Estimates", [
        f"Quotes and estimates provided through this website, phone, or email are preliminary and based on the information you share. Final pricing and scope are confirmed in writing before any work begins. {BUSINESS_NAME} reserves the right to adjust quotes as additional information or requirements become clear.",
    ]),
    ("4. Engagement And Scheduling", [
        f"Engagements are scheduled based on available capacity and agreed timelines. {BUSINESS_NAME} will make reasonable efforts to honor scheduled start dates and deliverables. You agree to provide accurate business information, access to accounts needed for service delivery, and timely feedback so work can proceed.",
    ]),
    ("5. Payment Terms", [
        "Payment terms are specified in your engagement agreement. Invoices are due by the date shown on each invoice unless otherwise agreed in writing. Late payments may incur late fees and may result in a pause in active campaigns or services until the balance is resolved.",
    ]),
    ("6. Performance And Guarantees", [
        f"{BUSINESS_NAME} commits to the scope of services outlined in your engagement agreement and delivers all work to professional industry standards. Marketing results are influenced by factors including market competition, ad spend, offer quality, and internal sales follow-up — so specific lead volume, call volume, or revenue outcomes are not guaranteed unless explicitly stated in writing.",
    ]),
    ("7. Limitation Of Liability", [
        f"To the fullest extent permitted by law, {BUSINESS_NAME} is not liable for indirect, incidental, consequential, or punitive damages arising from your use of this website or our services. Total liability for any claim is limited to the amount paid for the specific service in question during the preceding three months.",
    ]),
    ("8. Client Responsibilities", [
        "You agree to provide accurate business information, grant reasonable access to marketing accounts (Google Ads, Facebook, Google Business Profile, website) required for service delivery, respond to leads and calls generated by campaigns in a timely professional manner, and comply with all applicable laws including advertising and licensing regulations for your trade and service area.",
    ]),
    ("9. Intellectual Property", [
        f"All content on this website — including copy, design, graphics, photography, and code — is the property of {BUSINESS_NAME} or its licensors and is protected by copyright and trademark laws. You may not reproduce, redistribute, or modify any content without written permission.",
        "Work product delivered to you as part of an engagement (landing pages, ad copy, creative assets, websites) becomes your property upon full payment unless otherwise stated in your engagement agreement.",
    ]),
    ("10. Dispute Resolution", [
        f"Any dispute arising from these Terms or our services will first be addressed through good-faith negotiation. If unresolved, disputes will be handled through binding arbitration in Maricopa County, Arizona, under the rules of the American Arbitration Association. The laws of the State of Arizona govern these Terms.",
    ]),
    ("11. Changes To Terms", [
        f"{BUSINESS_NAME} reserves the right to update these Terms and Conditions at any time. Continued use of this website or our services after changes are posted constitutes acceptance of the updated Terms.",
    ]),
    ("12. Contact Us", [
        f"If you have any questions about these Terms and Conditions, contact {BUSINESS_NAME} at {PHONE_DISPLAY} or {EMAIL}.",
    ]),
]

PRIVACY_ES_SECTIONS = [
    ("1. Introducción", [
        f"Bienvenido a {BUSINESS_NAME}. {BUSINESS_NAME} es una agencia de marketing digital para servicios del hogar que brinda servicios en todo Estados Unidos, incluyendo {LEGAL_SERVICES_LIST_ES}. Esta Política de Privacidad explica cómo recolectamos, usamos, y protegemos la información que compartes con nosotros cuando visitas nuestro sitio o solicitas nuestros servicios.",
        f"Al usar nuestro sitio o contactarnos por formulario, correo, o llamada, aceptas las prácticas descritas en esta política. Si tienes preguntas, contáctanos en {EMAIL}.",
    ]),
    ("2. Información Que Recolectamos", [
        "Recolectamos dos tipos de información:",
        "Información que proporcionas directamente:",
        [
            "Tu nombre, número de teléfono, y correo electrónico",
            "Tu nombre de negocio e industria (cuando solicitas servicios)",
            "Cualquier mensaje, solicitud de servicio, o detalle que compartas en formularios o comunicaciones",
        ],
        "Información recolectada automáticamente:",
        [
            "Dirección IP y ubicación geográfica aproximada",
            "Tipo de navegador, dispositivo, y sistema operativo",
            "Páginas visitadas, tiempo de permanencia, y sitios de referencia (vía analítica estándar)",
        ],
    ]),
    ("3. Cómo Usamos Tu Información", [
        f"Usamos la información que recolectamos para responder a tus consultas y agendar asesorías, entregar los servicios de marketing de {BUSINESS_NAME} que solicitas, enviar comunicaciones de seguimiento relacionadas con tu solicitud, mejorar nuestro sitio y servicios, y cumplir con obligaciones legales.",
        f"{BUSINESS_NAME} no vende, renta, ni intercambia tu información personal con terceros con fines de marketing.",
    ]),
    ("4. Cómo Compartimos Tu Información", [
        "Solo compartimos tu información con proveedores confiables que nos ayudan a operar este sitio y entregar nuestros servicios — como proveedores de hosting, plataformas de correo, sistemas CRM, y herramientas de analítica. Estos socios están obligados por contrato a proteger tu información.",
        "También podemos revelar información cuando lo requiera la ley, una orden judicial, o una solicitud gubernamental, o cuando sea necesario para proteger nuestros derechos, seguridad, o propiedad.",
    ]),
    ("5. Cookies Y Tecnologías De Rastreo", [
        "Nuestro sitio puede usar cookies, píxeles, y tecnologías similares para entender cómo interactúan los visitantes, mejorar el rendimiento, y medir la efectividad del marketing. Puedes deshabilitar las cookies en la configuración de tu navegador; algunas funciones del sitio pueden no funcionar como se espera si se bloquean.",
    ]),
    ("6. Seguridad De Datos", [
        "Tomamos medidas administrativas, técnicas, y físicas razonables para proteger la información que compartes con nosotros. Sin embargo, ningún método de transmisión por internet o almacenamiento electrónico es 100% seguro, y no podemos garantizar seguridad absoluta.",
    ]),
    ("7. Enlaces A Terceros", [
        "Este sitio puede contener enlaces a sitios de terceros (como Google, Facebook, o plataformas asociadas). No somos responsables de sus prácticas de privacidad ni contenido. Te recomendamos revisar sus políticas de privacidad antes de proporcionar información.",
    ]),
    ("8. Privacidad De Menores", [
        f"Nuestros servicios están dirigidos a dueños y operadores de negocios — no a niños. No recolectamos intencionalmente información personal de individuos menores de 13 años. Si crees que un niño ha enviado información, contáctanos en {EMAIL} y la eliminaremos rápidamente.",
    ]),
    ("9. Tus Derechos", [
        f"Tienes derecho a solicitar acceso, corrección, o eliminación de la información personal que tenemos sobre ti. Dependiendo de tu estado de residencia, puedes tener derechos adicionales bajo las leyes de privacidad aplicables. Para ejercer estos derechos, contáctanos en {EMAIL}.",
    ]),
    ("10. Cambios A Esta Política", [
        "Podemos actualizar esta Política de Privacidad de tiempo en tiempo para reflejar cambios en nuestras prácticas, tecnología, u obligaciones legales. La fecha de \"Última actualización\" arriba siempre reflejará la revisión más reciente.",
    ]),
    ("11. Contáctanos", [
        f"Si tienes preguntas sobre esta Política de Privacidad o cómo manejamos tu información, por favor contacta a {BUSINESS_NAME} por teléfono al {PHONE_DISPLAY} o por correo a {EMAIL}.",
    ]),
]

TERMS_ES_SECTIONS = [
    ("1. Aceptación De Términos", [
        f"Al acceder o usar este sitio, solicitar servicios, o comunicarte con {BUSINESS_NAME} de cualquier manera, aceptas estos Términos y Condiciones. Si no estás de acuerdo, por favor no uses este sitio ni contrates nuestros servicios.",
    ]),
    ("2. Servicios Ofrecidos", [
        f"{BUSINESS_NAME} brinda servicios de marketing digital exclusivamente para contratistas de servicios del hogar en todo Estados Unidos, incluyendo {LEGAL_SERVICES_LIST_ES}. La disponibilidad, alcance, y entregables de los servicios están sujetos a los términos de cada acuerdo de servicio.",
    ]),
    ("3. Cotizaciones Y Estimados", [
        f"Las cotizaciones y estimados proporcionados a través de este sitio, teléfono, o correo son preliminares y se basan en la información que compartes. Los precios finales y el alcance se confirman por escrito antes de comenzar cualquier trabajo. {BUSINESS_NAME} se reserva el derecho de ajustar cotizaciones.",
    ]),
    ("4. Compromiso Y Programación", [
        f"Los compromisos se programan según capacidad disponible y cronogramas acordados. {BUSINESS_NAME} hará esfuerzos razonables para honrar las fechas de inicio programadas y los entregables. Aceptas proporcionar información precisa, acceso a cuentas necesarias, y retroalimentación oportuna.",
    ]),
    ("5. Términos De Pago", [
        "Los términos de pago se especifican en tu acuerdo de servicio. Las facturas vencen en la fecha mostrada a menos que se acuerde por escrito. Los pagos tardíos pueden incurrir en cargos y pueden resultar en una pausa de las campañas o servicios activos hasta que se resuelva el saldo.",
    ]),
    ("6. Desempeño Y Garantías", [
        f"{BUSINESS_NAME} se compromete al alcance de servicios delineado en tu acuerdo y entrega todo el trabajo con estándares profesionales de la industria. Los resultados de marketing están influenciados por factores que incluyen competencia de mercado, gasto en anuncios, calidad de oferta, y seguimiento interno de ventas — por lo tanto, resultados específicos de volumen de leads, llamadas, o ingresos no se garantizan a menos que se declare explícitamente por escrito.",
    ]),
    ("7. Limitación De Responsabilidad", [
        f"Hasta el máximo permitido por la ley, {BUSINESS_NAME} no es responsable por daños indirectos, incidentales, consecuentes, o punitivos derivados de tu uso de este sitio o nuestros servicios. La responsabilidad total por cualquier reclamo se limita al monto pagado por el servicio específico en cuestión durante los tres meses anteriores.",
    ]),
    ("8. Responsabilidades Del Cliente", [
        "Aceptas proporcionar información precisa, otorgar acceso razonable a las cuentas de marketing (Google Ads, Facebook, Google Business Profile, sitio web) requeridas para la entrega del servicio, responder a leads y llamadas generadas por las campañas de manera oportuna y profesional, y cumplir con todas las leyes aplicables incluyendo regulaciones de publicidad y licencias para tu oficio.",
    ]),
    ("9. Propiedad Intelectual", [
        f"Todo el contenido de este sitio — incluyendo textos, diseño, gráficos, fotografía, y código — es propiedad de {BUSINESS_NAME} o sus licenciantes y está protegido por leyes de derechos de autor y marcas. No puedes reproducir, redistribuir, o modificar ningún contenido sin permiso por escrito.",
        "El producto del trabajo entregado a ti como parte de un compromiso (páginas de aterrizaje, copys, activos creativos, sitios) se vuelve tu propiedad al pago completo a menos que se indique lo contrario.",
    ]),
    ("10. Resolución De Disputas", [
        f"Cualquier disputa que surja de estos Términos o nuestros servicios se abordará primero a través de negociación de buena fe. Si no se resuelve, las disputas se manejarán a través de arbitraje vinculante en el Condado de Maricopa, Arizona, bajo las reglas de la Asociación Americana de Arbitraje. Las leyes del Estado de Arizona rigen estos Términos.",
    ]),
    ("11. Cambios A Los Términos", [
        f"{BUSINESS_NAME} se reserva el derecho de actualizar estos Términos y Condiciones en cualquier momento. El uso continuado de este sitio o nuestros servicios después de publicar cambios constituye aceptación de los Términos actualizados.",
    ]),
    ("12. Contáctanos", [
        f"Si tienes preguntas sobre estos Términos y Condiciones, contacta a {BUSINESS_NAME} al {PHONE_DISPLAY} o {EMAIL}.",
    ]),
]


def build_legal_pages():
    write_file(clean_file("privacy-policy"),
               render_legal_page("en", "privacy", PRIVACY_EN_SECTIONS, "Privacy Policy"))
    write_file(clean_file("terms-and-conditions"),
               render_legal_page("en", "terms", TERMS_EN_SECTIONS, "Terms and Conditions"))
    write_file(clean_file("politica-de-privacidad"),
               render_legal_page("es", "privacy", PRIVACY_ES_SECTIONS, "Política de Privacidad"))
    write_file(clean_file("terminos-y-condiciones"),
               render_legal_page("es", "terms", TERMS_ES_SECTIONS, "Términos y Condiciones"))


# ── Build: 404 ───────────────────────────────────────────────────────────────

def build_404():
    title = "Page Not Found | " + BUSINESS_NAME
    description = "The page you were looking for isn't here — but your next marketing win could be. Call (602) 829-0009 or explore our services."
    head = render_head(None, "en", title, description, "og-image.webp", "/404.html", "/")
    nav = render_nav("en", "/404.html")
    main = f"""<main class="error-page">
  <div class="error-content">
    <div class="error-mark" aria-hidden="true">404</div>
    <h1>{html_escape(h1_from_title(title))}</h1>
    <p class="error-sub">This page took a wrong turn — but you don't have to. Most of the good stuff is one click away. Head back home, or tap the Call button and we'll point you to exactly what you need.</p>
    <div class="hero-ctas" style="justify-content:center;">
      <a href="/" class="btn-primary">Back To Home</a>
      <a href="tel:{PHONE_TEL}" class="btn-secondary">Call {PHONE_DISPLAY}</a>
    </div>
  </div>
</main>
"""
    footer = render_footer("en")
    modal = render_modal("en")
    mobile_cta = render_mobile_cta("en")
    html = head + "<body>\n" + nav + main + footer + modal + mobile_cta + render_body_close("en")
    write_file("404.html", html)


# ── Build: sitemap, robots, gitignore ────────────────────────────────────────

def build_support_files():
    urls = ["/", HOME_ES_PATH]
    for s in SERVICES:
        urls.append(clean_url(s["slug_en"]))
        urls.append(clean_url(s["slug_es"]))
    urls += [clean_url("privacy-policy"), clean_url("terms-and-conditions"),
             clean_url("politica-de-privacidad"), clean_url("terminos-y-condiciones")]

    today = datetime.date.today().isoformat()
    url_blocks = []
    for u in urls:
        priority = "1.0" if u == "/" else ("0.9" if u == HOME_ES_PATH else
                                            "0.3" if "policy" in u or "terms" in u or "politica" in u or "terminos" in u else "0.8")
        url_blocks.append(f"""  <url>
    <loc>https://{DOMAIN}{u}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>{priority}</priority>
  </url>""")
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(url_blocks) + "\n</urlset>\n"
    write_file("sitemap.xml", sitemap)

    robots = f"""User-agent: *
Allow: /
Disallow: /scripts/
Disallow: /.env

Sitemap: https://{DOMAIN}/sitemap.xml
"""
    write_file("robots.txt", robots)

    gitignore = """# Environment — NEVER commit
.env
.env.local
.env.*

# OS files
.DS_Store
Thumbs.db

# Editor files
.vscode/
.idea/
*.swp

# Python build cache
__pycache__/
*.pyc

# Claude Code — local settings and worktrees (keep launch.json for previewing)
.claude/settings.local.json
.claude/worktrees/
"""
    write_file(".gitignore", gitignore)


# ── Main ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Building Firefly Rise site...\n")

    build_homepage("en")
    build_homepage("es")

    build_service_pages("en")
    build_service_pages("es")

    build_legal_pages()
    build_404()
    build_support_files()

    print("\nDone.")
