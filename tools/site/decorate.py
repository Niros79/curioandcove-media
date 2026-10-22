"""v4 design pass for Curio & Cove (idempotent). Run after adding pages:
    python3 tools/site/decorate.py site/public
- swaps fonts to Fraunces + Inter and bumps style.css to v4
- adds the header CTA
- adds a photo to every article card (assets/img/sm/<slug>.jpg)
- adds a hero photo under each article title (assets/img/<slug>.jpg) + og:image
- replaces the arch icon on shelf pages with the shelf photo
"""
import os, re, sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else "site/public"
IMG = os.path.join(ROOT, "assets", "img")
SHELF = {"travel": "travel", "money-skills": "money", "home-garden": "home",
         "love-family": "love", "mind-spirit": "mind", "crafts-hobbies": "crafts"}
OLD_FONT = "family=Gloock&family=Nunito+Sans:opsz,wght@6..12,400;6..12,600;6..12,700"
NEW_FONT = "family=Fraunces:opsz,wght@9..144,600;9..144,700&family=Inter:wght@400;500;600;700"
CTA = '<a class="head-cta" href="/#newsletter">Free trip checklist</a>'


def has(name, sub=""):
    return os.path.exists(os.path.join(IMG, sub, name + ".jpg"))


def card_img(m):
    slug = m.group(2)
    if not has(slug, "sm"):
        return m.group(0)
    return (f'{m.group(1)}<img class="card-img" src="/assets/img/sm/{slug}.jpg" alt="" '
            f'loading="lazy" width="800" height="500">')


def run():
    n = 0
    for dirpath, _, files in os.walk(ROOT):
        for fn in files:
            if not fn.endswith(".html"):
                continue
            p = os.path.join(dirpath, fn)
            s = open(p, encoding="utf-8").read()
            o = s
            s = s.replace(OLD_FONT, NEW_FONT).replace("/assets/style.css?v=3", "/assets/style.css?v=5")
            if 'class="head-cta"' not in s and 'class="site-header"' in s:
                i = s.index('class="site-header"')
                j = s.index("</header>", i)
                s = s[:j] + "  " + CTA + "\n" + s[j:]
            # card photos
            s = re.sub(r'(<li class="card[^"]*"><a href="/([a-z0-9-]+)/">)(?!<img)', card_img, s)
            slug = os.path.basename(dirpath)
            # article hero photo
            if 'class="post-head"' in s and 'class="post-hero"' not in s and has(slug):
                i = s.index('class="post-head"')
                j = s.index("</header>", i) + len("</header>")
                fig = (f'\n  <figure class="post-hero"><img src="/assets/img/{slug}.jpg" alt="" '
                       f'width="1600" height="1000" fetchpriority="high"><figcaption>Photo: Pexels</figcaption></figure>')
                s = s[:j] + fig + s[j:]
                s = re.sub(r'(<meta property="og:image" content=")[^"]*(")',
                           rf'\1https://curioandcove.com/assets/img/{slug}.jpg\2', s, count=1)
            # shelf pages
            if slug in SHELF and 'class="cat-photo"' not in s:
                s = re.sub(r'<span class="arch arch-lg">.*?</svg></span>',
                           f'<img class="cat-photo" src="/assets/img/shelf-{SHELF[slug]}.jpg" alt="" width="1600" height="1000">',
                           s, count=1, flags=re.S)
            if s != o:
                open(p, "w", encoding="utf-8").write(s)
                n += 1
    print("updated", n, "pages")


if __name__ == "__main__":
    run()
