import os
HERE = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(HERE, "make_pins.py")).read().split("# ---- VPN pins ----")[0])  # helpers, palette, fonts
OUT2 = os.path.join(OUT, "lot20"); os.makedirs(OUT2, exist_ok=True)


# ---------- small icons ----------
def plane(d, cx, cy, s, col):
    d.polygon([(cx - s, cy + s * .15), (cx + s, cy - s * .1), (cx + s * .95, cy + s * .12), (cx - s, cy + s * .32)], fill=col)
    d.polygon([(cx - s * .1, cy), (cx + s * .25, cy - s * .75), (cx + s * .45, cy - s * .7), (cx + s * .3, cy)], fill=col)
    d.polygon([(cx - s * .1, cy + s * .2), (cx + s * .2, cy + s * .8), (cx + s * .4, cy + s * .75), (cx + s * .3, cy + s * .15)], fill=col)
    d.polygon([(cx - s * .85, cy + s * .15), (cx - s * .75, cy - s * .35), (cx - s * .6, cy - s * .35), (cx - s * .6, cy + s * .1)], fill=col)


def simcard(d, cx, cy, s, col, inner):
    d.polygon([(cx - s * .7, cy - s), (cx + s * .35, cy - s), (cx + s * .7, cy - s * .65), (cx + s * .7, cy + s), (cx - s * .7, cy + s)], fill=col)
    d.rounded_rectangle([cx - s * .4, cy - s * .15, cx + s * .4, cy + s * .6], radius=12, fill=inner)
    for k in (-1, 0, 1):
        d.line([(cx + k * s * .2, cy - s * .15), (cx + k * s * .2, cy + s * .6)], fill=col, width=6)


def calendar(d, cx, cy, s, col, inner):
    d.rounded_rectangle([cx - s, cy - s * .8, cx + s, cy + s], radius=24, fill=col)
    d.rectangle([cx - s, cy - s * .45, cx + s, cy - s * .3], fill=inner)
    for i in range(3):
        for j in range(3):
            x = cx - s * .6 + i * s * .6; y = cy - s * .05 + j * s * .35
            d.rounded_rectangle([x - 18, y - 12, x + 18, y + 12], radius=5, fill=inner)
    d.rounded_rectangle([cx - s * .55, cy - s, cx - s * .4, cy - s * .6], radius=6, fill=inner)
    d.rounded_rectangle([cx + s * .4, cy - s, cx + s * .55, cy - s * .6], radius=6, fill=inner)


def play(d, cx, cy, s, col, inner):
    d.rounded_rectangle([cx - s * 1.3, cy - s * .9, cx + s * 1.3, cy + s * .9], radius=s * .35, fill=col)
    d.polygon([(cx - s * .35, cy - s * .45), (cx - s * .35, cy + s * .45), (cx + s * .5, cy)], fill=inner)


def envelope(d, cx, cy, w, h, body, line, accent):
    x0, y0, x1, y1 = cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2
    d.rounded_rectangle([x0, y0, x1, y1], radius=24, fill=body)
    d.line([(x0 + 12, y0 + 14), (cx, cy + 10), (x1 - 12, y0 + 14)], fill=line, width=14, joint="curve")
    d.ellipse([x1 - 45, y0 - 45, x1 + 45, y0 + 45], fill=accent)


def camera(d, cx, cy, s, col, inner):
    d.rounded_rectangle([cx - s * 1.2, cy - s * .7, cx + s * 1.2, cy + s * .8], radius=30, fill=col)
    d.rounded_rectangle([cx - s * .45, cy - s * .95, cx + s * .45, cy - s * .6], radius=12, fill=col)
    d.ellipse([cx - s * .5, cy - s * .4, cx + s * .5, cy + s * .6], fill=inner)
    d.ellipse([cx - s * .28, cy - s * .18, cx + s * .28, cy + s * .38], fill=col)


def clock(d, cx, cy, r, col, inner):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
    d.line([(cx, cy), (cx, cy - r * .62)], fill=inner, width=16)
    d.line([(cx, cy), (cx + r * .45, cy + r * .2)], fill=inner, width=16)
    d.ellipse([cx - 14, cy - 14, cx + 14, cy + 14], fill=inner)


# ---------- templates ----------
def hero(bg, lab, lab_bg, lab_fg, icon, title, sub, tcol, scol, foot_fg, foot_bg, tsize=84):
    im = Image.new("RGB", (W, H), C[bg]); d = ImageDraw.Draw(im)
    label(d, lab, 110, C[lab_bg], C[lab_fg])
    icon(d)
    y = center(d, title, serif(tsize), 700, C[tcol])
    center(d, sub, sans(38, "Regular"), y + 40, C[scol], 780)
    footer(d, C[bg], C[foot_fg], C[foot_bg])
    return im


def numbered(lab, title, items, accent="mustard", lab_bg="teal", foot="teal", tsize=76, isize=40):
    im = Image.new("RGB", (W, H), C["cream"]); d = ImageDraw.Draw(im)
    label(d, lab, 100, C[lab_bg], C["cream"])
    y = center(d, title, serif(tsize), 220, C["ink"]) + 40
    step = min(205, (H - 200 - y) // len(items))
    y += max(0, (H - 200 - y) - step * len(items)) / 2
    for i, t in enumerate(items):
        bh = step - 24
        d.rounded_rectangle([90, y, W - 90, y + bh], radius=28, fill=C["card"])
        r = min(46, bh // 2 - 18)
        d.ellipse([125, y + bh / 2 - r, 125 + 2 * r, y + bh / 2 + r], fill=C[accent])
        n = str(i + 1); f = serif(int(r * 1.15))
        d.text((125 + r - d.textlength(n, font=f) / 2, y + bh / 2 - f.size * .62), n, font=f, fill=C["ink"])
        lines = wrap(d, t, sans(isize, "Medium"), W - 90 - 230 - 30)
        ty = y + bh / 2 - len(lines) * isize * 1.2 / 2
        for ln in lines:
            d.text((230, ty), ln, font=sans(isize, "Medium"), fill=C["ink"]); ty += isize * 1.2
        y += step
    footer(d, C["cream"], C["cream"], C[foot])
    return im


def rows(lab, title, items, bg="cream", lab_bg="terra", foot="teal", bar=None, tsize=78):
    dark = bg in ("teal", "night")
    im = Image.new("RGB", (W, H), C[bg]); d = ImageDraw.Draw(im)
    label(d, lab, 100, C[lab_bg], C["cream"] if lab_bg != "mustard" else C["ink"])
    y = center(d, title, serif(tsize), 220, C["cream"] if dark else C["ink"]) + 40
    step = min(215, (H - 200 - y) // len(items))
    y += max(0, (H - 200 - y) - step * len(items)) / 2
    for i, (n, ds) in enumerate(items):
        bh = step - 24
        d.rounded_rectangle([90, y, W - 90, y + bh], radius=28, fill=C["card"])
        if bar:
            d.rectangle([90, y + 18, 104, y + bh - 18], fill=C[bar[i % len(bar)]])
        dl = wrap(d, ds, sans(34, "Regular"), W - 90 - 135 - 30)[:2]
        blockh = 54 + len(dl) * 42
        ty = y + (bh - blockh) / 2
        d.text((135, ty), n, font=sans(44, "Bold"), fill=C["ink"]); ty += 58
        for ln in dl:
            d.text((135, ty), ln, font=sans(34, "Regular"), fill=C["muted"]); ty += 42
        y += step
    footer(d, C[bg], C["cream"], C[foot])
    return im


def statement(bg, lab, lab_bg, lab_fg, line1, line2, c1, c2, bullets, card_ok="teal", foot="mustard", foot_fg="ink", cta=None):
    im = Image.new("RGB", (W, H), C[bg]); d = ImageDraw.Draw(im)
    label(d, lab, 110, C[lab_bg], C[lab_fg])
    y = center(d, line1, serif(82), 280, C[c1])
    y = center(d, line2, serif(82), y + 20, C[c2]) + 60
    for t in bullets:
        d.rounded_rectangle([90, y, W - 90, y + 110], radius=28, fill=C["card"])
        d.ellipse([125, y + 33, 169, y + 77], fill=C[card_ok])
        d.line([(135, y + 55), (145, y + 66), (161, y + 44)], fill=C["cream"], width=7)
        d.text((200, y + 32), t, font=sans(33, "Medium"), fill=C["ink"])
        y += 132
    if cta:
        center(d, cta, sans(40, "Bold"), y + 25, C["teal"] if bg == "cream" else C["mustard"])
    footer(d, C[bg], C[foot_fg], C[foot])
    return im


# ---------- the 20 pins ----------
P = {}
P["01-vpn-hotel-wifi"] = lambda: hero("teal", "BEFORE YOU LOG IN", "mustard", "ink",
    lambda d: (wifi(d, W / 2, 520, C["cream"])), "Is Hotel & Airport Wi-Fi Safe?",
    "What to do before you check your bank or email on public Wi-Fi abroad", "cream", "soft", "ink", "mustard")
P["02-vpn-quick-pick"] = lambda: rows("VPN FOR TRAVEL", "NordVPN or Surfshark? The Quick Pick", [
    ("Solo traveller", "NordVPN, the most established brand"),
    ("Family or many devices", "Surfshark covers all your gadgets"),
    ("Not sure yet?", "Both offer a 30-day money-back guarantee"),
    ("Before you fly", "Install it and test it once at home")], bar=["teal", "terra", "mustard", "purple"])
P["03-vpn-4-times"] = lambda: numbered("TRAVEL SECURITY", "4 Times a VPN Really Helps Abroad", [
    "You rely on hotel, airport or café Wi-Fi", "Your banking app blocks foreign logins",
    "You want your usual sites to work normally", "You work remotely with client files"])
P["04-esim-compared"] = lambda: rows("TRAVEL ESIM GUIDE", "Best eSIM for Travel: 4 Compared", [
    ("Airalo", "first eSIM, short trip, simple setup"), ("Saily", "if online security matters to you"),
    ("Yesim", "unlimited plans when you need lots of data"), ("GigSky", "regional plans for multi-country trips")],
    bar=["teal", "terra", "mustard", "purple"], lab_bg="teal", foot="terra")
P["05-esim-5-steps"] = lambda: numbered("SKIP ROAMING FEES", "Set Up a Travel eSIM in 5 Steps", [
    "Buy the plan in the app", "Install it at home, on Wi-Fi", "Label it \"Travel\"",
    "On arrival, switch it on for data", "Turn data off on your main SIM"], accent="terra", lab_bg="terra")
P["06-esim-vs-roaming"] = lambda: rows("STAYING CONNECTED", "eSIM vs Roaming vs Local SIM", [
    ("Travel eSIM", "most trips: data on arrival, set up before you go"),
    ("Carrier roaming", "short trips, if your plan covers the destination"),
    ("Local SIM card", "long stays when you need a local number")],
    bg="cream", lab_bg="purple", foot="purple", bar=["teal", "mustard", "terra"])
P["07-checklist-when"] = lambda: rows("SAVE FOR YOUR NEXT TRIP", "What to Book and When: Trip Checklist", [
    ("2–3 months before", "flights, a stay with free cancellation, passport check"),
    ("About 1 month before", "travel insurance, tours and tickets, car or trains"),
    ("1–2 weeks before", "mobile data, airport transfer, cards, document copies"),
    ("Travel day", "online check-in, carry-on essentials, boarding pass")],
    bar=["teal", "terra", "mustard", "purple"], tsize=74)
P["08-checklist-1-month"] = lambda: hero("cream", "1 MONTH BEFORE YOUR TRIP", "terra", "cream",
    lambda d: calendar(d, W / 2, 480, 170, C["teal"], C["cream"]), "Do These 3 Things a Month Before You Travel",
    "Travel insurance, the tours that sell out, and your car or train tickets", "ink", "muted", "cream", "teal", tsize=78)
P["09-travel-day"] = lambda: numbered("TRAVEL DAY CHECKLIST", "Before You Leave for the Airport", [
    "Check in online, save the boarding pass", "Medication, chargers, documents in your carry-on",
    "Pack one change of clothes", "Get there early for international flights",
    "Keep your boarding pass until you're home"], accent="mustard", lab_bg="purple", foot="purple", isize=34)
P["10-europe-cheapest-months"] = lambda: rows("CHEAP FLIGHTS", "The Cheapest Months to Fly to Europe", [
    ("Cheapest", "January, February and November (not holiday weeks)"),
    ("Best value", "April–May and September–October"),
    ("Most expensive", "late June–August, Easter and Christmas")],
    bg="teal", lab_bg="mustard", foot="mustard", bar=["teal", "mustard", "terra"])
P["11-europe-how-far-ahead"] = lambda: hero("cream", "BOOKING TIPS", "teal", "cream",
    lambda d: calendar(d, W / 2, 480, 170, C["terra"], C["cream"]), "How Far Ahead to Book Flights to Europe",
    "Off-season: about 4 months. Summer: 5–7 months. Holidays: as early as you can.", "ink", "muted", "cream", "teal", tsize=80)
P["12-delay-600"] = lambda: hero("night", "FLIGHT DELAYED?", "mustard", "ink",
    lambda d: clock(d, W / 2, 470, 170, C["mustard"], C["night"]), "3+ Hours Late? You Could Be Owed €600",
    "EU rules cover any flight leaving the EU, and EU airlines flying in", "cream", "soft", "ink", "mustard")
P["13-delay-amounts"] = lambda: rows("EU261 COMPENSATION", "What Your Flight Delay Is Worth", [
    ("€250", "flights up to 1,500 km"), ("€400", "1,500–3,500 km, and longer flights within the EU"),
    ("€600", "over 3,500 km: most Europe–US, Asia or Australia flights")],
    lab_bg="terra", foot="terra", bar=["mustard", "terra", "teal"])
P["14-yt-5-ways"] = lambda: numbered("YOUTUBE + AI", "5 Ways AI Helps Grow a YouTube Channel", [
    "Turn one topic into dozens of video ideas", "Find what people actually search for",
    "Draft scripts you rewrite in your voice", "Test title and description variations",
    "Repurpose a blog post into a video"], accent="terra", lab_bg="terra", foot="terra", isize=34)
P["15-yt-weekly"] = lambda: rows("A SIMPLE WEEKLY PLAN", "A YouTube Workflow You Can Stick To", [
    ("Monday", "pick a topic, check search interest"), ("Tuesday", "outline and script with AI, then rewrite"),
    ("Wed–Thu", "film and edit"), ("Friday", "title, thumbnail, description, publish"),
    ("Weekend", "check YouTube Studio, add new ideas")], bar=["teal", "terra", "mustard", "purple", "teal"], lab_bg="teal", foot="teal", tsize=74)
P["16-yt-cant"] = lambda: hero("teal", "AN HONEST GUIDE", "mustard", "ink",
    lambda d: play(d, W / 2, 480, 140, C["terra"], C["cream"]), "What AI Can't Do for Your YouTube Channel",
    "Where AI really helps, where it doesn't, and the free tools to start with", "cream", "soft", "ink", "mustard", tsize=80)
P["17-nl-first-100"] = lambda: numbered("NEWSLETTER BASICS", "Your First 100 Email Subscribers", [
    "Invite friends, customers and colleagues", "Add the signup link to every bio",
    "Share newsletter snippets on social", "Offer one genuinely useful freebie"], accent="mustard", lab_bg="teal")
P["18-nl-why-list"] = lambda: statement("cream", "SIDE HUSTLE TIP", "terra", "cream",
    "Social media is rented.", "An email list is yours.", "ink", "terra",
    ["No algorithm decides who sees it", "Subscribers chose to hear from you", "Free to start on most platforms"],
    foot="teal", foot_fg="cream", cta="How to start one this weekend")
P["19-tb-how-money"] = lambda: rows("TRAVEL CREATORS", "How Travel Blogs Actually Make Money", [
    ("Affiliate links", "earn when readers book; the easiest place to start"),
    ("Display ads", "pay per view, once traffic is steady"),
    ("Brand deals", "come later, once you have an audience"),
    ("Your own products", "itineraries, guides or presets")], bar=["teal", "terra", "mustard", "purple"], lab_bg="purple", foot="purple")
P["20-tb-first-steps"] = lambda: hero("cream", "BEGINNER'S GUIDE", "teal", "cream",
    lambda d: camera(d, W / 2, 480, 160, C["teal"], C["cream"]), "Start a Travel Blog That Earns: First Steps",
    "Pick a platform, choose a focus, join a travel affiliate network and be transparent", "ink", "muted", "cream", "terra", tsize=80)

if __name__ == "__main__":
    for k, fn in P.items():
        fn().save(f"{OUT2}/pin-{k}.png")
    print("ok", len(P))
