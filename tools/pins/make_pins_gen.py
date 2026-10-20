import json
from make_pins_nov import *
G = []
def g(key, render, title, desc, link, alt): G.append((key, render, title, desc, link, alt))
g("gen-01-mistakes", lambda: rows("TRAVEL MONEY", "Travel Mistakes That Cost You Money", [
    ("Booking holiday flights late", "peak dates go up fast"), ("Paying for roaming", "use a travel eSIM"), ("Skipping insurance", "buy it soon after booking"), ("Ignoring bag fees", "count them in the fare")],
    bg="night", lab_bg="terra", foot="terra", bar=["terra", "mustard", "teal", "purple"], tsize=74),
    "Travel Mistakes That Quietly Cost You Money", "Booking holiday flights late, paying for roaming, skipping travel insurance and forgetting bag fees. Fix all four with one free trip planning checklist. #traveltips #budgettravel #travelmistakes", CHECK, "Night-blue pin: travel mistakes that cost you money")
g("gen-02-first", lambda: hero("teal", "FIRST TRIP ABROAD?", "mustard", "ink", lambda d: plane(d, W / 2, 470, 170, C["mustard"]),
    "Your First Trip Abroad, Step by Step", "What to book first, what to sort at home and what to pack on travel day", "cream", "soft", "ink", "mustard", tsize=82),
    "First Trip Abroad? Plan It Step by Step", "Passport and flights first, then your stay, insurance and transport, then eSIM, offline maps and travel-day essentials. Free printable checklist included. #firsttripabroad #tripplanning #traveltips", CHECK, "Teal pin with plane: your first trip abroad, step by step")
g("gen-03-apps", lambda: numbered("TRAVEL APPS", "Apps to Set Up Before Any Trip", [
    "Flight and price alerts", "A travel eSIM", "Offline maps", "A translator", "A VPN for public Wi-Fi"],
    accent="mustard", lab_bg="teal", foot="teal", isize=36),
    "5 Apps to Set Up Before Any Trip", "Flight price alerts, a travel eSIM, offline maps, a translator and a VPN for public Wi-Fi. Install them at home, not at the airport. #travelapps #traveltech #traveltips", APPS, "Numbered list: apps to set up before any trip")
g("gen-04-weekend", lambda: statement2("cream", "CITY BREAK", "teal", "cream", "Weekend away?", "Plan it in an hour", "ink", "teal",
    ["Set a fare alert, book on a dip", "Stay central, walk everywhere", "Check if a city pass pays off"], foot="teal", foot_fg="cream", cta="Free trip planning checklist"),
    "Plan a Weekend City Break in One Hour", "Set a fare alert and book on a dip, stay central, then do the 5-minute math on a city pass. Any city, any budget. #citybreak #weekendgetaway #traveltips", CHECK, "Cream pin: weekend away, plan it in an hour")
g("gen-05-habits", lambda: rows("CHEAP TRAVEL", "Travel More for Less: 4 Habits", [
    ("Fly off-peak", "midweek and shoulder season"), ("Compare airports", "nearby ones can be cheaper"), ("Use price alerts", "book when the fare dips"), ("Travel light", "skip checked bag fees")],
    bg="teal", lab_bg="mustard", foot="mustard", bar=["mustard", "terra", "purple", "cream"], tsize=76),
    "Travel More for Less: 4 Habits That Work Anywhere", "Fly off-peak, compare nearby airports, use price alerts and travel light. Simple habits that cut the cost of any trip, from anywhere. #budgettravel #cheapflights #travelhacks", FLY, "Teal pin: travel more for less, 4 habits")
g("gen-06-car", lambda: hero("cream", "ROAD TRIP ABROAD", "terra", "cream", lambda d: calendar(d, W / 2, 480, 170, C["terra"], C["cream"]),
    "Renting a Car Abroad Without Surprises", "Licence rules, deposits, insurance excess and fuel policy explained", "ink", "muted", "cream", "teal", tsize=80),
    "Renting a Car Abroad Without Nasty Surprises", "Licence and permit rules, a credit card for the deposit, the insurance excess and the fuel policy: what to check before you sign. #roadtrip #carrental #traveltips", CAR, "Cream pin: renting a car abroad without surprises")
if __name__ == "__main__":
    import shutil
    R = "/home/claude/curioandcove-media/pins/"
    jobs = [("lotnov", [10, 24, 49]), ("lotrome", [1, 3, 5])]
    k = 0
    for lot, ns in jobs:
        f = R + lot + "/queue.json"; q = json.load(open(f))
        for p in q:
            if p["n"] in ns:
                key, render, title, desc, link, alt = G[k]; k += 1
                img = f"pin-{lot}-{p['n']:02d}-{key}.png"
                render().save(R + lot + "/" + img)
                import os; os.remove(R + lot + "/" + p["image"]) if os.path.exists(R + lot + "/" + p["image"]) else None
                p.update(image=img, image_url=f"https://raw.githubusercontent.com/Niros79/curioandcove-media/main/pins/{lot}/{img}",
                         board_id=TRAVEL, title=title, description=desc, link=link, alt=alt)
                print(lot, p["n"], p["at"], title)
        json.dump(q, open(f, "w"), indent=1, ensure_ascii=False)
