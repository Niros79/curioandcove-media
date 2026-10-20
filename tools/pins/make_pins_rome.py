from make_pins_xmas import *
OUTR = "/home/claude/pins/out/lotrome"
R = {}
R["rome-01-3days"] = lambda: rows("ROME ITINERARY", "3 Days in Rome: The Perfect First Visit", [
    ("Day 1", "Colosseum, Roman Forum, Monti at night"),
    ("Day 2", "Vatican Museums, St Peter's, Trastevere"),
    ("Day 3", "Pantheon, Navona, Trevi, sunset at Pincio")],
    bg="teal", lab_bg="mustard", foot="mustard", bar=["terra", "mustard", "purple"])
R["rome-02-book"] = lambda: numbered("BEFORE YOU GO", "Book These 4 Things Before Rome", [
    "Colosseum and Roman Forum timed ticket", "Vatican Museums entry (closed most Sundays)",
    "Borghese Gallery, if you want to go", "A central stay with free cancellation"],
    accent="terra", lab_bg="terra", foot="terra", isize=34)
R["rome-03-fees"] = lambda: hero("cream", "NEW IN 2026", "terra", "cream",
    lambda d: calendar(d, W / 2, 480, 170, C["terra"], C["cream"]), "Rome's New Tourist Fees for 2026",
    "Trevi Fountain basin: €2. Pantheon: now €7. What's still free, and how to plan around it", "ink", "muted", "cream", "teal", tsize=82)
R["delay-faq-3h"] = lambda: hero("night", "FLIGHT DELAY RULES", "mustard", "ink",
    lambda d: clock(d, W / 2, 470, 170, C["mustard"], C["night"]), "How Late Before You're Owed Compensation?",
    "Under EU rules: 3+ hours at your final destination. Up to €600 per passenger", "cream", "soft", "ink", "mustard", tsize=78)
R["delay-faq-us"] = lambda: rows("EU261 EXPLAINED", "Flying a US Airline? Are You Covered?", [
    ("Leaving the EU", "covered on any airline, including US airlines"),
    ("Flying into the EU", "covered only on EU-based airlines"),
    ("Delay of 3+ hours", "€250 to €600, depending on distance")],
    lab_bg="terra", foot="terra", bar=["teal", "terra", "mustard"])
if __name__ == "__main__":
    for k, fn in R.items():
        fn().save(f"{OUTR}/pin-{k}.png")
