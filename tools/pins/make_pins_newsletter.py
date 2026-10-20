import os
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "make_pins.py")).read()
exec(src.split("# ---- VPN pins ----")[0])  # shared helpers, palette, fonts


def envelope(d, cx, cy, w, h, body, line, accent):
    x0, y0, x1, y1 = cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2
    d.rounded_rectangle([x0, y0, x1, y1], radius=24, fill=body)
    d.line([(x0 + 12, y0 + 14), (cx, cy + 10), (x1 - 12, y0 + 14)], fill=line, width=14, joint="curve")
    # little notification dot
    d.ellipse([x1 - 45, y0 - 45, x1 + 45, y0 + 45], fill=accent)
    f = sans(46, "Bold")
    d.text((x1 - d.textlength("1", font=f) / 2, y0 - 32), "1", font=f, fill=body)


def nl1():
    im = Image.new("RGB", (W, H), C["teal"]); d = ImageDraw.Draw(im)
    label(d, "SIDE HUSTLE BASICS", 110, C["mustard"], C["ink"])
    envelope(d, W / 2, 470, 360, 240, C["cream"], C["teal"], C["terra"])
    y = center(d, "How to Start a Newsletter for Your Side Hustle", serif(80), 690, C["cream"])
    center(d, "A free platform, your first signup form and what to send, step by step", sans(38, "Regular"), y + 40, C["soft"], 780)
    footer(d, C["teal"], C["ink"], C["mustard"])
    return im


def nl2():
    im = Image.new("RGB", (W, H), C["cream"]); d = ImageDraw.Draw(im)
    label(d, "OWN YOUR AUDIENCE", 110, C["terra"], C["cream"])
    y = center(d, "Followers can disappear overnight.", serif(84), 300, C["ink"])
    y = center(d, "Your email list can't.", serif(84), y + 30, C["terra"])
    y += 70
    for t in ["You own the list", "Subscribers chose to hear from you", "Works in every country, on every app"]:
        d.rounded_rectangle([90, y, W - 90, y + 110], radius=28, fill=C["card"])
        d.ellipse([125, y + 33, 169, y + 77], fill=C["teal"])
        d.line([(135, y + 55), (145, y + 66), (161, y + 44)], fill=C["cream"], width=7)
        d.text((205, y + 32), t, font=sans(34, "Medium"), fill=C["ink"])
        y += 135
    center(d, "Start a newsletter this weekend", sans(40, "Bold"), y + 30, C["teal"])
    footer(d, C["cream"], C["cream"], C["teal"])
    return im


def nl3():
    im = Image.new("RGB", (W, H), C["cream"]); d = ImageDraw.Draw(im)
    label(d, "BEGINNER CHECKLIST", 100, C["teal"], C["cream"])
    y = center(d, "Launch Your Newsletter in 6 Steps", serif(78), 220, C["ink"])
    items = ["Write a one-line promise", "Pick a free email platform", "Add a signup form + freebie",
             "Write your welcome email", "Send on a steady schedule", "Follow the email rules"]
    y += 40
    for i, t in enumerate(items):
        d.rounded_rectangle([90, y, W - 90, y + 122], radius=28, fill=C["card"])
        d.ellipse([125, y + 24, 199, y + 98], fill=C["mustard"])
        n = str(i + 1); f = serif(44)
        d.text((162 - d.textlength(n, font=f) / 2, y + 31), n, font=f, fill=C["ink"])
        d.text((230, y + 36), t, font=sans(38, "Medium"), fill=C["ink"])
        y += 140
    footer(d, C["cream"], C["cream"], C["teal"])
    return im


for name, fn in [("newsletter-1-how-to-start", nl1), ("newsletter-2-own-your-audience", nl2),
                 ("newsletter-3-checklist", nl3)]:
    fn().save(f"{OUT}/pin-{name}.png")
print("ok")
