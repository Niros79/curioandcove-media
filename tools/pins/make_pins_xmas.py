from make_pins_bf import *
OUTX = "/home/claude/pins/out/lotxmas"
def sprout(d, cx, cy, s, col, pot):
    d.rounded_rectangle([cx - s*0.55, cy + s*0.25, cx + s*0.55, cy + s*0.95], radius=18, fill=pot)
    d.line([(cx, cy + s*0.3), (cx, cy - s*0.45)], fill=col, width=14)
    d.ellipse([cx - s*0.75, cy - s*0.55, cx - s*0.05, cy - s*0.05], fill=col)
    d.ellipse([cx + s*0.05, cy - s*0.85, cx + s*0.75, cy - s*0.35], fill=col)
X = {}
X["xmas-01-quick"] = lambda: rows("CHRISTMAS GIFT GUIDE", "Gifts for Travelers They'll Actually Use", [
    ("City-breaker", "museum tickets or a city pass"),
    ("Digital nomad", "a VPN or password manager"),
    ("Homebody", "a smart indoor herb garden"),
    ("Road-tripper", "a dash cam for every drive")],
    bg="night", lab_bg="terra", foot="terra", bar=["terra", "mustard", "teal", "purple"], tsize=74)
X["xmas-02-experiences"] = lambda: statement2("cream", "GIFTS YOU CAN'T WRAP", "terra", "cream",
    "Give a memory,", "not more stuff", "ink", "terra",
    ["Museum or landmark tickets", "A city pass for their next trip", "A food tour with free cancellation"],
    card_ok="terra", foot="terra", foot_fg="cream", cta="Experience gift ideas inside")
X["xmas-03-lastminute"] = lambda: hero("night", "LAST-MINUTE GIFTS", "mustard", "ink",
    lambda d: envelope(d, W / 2, 480, 300, 200, C["cream"], C["night"], C["mustard"]),
    "Gifts You Can Send by Email on Dec 24", "Attraction tickets, subscriptions and trip promise cards", "cream", "soft", "ink", "mustard", tsize=80)
X["xmas-04-stocking"] = lambda: numbered("STOCKING STUFFERS", "Travel Gifts Under $25", [
    "Universal adapter with USB ports", "Packing cubes or compression bags", "A compact power bank",
    "A luggage tracker tag", "Sleep mask and good earplugs"], accent="terra", lab_bg="terra", foot="terra", isize=36)
X["xmas-05-homebody"] = lambda: hero("cream", "FOR THE HOMEBODY", "teal", "cream",
    lambda d: sprout(d, W / 2, 470, 190, C["teal"], C["terra"]),
    "Fresh Herbs All Winter: A Gift for Plant Lovers", "A smart indoor garden grows herbs on the kitchen counter, no green thumb needed", "ink", "muted", "cream", "teal", tsize=76)
X["xmas-06-tech"] = lambda: statement2("cream", "FOR THE TECH-SAVVY TRAVELER", "teal", "cream",
    "Gifts they'll use", "every single day", "ink", "teal",
    ["A VPN for hotel and airport Wi-Fi", "A password manager for every login", "Mobile data for their next trip"],
    foot="teal", foot_fg="cream", cta="See the full gift guide")
X["xmas-07-choose"] = lambda: numbered("GIFT-GIVING TIP", "How to Pick the Perfect Travel Gift", [
    "Ask where they're going next", "Choose something used every week", "Pick flexible dates and refunds"],
    accent="mustard", lab_bg="purple", foot="purple")
if __name__ == "__main__":
    for k, fn in X.items():
        fn().save(f"{OUTX}/pin-{k}.png")
