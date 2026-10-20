"""Helpers to add a new article/page to the Curio & Cove static site (site_out)."""
import json, re, os

import os as _os
SITE = _os.environ.get("CC_SITE", "/home/claude/site_out")
TEMPLATE = f"{SITE}/do-you-need-a-vpn-when-you-travel/index.html"
A = 'rel="sponsored nofollow noopener" target="_blank"'

LINKS = {
    "nordvpn": "https://www.anrdoezrs.net/click-101697384-12814518",
    "surfshark": "https://www.jdoqocy.com/click-101697384-15438560",
    "nordpass": "https://www.kqzyfj.com/click-101697384-13868703",
    "clickgrow": "https://www.dpbolvw.net/click-101697384-11792320",
    "rexing": "https://www.dpbolvw.net/click-101697384-15019509",
    "abracadabra": "https://www.anrdoezrs.net/click-101697384-17267156",
    "tripcom": "https://www.tkqlhce.com/click-101697384-11947208",
    "kit": "https://partners.kit.com/x60xmzo3zk03",
    "tubemagic": "https://tubemagic.com/ds#aff=SorinSerban",
    "saily": "https://saily.tpm.lv/i1NUak7J",
    "yesim": "https://yesim.tpm.lv/BRdfvpN3",
    "gigsky": "https://gigsky.tpm.lv/yBYfjR4k",
    "drimsim": "https://drimsim.tpm.lv/OpVW6kki",
    "kiwi": "https://kiwi.tpm.lv/oyXFK7E1",
    "airhelp": "https://airhelp.tpm.lv/msA3EhRz",
    "gettransfer": "https://gettransfer.tpm.lv/vsoIu6TN",
    "localrent": "https://localrent.tpm.lv/y7LwGKjK",
    "gocity": "https://gocity.tpm.lv/cUPURB8r",
    "tiqets": "https://tiqets.tpm.lv/iUScXcHE",
    "radical": "https://radicalstorage.tpm.lv/J22dmTvc",
    "sellfy": "https://sellfy.com/?via=sorin-curio-and-cove",
    "elevenlabs": "https://try.elevenlabs.io/9tyqbjdbsh85",
    "doola": "https://app.doola.com/signup/registration?mwr=curio-ef72",
}
CJ = {"nordvpn", "surfshark", "nordpass", "clickgrow", "rexing", "abracadabra"}


def url(key, sid=None, trip_path=None):
    u = LINKS[key]
    if key == "tripcom":
        path = trip_path or "flights"
        u += f"?url=https%3A%2F%2Fwww.trip.com%2F{path}%2F"
        if sid:
            u += f"&amp;sid={sid}"
    elif key in CJ and sid:
        u += f"?sid={sid}"
    return u


def a(key, text, sid=None, trip_path=None):
    return f'<a href="{url(key, sid, trip_path)}" {A}>{text}</a>'


def btn(key, text, sid=None, trip_path=None):
    return f'<p><a class="btn" href="{url(key, sid, trip_path)}" {A}>{text}</a></p>'


def faq(items):
    h = '\n<h2>Frequently asked questions</h2>\n'
    for q, ans in items:
        h += f'<h3>{q}</h3>\n<p>{ans}</p>\n'
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub('<[^>]+>', '', ans)}}
        for q, ans in items]}
    return h, '<script type="application/ld+json">' + json.dumps(ld) + '</script>\n'


def card(slug, title, excerpt, read, niche, cat_label=None):
    c = f'<span class="card-cat">{cat_label}</span>' if cat_label else ''
    return (f'<li class="card niche-{niche}"><a href="/{slug}/">{c}<span class="card-title">{title}</span>'
            f'<span class="card-excerpt">{excerpt}</span><span class="card-meta">{read}</span></a></li>')


CATS = {"travel": ("Travel", "travel"), "money-skills": ("Money &amp; Skills", "money-skills"),
        "home-garden": ("Home &amp; Garden", "home-garden"), "love-family": ("Love &amp; Family", "love-family")}
CAT_LABEL = {"travel": "Travel", "money-skills": "Money & Skills", "home-garden": "Home & Garden", "love-family": "Love & Family"}


def make(slug, title, desc, cat, body, read, excerpt, more_cards, faq_items=None, date="2026-10-17",
         date_text="October 17, 2026", aff=True, article=True, add_listing=True):
    src = open(TEMPLATE).read()
    head = src[:src.index('<article')]
    for o, n in [('Do You Need a VPN When You Travel? An Honest Guide | Curio & Cove', title + ' | Curio & Cove'),
                 ("When a VPN is genuinely useful abroad, when it isn't, how NordVPN and Surfshark compare for travellers, and how to set one up before you leave.", desc),
                 ('do-you-need-a-vpn-when-you-travel', slug),
                 ('Do You Need a VPN When You Travel? An Honest Guide', title),
                 ('2026-10-13', date)]:
        head = head.replace(o, n)
    if not article:
        head = re.sub(r'<script type="application/ld\+json">.*?</script>\n', '', head, count=1)
        head = head.replace('<meta property="og:type" content="article">', '<meta property="og:type" content="website">')
        head = re.sub(r'<meta property="article:published_time"[^>]*>\n', '', head)
    fq = ""
    if faq_items:
        fh, ld = faq(faq_items)
        fq = fh
        head = head.replace('<link rel="icon"', ld + '<link rel="icon"', 1)
    catname, catslug = CATS[cat]
    note = ('<p class="aff-note">This article contains affiliate links. If you buy through them, we may earn a commission '
            'at no extra cost to you. <a href="/disclosure/">How this works</a>.</p>\n') if aff else ''
    meta = f'<p class="post-meta">Published {date_text} &ndash; {read}</p>' if article else ''
    art = f'''<article class="post niche-{cat}">
  <header class="post-head">
    <p class="crumbs"><a href="/{catslug}/">{catname}</a></p>
    <h1>{title}</h1>
    {meta}
  </header>
  <div class="prose post-body">
    {note}
{body}
{fq}
  </div>
</article>
'''
    more = ('<section class="latest more">\n  <h2>Keep exploring</h2>\n  <ul class="cards">' + ''.join(more_cards) +
            '</ul>\n</section>\n\n') if more_cards else ''
    tail = src[src.index('</main>'):]
    os.makedirs(f"{SITE}/{slug}", exist_ok=True)
    open(f"{SITE}/{slug}/index.html", "w").write(head + art + more + tail)
    if add_listing:
        for p in ["index.html", f"{catslug}/index.html"]:
            s = open(f"{SITE}/{p}").read()
            if f'href="/{slug}/"' in s.split('<ul class="cards">', 1)[-1][:3000]:
                continue
            k = s.index('<ul class="cards">') + len('<ul class="cards">')
            has = 'card-cat' in s[k:k + 400]
            s = s[:k] + card(slug, title, excerpt, read, cat, CAT_LABEL[cat] if has else None) + s[k:]
            open(f"{SITE}/{p}", "w").write(s)
    sm = open(f"{SITE}/sitemap.xml").read()
    if f"/{slug}/<" not in sm:
        sm = sm.replace('</urlset>', f'  <url><loc>https://curioandcove.com/{slug}/</loc><lastmod>{date}</lastmod></url>\n</urlset>')
        open(f"{SITE}/sitemap.xml", "w").write(sm)
    words = len(re.sub('<[^>]+>', ' ', body).split())
    return words


def check(slug):
    s = open(f"{SITE}/{slug}/index.html").read()
    ext = re.findall(r'<a ([^>]*href="https?://(?!curioandcove)[^"]*"[^>]*)>', s)
    miss = [e for e in ext if 'sponsored' not in e and 'pinterest' not in e and 'mailto' not in e]
    broken = [u for u in re.findall(r'href="(/[^"#]*)"', s)
              if not os.path.exists(SITE + u + ('index.html' if u.endswith('/') else ''))]
    for m in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s):
        json.loads(m)
    return {"external": len(ext), "missing_sponsored": miss, "broken_internal": broken}


def existing_card(slug):
    """Return the card markup for an existing article from the homepage listing."""
    s = open(f"{SITE}/index.html").read()
    m = re.search(r'<li class="card[^"]*"><a href="/' + re.escape(slug) + r'/">.*?</li>', s)
    return m.group(0) if m else ''
