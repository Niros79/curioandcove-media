from make_pins_lot20 import *
OUTBF = "/home/claude/pins/out/lotbf"
def statement2(bg, lab, lab_bg, lab_fg, line1, line2, c1, c2, bullets, mark="check", card_ok="teal", foot="mustard", foot_fg="ink", cta=None):
    im = Image.new("RGB", (W, H), C[bg]); d = ImageDraw.Draw(im)
    label(d, lab, 110, C[lab_bg], C[lab_fg])
    bh, gap = 150, 26
    total = 2 * 100 + 20 + 80 + len(bullets) * (bh + gap) + (110 if cta else 0)
    y0 = max(240, (H - 160 - total) / 2 + 60)
    y = center(d, line1, serif(92), y0, C[c1])
    y = center(d, line2, serif(92), y + 20, C[c2]) + 80
    for t in bullets:
        d.rounded_rectangle([90, y, W - 90, y + bh], radius=30, fill=C["card"])
        cx, cy = 165, y + bh / 2
        d.ellipse([cx - 32, cy - 32, cx + 32, cy + 32], fill=C[card_ok])
        if mark == "check":
            d.line([(cx - 15, cy), (cx - 3, cy + 13), (cx + 17, cy - 13)], fill=C["cream"], width=9)
        else:
            d.line([(cx - 13, cy - 13), (cx + 13, cy + 13)], fill=C["cream"], width=9)
            d.line([(cx - 13, cy + 13), (cx + 13, cy - 13)], fill=C["cream"], width=9)
        lines = wrap(d, t, sans(40, "Medium"), W - 90 - 230 - 30)
        ty = cy - len(lines) * 48 / 2
        for ln in lines:
            d.text((230, ty), ln, font=sans(40, "Medium"), fill=C["ink"]); ty += 48
        y += bh + gap
    if cta:
        center(d, cta, sans(44, "Bold"), y + 40, C["teal"] if bg == "cream" else C["mustard"])
    footer(d, C[bg], C[foot_fg], C[foot])
    return im

B = {}
B["bf-01-worth-it"] = lambda: rows("BLACK FRIDAY 2026", "Black Friday Deals Actually Worth It", [
    ("VPN", "deepest discount of the year on 2-year plans"),
    ("Password manager", "best bought together with your VPN"),
    ("Travel eSIM", "only for a trip you've already booked"),
    ("Flights", "compare against the fare you've been watching")],
    bg="night", lab_bg="mustard", foot="mustard", bar=["teal", "terra", "mustard", "purple"])
B["bf-02-real-deal"] = lambda: numbered("BLACK FRIDAY TIP", "How to Spot a Real Deal in 60 Seconds", [
    "Check the renewal price, not just the first bill", "Compare per month over the same length",
    "Look for a 30-day money-back guarantee", "Only buy what you'd use anyway"],
    accent="mustard", lab_bg="terra", foot="terra", isize=36)
B["bf-03-vpn"] = lambda: rows("BLACK FRIDAY VPN DEALS", "NordVPN or Surfshark This Black Friday?", [
    ("Travelling solo", "NordVPN: the most established brand"),
    ("Family, many devices", "Surfshark: unlimited devices, one plan"),
    ("Best time to buy", "2-year plans with bonus months"),
    ("Not sure?", "use the 30-day money-back window")],
    bg="teal", lab_bg="mustard", foot="mustard", bar=["teal", "terra", "mustard", "purple"], tsize=72)
B["bf-04-skip"] = lambda: statement2("cream", "BLACK FRIDAY 2026", "terra", "cream",
    "Don't buy these", "on Black Friday", "ink", "terra",
    ["\"Make money fast\" course bundles", "Lifetime plans from unknown brands", "Travel gadgets with no trip planned"],
    mark="cross", card_ok="terra", foot="teal", foot_fg="cream", cta="What IS worth buying: see the list")
B["bf-05-checklist"] = lambda: rows("SAVE THIS", "Your Black Friday Checklist", [
    ("Now", "list what you'll really use, note today's prices"),
    ("Nov 23–30", "compare per month, then buy"),
    ("Right after", "set a reminder before renewal"),
    ("Before your trip", "install and test everything at home")],
    lab_bg="purple", foot="purple", bar=["teal", "terra", "mustard", "purple"])
B["bf-06-date"] = lambda: hero("night", "MARK YOUR CALENDAR", "mustard", "ink",
    lambda d: calendar(d, W / 2, 480, 170, C["mustard"], C["night"]), "Black Friday 2026 Is November 27",
    "Cyber Monday is November 30, and many deals start weeks earlier", "cream", "soft", "ink", "mustard", tsize=84)
B["bf-07-free"] = lambda: statement2("cream", "SIDE HUSTLE TIP", "teal", "cream",
    "Free tools beat", "Black Friday deals", "ink", "teal",
    ["Kit: free up to 10,000 subscribers", "Free AI assistants for everyday tasks", "Free YouTube research to start"],
    foot="teal", foot_fg="cream", cta="When it IS worth paying")
if __name__ == "__main__":
    for k, fn in B.items():
        fn().save(f"{OUTBF}/pin-{k}.png")
