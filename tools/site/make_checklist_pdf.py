from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor

GF = "/usr/share/fonts/truetype/google-fonts/"
pdfmetrics.registerFont(TTFont("P", GF + "Poppins-Regular.ttf"))
pdfmetrics.registerFont(TTFont("PM", GF + "Poppins-Medium.ttf"))
pdfmetrics.registerFont(TTFont("PB", GF + "Poppins-Bold.ttf"))
TEAL, INK, MUST, TERRA, CREAM, MUTED = (HexColor(x) for x in ("#1f4e4a", "#1f2a30", "#e0a83c", "#c8643b", "#f6f1e7", "#5b6670"))
W, H = A4
OUT = "/home/claude/site_out/freebies/trip-planning-checklist.pdf"

STAGES = [
    ("2–3 MONTHS BEFORE", "The big bookings", TEAL, [
        "Fix your dates (flexible by a day or two saves money)",
        "Book the flight first: compare airlines and check baggage rules",
        "Check the arrival time: late landing = transfer + extra night?",
        "Book your stay with free cancellation, location over size",
        "Passport valid 3–6 months after return, with blank pages",
        "Visa or electronic travel permit (e.g. ESTA, UK ETA) from the official site",
    ]),
    ("ABOUT 1 MONTH BEFORE", "Protect the trip", TERRA, [
        "Buy travel insurance soon after booking (check medical limit and excess)",
        "Book the 1–2 tours or tickets you'd hate to miss (free cancellation)",
        "Reserve a rental car or plan trains between cities",
        "Tell your bank you're travelling; check card fees abroad",
    ]),
    ("1–2 WEEKS BEFORE", "Details that save you on arrival", MUST, [
        "Sort out mobile data: install a travel eSIM at home, on Wi-Fi",
        "Book the airport transfer or note the train/bus route",
        "Install a VPN and turn on auto-connect for public Wi-Fi",
        "Update passwords and turn on two-factor authentication",
        "Save copies of passport, insurance and bookings (encrypted)",
        "Download offline maps and the key apps (airline, transport, translator)",
    ]),
    ("TRAVEL DAY", "Before you leave for the airport", TEAL, [
        "Online check-in done, boarding pass saved on your phone",
        "Medication, chargers and documents in your carry-on",
        "One change of clothes in your carry-on",
        "Arrive early for international flights",
        "Keep your boarding pass until you're home (delay claims)",
    ]),
]


def header(c, title, sub):
    c.setFillColor(CREAM); c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(TEAL); c.rect(0, H - 120, W, 120, fill=1, stroke=0)
    c.setFillColor(MUST); c.setFont("PB", 10); c.drawString(40, H - 42, "CURIO & COVE")
    c.setFillColor(CREAM); c.setFont("PB", 24); c.drawString(40, H - 76, title)
    c.setFont("P", 11); c.drawString(40, H - 100, sub)


def footer(c, n):
    c.setFillColor(TEAL); c.rect(0, 0, W, 36, fill=1, stroke=0)
    c.setFillColor(CREAM); c.setFont("PM", 9)
    c.drawString(40, 14, "curioandcove.com  ·  Full guide: curioandcove.com/trip-planning-checklist/")
    c.drawRightString(W - 40, 14, f"Page {n}/2")


def stage(c, y, lab, title, col, items):
    c.setFillColor(col); c.roundRect(40, y - 22, 170, 20, 10, fill=1, stroke=0)
    c.setFillColor(CREAM if col != MUST else INK); c.setFont("PB", 8.5); c.drawString(50, y - 16, lab)
    c.setFillColor(INK); c.setFont("PB", 13); c.drawString(222, y - 17, title)
    y -= 38
    for t in items:
        c.setStrokeColor(col); c.setLineWidth(1.4); c.roundRect(44, y - 3, 11, 11, 2, fill=0, stroke=1)
        c.setFillColor(INK); c.setFont("P", 10.2); c.drawString(66, y, t)
        y -= 21
    return y - 14


c = canvas.Canvas(OUT, pagesize=A4)
c.setTitle("Trip Planning Checklist – Curio & Cove"); c.setAuthor("Curio & Cove")
header(c, "Trip Planning Checklist", "What to book and when, in the order that saves money and stress. Tick as you go.")
y = H - 150
for s in STAGES[:2]:
    y = stage(c, y, *s)
# notes box
c.setFillColor(HexColor("#ffffff")); c.roundRect(40, 60, W - 80, y - 70, 12, fill=1, stroke=0)
c.setFillColor(TEAL); c.setFont("PB", 11); c.drawString(56, y - 30, "My trip")
c.setFillColor(MUTED); c.setFont("P", 9.5)
yy = y - 52
for lab in ["Destination", "Dates", "Flight", "Stay", "Insurance policy no.", "Emergency contact"]:
    c.drawString(56, yy, lab); c.setStrokeColor(HexColor("#d9d2c4")); c.line(170, yy - 2, W - 60, yy - 2); yy -= 26
footer(c, 1); c.showPage()

header(c, "Trip Planning Checklist", "Part 2: the final weeks and travel day.")
y = H - 150
for s in STAGES[2:]:
    y = stage(c, y, *s)
c.setFillColor(HexColor("#ffffff")); c.roundRect(40, 60, W - 80, y - 70, 12, fill=1, stroke=0)
c.setFillColor(TEAL); c.setFont("PB", 11); c.drawString(56, y - 30, "Helpful guides on Curio & Cove")
c.setFillColor(INK); c.setFont("P", 10)
yy = y - 52
for t in ["Cheapest time to fly to Europe  ·  curioandcove.com/cheapest-time-to-fly-to-europe/",
          "Best eSIM for travel  ·  curioandcove.com/best-esim-for-travel/",
          "NordVPN vs Surfshark for travel  ·  curioandcove.com/nordvpn-vs-surfshark-travel/",
          "Flight delayed? Claim up to €600  ·  curioandcove.com/eu-flight-delay-compensation-americans/",
          "All the tools we recommend  ·  curioandcove.com/tools/"]:
    c.drawString(56, yy, t); yy -= 20
footer(c, 2); c.save()
print(OUT)
