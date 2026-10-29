# CLAUDE.md – Curio & Cove + 4Travel Pro (stare la 29 oct 2026, 23:15)

Citește fișierul ăsta la începutul fiecărei sesiuni. Sursa detaliată a deciziilor mai vechi: documentul de proiect `claude/REGULI-SI-DECIZII.md`.
Sorin (Constanța) scrie în română; răspunsuri scurte, pas cu pas; lucrează, nu pune întrebări inutile.

## 1. Cele două site-uri (identitate separată)
| | curioandcove.com | 4travel.pro |
|---|---|---|
| Ce e | blog lifestyle + afiliere, ENGLEZĂ, global | hub de rezervări Travelpayouts, 9 limbi + /ro/ |
| Rafturi / secțiuni | Travel, Money & Skills, Home & Garden, Love & Family, Mind & Spirit, Crafts & Hobbies (NU doar travel!) | 11 servicii (zboruri, cazări, sejururi, transfer, auto, biciclete, eSIM, asigurare, tururi, bagaje, zbor întârziat), ghiduri RO, idei, vacanțe |
| Repo | Niros79/curioandcove-media (site în `site/public`, push pe main = deploy Cloudflare) | Niros79/4travel-pro (GitHub Pages, CNAME www.4travel.pro) |
| Build | `tools/site/newpage.py`, apoi `python3 tools/site/decorate.py site/public` | `python3 build_index.py && PAGE_LANG=ro python3 build_index.py` (f-strings: acolade dublate `{{ }}`; texte în `extra_i18n.py`) |
| Analytics | GA4 `G-6YEV0CZ9VC` (nu-l dubla) | DOAR scriptul Travelpayouts emrldtp.com → de pus Cloudflare Web Analytics |

Repo-ul curioandcove-media e PUBLIC (raw.githubusercontent merge fără login). Nu pune aici parole sau date personale.
Nu pune CLAUDE.md sau alte .md interne în 4travel-pro: GitHub Pages ar publica fișierul pe site.

### Ce e live (29 oct)
- **Curio:** homepage compact (filtre pe rafturi, 8 carduri + „Show more guides”, înălțime ~2.900 px). Viator + SafetyWing în: cheap-winter-city-breaks-europe, are-city-passes-worth-it, trip-planning-checklist.
- **4travel:** redesign compact (hero cu poză, 11 servicii ca iconițe, tab-uri pentru idei, secțiunea Ghiduri RO). Tab „Asigurare” cu SafetyWing, secțiunea Viator cu 10 orașe (iframe srcdoc pe oraș). **Fix mobil 29 oct** (commit d14c5c9): carduri de ghid la 80%, servicii pe 4 coloane, fără bare de scroll.
- **Ghiduri RO pe 4travel (29 oct):** /sejur-all-inclusive/ (hub), /bulgaria-all-inclusive/, /turcia-all-inclusive/, /egipt-all-inclusive/, /grecia-cu-masina/, plus /wizz-air/ (mai vechi). Toate cu FAQ JSON-LD, Trip.com pe PID 4travel, Viator și legături între ele.
- Widget-ul de zboruri Travelpayouts rămâne în engleză („To”, „Search”); nu suportă română.

## 2. Afiliere (ID-uri)
- **CJ:** Trip.com ad 11947208. Link `https://www.tkqlhce.com/click-<PID>-11947208?url=<url trip.com codat>&sid=...`. PID Curio 101697384, **PID 4travel 101916040** (de verificat în rapoarte CJ că se înregistrează click-urile; s-a văzut utm_campaign=null). Alte programe CJ: NordVPN, Surfshark, NordPass, Click & Grow (nu direct pe social), Rexing, Abracadabra. Aplicări 29 oct: Tui.ro 5%, DerTour.ro 4%, eSky, Iberostar, Barcelo (în așteptare). Sandals: respins automat.
- **Travelpayouts** marker 662933: proiect Curio 582262, proiect 4travel.1 502962.
- **Viator** pid P00328028, mcid 42383: `?pid=P00328028&mcid=42383&medium=link&campaign=<tag>`. Widget dinamic W-14b249a7-ab36-49dc-9f79-503658edd3af. widget.js randează o singură dată pe pagină, deci folosește iframe srcdoc pe oraș. Orașe verificate: Lisbon d538, Porto d26879, Seville d556, Athens d496, Prague d462, Budapest d499, Krakow d529.
- **SafetyWing** referenceID 26624480: `https://safetywing.com/nomad-insurance?referenceID=26624480&utm_source=26624480&utm_medium=Ambassador&utm_campaign=<tag>`. Widget de preț `safetywing-price-widget-v2.js`.
- Mail trimis (29 oct, de pe niros.link) la Viator și SafetyWing pentru adăugarea 4travel.pro ca al doilea site; aștept răspuns.
- CloudTraffic ID 6094 (testează linkul înainte: ofertele [DUPLICATED] duc la test.test). Digistore24 `#aff=SorinSerban` (produsele cu pagini de vânzare agresive doar pe site, NU pe social). Kit, Sellfy, ElevenLabs, doola: vezi `claude/lista-programe-active-2026-10-22.md`.

## 3. Shorts / clipuri video
- **Stilul nou „viral” (29 oct): `tools/reels/make_viral.py`.** Se folosește de acum pentru toate clipurile.
  - Cârligul vorbit are maximum 8 cuvinte și se termină în ~2 s.
  - Subtitrări ASS cuvânt cu cuvânt (2 cuvinte pe ecran, cuvântul rostit cu galben).
  - Tăieturi la 1,6 s, cu punch-in și sunet „whoosh”.
  - Fără card de final: ultima frază duce în cârlig, ca să se reia singur.
  - Linkul și întrebarea pentru comentarii stau în descriere și în comentariul fixat.
  - Spec: hook_spoken, hook_text (`\N` = rând nou), chunks, question, clips, music_file.
  - ~2 minute de randare.
- Generatorul vechi `make_short.py` (cu cap_y/cap_maxw/cap_size pentru zonele sigure, preset veryfast) rămâne pentru clipurile doar cu text, de exemplu cele RO.
- Voce: Kokoro (kokoro.onnx + voices.bin în tools/reels, ignorate în git), am_michael. **Kokoro nu are română** → clipurile RO sunt doar text + muzică (sau ElevenLabs RO, voice onwK4e9ZLuTAKqWW03F9, plătit).
- Footage în `tools/reels/footage/` (ignorat în git). Pexels: din Chrome, `fetch('/download/video/<ID>/')` → `r.url` dă link-ul de pe videos.pexels.com, apoi descarci din shell. Clipurile apt1–apt5 = aeroport (29 oct). Capturile site-ului 4travel: Playwright local pe http.server, cu fonturile Archivo/Inter servite din @fontsource (rutare fonts.googleapis).
- **Unde se salvează clipurile (Sorin le ia de aici):** `reels/2026-10/<subiect>/` (YouTube), `tiktok-usa/2026-10/<subiect>/`, `facebook/2026-10/<subiect>/`, fiecare cu un fișier `...-TEXTE.txt` (titlu, descriere, hashtag-uri, link Bitly pe platformă). Mereu commit + push pe main.
- Clipuri făcute pe 29 oct:
  - **voucher**: EU261, v1 39 s + **v2 VIRAL 25 s**. Bitly: YT bit.ly/47PfuiJ, TikTok bit.ly/4Bw0i7K, FB bit.ly/3UV1AZu.
  - **4travel-prezentare**: „Vacanța 2027 te poate costa cu sute de euro mai puțin”, 39 s, text + muzică, capturi reale din site. Bitly: YT bit.ly/3W2P3DI, TikTok bit.ly/4e2kSCO, FB bit.ly/4BzkFko.
- **Programat:** v2 voucher pe YouTube **vineri 30 oct, 19:00** (ora României), prin Metricool (blogId 7276302, post 410550810). Sorin fixează comentariul cu linkul după publicare.
- Cercetare (yt-viral, 2.931 de Shorts): `claude/youtube-shorts-cercetare-2026-10-29.md`. Merg: „primul lucru pe care îl fac…”, clasamentele („orașe care chiar merită”), avertismentele („nu lua voucherul”), greșelile de evitat. Cârligele se scorează cu `hookscore.py` din skill-ul yt-script (doar pentru engleză).
- **Următoarele clipuri (aprobate ca direcție):**
  - Curio, câte unul pe raft:
    - somn: „Why do you wake up tired? Try this 10 minute evening routine…” (66);
    - hobby-uri: „Before you start a winter hobby, check which 5 need almost no money or experience” (67);
    - ierburi: „Before you buy supermarket herbs again…” (57);
    - cadouri de Crăciun (57);
    - AI gratuit pentru sarcini zilnice (54);
    - Black Friday (cârligul trebuie lucrat).
  - 4travel: prezentarea în stil viral, Wizz Air cu voucherul, Bulgaria early booking.
  - NU mai ancora totul pe travel.

## 4. Platforme și conexiuni
- **YouTube** (canal Curio & Cove UCV5XwLMddQt2xb8ZD8ogMZg, @niros-curioandco, pe contul Google niros.link): 13 clipuri publice, 2.524 de vizualizări, 1 abonat (29 oct). Prin Composio, cotele YouTube API sunt COMUNE cu alți clienți Composio (29 oct: limita de încărcări și cea de citiri epuizate, deci eroare 429/403).
  - **Propunere în curs:** proiect Google Cloud propriu (YouTube Data API v3 + Analytics API, OAuth în producție) conectat în Composio. Atenție: proiectele neverificate încarcă doar PRIVAT până la auditul YouTube API, deci până atunci publicăm prin Metricool.
  - Sorin vrea ca Claude să gestioneze canalul ca pe Pinterest: un Short pe zi, titluri, descrieri, playlist-uri, comentarii, raport lunea. NU se șterg clipuri și NU se schimbă setările canalului fără întrebare.
- **Metricool** (blogId 7276302): YouTube, TikTok gheorghesorin06, Facebook, Pinterest, Instagram, Threads și Bluesky sunt conectate. Planul gratuit are ~20 de postări pe lună.
- **Pinterest** curioandcove (Composio, direct): 92 de pin-uri, 144 de afișări și 1 click în 30 de zile (29 oct). Ținta: 3 pin-uri pe zi pe cuvinte căutate.
- **Bitly** conectat: câte un link pe platformă cu UTM (`utm_source`=platforma, `utm_campaign`=subiectul).
- **Reddit** u/CurioandCove: maximum 1 comentariu din 3 cu link, niciodată link de afiliat; extensia Chrome nu are voie pe reddit.com. **Quora/Medium**: fără linkuri directe de afiliat.
- **Facebook / Instagram:** NU reconecta fără cererea explicită a lui Sorin. Grupurile FB românești pentru 4travel le postează Sorin manual.
- **vidIQ:** fără credite (29 oct). **PostHog:** proiectul 319928 nu primește date.
- **Gmail** (conect.media@gmail.com) poate trimite mailuri la cerere.

## 5. Planul de trafic (doc „Plan de trafic Curio & Cove + 4Travel Pro”, 29 oct)
- Lucruri de făcut de Sorin:
  - Cloudflare Web Analytics pe ambele site-uri (Sorin dă codul);
  - Search Console pentru 4travel + cererea de indexare a celor 5 ghiduri;
  - cheile .env pentru OpenMontage pe laptop;
  - 5–8 grupuri FB;
  - aprobarea listei săptămânale lunea.
- Ritm:
  - Shorts: 4 pe săptămână EN + 2 pe săptămână RO (de acum: unul pe zi);
  - 2 ghiduri SEO pe săptămână pe fiecare site;
  - 3 pin-uri pe zi.
- Calendar de sezon: early booking 2027, târguri de Crăciun, Revelion, **Black Friday 27 nov**.
- Ținte la 29 nov: 7.500 de vizualizări YT, 30 de abonați, 1.500 de afișări Pinterest pe lună, Google Curio 100 de afișări pe zi, 4travel 50 pe zi, Kit 25 de abonați, 16 ghiduri noi.
- Ghiduri următoare: /vacanta-exotica-buget/, /early-booking-2027/, târguri de Crăciun cu zbor din România, Revelion, acte Turcia/Egipt, Black Friday la vacanțe; Curio EN: Christmas markets on a budget, cheap New Year city breaks, Black Friday travel deals.

## 6. Unelte instalate
- OpenMontage (/home/claude/OpenMontage, `make setup`): fără chei merg editarea, subtitrările și muzica; generarea de imagini, video și TTS cere chei (Sorin le pune în .env pe laptop, după ce leagă calculatorul).
- Skill YouTube (youtube-agent: yt-script, yt-viral, yt-package, yt-seo etc.).
- Pluginuri trimise lui Sorin pe 29 oct: superpowers, andrej-karpathy-skills, mattpocock-skills, ponytail (fără panoul band). ECC (311 skill-uri) NEinstalat: propunerea e o selecție de 10–20. gstack NEinstalat: cere setup pe laptop și regula lui „nu folosi Chrome” NU se aplică.
- Skill-uri Anthropic propuse: academy-guide, discernment-nudge, webapp-testing.

## 7. Reguli de lucru (permanente)
- Schimbările pe site: ramură draft, apoi capturi de probă (Playwright local, mobil 390 px + desktop), apoi OK de la Sorin, apoi merge pe main, apoi verificare pe site-ul live.
- Înainte să schimbi ceva existent (furnizori, linkuri), verifică ce era și păstrează alegerile lui Sorin.
- Claude NU face: parole, logări, conturi noi, captcha, OTP, date de plată/bancă/fiscale/ID, chei API. Le face Sorin.
- Mesajele în numele lui Sorin cer acordul lui. Conectările OAuth noi cer acord explicit; dacă apare ceva neașteptat, te oprești.
- Liste de postări: aprobate de Sorin (excepție: gestiunea YouTube/Pinterest delegată pe 29 oct, cu raport lunea).
- Conținut fără get-rich-quick, MLM, crypto, suplimente, gambling, dating, trading. Fără cifre inventate în cârlige sau scenarii.
- Livrarea: fișierele mari pe GitHub (foldere pe platformă) + linkuri trimise; Sorin le ia de acolo.
