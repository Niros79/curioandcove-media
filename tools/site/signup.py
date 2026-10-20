import glob,re
from newpage import *
FORM='''<section class="signup" aria-labelledby="signup-title" style="max-width:720px;margin:2.5rem auto;padding:1.6rem 1.4rem;background:var(--paper,#f6f1e7);border-radius:16px;border:1px solid rgba(0,0,0,.08)">
  <h2 id="signup-title" style="margin-top:0">Free: the Trip Planning Checklist (PDF)</h2>
  <p>What to book and when, in the order that saves money and stress, on two printable pages. Join the Curio &amp; Cove newsletter and we'll send it straight to your inbox, plus one useful guide a week. No spam, unsubscribe anytime.</p>
  <form action="https://app.kit.com/forms/10059486/subscriptions" method="post" style="display:flex;flex-wrap:wrap;gap:.6rem;align-items:center">
    <label for="ck-email" style="position:absolute;left:-9999px">Email address</label>
    <input id="ck-email" name="email_address" type="email" required placeholder="Your email address" autocomplete="email" style="flex:1 1 220px;min-width:0;padding:.8rem 1rem;border-radius:999px;border:1px solid rgba(0,0,0,.2);font:inherit">
    <button class="btn" type="submit" style="margin:0">Send me the checklist</button>
  </form>
  <p style="font-size:.85rem;margin:.6rem 0 0;opacity:.75">By subscribing you agree to receive emails from Curio &amp; Cove. See our <a href="/privacy/">privacy policy</a>.</p>
</section>
'''
n=0
for f in glob.glob(SITE+'/**/index.html',recursive=True):
    if any(x in f for x in ['/tools/','/about/','/disclosure/','/privacy/','/thank-you/']): continue
    s=open(f).read()
    if 'signup-title' in s: continue
    if '<section class="latest more">' in s: s=s.replace('<section class="latest more">',FORM+'\n<section class="latest more">',1)
    elif f.endswith('/site_out/index.html') and '<h2 id="shelves-title">' in s:
        k=s.rfind('<section',0,s.index('<h2 id="shelves-title">')); s=s[:k]+FORM+'\n'+s[k:]
    else: s=s.replace('</main>',FORM+'\n</main>',1)
    open(f,'w').write(s); n+=1
print('signup added to',n)
