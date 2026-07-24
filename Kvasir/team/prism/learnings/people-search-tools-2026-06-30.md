# PRISM Learning Report: People-Search & OSINT Tools
**Date:** 2026-06-30
**Analyst:** PRISM

---

## Table of Contents
1. [Tool Studies](#tool-studies)
   - [Sherlock](#1-sherlock)
   - [Maigret](#2-maigret)
   - [GHunt](#3-ghunt)
   - [Osintgram](#4-osintgram)
   - [PhoneInfoga](#5-phoneinfoga)
   - [PimEyes](#6-pimeyes)
   - [Epieos](#7-epieos)
   - [WhatsMyName](#8-whatsmyname)
2. [Tool Comparison Matrix](#tool-comparison-matrix)
3. [Person Investigation Playbook](#person-investigation-playbook)

---

# Tool Studies

## 1. Sherlock

### What It Is
Sherlock is the most well-known open-source username search tool (85K+ GitHub stars). It hunts for social media accounts by searching a single username across **400+ websites and social networks**. Written in Python (97.3%), MIT licensed.

### How to Install
```bash
pipx install sherlock-project    # Recommended
pip install sherlock-project     # Alternative
docker run -it --rm sherlock/sherlock  # Docker
```

### How to Use
```bash
# Basic search
sherlock username

# Multiple usernames
sherlock user1 user2 user3

# Output formats
sherlock username --csv          # CSV export
sherlock username --xlsx         # Excel export
sherlock username --txt          # Text file

# Filtering
sherlock username --site Instagram --site GitHub   # Specific sites only
sherlock username --nsfw                            # Include adult sites
sherlock username --timeout 30                      # Custom timeout

# Proxy support
sherlock username --proxy socks5://127.0.0.1:9050

# Browse results
sherlock username --browse      # Open all found profiles in browser

# Print all results (including not found)
sherlock username --print-all
```

### What We Can Find
- Accounts on 400+ platforms across categories:
  - Social media: Instagram, Twitter/X, TikTok, Reddit, LinkedIn
  - Developer: GitHub, GitLab, HackerOne, Bugcrowd
  - Gaming: Steam, Xbox, PlayStation, Epic Games
  - Messaging: Telegram, Discord, Signal
  - Video: YouTube, Twitch, Vimeo
  - Creative: SoundCloud, DeviantArt, Behance
  - Dating: Badoo, OKCupid
  - Regional: Weibo, VK, Habr
- Profile URLs for each found account

### Limitations
- Only checks if a username *exists* — extracts no profile content
- 400+ sites, but not 3000+ (Maigret covers more)
- Community packages for ParrotOS and Ubuntu 24.04 are broken
- HTTP-response dependent — site changes break detection
- No recursive search or cross-referencing between found accounts
- No AI analysis or report generation beyond simple lists
- False positives possible with `--ignore-exclusions`

### Key Takeaways
- Good for **first pass** — fast, simple, covers the major platforms
- Best used as a quick reconnaissance tool before deeper investigation
- The `--browse` flag is useful to immediately inspect found profiles

---

## 2. Maigret

### What It Is
Maigret is Sherlock's more powerful successor (33K+ GitHub stars). It searches **3,000+ sites** and extracts available profile information using the socid_extractor library. Written in Python, MIT licensed. Supports recursive search, tag filtering, AI analysis, and multiple report formats.

### How to Install
```bash
pip3 install maigret            # Requires Python >= 3.10
pip3 install maigret[pdf]       # With PDF support
docker run soxoj/maigret:latest username --html   # Docker CLI
docker run -p 5000:5000 soxoj/maigret:web         # Docker web UI
```

### How to Use
```bash
# Basic search (scans top 500 sites by default)
maigret username

# Full scan (all 3000+ sites)
maigret username -a

# Report generation
maigret username --html         # Interactive HTML report
maigret username --pdf          # PDF report
maigret username --csv          # CSV
maigret username --xmind        # XMind mind map

# Tag filtering
maigret username --tags photo,dating   # Sites by category
maigret username --tags us              # US-focused sites

# Recursive/advanced
maigret username --parse URL               # Extract usernames from a profile page
maigret user1 user2 user3 -a               # Multi-user full scan
maigret username --keywords python rust     # Highlight keyword matches

# AI analysis
export OPENAI_API_KEY=sk-...
maigret username --ai

# Proxy
maigret username --proxy socks5://127.0.0.1:9050
maigret username --tor-proxy socks5://127.0.0.1:9050

# Interactive web mode
maigret --web 5000

# Permute username variants from name
maigret --permute "john doe"
```

### What We Can Find
- Accounts on **3,000+ sites** (default run checks top 500)
- Extracted profile info: name, bio, photo, location, links to other accounts
- Connected usernames and IDs via recursive search
- Tag-filtered results by category (social, dating, dev, shopping, etc.)
- Keyword-highlighted matches
- AI-generated investigation summary (with API key)

### Limitations
- Cloudflare bypass is experimental/unstable
- PDF reports require system graphics libraries
- Some sites break over time — active maintenance required
- AI analysis only works with OpenAI-compatible API key
- Does not manage Tor/I2P daemons — must run separately
- Full 3000+ scan is slower than Sherlock's 400 site scan
- Commercial version (5000+ sites, API) is a paid product

### Key Takeaways
- **Best username search tool available** for depth (3000+ sites)
- The recursive search and profile info extraction are game-changers
- Multiple output formats (HTML, PDF, XMind, graph) are ideal for reporting
- Web UI mode makes it accessible to non-technical investigators
- The `--permute` feature generates variations like "johndoe", "john_doe", etc.

---

## 3. GHunt

### What It Is
GHunt is an offensive Google framework that queries Google's internal (but publicly accessible) APIs to gather intelligence from a single identifier like an email address. Written in Python, AGPL v3 licensed. Requires authentication via the GHunt Companion browser extension.

### How to Install
```bash
pipx install ghunt             # Recommended
pip install ghunt              # For library use
```

### Setup & Authentication
```bash
ghunt login                    # One-time setup, provides 3 auth methods
```
Auth methods:
1. **Companion mode** — browser extension sends cookies to GHunt
2. **Paste base64** — copy cookies from extension as encoded text
3. **Manual entry** — enter all cookies by hand

### Modules & Usage

| Module | Input | Output |
|--------|-------|--------|
| `email` | Gmail address | GAIA ID, YouTube channel, Google Photos, Maps review patterns, device model/firmware, activated services |
| `gaia` | GAIA ID | Reverse-lookup to recover linked Gmail and associated Google services |
| `drive` | Google Drive URL | Metadata: owner name, GAIA ID, timestamps, revision count, permissions |
| `geolocate` | Wi-Fi BSSID | Approximate physical coordinates (no API key needed) |
| `spiderdal` | URL/package name | Android apps/assets tied to a target via Digital Asset Links |

```bash
# Email intelligence
ghunt email target@gmail.com
ghunt email target@gmail.com --json report.json

# GAIA ID lookup (reverse email search)
ghunt gaia 12345678901234567890

# Drive file metadata
ghunt drive https://drive.google.com/file/d/ABC123/view

# Geolocate a Wi-Fi network
ghunt geolocate 00:11:22:33:44:55

# Discover linked assets
ghunt spiderdal https://example.com
```

### What We Can Find
From a single Gmail address:
- **GAIA ID** (Google's internal, persistent user identifier)
- **YouTube channel** (handle, subscriber count, content)
- **Google Photos** (public albums, potential geo-tags)
- **Google Maps reviews** (count, ratings histogram, potential location patterns)
- **Device info** (model, firmware version)
- **Activated Google services**
- **Profile picture** (via GAIA endpoint)

### Limitations
- **No longer returns the account holder's real name** (Google hardened this in 2024)
- Requires valid authenticated Google session — tokens expire
- Companion browser extension not compatible with Docker
- Google may detect and block suspicious API access patterns
- Only works within Google's ecosystem — no cross-platform search
- Requires Python >= 3.10 (3.13+ supported)

### Key Takeaways
- **Essential for Google-specific investigations** — no other tool does this
- The GAIA ID is a persistent identifier that can link accounts across Google services
- Maps review patterns can reveal location history and travel habits
- Works best when combined with other tools for a complete picture
- The online version at osint.industries is useful for quick checks

---

## 4. Osintgram

### What It Is
Osintgram is a dedicated Instagram OSINT tool that provides an interactive shell for collecting and analyzing data from any public Instagram account. Written in Python, GPL-3.0 licensed. Connects via Instagram's private API.

### How to Install
```bash
git clone https://github.com/Datalux/Osintgram.git
cd Osintgram
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# Edit config/credentials.ini with Instagram credentials or HikerAPI token
```

### How to Use
```bash
# Interactive shell
python3 main.py target_username

# Direct command
python3 main.py target_username --command info

# With HikerAPI token
HIKERAPI_TOKEN=token python3 main.py target_username -c followers
```

### Available Commands

| Command | What It Extracts |
|---------|-----------------|
| `info` | General profile information |
| `photos` | Download all user photos |
| `propic` | Download profile picture |
| `stories` | Download user's stories |
| `followers` | List of followers |
| `followings` | List of accounts the target follows |
| `comments` | Comment counts |
| `likes` | Like counts |
| `captions` | Photo captions |
| `hashtags` | Hashtags used |
| `photodes` | Photo descriptions |
| `mediatype` | Photo vs video classification |
| `tagged` | Users the target tagged |
| `wcommented` | Users who commented |
| `wtagged` | Users who tagged the target |
| `addrs` | Addresses embedded in photo metadata |
| `fwersemail` | Emails of followers |
| `fwingsemail` | Emails of followings |
| `fwersnumber` | Phone numbers of followers |
| `fwingsnumber` | Phone numbers of followings |

### What We Can Find
- Full profile metadata (bio, followers count, following count, posts count)
- All public photos and their metadata (including EXIF geo-location via `addrs`)
- Follower/following lists (can be used for network analysis)
- Email addresses and phone numbers scraped from follower profiles
- Engagement patterns (likes, comments per post)
- Hashtag usage patterns
- Tagged user network

### Limitations
- **Cannot access private profiles** — Instagram's biggest OSINT barrier
- Using personal Instagram account risks ban ("do not use your primary account")
- Instagram's `challenge_required` error requires manual intervention
- API rate limits apply
- Requires Instagram credentials or paid HikerAPI subscription
- Depends on `instagram_private_api` library which can break when Instagram updates
- Last stable release (v1.3) was May 2021 — may have compatibility issues

### Key Takeaways
- **The best Instagram-specific OSINT tool** available
- Critical for mapping social networks (followers/followings analysis)
- EXIF geo-data extraction is powerful for location-based investigation
- Use a dedicated burner Instagram account, never a personal one
- Combine with Sherlock/Maigret for cross-platform username correlation

---

## 5. PhoneInfoga

### What It Is
PhoneInfoga is an advanced OSINT framework for international phone number intelligence. Originally Python, rewritten in Go (v2). 16.8K GitHub stars, GPL-3.0 licensed. **Current status: stable but unmaintained** — the repository may be archived.

### How to Install
```bash
# v2 (Go) — runs as a web service
docker run sundowndev/phoneinfoga serve --port 5000
# Or download binary from releases

# v1 (Python legacy)
git clone https://github.com/sundowndev/phoneinfoga.git
cd phoneinfoga && git checkout v1.11
pip install -r requirements.txt
python3 phoneinfoga.py -n "+15556661212"
```

### How to Use
```bash
# v2: Start the server
phoneinfoga serve --port 5000
phoneinfoga serve --disable numverify   # Skip a scanner

# v2: REST API
curl -X POST http://localhost:5000/api/v2/numbers \
  -H "Content-Type: application/json" \
  -d '{"number": "+15556661212"}'

# v1: CLI (legacy)
python3 phoneinfoga.py -n "+442071838750"
python3 phoneinfoga.py -n "+42837544833" -s ovh      # Specific scanner
python3 phoneinfoga.py -n "+42837544833" -s all --osint  # Full OSINT
python3 phoneinfoga.py -i numbers.txt -o results.txt     # Batch scan
```

### Scanners

| Scanner | What It Does | API Key Needed? |
|---------|-------------|:---:|
| Local | Parses number, extracts country, carrier, E164 format | No |
| Numverify | Validates existence, returns line type (mobile/landline/VoIP), carrier | Yes |
| OVH | Checks if number is owned by OVH Telecom (EU focus) | No |
| Google Search | Generates Google dork search URLs for footprints/reputation | No |
| Google CSE | Programmatic Google Custom Search Engine | Yes |

### What We Can Find
- Number validation (does this number exist?)
- Geographic origin (country, area code)
- Carrier information
- Line type (mobile vs landline vs VoIP)
- OVH Telecom ownership check
- Google dork links for social media, reputation reports, scam databases
- Connected online accounts (via Google search)

### Limitations
- **Stable but unmaintained** — bugs won't be fixed
- v2 no longer automatically scrapes Google results (generates links instead)
- Cloudflare and CAPTCHA block automated searches
- Numverify and Google CSE require paid API keys
- No real-time location tracking or phone hacking (explicitly states this)
- Doesn't claim to provide verified data
- Primarily a passive information-gathering tool
- Most powerful features require paid API subscriptions

### Key Takeaways
- Good for **initial phone number validation** (country, carrier, line type)
- The Google dork generation is useful even without paid APIs
- Best results come from combining with Google dork searches manually
- Consider this a starting point, not a complete solution for phone number intel
- For serious phone OSINT, budget for Numverify or similar paid API access

---

## 6. PimEyes

### What It Is
PimEyes is a commercial reverse face search engine. It uses facial recognition to find where a person's face appears across the open web. A controversial and powerful tool described by the BBC as "facial recognition on steroids."

### How It Works
1. Upload a photo containing a face
2. PimEyes scans the open web for matching faces
3. Results show websites and images where that face appears
4. **Excludes social media and video platforms** by design

### Pricing Tiers

| Tier | Features |
|------|----------|
| Free | Search only — cannot view source URLs |
| Open Plus (~$29.99/mo) | View source website URLs, set alerts |
| PROtect | All features + photo erasure request |
| OSINT by PimEyes | Institutional product for law enforcement/intelligence |

### What We Can Find
- All publicly indexed photos of a person on the open web
- Websites where the person's face appears (blogs, news, forums, etc.)
- Different photos of the same person (different backgrounds, angles, with other people)
- Cross-referencing faces across multiple contextually unrelated sites
- Pattern of life (where has this person been photographed?)
- Associates (who else appears in the same photos)

### Limitations
- **Does not search social media** (Facebook, Instagram, Twitter, TikTok, etc.)
- **Does not search video platforms** (YouTube, etc.)
- Paid subscription required to see source URLs (the most valuable information)
- Opt-out is irreversible and requires identity proof
- Ethics/legal concerns around facial recognition use
- Results limited to what search engines have indexed
- Cannot guarantee current accuracy — may return outdated results
- Premium pricing for the OSINT tier is enterprise-level

### Key Takeaways
- **The most powerful face search tool** for the open web
- Critical for discovering a person's presence on sites they didn't expect to be found
- Use for: finding impersonation, verifying identity, locating witness sources
- Must be combined with social media search tools for complete coverage
- Budget for Open Plus subscription if this is a regular investigation need
- Be aware of legal and ethical restrictions in your jurisdiction

---

## 7. Epieos

### What It Is
Epieos is a free (with premium tiers) OSINT tool for reverse email and phone number lookup. It checks an email address across **140+ websites and social networks** without alerting the target. Also offers Google account intelligence.

### How It Works (Web Interface)
1. Go to https://epieos.com
2. Enter an email address or phone number
3. Epieos quietly checks 140+ platforms for linked accounts
4. Results show which platforms the email/phone is registered on

### Key Features

| Feature | Description |
|---------|-------------|
| Reverse Email Lookup | Check email across 140+ sites without notifying target |
| Phone Number Lookup | Identify services linked to a phone number |
| Google Account Intel | Retrieve Google Account ID, profile photo, Maps review activity |
| Data Breach Detection | Check if email appears in known breaches |
| Cross-Platform Correlation | Build identity profile across services |
| Maltego Integration | Available as a Transform Hub module |

### What We Can Find
- Social media accounts linked to an email (Google, Skype, Facebook, LinkedIn, etc.)
- Platform registrations (GitHub, Duolingo, Pinterest, Strava, Fitbit, Nike, Etsy, Flickr, etc.)
- Google Account ID + approximate profile photo
- Google Maps review history and patterns
- Data breach history for the email
- Phone number linked accounts and services

### Limitations
- Primarily email-centric — phone lookup may require premium
- Provides data points/fragments, not comprehensive identity reports
- Assumes OSINT knowledge — not beginner-friendly
- Limited customer support
- Results depend on platform cooperation and may miss some accounts
- 140+ sites is good but less than Maigret's 3000+ username search
- Free tier may have result limits

### Key Takeaways
- **Excellent for "what is this email used for?"** investigations
- The Google Account ID extraction is powerful — feeds into GHunt's gaia module
- Silent checking (no target notification) is critical for covert investigations
- Maltego integration makes it usable in professional investigation workflows
- Use free tier for quick checks, premium for deeper phone lookups

---

## 8. WhatsMyName

### What It Is
WhatsMyName is a free, open-source username enumeration tool that checks a username across **1,000+ websites and platforms**. Created by OSINT Combine (Chris Poulter) and Micah "WebBreacher" Hoffman. Available as a web app, Python CLI, and Chrome extension.

### How to Use

**Web Interface:**
```
https://whatsmyname.app/?q=USERNAME
```

**Python CLI:**
```bash
git clone https://github.com/WebBreacher/WhatsMyName.git
cd WhatsMyName
python3 web_accounts_list_checker.py -u username
python3 web_accounts_list_checker.py -u username -c social     # Category filter
python3 web_accounts_list_checker.py -u username --format csv  # CSV export
```

**Chrome Extension:**
- Install from Chrome Web Store
- Browse any page, click extension to check if the current site has a username search

### What We Can Find
- Profile presence across 1,000+ platforms
- Category-filtered results (social, dating, shopping, business, dev, etc.)
- Direct profile URLs
- CSV/JSON exportable results

### Limitations
- Requires cookies; CAPTCHA appears after each search
- Covers 1,000+ platforms but not all (Facebook and Instagram notably excluded)
- False positives possible — "found" result may lead to "page does not exist"
- Same username ≠ same person — multiple people can share a username
- Not as many sites as Maigret (3000+), but more than Sherlock (400+)

### Key Takeaways
- **Good middle ground** between Sherlock (fast, fewer sites) and Maigret (deeper, slower)
- The Chrome extension is unique — useful for live browsing investigations
- Used by major OSINT platforms (Spiderfoot, Recon-ng, sn0int, Blackbird)
- Category filtering helps narrow results to relevant platforms
- The JSON data file is used by multiple other tools — contributes to the OSINT ecosystem

---

# Tool Comparison Matrix

| Tool | Input | Sites/Scope | Free? | Output Formats | Best For | Limitations |
|------|-------|-------------|:-----:|----------------|----------|-------------|
| **Sherlock** | Username | 400+ sites | Yes | TXT, CSV, XLSX | Quick first pass | No profile data extraction |
| **Maigret** | Username | 3000+ sites | Yes | HTML, PDF, CSV, XMind, Graph, Neo4j | Deep username investigation | Slower, Cloudflare bypass experimental |
| **GHunt** | Email/GAIA ID | Google ecosystem | Yes | JSON, CLI | Google account intelligence | Requires auth session, real name blocked |
| **Osintgram** | Instagram username | Instagram only | Yes | CLI, downloaded media | Instagram analysis | Private profiles blocked, needs IG credentials |
| **PhoneInfoga** | Phone number | Phone databases | Yes | CLI, API, Web UI | Phone number intel | Unmaintained, most features need paid APIs |
| **PimEyes** | Photo | Open web | Freemium | Web | Reverse face search | Excludes social media, paid to see results |
| **Epieos** | Email/Phone | 140+ platforms | Freemium | Web, Maltego | Email-platform correlation | Email-centric, technical interface |
| **WhatsMyName** | Username | 1000+ sites | Yes | CSV, JSON, Web | Quick web-based search | CAPTCHA after each search |

---

# Person Investigation Playbook

## Phase 1: Initial Reconnaissance
**Goal:** Gather every known identifier and start surface mapping.

### Step 1: Collect All Known Identifiers
The more identifiers you have, the more you can cross-reference:
- Full name (including middle names, maiden names, aliases)
- Usernames (across any known platforms)
- Email addresses (all known variants)
- Phone numbers (international format)
- Physical addresses (past and present)
- Photos of the person
- URLs (personal websites, social profiles, business pages)
- Dates of birth
- Employer/school information

### Step 2: Username Search — Broad Sweep
```bash
# First pass — fast, broad
sherlock username --csv --output sherlock_results.csv

# Second pass — deep, thorough
maigret username -a --html --output maigret_report.html

# Third pass — alternative DB check via web
# Browse to: https://whatsmyname.app/?q=USERNAME
```

**Analyze results:** Create a table of every platform where the username exists. Note which platforms are likely real vs. auto-created or abandoned.

### Step 3: Email Address Search
```
# Use Epieos (web) to check 140+ platforms
# URL: https://epieos.com

# If Gmail, run GHunt
ghunt email target@gmail.com --json ghunt_results.json
```

**Analyze results:**
- What platforms is this email registered on?
- Is there a Google Account? If so, what's the GAIA ID?
- Are there Google Photos, YouTube channels, Maps reviews?
- Check HaveIBeenPwned for breach history (password reuse risk)

### Step 4: Phone Number Search
```
# PhoneInfoga — basic validation
phoneinfoga serve --port 5000
# Then via API or check Google dork URLs generated

# Epieos phone lookup
# URL: https://epieos.com
```

**Analyze results:**
- Country and carrier (is it a burner? prepaid? VoIP?)
- Is the number on OVH Telecom?
- What platforms are linked to this number?
- Any scam/reputation reports?

---

## Phase 2: Social Media Deep Dive
**Goal:** Extract all available information from discovered social media profiles.

### Step 5: Instagram Analysis
If an Instagram account was found:
```bash
# Use a BURNER account (never your personal one)
python3 main.py target_username

# In interactive shell, run these commands:
info         # Profile metadata
followers    # Follower list — network mapping
followings   # Following list — interests, associations
photos       # Download all photos
addrs        # EXIF geo-location data
hashtags     # Interest/movement tracking
captions     # Writing style, relationships, activities
```

### Step 6: Google Account Deep Dive
If a Gmail or GAIA ID was found:
```bash
ghunt email target@gmail.com
ghunt gaia GAIA_ID
ghunt drive https://drive.google.com/...  # If drive links found
```

**What to look for:**
- YouTube channel activity (content, comments, subscriptions)
- Google Maps reviews (location history, travel patterns)
- Google Photos (public albums, people tagged)
- Device model (what device do they use?)

### Step 7: Cross-Platform Correlation
```bash
# Maigret recursive search using discovered usernames
maigret username2 -a --html
maigret username3 -a --html

# Parse a discovered profile URL to extract more usernames
maigret --parse https://example.com/profile/someuser
```

**Create an identity graph:**
- Link all discovered profiles to the same person
- Note any unique identifiers shared across platforms (same bio text, same profile photo, same naming pattern)

---

## Phase 3: Visual & Biometric Search
**Goal:** Find the person's face and image footprint across the web.

### Step 8: Reverse Face Search
```
1. Go to https://pimeyes.com
2. Upload the best available photo of the target
3. Review results (requires Open Plus subscription to see source URLs)
4. Note every site where the face appears
5. Set alerts for ongoing monitoring
```

**For each photo found:**
- What context is the photo in? (News article, forum post, company page?)
- Who else appears in the photo?
- What does the background reveal? (Location, event, time period?)
- Is the photo being used with permission? (Impersonation risk)

**If PimEyes is unavailable or insufficient:**
- Google Images reverse image search
- Yandex Images reverse search (often better for Eastern Europe/Asia)
- TinEye reverse image search

---

## Phase 4: Relationship & Network Mapping
**Goal:** Map the person's connections, affiliations, and patterns.

### Step 9: Follower/Following Network Analysis
From Instagram (Osintgram):
```
followers   > output/followers.txt
followings  > output/followings.txt
```

**Technique:** Export followers list, then run those usernames through Sherlock/Maigret to find cross-platform linked accounts. Look for:
- High-value connections (influencers, employers, family members)
- Unusual connections (criminal associations, competing interests)
- Bot/fake follower ratio (indicator of paid followers)

### Step 10: Digital Asset Discovery
```bash
# Check if the person has a domain or app
ghunt spiderdal https://target-personal-website.com

# Google Dorking for the person
site:linkedin.com/in "full name" "company"
site:facebook.com "full name" "city"
"email@example.com" filetype:pdf
```

### Step 11: Data Breach & Password Analysis
- Check breach databases (HaveIBeenPwned, DeHashed, IntelX)
- If email appears in breaches, note the breached platform
- Cross-reference passwords (never crack — just note reuse patterns across platforms)
- Check for pastebin/discord leaks mentioning the email or username

---

## Phase 5: Compilation & Reporting
**Goal:** Create a complete dossier of findings.

### Step 12: Generate Reports
```bash
# Maigret HTML report (most comprehensive)
maigret username -a --html

# Maigret PDF report
maigret username -a --pdf

# Maigret interactive graph
maigret username --graph

# Export all GHunt data
ghunt email target@gmail.com --json ghunt_full.json
```

### Step 13: Dossier Structure
Organize findings in a standardized format:

```
PERSON INVESTIGATION DOSSIER
===========================
Subject: [Full Name]
Also known as: [Aliases, usernames]

IDENTIFIERS
- Emails: [...]
- Phones: [...]
- Usernames: [...]
- GAIA IDs: [...]

SOCIAL MEDIA PRESENCE
- Instagram: [link], [findings summary]
- Twitter/X: [link], [findings summary]
- LinkedIn: [link], [findings summary]
- YouTube: [link], [findings summary]
- Others: [list]

GOOGLE ECOSYSTEM
- Google Account: [GAIA ID, profile photo]
- YouTube channel: [handle, subscribers]
- Google Photos: [albums found]
- Maps activity: [review count, patterns]

PHOTO FOOTPRINT
- PimEyes results: [count of matches]
- Key photos: [description, context, source]

NETWORK
- Notable followers/followings: [list]
- Associations: [people/groups connected]
- Employers: [...]
- Education: [...]

PATTERNS
- Writing style: [...]
- Activity times: [...]
- Geographic patterns: [...]
- Interests: [...]

BREACH/EXPOSURE HISTORY
- Known breaches: [...]
- Exposed data: [...]

RISK ASSESSMENT
- OpSec level: [Low/Medium/High]
- Notable risks: [...]
```

---

## Operational Security (OpSec) Guidelines

### For the Investigator
1. **Use a dedicated investigation machine** — VM or separate OS, never your daily driver
2. **VPN + Tor** — Route all traffic through VPN, use Tor for sensitive queries
3. **Burner accounts** — Never use personal accounts for social media OSINT
4. **No target notification** — Never "friend request" or interact unless absolutely necessary
5. **Log everything** — Timestamp every action, save all raw output
6. **Clean environment** — Clear cookies, cache, and localStorage between sessions
7. **Isolated browser** — Use a separate browser profile or container for investigations

### Legal & Ethical Boundaries
- This playbook is for **legal and ethical investigations only**
- Do not access private/restricted content without authorization
- Do not attempt to crack passwords, hack accounts, or perform DoS
- Respect privacy laws in your jurisdiction (GDPR, PIPEDA, etc.)
- Document your legal basis for the investigation
- Be aware that some tools (PimEyes, GHunt) may have usage restrictions

---

## Quick Reference: Recommended Investigation Flow

```
1. Collect identifiers
        |
2. Sherlock / Maigret (username sweep)
        |
3. Epieos (email-platform check)
        |
4. GHunt (Google ecosystem)
        |
5. PhoneInfoga (phone number)
        |
6. Osintgram (if Instagram found)
        |
7. PimEyes (face search)
        |
8. Relationship mapping
        |
9. Breach data check
        |
10. Compile dossier
```

---

## Tool Selection Guide

| Situation | Recommended Tool(s) |
|-----------|-------------------|
| "I have a username" | Maigret (primary), Sherlock (secondary), WhatsMyName (web check) |
| "I have an email" | Epieos (broad check), GHunt (if Gmail) |
| "I have a phone number" | PhoneInfoga, Epieos phone lookup |
| "I have a photo" | PimEyes, Google Images, Yandex Images |
| "I have an Instagram handle" | Osintgram |
| "I need a quick check" | WhatsMyName web app |
| "I need a formal report" | Maigret (HTML/PDF) + GHunt JSON |
| "I need network analysis" | Osintgram (followers/followings) + Maigret recursive |

---

*End of Report — PRISM OSINT Research Team*
