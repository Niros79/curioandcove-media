import os
from PIL import Image, ImageDraw, ImageFont
W, H = 1000, 1500
GF = "/usr/share/fonts/truetype/google-fonts/"
OUT = os.path.dirname(os.path.abspath(__file__)) + "/out"
os.makedirs(OUT, exist_ok=True)
C = dict(teal=(31, 78, 74), cream=(246, 239, 228), terra=(200, 100, 59), mustard=(224, 169, 59),
         ink=(34, 40, 38), soft=(232, 222, 206), muted=(110, 116, 110), card=(255, 252, 246),
         night=(38, 30, 52), pumpkin=(232, 120, 40), purple=(96, 70, 130))


def serif(n):
    f = ImageFont.truetype(GF + "Lora-Variable.ttf", n)
    f.set_variation_by_name("Bold")
    return f


def sans(n, w="Medium"):
    return ImageFont.truetype(GF + f"Poppins-{w}.ttf", n)


def wrap(d, t, f, mw):
    out, cur = [], ""
    for w in t.split():
        x = (cur + " " + w).strip()
        if d.textlength(x, font=f) <= mw:
            cur = x
        else:
            out.append(cur); cur = w
    out.append(cur)
    return out


def center(d, t, f, y, col, mw=840, gap=1.15):
    for ln in wrap(d, t, f, mw):
        d.text(((W - d.textlength(ln, font=f)) / 2, y), ln, font=f, fill=col)
        y += f.size * gap
    return y


def footer(d, bg, fg, accent):
    d.rectangle([0, H - 150, W, H], fill=accent)
    center(d, "curioandcove.com", sans(44, "Bold"), H - 108, fg)


def label(d, text, y, bg, fg):
    f = sans(30, "Bold")
    tw = d.textlength(text, font=f)
    d.rounded_rectangle([(W - tw) / 2 - 30, y, (W + tw) / 2 + 30, y + 64], radius=32, fill=bg)
    d.text(((W - tw) / 2, y + 12), text, font=f, fill=fg)


def shield(d, cx, cy, s, col, inner):
    pts = [(cx - s, cy - s * 1.0), (cx, cy - s * 1.25), (cx + s, cy - s * 1.0), (cx + s, cy + s * 0.1),
           (cx, cy + s * 1.2), (cx - s, cy + s * 0.1)]
    d.polygon(pts, fill=col)
    # lock
    d.rounded_rectangle([cx - s * 0.38, cy - s * 0.05, cx + s * 0.38, cy + s * 0.5], radius=10, fill=inner)
    d.arc([cx - s * 0.26, cy - s * 0.42, cx + s * 0.26, cy + s * 0.1], 180, 360, fill=inner, width=14)


def wifi(d, cx, cy, col):
    for r in (150, 105, 60):
        d.arc([cx - r, cy - r, cx + r, cy + r], 225, 315, fill=col, width=22)
    d.ellipse([cx - 18, cy - 18, cx + 18, cy + 18], fill=col)


def pumpkin(d, cx, cy, r, body, stem, face):
    for dx in (-0.55, 0.55, 0):
        d.ellipse([cx + dx * r - r * 0.7, cy - r * 0.8, cx + dx * r + r * 0.7, cy + r * 0.8], fill=body)
    d.rounded_rectangle([cx - 14, cy - r * 1.05, cx + 14, cy - r * 0.7], radius=6, fill=stem)
    d.polygon([(cx - r * 0.5, cy - r * 0.15), (cx - r * 0.25, cy - r * 0.15), (cx - r * 0.37, cy - r * 0.38)], fill=face)
    d.polygon([(cx + r * 0.5, cy - r * 0.15), (cx + r * 0.25, cy - r * 0.15), (cx + r * 0.37, cy - r * 0.38)], fill=face)
    d.chord([cx - r * 0.55, cy - r * 0.2, cx + r * 0.55, cy + r * 0.5], 0, 180, fill=face)


# ---- VPN pins ----
def vpn1():
    im = Image.new("RGB", (W, H), C["teal"]); d = ImageDraw.Draw(im)
    label(d, "TRAVEL TIPS", 110, C["mustard"], C["ink"])
    shield(d, W / 2, 470, 150, C["cream"], C["teal"])
    y = center(d, "Do You Need a VPN When You Travel?", serif(84), 700, C["cream"])
    center(d, "When it really helps, when it doesn't, and how to set one up before your trip", sans(38, "Regular"), y + 40, C["soft"], 780)
    footer(d, C["teal"], C["ink"], C["mustard"])
    return im


def vpn2():
    im = Image.new("RGB", (W, H), C["cream"]); d = ImageDraw.Draw(im)
    label(d, "BEFORE YOU LOG IN", 110, C["terra"], C["cream"])
    wifi(d, W / 2, 470, C["teal"])
    y = center(d, "Using Hotel or Airport Wi-Fi?", serif(84), 580, C["ink"])
    center(d, "Read this before you check your bank or email abroad", sans(40, "Regular"), y + 40, C["muted"], 760)
    footer(d, C["cream"], C["cream"], C["teal"])
    return im


def vpn3():
    im = Image.new("RGB", (W, H), C["cream"]); d = ImageDraw.Draw(im)
    label(d, "TRAVEL SECURITY CHECKLIST", 100, C["teal"], C["cream"])
    y = center(d, "5 Things to Set Up Before Your Trip", serif(76), 220, C["ink"])
    items = ["Install a VPN on every device", "Test it once at home", "Auto-connect on public Wi-Fi",
             "Use unique passwords", "Turn on two-factor login"]
    y += 40
    for i, t in enumerate(items):
        d.rounded_rectangle([90, y, W - 90, y + 140], radius=30, fill=C["card"])
        d.ellipse([125, y + 30, 205, y + 110], fill=C["mustard"])
        n = str(i + 1); f = serif(48)
        d.text((165 - d.textlength(n, font=f) / 2, y + 38), n, font=f, fill=C["ink"])
        d.text((240, y + 44), t, font=sans(40, "Medium"), fill=C["ink"])
        y += 165
    footer(d, C["cream"], C["cream"], C["teal"])
    return im


# ---- Halloween pins ----
def hal1():
    im = Image.new("RGB", (W, H), C["night"]); d = ImageDraw.Draw(im)
    label(d, "HALLOWEEN 2026", 110, C["pumpkin"], C["night"])
    pumpkin(d, W / 2, 470, 170, C["pumpkin"], (70, 110, 60), C["night"])
    y = center(d, "15 Easy Family Halloween Costume Ideas", serif(84), 720, C["cream"])
    center(d, "Group themes kids love, plus last-minute ideas from your wardrobe", sans(38, "Regular"), y + 40, C["soft"], 780)
    footer(d, C["night"], C["night"], C["pumpkin"])
    return im


def hal2():
    im = Image.new("RGB", (W, H), C["pumpkin"]); d = ImageDraw.Draw(im)
    label(d, "NO SEWING NEEDED", 110, C["night"], C["cream"])
    y = center(d, "Last-Minute Costumes From Your Closet", serif(84), 230, C["night"])
    ideas = [("Ghost", "a white sheet or tee + face paint"), ("Mummy", "white layers + strips of old sheet"),
             ("Black cat", "black clothes + paper ears"), ("Tourist", "loud shirt, sunglasses, map"),
             ("Scarecrow", "flannel, jeans, straw hat")]
    y += 50
    for name, desc in ideas:
        d.rounded_rectangle([90, y, W - 90, y + 130], radius=28, fill=C["cream"])
        d.text((130, y + 18), name, font=sans(42, "Bold"), fill=C["night"])
        d.text((130, y + 74), desc, font=sans(32, "Regular"), fill=C["muted"])
        y += 150
    footer(d, C["pumpkin"], C["cream"], C["night"])
    return im


def hal3():
    im = Image.new("RGB", (W, H), C["cream"]); d = ImageDraw.Draw(im)
    label(d, "FAMILY COSTUME THEMES", 110, C["purple"], C["cream"])
    y = center(d, "Halloween Themes With a Role for Everyone", serif(80), 230, C["ink"])
    themes = [("Space crew", "astronauts, an alien, a planet"), ("Farm animals", "cow, pig, sheep + farmer"),
              ("Under the sea", "diver, octopus, jellyfish"), ("Haunted house", "vampire, mummy, witch, cat"),
              ("Breakfast table", "bacon, eggs, toast, coffee")]
    y += 40
    for i, (n, ds) in enumerate(themes):
        col = [C["pumpkin"], C["purple"], C["teal"], C["night"], C["mustard"]][i]
        d.rounded_rectangle([90, y, W - 90, y + 130], radius=28, fill=C["card"])
        d.rectangle([90, y + 20, 104, y + 110], fill=col)
        d.text((140, y + 18), n, font=sans(42, "Bold"), fill=C["ink"])
        d.text((140, y + 74), ds, font=sans(32, "Regular"), fill=C["muted"])
        y += 150
    footer(d, C["cream"], C["cream"], C["purple"])
    return im


for name, fn in [("vpn-1-do-you-need", vpn1), ("vpn-2-hotel-wifi", vpn2), ("vpn-3-checklist", vpn3),
                 ("halloween-1-15-ideas", hal1), ("halloween-2-closet", hal2), ("halloween-3-themes", hal3)]:
    fn().save(f"{OUT}/pin-{name}.png")
print("ok")
