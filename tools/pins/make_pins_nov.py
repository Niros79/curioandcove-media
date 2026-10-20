import json, os, sys
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from make_pins_new import *

OUTV = "/home/claude/pins/out/lotnov"
os.makedirs(OUTV, exist_ok=True)
TRAVEL, SIDE, FAMILY, JOURNAL = "1094023003171921131", "1094023003171940577", "1094023003171970038", "1094023003171920516"
S = "https://curioandcove.com/"
ESIM, VPN, NVS, PASS = S + "best-esim-for-travel/", S + "do-you-need-a-vpn-when-you-travel/", S + "nordvpn-vs-surfshark-travel/", S + "best-password-manager-for-travelers/"
FLY, EU, DELAY, CHECK = S + "how-to-find-cheap-flights/", S + "cheapest-time-to-fly-to-europe/", S + "eu-flight-delay-compensation-americans/", S + "trip-planning-checklist/"
ROME, PASSES, CAR, APPS = S + "3-days-in-rome-itinerary/", S + "are-city-passes-worth-it/", S + "renting-a-car-abroad/", S + "best-travel-apps/"
GIFTS, BF, EVEN, NEWS = S + "christmas-gifts-for-travelers/", S + "black-friday-deals-travelers-side-hustlers/", S + "screen-free-family-evening-ideas-fall/", S + "start-newsletter-side-hustle/"
AI, YT, WEB, BLOG, HAL, JRN = S + "everyday-tasks-free-ai-assistant/", S + "grow-youtube-channel-ai-tools/", S + "build-website-side-project-ai/", S + "make-money-travel-blog-instagram/", S + "family-halloween-costume-ideas/", S + "how-to-start-journaling-prompts/"

P = []  # (key, render, board, title, description, link, alt)
def add(key, render, board, title, desc, link, alt):
    P.append((key, render, board, title, desc, link, alt))

# eSIM (strongest Google topic)
add("esim-01-what", lambda: hero("teal", "TRAVEL eSIM", "mustard", "ink", lambda d: simcard(d, W / 2, 480, 170, C["mustard"], C["teal"]),
    "Stop Paying for Roaming: Get a Travel eSIM", "What it is, how it works and how to pick a plan for any trip", "cream", "soft", "ink", "mustard", tsize=78),
    TRAVEL, "Stop Paying for Roaming: How a Travel eSIM Works", "A travel eSIM gives you local-rate mobile data without swapping SIM cards. Install it at home, switch it on when you land, keep WhatsApp working. Our beginner guide compares Airalo, Saily, Yesim and GigSky. #esim #traveltips #traveltech", ESIM, "Teal pin with a SIM card icon: Stop paying for roaming, get a travel eSIM")
add("esim-02-steps", lambda: numbered("eSIM SETUP", "Set Up Your Travel eSIM in 5 Steps", [
    "Buy the plan in the app", "Install it at home, on Wi-Fi", "Label it \"Travel\"", "Switch it on when you land", "Turn off data on your home SIM"],
    accent="mustard", lab_bg="teal", foot="teal", isize=34),
    TRAVEL, "Set Up Your Travel eSIM in 5 Easy Steps", "Install at home on Wi-Fi, label it, switch it on for data when you land and turn data off on your home SIM to avoid a surprise bill. The full step-by-step guide, plus how much data you need. #esim #travelhacks #internationaltravel", ESIM, "Numbered list: set up your travel eSIM in 5 steps")
add("esim-03-data", lambda: rows("HOW MUCH DATA?", "How Much eSIM Data Do You Need for a Week?", [
    ("Maps, chat, email", "about 3–5 GB"), ("Plus social and photos", "about 5–10 GB"), ("Video calls, streaming", "10 GB+ or unlimited")],
    bg="cream", lab_bg="teal", foot="teal", bar=["teal", "mustard", "terra"], tsize=72),
    TRAVEL, "How Much Data Do You Need for a 1-Week Trip?", "Maps, messages and email: about 3–5 GB a week. Add social media and photo uploads: 5–10 GB. Video calls or streaming: 10 GB+ or an unlimited plan. Rough guide, plus tips to make data last. #esim #traveltips #budgettravel", ESIM, "Table of eSIM data needs for a one-week trip")
add("esim-04-mistakes", lambda: statement2("cream", "eSIM MISTAKES", "terra", "cream", "Don't wait", "until you land", "ink", "terra",
    ["Install at home, on Wi-Fi", "Keep the eSIM if you might top up", "Turn off roaming on your home SIM"], card_ok="terra", foot="terra", foot_fg="cream", cta="4 eSIM mistakes to avoid"),
    TRAVEL, "4 Travel eSIM Mistakes That Cost Money", "Waiting until you land to install it, deleting it before a top-up, buying too little data and leaving roaming on for your home SIM. Avoid all four with this quick guide. #esim #travelmistakes #traveltips", ESIM, "Cream pin: don't wait until you land, eSIM mistakes to avoid")
add("esim-05-compare", lambda: rows("eSIM COMPARED", "Airalo Alternatives: Saily, Yesim and GigSky", [
    ("Airalo", "huge choice of countries, easy first time"), ("Saily", "simple app with security extras"), ("Yesim", "good for bigger data needs"), ("GigSky", "regional plans for multi-country trips")],
    bg="night", lab_bg="mustard", foot="mustard", bar=["teal", "terra", "mustard", "purple"], tsize=70),
    TRAVEL, "Airalo Alternatives: Saily vs Yesim vs GigSky", "Looking beyond Airalo? Saily (from the makers of NordVPN), Yesim and GigSky compared for first-timers, heavy data users and multi-country trips. Prices change, so compare for your exact destination. #esim #airalo #traveltech", ESIM, "Comparison pin of Airalo, Saily, Yesim and GigSky")
add("esim-06-roaming", lambda: hero("cream", "eSIM vs ROAMING", "teal", "cream", lambda d: wifi(d, W / 2, 520, C["teal"]),
    "Roaming, Local SIM or eSIM? The Honest Answer", "Which one is cheapest and easiest for your next trip abroad", "ink", "muted", "cream", "teal", tsize=80),
    TRAVEL, "Roaming vs Local SIM vs eSIM: Which Is Best?", "Roaming is easy but often expensive, a local SIM means queues and swapping cards, and a travel eSIM sits in the middle: local-rate data, set up from home. Here's how to choose. #esim #roaming #traveltips", ESIM, "Cream pin with Wi-Fi icon: roaming, local SIM or eSIM")
# VPN / security
add("vpn-01-holiday", lambda: hero("night", "HOLIDAY TRAVEL", "mustard", "ink", lambda d: wifi(d, W / 2, 520, C["mustard"]),
    "Using Airport Wi-Fi This Holiday? Read This First", "When a travel VPN really helps, and when you can skip it", "cream", "soft", "ink", "mustard", tsize=78),
    TRAVEL, "Using Airport or Hotel Wi-Fi This Holiday? Read This", "Public Wi-Fi is shared with strangers. Here's when a VPN genuinely protects you on the road, when it doesn't matter, and how to set one up in five minutes before you fly. #travelsecurity #vpn #holidaytravel", VPN, "Night-blue pin: using airport Wi-Fi this holiday, read this first")
add("vpn-02-setup", lambda: numbered("BEFORE YOU FLY", "Set Up a VPN in 5 Minutes", [
    "Install it on every device", "Log in at home", "Turn on auto-connect for unknown Wi-Fi", "Save a home-country server for banking", "Check VPN rules at your destination"],
    accent="mustard", lab_bg="teal", foot="teal", isize=33),
    TRAVEL, "Set Up a Travel VPN in 5 Minutes Before You Fly", "Install on every device, log in at home, turn on auto-connect for unknown Wi-Fi, save a home-country server for banking and check the rules where you're going. #vpn #travelprep #onlinesecurity", NVS, "Numbered list: set up a travel VPN in five minutes")
add("vpn-03-bf", lambda: statement2("cream", "BLACK FRIDAY TIP", "teal", "cream", "Buying a VPN?", "Wait for November", "ink", "teal",
    ["Biggest discounts of the year", "Check the renewal price", "30-day money-back on both"], foot="teal", foot_fg="cream", cta="NordVPN vs Surfshark, compared"),
    TRAVEL, "Buying a VPN? Why Black Friday Is the Best Time", "The biggest VPN discounts of the year usually land around Black Friday (Nov 27). Compare NordVPN and Surfshark, check the renewal price and use the 30-day money-back guarantee. #blackfriday #vpn #nordvpn #surfshark", NVS, "Cream pin: buying a VPN, wait for November")
add("vpn-04-family", lambda: rows("ONE PLAN, WHOLE FAMILY", "Every Phone and Tablet Protected", [
    ("Surfshark", "unlimited devices on one plan"), ("NordVPN", "up to 10 devices at once"), ("Both", "auto-connect on public Wi-Fi")],
    bg="teal", lab_bg="mustard", foot="mustard", bar=["mustard", "terra", "purple"], tsize=74),
    TRAVEL, "Travelling as a Family? One VPN for Every Device", "Surfshark covers unlimited devices on one plan; NordVPN covers up to 10 at once. Here's which suits your family and how to set both up before the holidays. #familytravel #vpn #travelsecurity", NVS, "Teal pin comparing VPN device limits for families")
add("pass-01-holiday", lambda: statement2("cream", "BEFORE THE HOLIDAYS", "terra", "cream", "One password", "everywhere?", "ink", "terra",
    ["Unique password for every account", "Two-factor on email and bank", "Passport copy in an encrypted note"], card_ok="terra", foot="terra", foot_fg="cream", cta="Fix it in one evening"),
    TRAVEL, "Fix Your Passwords Before Holiday Travel", "Reusing one password is the easiest way to lose an account on the road. Set up a password manager in one evening: unique passwords, two-factor login and an encrypted passport note. #onlinesecurity #passwordmanager #traveltips", PASS, "Cream pin: one password everywhere, fix it before the holidays")
add("pass-02-family", lambda: hero("teal", "FAMILY SECURITY", "mustard", "ink", lambda d: shield(d, W / 2, 480, 170, C["mustard"], C["teal"]),
    "Share Logins Safely With Your Family", "How a family password manager keeps travel accounts safe", "cream", "soft", "ink", "mustard", tsize=80),
    TRAVEL, "Share Logins Safely With Your Family", "Stop sending passwords by text. A family password manager lets you share streaming, airline and booking logins safely, and keeps a copy of passports in an encrypted note. #familytech #passwordmanager #travelsecurity", PASS, "Teal pin with shield icon: share logins safely with your family")
# Flights
add("fly-01-holiday", lambda: rows("HOLIDAY FLIGHTS", "When to Book Christmas Flights", [
    ("Peak dates", "start watching early, book 5–7 months ahead"), ("Still not booked?", "set a price alert today"), ("Be flexible", "shifting a day can change the fare")],
    bg="night", lab_bg="terra", foot="terra", bar=["terra", "mustard", "teal"], tsize=78),
    TRAVEL, "When to Book Christmas and Holiday Flights", "For peak dates the rule of thumb is 5–7 months ahead. Not booked yet? Set a price alert today, compare nearby airports and be flexible by a day. The full cheap-flights playbook. #cheapflights #holidaytravel #christmastravel", FLY, "Night-blue pin: when to book Christmas flights")
add("fly-02-myths", lambda: statement2("cream", "FLIGHT MYTHS", "teal", "cream", "Incognito mode", "won't save you money", "ink", "teal",
    ["Flight day matters more than booking day", "Last-minute is rarely cheaper", "Count bags in the price"], foot="teal", foot_fg="cream", cta="What actually works"),
    TRAVEL, "3 Cheap Flight Myths That Waste Your Time", "Incognito mode doesn't lower fares, the day you fly matters far more than the day you book, and last-minute is rarely cheaper. Here's what actually works instead. #cheapflights #travelhacks #flightdeals", FLY, "Cream pin: incognito mode won't save you money on flights")
add("fly-03-airports", lambda: hero("teal", "FLIGHT HACK", "mustard", "ink", lambda d: plane(d, W / 2, 470, 170, C["mustard"]),
    "Check the Airport an Hour Away", "A second airport can be much cheaper, especially with budget airlines", "cream", "soft", "ink", "mustard", tsize=82),
    TRAVEL, "The Simplest Cheap Flight Hack: Check Nearby Airports", "A second airport an hour away can be much cheaper, especially with budget airlines. Compare them in one search, then count the transfer cost. 7 habits for cheap flights from anywhere. #cheapflights #budgettravel #travelhacks", FLY, "Teal pin with plane icon: check the airport an hour away")
add("fly-04-realprice", lambda: numbered("THE REAL PRICE", "Is That Cheap Flight Really Cheap?", [
    "Add carry-on and checked bags", "Add seat and check-in fees", "Add the airport transfer", "Check the arrival time"],
    accent="terra", lab_bg="terra", foot="terra", isize=36),
    TRAVEL, "Is That Cheap Flight Really Cheap? Check 4 Things", "Bags, seat and check-in fees, the transfer from a remote airport and a 1 a.m. arrival can make a cheap fare cost more than a full-service ticket. #cheapflights #budgetairlines #traveltips", FLY, "Numbered list: is that cheap flight really cheap")
add("fly-05-alerts", lambda: hero("cream", "PRICE ALERTS", "terra", "cream", lambda d: clock(d, W / 2, 470, 170, C["terra"], C["cream"]),
    "Watch the Fare for a Week, Then Pounce", "How to use price alerts to book flights at the right moment", "ink", "muted", "cream", "teal", tsize=80),
    TRAVEL, "How to Use Flight Price Alerts the Right Way", "Set an alert, watch the route for a week or two to learn what 'normal' looks like, then book when it dips. Good fares rarely last more than a day or two. #cheapflights #flightdeals #travelplanning", FLY, "Cream pin with clock icon: watch the fare, then book")
add("eu-01-winter", lambda: rows("EUROPE IN WINTER", "The Cheapest Months to Fly to Europe", [
    ("January–March", "low fares outside the holidays"), ("November", "quiet, cheap, cosy cities"), ("Most expensive", "summer and Christmas weeks")],
    bg="teal", lab_bg="mustard", foot="mustard", bar=["mustard", "terra", "purple"], tsize=78),
    TRAVEL, "The Cheapest Months to Fly to Europe", "January to March and November are the sweet spots; summer and the Christmas weeks cost the most. Month by month, plus how far ahead to book from the US, UK, Canada and Australia. #europetravel #cheapflights #budgettravel", EU, "Teal pin: the cheapest months to fly to Europe")
add("eu-02-citybreak", lambda: statement2("cream", "WINTER CITY BREAK", "teal", "cream", "Europe in winter", "costs less", "ink", "teal",
    ["Cheaper flights and hotels", "Shorter queues at big sights", "Christmas markets in December"], foot="teal", foot_fg="cream", cta="Best months to fly"),
    TRAVEL, "Why a Winter City Break in Europe Costs Less", "Outside the holiday weeks, winter brings cheaper flights and hotels and much shorter queues at the big sights. When to go and when to book. #citybreak #europetravel #wintertravel", EU, "Cream pin: Europe in winter costs less")
add("eu-03-book", lambda: numbered("BOOKING EUROPE", "Flying to Europe? Book at the Right Time", [
    "Off-season: book about 2–4 months ahead", "Summer: book 5–7 months ahead", "Compare nearby airports", "Be flexible by a few days"],
    accent="mustard", lab_bg="purple", foot="purple", isize=34),
    TRAVEL, "How Far Ahead to Book Flights to Europe", "Off-season long-haul: about 2–4 months ahead. Summer and holidays: 5–7 months. Compare nearby airports and be flexible by a few days. #europetravel #flighttips #travelplanning", EU, "Numbered list: flying to Europe, book at the right time")
add("delay-01-owed", lambda: hero("night", "FLIGHT DELAYED?", "mustard", "ink", lambda d: clock(d, W / 2, 470, 170, C["mustard"], C["night"]),
    "You Could Be Owed Up to €600", "3+ hours late on a flight in or out of the EU? Here's how to claim", "cream", "soft", "ink", "mustard", tsize=84),
    TRAVEL, "Flight Delayed in Europe? You Could Be Owed Up to €600", "Arrived 3+ hours late on a flight leaving the EU, or on an EU airline flying into it? You may be owed €250–€600 per passenger. Plain-English guide to EU261. #flightdelay #eu261 #travelrights", DELAY, "Night-blue pin: flight delayed, you could be owed up to 600 euros")
add("delay-02-steps", lambda: numbered("HOW TO CLAIM", "Claim Flight Delay Compensation", [
    "Keep your boarding pass", "Note your real arrival time", "Ask the airline for the reason", "Claim directly, it's free", "Or use a claim service"],
    accent="terra", lab_bg="terra", foot="terra", isize=34),
    TRAVEL, "How to Claim Flight Delay Compensation in 5 Steps", "Keep your boarding pass, note the arrival time, ask the reason, claim directly with the airline (it's free) or let a no-win-no-fee service do it. #flightdelay #travelhacks #eu261", DELAY, "Numbered list: how to claim flight delay compensation")
add("delay-03-old", lambda: statement2("cream", "DID YOU KNOW?", "teal", "cream", "Old delays", "can still be claimed", "ink", "teal",
    ["Time limits depend on the country", "Often several years", "Keep your booking emails"], foot="teal", foot_fg="cream", cta="Check your old flights"),
    TRAVEL, "You Can Still Claim for Old Flight Delays", "There's no single EU deadline: each country sets its own time limit, often several years. A delay from last year may still pay out. #flightdelay #eu261 #travelrights", DELAY, "Cream pin: old flight delays can still be claimed")
# Trip planning / free PDF
add("check-01-free", lambda: hero("mustard", "FREE PRINTABLE", "teal", "cream", lambda d: calendar(d, W / 2, 480, 170, C["teal"], C["mustard"]),
    "The Trip Planning Checklist (Free PDF)", "What to book and when, in the order that saves money and stress", "ink", "ink", "cream", "teal", tsize=80),
    TRAVEL, "Free Trip Planning Checklist (Printable PDF)", "What to book and when, from 3 months out to travel day: flights, stay, insurance, eSIM, transfers and the small things people forget. Free printable PDF. #tripplanning #travelchecklist #freeprintable", CHECK, "Mustard pin: free trip planning checklist PDF")
add("check-02-order", lambda: rows("WHAT TO BOOK WHEN", "Book Your Trip in This Order", [
    ("2–3 months before", "flights, stay, passport and visa"), ("1 month before", "insurance, tours, car or trains"), ("1–2 weeks before", "eSIM, transfer, VPN, offline maps")],
    bg="cream", lab_bg="terra", foot="teal", bar=["teal", "terra", "mustard"], tsize=76),
    TRAVEL, "Book Your Trip in This Order (and Save Money)", "2–3 months before: flights, stay, passport and visa. 1 month: insurance, tours and transport. 1–2 weeks: eSIM, airport transfer, VPN and offline maps. Get the free checklist. #tripplanning #travelplanning #traveltips", CHECK, "Table: book your trip in this order")
add("check-03-forget", lambda: statement2("cream", "TRAVEL DAY", "teal", "cream", "Don't leave", "without these", "ink", "teal",
    ["Boarding pass saved on your phone", "Medication and chargers in your carry-on", "One change of clothes"], foot="teal", foot_fg="cream", cta="Free trip planning checklist"),
    TRAVEL, "Travel Day Checklist: Don't Leave Without These", "Boarding pass saved on your phone, medication and chargers in your carry-on, a change of clothes, and your boarding pass kept until you're home. #travelchecklist #packingtips #traveltips", CHECK, "Cream pin: don't leave on travel day without these")
add("check-04-winter", lambda: numbered("WINTER TRIP", "Sort These Before a Winter Trip Abroad", [
    "Book flights early for holiday dates", "Buy travel insurance soon after booking", "Install an eSIM at home", "Download offline maps", "Save copies of your documents"],
    accent="terra", lab_bg="teal", foot="teal", isize=33),
    TRAVEL, "What to Sort Out Before a Winter Trip Abroad", "Holiday flights, insurance right after booking, an eSIM installed at home, offline maps and encrypted copies of your documents. The full checklist is free. #wintertravel #tripplanning #holidaytravel", CHECK, "Numbered list: sort these before a winter trip abroad")
# Rome, passes, car, apps
add("rome-04-winter", lambda: hero("terra", "ROME IN WINTER", "cream", "terra", lambda d: calendar(d, W / 2, 480, 170, C["cream"], C["terra"]),
    "3 Days in Rome With Fewer Crowds", "A first-visit plan that works even in the quiet season", "cream", "soft", "cream", "teal", tsize=84),
    TRAVEL, "3 Days in Rome With Fewer Crowds", "Colosseum and Forum, the Vatican and St Peter's, then the Pantheon, Navona and Trevi. A first-visit itinerary with booking tips that work in the quieter months. #rome #italytravel #citybreak", ROME, "Terracotta pin: 3 days in Rome with fewer crowds")
add("rome-05-tickets", lambda: numbered("ROME TIP", "Book These Before You Land in Rome", [
    "Colosseum timed ticket", "Vatican Museums (not on most Sundays)", "Borghese Gallery, if you want it", "A central stay"],
    accent="mustard", lab_bg="terra", foot="terra", isize=36),
    TRAVEL, "Book These Before You Land in Rome", "Colosseum timed tickets and Vatican Museums slots sell out; the Vatican is closed most Sundays. Book these four things first. #rome #romeitinerary #traveltips", ROME, "Numbered list: book these before you land in Rome")
add("rome-06-free", lambda: statement2("cream", "ROME ON A BUDGET", "terra", "cream", "Free in Rome", "and still magical", "ink", "terra",
    ["Trevi Fountain from the square", "Piazza Navona at night", "Sunset at the Pincio"], card_ok="terra", foot="terra", foot_fg="cream", cta="The full 3-day plan"),
    TRAVEL, "Free Things to Do in Rome", "Trevi from the square, Piazza Navona at night and sunset from the Pincio terrace cost nothing. Fit them into a 3-day first visit. #rome #budgettravel #italy", ROME, "Cream pin: free in Rome and still magical")
add("pass-03-worth", lambda: rows("CITY PASSES", "Is a City Pass Worth It? Do the Math", [
    ("List", "only what you'll really visit"), ("Add up", "the normal ticket prices"), ("Compare", "with the pass price for your days")],
    bg="teal", lab_bg="mustard", foot="mustard", bar=["mustard", "terra", "purple"], tsize=76),
    TRAVEL, "Is a City Pass Worth It? The 5-Minute Math", "List what you'll really visit, add up the normal ticket prices and compare with the pass. Worth it for busy first visits; poor value for slow travellers. #citypass #citybreak #budgettravel", PASSES, "Teal pin: is a city pass worth it, do the math")
add("pass-04-when", lambda: statement2("cream", "CITY PASS", "teal", "cream", "Worth it if", "you love busy days", "ink", "teal",
    ["First visit, big-name sights", "3+ paid attractions a day", "Includes a cruise or hop-on bus"], foot="teal", foot_fg="cream", cta="When it's not worth it"),
    TRAVEL, "When a City Pass Is (and Isn't) Worth It", "First visit, 3+ paid attractions a day, and extras like a cruise or hop-on bus? A pass can pay off. Slow traveller? Buy single tickets. #citypass #traveltips #citybreak", PASSES, "Cream pin: a city pass is worth it if you love busy days")
add("car-01-winter", lambda: numbered("WINTER ROAD TRIP", "Renting a Car Abroad This Winter?", [
    "Check licence and permit rules", "Use a credit card for the deposit", "Know the insurance excess", "Ask about winter tyres", "Film the car before you drive"],
    accent="mustard", lab_bg="purple", foot="purple", isize=34),
    TRAVEL, "Renting a Car Abroad This Winter? Check These First", "Licence and permit rules, a credit card for the deposit, the insurance excess, winter equipment and a quick video of the car before you drive off. #roadtrip #carrental #wintertravel", CAR, "Numbered list: renting a car abroad this winter")
add("apps-01-holiday", lambda: rows("TRAVEL APPS", "Install These Before Your Holiday Trip", [
    ("Booking", "flights, stays and trains"), ("Data", "a travel eSIM"), ("Security", "VPN and password manager"), ("Offline", "maps and translation")],
    bg="cream", lab_bg="teal", foot="teal", bar=["teal", "terra", "mustard", "purple"], tsize=74),
    TRAVEL, "The Travel Apps to Install Before Your Holiday Trip", "One app for bookings, a travel eSIM for data, a VPN and password manager for security, and offline maps and translation. Set them all up at home. #travelapps #traveltech #holidaytravel", APPS, "Table of travel apps to install before a trip")
# Christmas gifts
add("gift-01-list", lambda: hero("terra", "CHRISTMAS LIST 2026", "cream", "terra", lambda d: plane(d, W / 2, 470, 170, C["cream"]),
    "Gift Ideas for the Traveler on Your List", "Experiences, tech and cozy gifts they'll actually use", "cream", "soft", "cream", "teal", tsize=82),
    TRAVEL, "Christmas Gift Ideas 2026 for the Traveler on Your List", "City passes and museum tickets, VPN subscriptions, dash cams, cozy gifts for homebodies and digital gifts you can send on Christmas Eve. #christmasgifts #giftideas #travelgifts", GIFTS, "Terracotta pin: Christmas gift ideas for travelers 2026")
add("gift-02-digital", lambda: statement2("cream", "LAST-MINUTE GIFTS", "terra", "cream", "Forgot someone?", "Send it today", "ink", "terra",
    ["Attraction tickets by email", "A VPN or password manager", "A trip you'll plan together"], card_ok="terra", foot="terra", foot_fg="cream", cta="Digital gifts for travelers"),
    TRAVEL, "Last-Minute Digital Gifts for Travelers", "Attraction tickets delivered by email, a VPN or password manager subscription, or a promise of a trip you'll plan together. All can be sent the same day. #lastminutegifts #christmasgifts #travelgifts", GIFTS, "Cream pin: forgot someone, send a digital gift today")
add("gift-03-who", lambda: rows("GIFT GUIDE", "The Right Gift for Every Traveler", [
    ("City-breaker", "museum tickets or a city pass"), ("Digital nomad", "a VPN or password manager"), ("Road-tripper", "a dash cam"), ("Homebody", "a smart indoor herb garden")],
    bg="night", lab_bg="mustard", foot="mustard", bar=["teal", "terra", "mustard", "purple"], tsize=74),
    TRAVEL, "The Right Christmas Gift for Every Kind of Traveler", "City-breakers get tickets, digital nomads get a VPN, road-trippers get a dash cam, homebodies get an indoor herb garden. Quick picks for every budget. #giftguide #christmasgifts #travelgifts", GIFTS, "Night-blue pin: the right gift for every traveler")
add("gift-04-stocking", lambda: numbered("STOCKING STUFFERS", "Travel Stocking Stuffers Under $25", [
    "Packing cubes", "Universal adapter", "Luggage tags", "Travel journal", "A city map print"],
    accent="mustard", lab_bg="teal", foot="teal", isize=36),
    TRAVEL, "Travel Stocking Stuffers Under $25", "Small, useful gifts for the traveler in the family, plus ideas for experiences and tech. #stockingstuffers #christmasgifts #giftsunder25", GIFTS, "Numbered list: travel stocking stuffers under 25 dollars")
add("gift-05-experience", lambda: hero("cream", "GIFTS YOU CAN'T WRAP", "teal", "cream", lambda d: calendar(d, W / 2, 480, 170, C["teal"], C["cream"]),
    "Give a Memory, Not Another Object", "Experience gifts for travelers: tickets, tours and city passes", "ink", "muted", "cream", "teal", tsize=82),
    TRAVEL, "Experience Gifts for Travelers: Give a Memory", "Museum tickets, tours and city passes make gifts that don't need a suitcase. Ideas for every budget and how to choose. #experiencegifts #christmasgifts #travelgifts", GIFTS, "Cream pin: give a memory, not another object")
# Black Friday
add("bf-01-date", lambda: hero("night", "BLACK FRIDAY 2026", "mustard", "ink", lambda d: calendar(d, W / 2, 480, 170, C["mustard"], C["night"]),
    "Friday, November 27: Plan Your Buys Now", "Which travel and side-hustle deals are worth waiting for", "cream", "soft", "ink", "mustard", tsize=78),
    SIDE, "Black Friday 2026 Is November 27: What's Worth Buying", "VPNs, password managers and travel eSIMs often see their best prices of the year. Plan now, check renewal prices and skip the rest. #blackfriday2026 #deals #traveldeals", BF, "Night-blue pin: Black Friday 2026 is November 27")
add("bf-02-spot", lambda: numbered("BLACK FRIDAY", "Spot a Real Deal in 60 Seconds", [
    "Check the renewal price", "Compare per month, same length", "Look for a money-back guarantee", "Only buy what you'd use anyway"],
    accent="mustard", lab_bg="terra", foot="terra", isize=35),
    SIDE, "How to Spot a Real Black Friday Deal in 60 Seconds", "Check the renewal price, compare per month over the same length, look for a money-back guarantee and only buy what you'd use anyway. #blackfriday #smartshopping #deals", BF, "Numbered list: spot a real Black Friday deal")
add("bf-03-skip", lambda: statement2("cream", "BLACK FRIDAY", "terra", "cream", "Skip these", "deals", "ink", "terra",
    ["\"Make money fast\" bundles", "Lifetime plans from unknown brands", "Gadgets for trips you haven't planned"], card_ok="terra", foot="terra", foot_fg="cream", cta="What's actually worth it"),
    SIDE, "Black Friday Deals to Skip", "'Make money fast' bundles, lifetime plans from unknown companies and gadgets for trips you haven't planned. Here's what's actually worth it. #blackfriday #moneytips #deals", BF, "Cream pin: Black Friday deals to skip")
# Family evenings / halloween / journaling
add("fam-01-winter", lambda: rows("SCREEN-FREE EVENINGS", "Cozy Family Nights Without Screens", [
    ("Cozy nights in", "board games, blanket fort, story night"), ("In the kitchen", "bake together, soup night"), ("Creative", "crafts and a family journal")],
    bg="teal", lab_bg="mustard", foot="mustard", bar=["mustard", "terra", "purple"], tsize=76),
    FAMILY, "Cozy Screen-Free Family Nights for Fall and Winter", "Board games, baking together, crafts and slow evenings: 20 easy ideas for the whole family, plus how to make screen-free nights stick. #familytime #screenfree #cozyevenings", EVEN, "Teal pin: cozy family nights without screens")
add("fam-02-stick", lambda: statement2("cream", "FAMILY TIP", "teal", "cream", "One screen-free", "night a week", "ink", "teal",
    ["Pick a fixed night", "Let kids choose the activity", "Phones in a basket"], foot="teal", foot_fg="cream", cta="20 easy ideas"),
    FAMILY, "Start One Screen-Free Night a Week", "Pick a fixed night, let the kids choose, put phones in a basket. 20 easy ideas to make it a habit. #screenfree #familyactivities #parentingtips", EVEN, "Cream pin: one screen-free night a week")
add("fam-03-kitchen", lambda: numbered("FAMILY NIGHT", "Kitchen Nights the Kids Will Love", [
    "Make-your-own pizza", "Bake and decorate cookies", "Soup and bread night", "Hot chocolate bar"],
    accent="terra", lab_bg="terra", foot="terra", isize=36),
    FAMILY, "Kitchen Nights the Whole Family Will Love", "Homemade pizza, cookie decorating, soup and bread, a hot chocolate bar: easy, cheap screen-free evenings for cold months. #familyfun #cozyhome #kidsactivities", EVEN, "Numbered list: kitchen nights the kids will love")
add("hal-01-last", lambda: hero("night", "LAST-MINUTE HALLOWEEN", "pumpkin", "ink", lambda d: pumpkin(d, W / 2, 500, 150, C["pumpkin"], C["teal"], C["night"]),
    "Family Costumes From Your Closet", "Easy group ideas with no sewing, ready by tonight", "cream", "soft", "ink", "mustard", tsize=80),
    FAMILY, "Last-Minute Family Halloween Costumes (No Sewing)", "Group themes where everyone gets a role, made mostly from things already in your closet. Ready by tonight. #halloweencostumes #familycostumes #lastminutecostume", HAL, "Night pin with pumpkin: last-minute family costumes")
add("hal-02-group", lambda: rows("FAMILY COSTUMES", "Halloween Group Ideas for Every Family", [
    ("Family of 3", "a classic trio theme"), ("With a baby", "baby as the star prop"), ("With teens", "a pop-culture crew")],
    bg="cream", lab_bg="terra", foot="terra", bar=["terra", "mustard", "purple"], tsize=76),
    FAMILY, "Halloween Group Costume Ideas for Every Family", "Ideas for families of three, families with a baby and families with teens, mostly DIY and budget-friendly. #familycostumes #halloween2026 #diycostume", HAL, "Table of Halloween group costume ideas")
add("jrn-01-yearend", lambda: numbered("YEAR-END JOURNAL", "Journal Prompts to Close the Year", [
    "What surprised me this year?", "What am I proud of?", "What can I let go of?", "What do I want more of next year?"],
    accent="mustard", lab_bg="purple", foot="purple", isize=34),
    JOURNAL, "Year-End Journal Prompts for Beginners", "Four gentle prompts to look back on the year and plan the next one, plus how to start a journaling habit in 5 minutes a day. #journalprompts #journaling #selfcare", JRN, "Numbered list: journal prompts to close the year")
# Side hustle / AI
add("ai-01-holiday", lambda: rows("FREE AI HELPER", "Let AI Plan the Holiday Busywork", [
    ("Gifts", "brainstorm ideas by budget"), ("Meals", "a holiday menu and shopping list"), ("Trips", "a weekend plan in minutes")],
    bg="night", lab_bg="mustard", foot="mustard", bar=["teal", "terra", "mustard"], tsize=76),
    SIDE, "Let a Free AI Assistant Handle the Holiday Busywork", "Brainstorm gifts by budget, plan a holiday menu and shopping list, or sketch a weekend trip in minutes. 12 everyday tasks with ready-to-copy prompts. #aitools #productivity #holidayplanning", AI, "Night pin: let AI plan the holiday busywork")
add("ai-02-tasks", lambda: numbered("FREE AI", "Everyday Tasks a Free AI Does in Seconds", [
    "Plan a week of meals", "Rewrite an awkward email", "Explain a confusing bill", "Build a simple budget", "Plan a day trip"],
    accent="terra", lab_bg="mustard", foot="mustard", isize=34),
    SIDE, "5 Everyday Tasks a Free AI Assistant Does in Seconds", "Meal plans, awkward emails, confusing bills, a simple budget and a day-trip plan, with prompts you can copy. #chatgpttips #aitools #lifehacks", AI, "Numbered list: everyday tasks a free AI does in seconds")
add("ai-03-rules", lambda: statement2("cream", "USING AI SAFELY", "teal", "cream", "Never paste", "passwords into AI", "ink", "teal",
    ["Check facts and numbers", "Keep personal data out", "Edit before you send"], foot="teal", foot_fg="cream", cta="3 ground rules + 12 tasks"),
    SIDE, "3 Ground Rules Before You Use a Free AI Assistant", "Check facts and numbers, keep passwords and personal data out, and edit before you send. Then try 12 everyday tasks. #aitips #onlinesafety #productivity", AI, "Cream pin: never paste passwords into AI")
add("news-01-newyear", lambda: hero("teal", "SIDE HUSTLE", "mustard", "ink", lambda d: envelope(d, W / 2, 470, 300, 200, C["cream"], C["teal"], C["mustard"]),
    "Start a Newsletter Before the New Year", "One topic, one promise, a free tool and your first 100 subscribers", "cream", "soft", "ink", "mustard", tsize=80),
    SIDE, "Start a Newsletter Side Hustle Before the New Year", "Pick one topic and one promise, use a free email platform, write a welcome email and share your link where you already have an audience. Step-by-step guide. #newsletter #sidehustle #emailmarketing", NEWS, "Teal pin with envelope: start a newsletter before the new year")
add("news-02-money", lambda: numbered("NEWSLETTER INCOME", "4 Ways a Newsletter Makes Money", [
    "Sponsorships", "Affiliate links", "Paid subscriptions", "Your own products"],
    accent="mustard", lab_bg="teal", foot="teal", isize=38),
    SIDE, "4 Ways a Newsletter Makes Money", "Sponsorships, affiliate links, paid subscriptions and your own products. Most earning newsletters combine a few. How to start with $0. #newsletter #sidehustle #makemoneyonline", NEWS, "Numbered list: 4 ways a newsletter makes money")
add("yt-01-ai", lambda: hero("night", "YOUTUBE + AI", "mustard", "ink", lambda d: play(d, W / 2, 480, 170, C["mustard"], C["night"]),
    "Grow a YouTube Channel With AI Tools", "Ideas, keywords, scripts and voiceovers, without losing your own voice", "cream", "soft", "ink", "mustard", tsize=80),
    SIDE, "How to Grow a YouTube Channel With AI Tools", "Use AI for video ideas, keyword research, script drafts and voiceovers, then add your own voice. A simple weekly workflow for beginners. #youtubetips #aitools #contentcreator", YT, "Night pin with play icon: grow a YouTube channel with AI")
add("web-01-ai", lambda: statement2("cream", "SIDE PROJECT", "terra", "cream", "Build your site", "in a weekend", "ink", "terra",
    ["AI writes the first draft", "Pick a simple builder", "Launch, then improve"], card_ok="terra", foot="terra", foot_fg="cream", cta="Step-by-step with AI"),
    SIDE, "Build a Website for Your Side Project in a Weekend", "Let AI draft your pages, pick a simple builder, launch and improve as you go. Beginner-friendly guide with tool picks. #sideproject #websitedesign #aitools", WEB, "Cream pin: build your site in a weekend")
add("blog-01-sell", lambda: rows("TRAVEL CREATORS", "Ways a Travel Blog Makes Money", [
    ("Affiliate links", "tools and bookings you recommend"), ("Your products", "itineraries, guides, presets"), ("Brand work", "once you have an audience")],
    bg="teal", lab_bg="mustard", foot="mustard", bar=["mustard", "terra", "purple"], tsize=76),
    SIDE, "How a Travel Blog or Instagram Actually Makes Money", "Affiliate links, selling your own itineraries and presets, and brand work once you have an audience. Honest guide for beginners. #travelblogger #makemoneyonline #sidehustle", BLOG, "Teal pin: ways a travel blog makes money")

def schedule(n, start=datetime(2026, 10, 24, tzinfo=ZoneInfo("Europe/Bucharest"))):
    slots = [(3, 20), (5, 50), (11, 50), (20, 50)]
    out = []
    d = start
    while len(out) < n:
        for h, m in slots:
            out.append(d.replace(hour=h, minute=m))
        d += timedelta(days=1)
    return out[:n]

if __name__ == "__main__":
    # spread topics: interleave so the same link isn't posted back to back
    order = sorted(range(len(P)), key=lambda i: (0 if P[i][0].startswith("hal") else 1, i % 4, i))
    pins = [P[i] for i in order]
    times = schedule(len(pins))
    q = []
    for n, ((key, render, board, title, desc, link, alt), at) in enumerate(zip(pins, times), 1):
        img = f"pin-nov-{n:02d}-{key}.png"
        if "--no-render" not in sys.argv:
            render().save(f"{OUTV}/{img}")
        q.append(dict(n=n, at=at.isoformat(), image=img,
                      image_url=f"https://raw.githubusercontent.com/Niros79/curioandcove-media/main/pins/lotnov/{img}",
                      board_id=board, title=title[:100], description=desc[:500], link=link, alt=alt[:500], status="pending"))
    json.dump(q, open(f"{OUTV}/queue.json", "w"), indent=1, ensure_ascii=False)
    print(len(q), q[0]["at"], q[-1]["at"])
