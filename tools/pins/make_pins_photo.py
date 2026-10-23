"""Photo pins (Pexels photo + title panel) for the Oct 23 article batch.
Run: python3 tools/pins/make_pins_photo.py  -> writes pins/lotwinter/*.png and queue.json
"""
import json, os, sys, urllib.request, io
from datetime import datetime
from zoneinfo import ZoneInfo
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LOT = "lotwinter"
OUT = os.path.join(ROOT, "pins", LOT)
CACHE = os.environ.get("PIN_CACHE", "/tmp/pin_photos")
os.makedirs(OUT, exist_ok=True); os.makedirs(CACHE, exist_ok=True)
W, H, PH = 1000, 1500, 940
PAPER, INK, MUTED = (234, 226, 211), (28, 46, 41), (95, 104, 98)
ACC = {"teal": (31, 92, 86), "terra": (178, 90, 60), "mustard": (196, 150, 50), "plum": (110, 70, 100)}
SERIF = "/usr/share/fonts/truetype/google-fonts/Lora-Variable.ttf"
SANS_B = "/usr/share/fonts/opentype/inter/Inter-Bold.otf"
SANS = "/usr/share/fonts/opentype/inter/Inter-Medium.otf"
TRAVEL, SIDE, FAMILY, JOURNAL = "1094023003171921131", "1094023003171940577", "1094023003171970038", "1094023003171920516"
S = "https://curioandcove.com/"
TRIP = "https://www.tkqlhce.com/click-101697384-11947208?url=https%3A%2F%2Fwww.trip.com%2F{p}%2F&sid={sid}"
CT = "https://trl.cldtraflink.com/click?pid=6094&offer_id={o}&sub1={s}"
KIT = "https://partners.kit.com/x60xmzo3zk03"
TIQETS = "https://tiqets.tpm.lv/iUScXcHE"
SELLFY = "https://sellfy.com/?via=sorin-curio-and-cove"
RAW = f"https://raw.githubusercontent.com/Niros79/curioandcove-media/main/pins/{LOT}/"


def serif(size):
    f = ImageFont.truetype(SERIF, size)
    try:
        f.set_variation_by_name("Bold")
    except Exception:
        pass
    return f


def photo(pid):
    p = os.path.join(CACHE, f"{pid}.jpg")
    if not os.path.exists(p):
        url = f"https://images.pexels.com/photos/{pid}/pexels-photo-{pid}.jpeg?auto=compress&cs=tinysrgb&w=1600"
        urllib.request.urlretrieve(url, p)
    return Image.open(p).convert("RGB")


def wrap(d, text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            lines.append(cur); cur = w
    lines.append(cur)
    return lines


def render(pid, kicker, title, sub, acc, fname, focus=(0.5, 0.5)):
    im = Image.new("RGB", (W, H), PAPER)
    im.paste(ImageOps.fit(photo(pid), (W, PH), centering=focus), (0, 0))
    d = ImageDraw.Draw(im)
    a = ACC[acc]
    kf = ImageFont.truetype(SANS_B, 30)
    kw = d.textlength(kicker, font=kf) + 48
    d.rounded_rectangle([60, PH - 34, 60 + kw, PH + 30], radius=32, fill=a)
    d.text((84, PH - 20), kicker, font=kf, fill=(255, 255, 255))
    size = 78
    while True:
        tf = serif(size)
        lines = wrap(d, title, tf, W - 120)
        if len(lines) <= 3 or size <= 56:
            break
        size -= 4
    y = PH + 62
    for ln in lines:
        d.text((60, y), ln, font=tf, fill=INK); y += int(size * 1.16)
    sf = ImageFont.truetype(SANS, 32)
    for ln in wrap(d, sub, sf, W - 120)[:2]:
        d.text((60, y + 8), ln, font=sf, fill=MUTED); y += 44
    ff = ImageFont.truetype(SANS_B, 28)
    d.rectangle([0, H - 70, W, H], fill=a)
    t = "curioandcove.com"
    d.text(((W - d.textlength(t, font=ff)) / 2, H - 52), t, font=ff, fill=(255, 255, 255))
    im.save(os.path.join(OUT, fname), optimize=True)


TZ = ZoneInfo("Europe/Bucharest")
SLOTS = []
for day in range(24, 30):
    for hh, mm in [(0, 20), (14, 50)]:
        SLOTS.append(datetime(2026, 10, day, hh, mm, tzinfo=TZ))

# key, photo id, focus, kicker, title on image, subtitle, accent, board, pin title, description, link, alt
PINS = [
 ("citybreak-1", 19099383, (0.5, 0.4), "WINTER TRAVEL", "10 Cheap Winter City Breaks in Europe", "Christmas markets, mild cities and low winter prices", "teal", TRAVEL,
  "10 Cheap Winter City Breaks in Europe", "From Christmas-market Prague and Kraków to mild Lisbon and Seville: winter is when European city breaks get cheap. Compare flight + hotel deals for your dates. (Affiliate link) #winterTravel #citybreak #europetravel #christmasmarkets",
  TRIP.format(p="packages", sid="pin-citybreak-1"), "Snowy Prague old town square with a Christmas tree"),
 ("gifts-1", 6334540, (0.5, 0.5), "CHRISTMAS 2026", "Christmas Gifts the Whole Family Will Remember", "Give a day out instead of more stuff", "terra", FAMILY,
  "Christmas Gift Idea: Give the Whole Family a Day Out", "Tickets to a museum, zoo, show or attraction are the gift people still talk about years later. Book instant mobile tickets and wrap a simple voucher. (Affiliate link) #christmasgifts #experiencegifts #familygifts #giftideas",
  TIQETS, "Wrapped presents under a Christmas tree"),
 ("newsletter-1", 1766604, (0.5, 0.5), "SIDE INCOME", "How to Start a Paid Newsletter From Zero", "Free list first, paid tier later: the realistic way", "teal", SIDE,
  "How to Start a Paid Newsletter From Zero", "Start free, build trust, then add a paid tier. Kit lets you build your list on a free plan and switch on paid subscriptions when you're ready. (Affiliate link) #newsletter #sidehustle #creatoreconomy #emailmarketing",
  KIT, "Notebook, laptop and coffee on a cafe table"),
 ("garden-1", 8543138, (0.5, 0.5), "INDOOR GARDEN", "12 Easy Things to Grow Indoors This Winter", "Microgreens, herbs and salad leaves on a windowsill", "teal", FAMILY,
  "12 Easy Things to Grow Indoors This Winter", "Microgreens ready in 7 to 14 days, herbs that grow all winter, and the light they need. A simple indoor garden for small flats. #indoorgarden #microgreens #wintergardening #herbs",
  S + "indoor-winter-garden/", "Tray of fresh microgreens and herbs"),
 ("sleep-1", 4058794, (0.5, 0.35), "BETTER SLEEP", "A 60-Minute Evening Routine for Better Sleep", "Dim lights, empty your head onto paper, sleep", "plum", JOURNAL,
  "A 60-Minute Evening Routine for Better Sleep", "Five minutes writing tomorrow's list before bed calms a racing mind. A good planner makes the habit easy to keep. (Affiliate link) #sleeproutine #eveningroutine #planner #selfcare",
  CT.format(o=2942, s="pin-sleep-routine"), "Woman reading in bed by warm lamplight"),
 ("hobbies-1", 6633330, (0.5, 0.5), "COSY HOBBIES", "15 Cosy Winter Hobbies to Try at Home", "Learn one properly this winter with an expert-led course", "mustard", JOURNAL,
  "15 Cosy Winter Hobbies to Try at Home", "Photography, gardening, cooking and more: learn a new hobby this winter with online courses taught by experts, with personal feedback. (Affiliate link) #winterhobbies #learnsomethingnew #hobbies #cozy",
  CT.format(o=2954, s="pin-hobbies"), "Hands knitting a green blanket in an armchair"),
 ("citybreak-2", 19627783, (0.5, 0.5), "MILD WINTER CITIES", "Warm Winter City Breaks: Lisbon, Seville, Athens", "Swap the heavy coat for sunny winter streets", "terra", TRAVEL,
  "Warm Winter City Breaks in Europe: Lisbon, Seville, Athens", "Southern Europe is mild in winter and hotels drop to low-season prices. Find a central hotel for your city break. (Affiliate link) #lisbon #seville #athens #wintersun #citybreak",
  TRIP.format(p="hotels", sid="pin-citybreak-2"), "Yellow tram 28 on a sunny Lisbon street"),
 ("gifts-2", 8307520, (0.5, 0.45), "GIFTS FOR GRANDPARENTS", "Gifts for Grandparents Who Have Everything", "An online course in the hobby they love", "terra", FAMILY,
  "Gifts for Grandparents Who Have Everything", "Retirement brings time for hobbies. Give an online course in gardening, photography or cooking, taught by well-known experts. (Affiliate link) #giftsforgrandparents #christmasgifts #giftideas #retirement",
  CT.format(o=2954, s="pin-gifts-grandparents"), "Grandparents and a child looking at photos together"),
 ("newsletter-2", 8297056, (0.5, 0.5), "NEWSLETTER MATH", "What 200 Paying Subscribers Really Earn", "At $5 a month that is $1,000 a month, before fees", "teal", SIDE,
  "What 200 Paying Newsletter Subscribers Really Earn", "200 readers at $5 a month is $1,000 a month before fees. Build your list free on Kit and turn on paid subscriptions when readers ask for more. (Affiliate link) #paidnewsletter #sidehustle #onlineincome #newsletter",
  KIT, "Woman typing on a laptop holding a pen"),
 ("garden-2", 1309426, (0.5, 0.5), "WINDOWSILL GREENS", "Fresh Greens in 7 Days: Microgreens on a Windowsill", "The fastest win in winter gardening", "teal", FAMILY,
  "Fresh Greens in 7 Days: Grow Microgreens on a Windowsill", "Sow pea, radish or sunflower seeds thickly on a tray and snip them in a week or two. Plus 11 more easy things to grow indoors this winter. #microgreens #indoorgardening #windowsillgarden",
  S + "indoor-winter-garden/", "Fresh parsley leaves close up"),
 ("sleep-2", 4577650, (0.5, 0.5), "SLEEP HOT?", "Sleep Hot? A Cooler Bed for Better Sleep", "Cool or warm each side of the bed separately", "plum", JOURNAL,
  "Sleep Hot? A Cooler Bed Can Help You Sleep Better", "Most people sleep better when the bed stays cool. If you or your partner overheat at night, a temperature-controlled mattress cover cools or warms each side separately. (Affiliate link) #sleepbetter #hotsleeper #sleephygiene",
  CT.format(o=545, s="pin-sleep-cool"), "Books and a lamp on a bedside table"),
 ("hobbies-2", 19479498, (0.5, 0.5), "HOBBY TO INCOME", "Winter Hobbies That Can Earn a Little Money", "Sell patterns, printables and digital art", "mustard", SIDE,
  "Winter Hobbies That Can Earn a Little Money", "Crochet patterns, printable planners and digital art can be sold again and again. Open a simple store that delivers the files for you. (Affiliate link) #sidehustle #digitalproducts #crochetpatterns #printables",
  SELLFY, "Knitting needles and balls of yarn"),
]

if __name__ == "__main__":
    q = []
    for i, (key, pid, focus, kick, t_img, sub, acc, board, title, desc, link, alt) in enumerate(PINS):
        fn = f"pin-win-{i + 1:02d}-{key}.png"
        render(pid, kick, t_img, sub, acc, fn, focus)
        q.append({"n": i + 1, "at": SLOTS[i].isoformat(), "image": fn, "image_url": RAW + fn, "board_id": board,
                  "title": title, "description": desc, "link": link, "alt": alt, "status": "pending"})
    json.dump(q, open(os.path.join(OUT, "queue.json"), "w"), indent=1, ensure_ascii=False)
    print(len(q), "pins;", q[0]["at"], "->", q[-1]["at"])
