---
name: "curioandcove-growth"
description: "Run growth work for Curio & Cove (curioandcove.com): research what people ask, write/update articles, make pins and reels, answer on Quora/Reddit/Medium, check mail, affiliates and stats."
---

# Curio & Cove – growth operations (v1, 20 Oct 2026)

Owner: Sorin (writes in Romanian; reply to him in Romanian, short and clear, step by step). Site and all public content are in **English for a global audience** (US, UK, CA, AU, EU). Never anchor everything on one destination.

## 0. Start of every session
1. Read the project docs `claude/curioandcove-status-*.md` (newest), `claude/curioandcove-affiliate-links-2026-10-13.md`, the latest `claude/pachet-quora-medium-*.md`, and `tools/skill/IMPROVEMENTS.md` in the repo (lessons learned – they override older instructions below).
2. Clone/pull GitHub `Niros79/curioandcove-media` (add_repo with push access). It is the source of truth:
   - `site/public/` = the live HTML site. Push to `main` → Cloudflare Worker `orange-voice-3e98` deploys in ~60 s. No zips.
   - `pins/<lot>/` = pin PNGs + `queue.json` (fields: n, at, image, image_url, board_id, title, description, link, alt, status).
   - `reels/`, `facebook/`, `tiktok-usa/` = videos + caption txt.
   - `weekly/` = Quora/Medium packs, `extension-playbook.md`, `log.md`.
   - `tools/site` (newpage.py, signup.py, kitjs.py, make_checklist_pdf.py), `tools/pins`, `tools/reels`, `tools/skill`.
   - Work copy: `cp -r site/public /home/claude/site_out` and `export CC_SITE=/home/claude/site_out`; after edits `cp -r /home/claude/site_out/. site/public/`, commit, push.
3. Commits: author `Claude <noreply@anthropic.com>` plus the attribution trailers from the system reminder.
4. Verify live pages with Composio `COMPOSIO_REMOTE_BASH_TOOL` + curl (WebFetch is cached and unreliable here).

## 1. Tools and connections
- **Composio** (reuse the session id): Pinterest (alias curioandcove), Google Search Console (`sc-domain:curioandcove.com`), Kit (form id 10059486), Gmail alias `niros` (niros.link@gmail.com – receives hello@curioandcove.com), ScrapeCreators (paid, ~$0.001/credit: search Reddit/Threads/YouTube/LinkedIn), Reddit (connect once Sorin has an account).
- **Gmail connector** = conect.media@gmail.com (Travelpayouts, Metricool, CJ newsletters).
- **Metricool** brandId 7276302, free plan = 20 posts/month (counted per post). Networks: Instagram, TikTok, YouTube Shorts, Threads, Bluesky. No Facebook.
- **Claude in Chrome extension** (Sorin's real Chrome): Quora, Medium, Travelpayouts, PartnerStack, Dub, CJ, Kit UI. Load tools in one ToolSearch call; work in a new tab; if the tab group disappears, call tabs_context_mcp with createIfEmpty. Quora's editor is slow → type in chunks, wait 20–25 s, don't type list numbers after the first item (auto-list).
- **Scheduled tasks**: pin publishers (00:25, 03:25, 05:55, 08:55, 11:55, 14:55, 17:55, 20:55 Romania) read `pins/*/queue.json`; Monday 08:53 Quora/Medium weekly pack.
- Pinterest boards: Travel Tips 1094023003171921131 · Side Hustles & AI Tools 1094023003171940577 · Family Fun & Holidays 1094023003171970038 · Indoor Herb Garden 1094023003171920084 · Journaling & Self-Care 1094023003171920516 · Herbal Tea 1094023003171920102.

## 2. Research – what people want (weekly, cheap sources first)
1. **Search Console** (`GOOGLE_SEARCH_CONSOLE_SEARCH_ANALYTICS_QUERY`, dimensions page/query, last 28 days, data_state all): pages at position 8–20 = upgrade first; queries with impressions but no page = new article ideas.
2. **Pinterest Trends** (`PINTEREST_GET_KEYWORD_TRENDS`, regions US, GB+IE, CA, AU+NZ; trend_type growing + seasonal; interests travel, finance, education, parenting, gardening, home_decor). Plan pins 45–60 days ahead of seasons.
3. **Fresh questions**: `SCRAPECREATORS_SEARCH_REDDIT` / `SEARCH_THREADS_POSTS` / `SEARCH_YOUTUBE` with our keywords (tell Sorin the cost first if >200 calls). Also Quora search (extension) and Google "People also ask" via WebSearch.
4. Output: question → matching guide (or "new article needed"). Save it in the weekly pack.

## 3. Content on the site
- Use `tools/site/newpage.py` (`make()` adds the page to homepage, category and sitemap; `check()` validates links/JSON-LD; `faq()` builds FAQ + FAQPage schema). Every new page gets the Kit signup block (`signup.py`) and the AJAX script (`kitjs.py`).
- Articles: 1,500+ words, honest, answer first, tables where useful, FAQ, 3+ internal links, affiliate disclosure note, external affiliate links `rel="sponsored nofollow noopener" target="_blank"`. Verify current facts (prices, rules) before stating them.
- Priority: upgrade pages ranking 8–20; then new "money" articles using active programs (see affiliate doc): Sellfy, doola, NordVPN/Surfshark/NordPass, Kit, ElevenLabs, Klook/Trip.com/Travelpayouts.
- After pushing: verify with curl; optionally resubmit the sitemap in Search Console.

## 4. Pinterest pins
- 3–5 new pins/day, always about 2 weeks queued ahead. PNGs 1000×1500 in the `tools/pins` style (teal #1f4e4a, mustard #e0a83c, terracotta #c8643b, cream #f6f1e7; Poppins).
- Write `queue.json` entries (evening US/UK/AU = night in Romania), push PNGs + queue; scheduled tasks publish them.
- Always also give Sorin the txt list: Data și ora · Poza · Board · Titlu · Descriere · Link · Alt text.
- Never link Click & Grow directly in social posts; The Self-Sufficient Backyard is banned on social.

## 5. Reels / shorts
- 6–10 s, cinematic real footage, big hook in the first frame, different vibrant music per clip, CTA "link in the first comment" (Threads/Bluesky: link in text). Tools in `tools/reels`.
- Upload to `reels/YYYY-MM/`, schedule in Metricool (19:00 Romania), max 20 posts/month. Separate Facebook variants (`facebook/`) and TikTok-USA variants (`tiktok-usa/`) + txt; Sorin posts those manually.

## 6. Answering people (community)
- **Quora** (extension): daily playbook `weekly/extension-playbook.md` – 2 recent questions/day, link only in one, no affiliate links, facts only from our guide. Log URLs in `weekly/log.md`.
- **Medium** (extension): 1 import/week via medium.com/p/import (canonical kept), disclosure line, 5 tags (add topics one at a time, clicking the suggestion), remove "| Curio & Cove" from titles, rebuild tables as text, fix sentences whose bold links were dropped; 2 thoughtful responses on others' stories (no links).
- **Reddit** (Composio, once connected): weeks 1–3 only helpful comments, no links (r/travel, r/solotravel, r/digitalnomad, r/TravelHacks, r/Newsletters, r/sidehustle); read `REDDIT_GET_SUBREDDIT_RULES` first; later a link only where allowed and directly answering. Respect rate limits.
- **Travel Stack Exchange, Indie Hackers** (extension): complete answers, disclose the site is ours.
- **Facebook groups**: prepare 3–5 answers/week for Sorin to post from his personal profile.
- Public posts need Sorin's OK; he may give a standing OK for a named routine – note it in the status doc.

## 7. Mail and affiliates
- Read both inboxes weekly (niros via Composio `GMAIL_FETCH_EMAILS` + body decode; conect.media via Gmail tools): approvals, rejections, payouts, terms changes, new offers. Update the affiliate doc.
- Apply to programs with the extension using hello@curioandcove.com and the texts in `claude/aplicari-afiliere-2026-10-17.md`. Never create accounts, enter passwords, payment/bank/tax data, or accept terms without Sorin's explicit OK.
- Reapply dates: Booking/BBC Maestro/Proton from 15 Nov 2026; PartnerStack Network ~Dec 2026; MailerLite with the hello@ address.
- No get-rich-quick, MLM, crypto, supplements, gambling or dating offers.

## 8. Reporting
- End of each session: update/write `claude/curioandcove-status-YYYY-MM-DD.md` (done / waiting on Sorin / next), the weekly log, and the affiliate doc if links changed.
- Weekly report to Sorin (Romanian): Pinterest views and pins, Metricool reels, Search Console clicks/impressions/top movers, Quora/Medium/Reddit activity, mail news, next 3 actions.
- Ask before anything expensive or irreversible; otherwise proceed and report.

## 9. Improving this skill (keep it alive)
- `tools/skill/IMPROVEMENTS.md` in the repo is the running log. After every session append, dated: what failed, the fix, new links/IDs, new channels, Sorin's new decisions or preferences. Read it at start; it wins over sections 1–8 when they conflict.
- When the log has 3+ substantial changes, or Sorin asks, rewrite this SKILL.md with the changes merged in (bump the version in the title), copy it to `tools/skill/SKILL.md`, and offer it to Sorin as an update with propose_skills (kind: improvement, target: curioandcove-growth). Clear merged items from the log.
- Open ideas to try (move to the sections above once proven): Bluesky/Threads replies to fresh questions; Pinterest idea pins/video pins from reels; a Kit welcome sequence + monthly newsletter; Travel Stack Exchange; YouTube channel rename; 4travel.pro intent pages; JVZoo/Digistore24/CloudTraffic offers; dedicated Curio & Cove social accounts; weekly analytics dashboard.