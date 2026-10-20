from make_pins_rome import *
OUTN = "/home/claude/pins/out/lotnew"
N = {}
N["new-01-vpn-compare"] = lambda: rows("VPN FOR TRAVEL", "NordVPN vs Surfshark: Which One for Your Trip?", [
    ("Solo or couple", "NordVPN: up to 10 devices, top brand"), ("Family", "Surfshark: unlimited devices, one plan"),
    ("Both", "30-day money-back guarantee"), ("Before you fly", "turn on auto-connect for public Wi-Fi")],
    bg="night", lab_bg="mustard", foot="mustard", bar=["teal", "terra", "mustard", "purple"], tsize=72)
N["new-02-vpn-family"] = lambda: hero("teal", "TRAVELLING AS A FAMILY?", "mustard", "ink",
    lambda d: wifi(d, W / 2, 520, C["cream"]), "One VPN Plan for Every Phone and Tablet",
    "Why families pick Surfshark, and when NordVPN is the better choice", "cream", "soft", "ink", "mustard", tsize=80)
N["new-03-password"] = lambda: statement2("cream", "TRAVEL SECURITY", "terra", "cream",
    "Reused passwords?", "Fix it in one evening", "ink", "terra",
    ["Unique password for every account", "Logins synced to your phone", "Passport details in an encrypted note"],
    card_ok="terra", foot="terra", foot_fg="cream", cta="The one-evening setup plan")
N["new-04-password-steps"] = lambda: numbered("PASSWORD MANAGER", "Set Up a Password Manager in 6 Steps", [
    "Install on phone, laptop and browser", "Import your saved passwords", "Change email, bank and phone first",
    "Turn on two-factor authentication", "Add an encrypted travel note", "Share logins with your travel partner"],
    accent="mustard", lab_bg="teal", foot="teal", isize=32)
N["new-05-cheap-flights"] = lambda: numbered("CHEAP FLIGHTS", "7 Habits for Cheap Flights From Anywhere", [
    "Be flexible by a few days", "Compare airlines and nearby airports", "Try creative routes",
    "Book at the right time", "Set price alerts", "Count the real price with bags", "Ignore the incognito myth"],
    accent="terra", lab_bg="terra", foot="terra", isize=32)
N["new-06-when-book"] = lambda: rows("WHEN TO BOOK", "How Far Ahead to Book Flights", [
    ("Short-haul, off-season", "book about 3–8 weeks ahead"), ("Long-haul, off-season", "book about 2–4 months ahead"),
    ("Summer and holidays", "book 5–7 months ahead")], bg="teal", lab_bg="mustard", foot="mustard", bar=["mustard", "terra", "purple"])
N["new-07-car-rental"] = lambda: numbered("RENTING A CAR ABROAD", "Check These Before You Rent a Car Abroad", [
    "Licence and driving permit rules", "Deposit and credit card", "Insurance excess", "Full-to-full fuel policy",
    "Border and mileage rules"], accent="mustard", lab_bg="purple", foot="purple", isize=34)
N["new-08-car-pickup"] = lambda: statement2("cream", "CAR RENTAL TIP", "teal", "cream",
    "Film the car", "before you drive off", "ink", "teal",
    ["Every side, wheels and windscreen", "Fuel gauge and mileage", "Every scratch on the form"],
    foot="teal", foot_fg="cream", cta="The full rental checklist")
N["new-09-apps"] = lambda: rows("TRAVEL APPS", "Apps to Install Before Your Next Trip", [
    ("Booking", "flights, hotels and trains in one app"), ("Data", "a travel eSIM, set up at home"),
    ("Security", "a VPN and a password manager"), ("Offline", "maps and translation packs")],
    lab_bg="terra", foot="terra", bar=["teal", "terra", "mustard", "purple"])
N["new-10-tools"] = lambda: hero("cream", "OUR TOOLKIT", "teal", "cream",
    lambda d: plane(d, W / 2, 470, 170, C["teal"]), "The Travel Tools We Actually Recommend",
    "Booking, eSIMs, security, transfers and more, with one honest line each", "ink", "muted", "cream", "teal", tsize=80)
if __name__ == "__main__":
    for k, fn in N.items():
        fn().save(f"{OUTN}/pin-{k}.png")
