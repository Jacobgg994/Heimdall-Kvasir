# SCOPE Deep Dive: Advanced OSINT Tools & Platforms
**Date**: 2026-06-30
**Analyst**: SCOPE 🔬
**Classification**: TEAM INTERNAL

---

## Table of Contents

1. [DeepDive — Autonomous 3D Investigation Graph](#1-deepdive)
2. [OnionClaw — AI Agent Tor Access & Dark Web Search](#2-onionclaw)
3. [Leaker — Passive Leak Enumeration](#3-leaker)
4. [The Collector — Advanced Web Crawler with Tor Stealth](#4-the-collector)
5. [OSINT-D2 — Agentic OSINT Profiling Platform](#5-osint-d2)
6. [Awesome OSINT Arsenal — 751+ Tools Master Catalog](#6-awesome-osint-arsenal)
7. [DeHashed.com — Breach Intelligence Search Engine](#7-dehashed)
8. [Intelligence X (IntelX.io) — Dark Web & Leak Search Engine](#8-intelx)
9. [GeoSpy.ai — AI Visual Geolocation Intelligence](#9-geospy)
10. [Master OSINT Workflow: Unified Pipeline](#10-master-workflow)

---

## 1. DeepDive — Autonomous 3D Investigation Graph

### What It Is
DeepDive is an autonomous OSINT investigation tool that constructs **interactive 3D relationship graphs** from a single seed subject (name, company, or event). It runs simultaneous searches across multiple angles, extracts entities (people, organizations, locations, financial flows, events), and builds a live graph that expands automatically. A persistent AI agent lives inside the graph interface and answers questions about findings.

**Creator**: Sinndarkblade (unmaintained after personal tragedy — released to public under MIT)
**Language**: Python 81%, JavaScript 9%, CSS 7%, HTML 2%
**License**: MIT

### Installation
```bash
git clone https://github.com/Sinndarkblade/deepdive
cd deepdive
pip install -r requirements.txt
python3 server/app.py
```
Web UI opens at `http://localhost:8766/board`, settings at `http://localhost:8766/settings`. No build step required — frontend runs directly from filesystem.

### Key Features

| Feature | Description |
|---|---|
| **3D Force-Directed Graph** | Rotate, zoom, collapse branches, focus nodes |
| **Timeline View** | All dated events arranged chronologically |
| **Sankey Money Flow** | Financial connections visualized |
| **Persistent AI Chat Agent** | Embedded in board, aware of graph state |
| **Multi-Provider AI** | OpenAI, DeepSeek, Groq, Anthropic, local Ollama |
| **Search Backends** | DuckDuckGo, SearXNG, local file search |
| **Document Ingestion** | TXT, PDF, CSV, JSON, HTML, MD, XML |
| **HTML Report Generation** | Print-to-PDF capability |
| **Obsidian Export** | Entities become notes with wiki-links |
| **Cross-Investigation Linking** | Fuzzy name matching across cases |
| **7 Glass Themes** | Aero, Dark, Emerald, Violet, Crimson, Amber, Midnight |
| **CLI Skill** | `/deepdive [subject]` for Claude Code/OpenClaw |
| **Plugin System** | Custom search sources, tools, and AI prompts |

### AI Provider Advice
- **DeepSeek** (`deepseek-chat`): "Best value — comparable to GPT-4 on investigative tasks at fraction of cost"
- **OpenAI** (`gpt-4o`): "Best general coverage"
- **Anthropic** (`claude-3-5-sonnet`): "Strong on complex multi-hop reasoning"
- **Local Ollama**: "Quality varies, not recommended for large investigations"

### CLI Commands (via skill)
```
/deepdive Ghislaine Maxwell
/deepdive expand Jeffrey Epstein
/deepdive money
/deepdive gaps
/deepdive report
```

### Team Usage Potential
- **Corporate investigations**: Map shell companies, directors, and financial flows
- **Competitive intelligence**: Graph relationships between competitors, partners, investors
- **Due diligence**: Automate background checks on entities
- **Pattern discovery**: Visualize connections humans would miss

### Pros
- Zero build pipeline, runs directly from filesystem
- Provider agnostic (cloud or local models)
- Document corpus ingestion for offline seed data
- Rich visualization: 3D graph + timeline + Sankey
- Plugin architecture for extensibility
- Cross-investigation fuzzy matching

### Cons
- **Unmaintained** — author explicitly stopped development, only 3 commits
- Extremely early-stage — maturity unproven
- No versioned releases
- Local model quality too low for serious investigations
- Desktop-only (no mobile)
- No Tor/proxy support or data encryption

---

## 2. OnionClaw — AI Agent Tor Access & Dark Web Search

### What It Is
OnionClaw gives AI agents full access to the **Tor network and .onion hidden services** through 7 core commands. It functions as an OpenClaw skill (drop-in) or standalone CLI toolkit. It queries **18 dark web search engines** simultaneously, fetches .onion pages, and performs LLM-based OSINT analysis.

**Creator**: JacobJandon (published under christinminor459)
**Language**: Python 100%
**License**: MIT

### Installation
```bash
# As OpenClaw skill (drop-in):
cp -r OnionClaw ~/.openclaw/skills/onionclaw

# Standalone:
git clone https://github.com/christinminor459/OnionClaw
cd OnionClaw
pip install requests[socks] beautifulsoup4 python-dotenv stem
cp .env.example .env
# Requires: Tor daemon running (127.0.0.1:9050)
```

### Architecture
```
User / OpenClaw Agent / CI
        |
        v
OnionClaw command layer (7 scripts + sync)
        |
        v
SICRY Engine (sicry.py — bundled)
  - Core logic: check_tor, renew, search, fetch, ask
  - SQLite DB for state (watch jobs, engine stats, result cache)
        |
        v
Tor SOCKS5 (9050) <-> Tor Control Port (9051)
        |
        v
Dark Web / Tor Network (18 search engines, .onion services)
```

### 7 Core Commands

| Command | Function |
|---|---|
| `check_tor.py` | Verify Tor connectivity, show exit IP |
| `renew.py` | Rotate Tor circuit (new exit node) |
| `check_engines.py` | Ping 18 dark web search engines, show latency |
| `search.py` | Parallel multi-engine search with dedup |
| `fetch.py` | Retrieve any .onion or clearnet URL via Tor |
| `ask.py` | LLM OSINT analysis in 4 modes |
| `pipeline.py` | End-to-end automated investigation (7 steps) |

### ask.py 4 Analysis Modes

| Mode | Focus | Extracts |
|---|---|---|
| `threat_intel` | General dark web OSINT | IoCs, infrastructure, actor mentions |
| `ransomware` | Malware/RaaS | C2 domains, hashes, MITRE ATT&CK TTPs |
| `personal_identity` | PII/breach exposure | SSNs, emails, passwords, risk severity |
| `corporate` | Corporate threat intel | Leaked credentials, source code, IAB activity |

### pipeline.py 7-Step Automated Investigation

| Step | Action | LLM Required? |
|---|---|---|
| 1 | Verify Tor is active | No |
| 2 | Check which engines are alive | No |
| 3 | Refine query to <=5 keywords | Yes (falls back gracefully) |
| 4 | Search all alive engines | No |
| 5 | Filter top 20 relevant results | Yes (falls back) |
| 6 | Batch-scrape pages concurrently | No |
| 7 | OSINT analysis and LLM report | Yes (falls back) |

### Team Usage Potential
- **Dark web monitoring**: Automate .onion forum crawling for mentions of client/company names
- **Credential leak hunting**: Search paste sites and dark web markets for exposed corp data
- **Threat actor tracking**: Monitor ransomware gang communications
- **Breach validation**: Cross-reference leaked data from surface sources on dark web
- **Identity protection**: Monitor personal PII exposure on dark markets

### Pros
- Drop-in OpenClaw integration with automatic agent discovery
- Dual-mode: standalone or agent plugin
- 18 dark web search engines with health checking
- LLM-optional — core works without any API key
- Autonomous pipeline in one command
- SQLite state management with caching
- TorPool scaling (multi-process Tor for throughput)
- Flexible LLM providers (OpenAI, Anthropic, Gemini, Ollama, llama.cpp)

### Cons
- Requires local Tor daemon configured correctly
- Circuit renewal needs extra ControlPort setup
- Dark web search engines are unstable ("Down" is common)
- No formal versioned releases
- 8,000-char content cap in fetch.py
- Keyword-sensitive search (not natural language)
- No CAPTCHA handling
- Jurisdictional risk with automated .onion access
- Dual-use concerns (same codebase enables defensive and offensive use)

---

## 3. Leaker — Passive Leak Enumeration

### What It Is
Leaker is a **Go-based passive leak enumeration tool** that queries **13 third-party leak databases** to find exposed credentials associated with a given search target. It supports email, username, domain, keyword, and phone number searches with deduplication, rate limiting, and credential verification.

**Creator**: Maksim Radaev (@vflame6)
**Language**: Go 99.8%
**License**: MIT
**Stars**: 544 | **Forks**: 78 | **Latest**: v1.6.7 (June 6, 2026)
**Releases**: 31 releases, 163 commits

### Installation
```bash
go install -v github.com/vflame6/leaker@latest
# Requires Go 1.24
# Or use Docker (Dockerfile included)
```

### 13 Integrated Data Sources

| Source | API Key | Search Types | Pricing |
|---|---|---|---|
| BreachDirectory | Yes | All (auto-detect) | Free via RapidAPI |
| DeHashed | Yes | email, username, domain, keyword, phone | Paid |
| Hudson Rock | No* | email, username, domain | Free/Paid |
| Intelligence X | Yes | All | Free tier |
| LeakCheck | Yes | email, username, domain, keyword, phone | Paid |
| LeakRadar | Yes | email, username, domain | Paid |
| Leak-Lookup | Yes | email, username, domain, keyword, phone | Paid |
| LeakSight | Yes | email, username, domain, keyword, phone | Paid |
| OSINTLeak | Yes | email, username, domain, keyword, phone | Paid |
| ProxyNova | No | All | Free |
| Snusbase | Yes | email, username, domain, keyword, phone | Paid |
| WeLeakInfo | Yes | email, username, domain, keyword, phone | Paid |
| WhiteIntel | Yes | email, username, domain | Paid |

### Key Features

| Feature | Description |
|---|---|
| **5 Search Commands** | `email`, `username`, `domain`, `keyword`, `phone` |
| **Deduplication** | Cross-source dedup (disable with `--no-deduplication`) |
| **JSONL Output** | Pipeline-friendly line-delimited JSON via `-j` |
| **Results Filtering** | Enabled by default; disable with `--no-filter` |
| **Source Metadata** | Shows source DB names via `-M` |
| **Local SQLite Cache** | Store results locally (`--db`) |
| **Credential Verification** | `-V`/`--verify` — validates via HIBP password check |
| **Rate Limiting** | Built-in per-source (disable with `-N` DANGER) |
| **HTTP Proxy** | `--proxy` flag |
| **Custom User-Agent** | `-A`/`--user-agent` |
| **Multi-Key Load Balancing** | Multiple API keys per source |
| **Source Selection** | `--sources online|all|local` or explicit names |

### Usage Examples
```bash
leaker email user@example.com
leaker username johndoe --sources "dehashed,intelx" --db leaks.db
leaker domain example.com -V -j -o results.jsonl
leaker phone +1234567890 --proxy socks5://127.0.0.1:9050
leaker keyword "company_name" --no-filter -M -v
```

### Team Usage Potential
- **Continuous credential monitoring**: Automate periodic scans of team/client emails
- **Incident response**: Check if compromised credentials appear in known breaches
- **Password reuse analysis**: Search passwords to reveal linked accounts
- **Domain exposure auditing**: Find all leaked credentials for a corporate domain
- **Phone number breach checks**: Validate if employee phone numbers are exposed

### Pros
- 13 sources aggregated in one tool
- Passive approach (queries existing databases)
- 5 search types for flexible recon
- Pipeline-friendly JSONL output
- Built-in rate limiting (reduces blocking)
- Cross-source deduplication
- HIBP credential verification
- Active development (31 releases)
- Good documentation with wiki pages

### Cons
- 11 of 13 sources require paid API keys
- Dependency on third-party services (fragile)
- Go 1.24 requirement
- Legality/ethics concerns with credential enumeration
- No offline/local breach DB support detailed
- No built-in auth for local SQLite cache

---

## 4. The Collector — Advanced Web Crawler with Tor Stealth

### What It Is
A **Python-based web crawler** designed for OSINT and red team operations. It systematically navigates target websites, collects page content, scans for specified keywords with context snippets, and stores everything in SQLite. Supports both standard reconnaissance and **anonymous Tor crawling** for .onion addresses.

**Creator**: Volkan Sah (Kucukbudak)
**Language**: Python 100%
**License**: GPLv3
**Status**: Alpha release 2025/26

### Installation
```bash
git clone https://github.com/VolkanSah/The_Collector
cd The_Collector

# Optional stealth dependencies:
pip install pysocks langdetect

# Tor required for dark web mode:
# apt install tor && tor &
```

### Key Features

| Feature | Description |
|---|---|
| **Multi-Threaded Crawling** | Configurable concurrency (`--threads`) |
| **Configurable Depth** | Link-following depth (`--depth`) |
| **Page Cap** | Limit total pages (`--max`) |
| **MD5 Duplicate Detection** | Content hashing to avoid duplicates |
| **Keyword Detection** | Search for keywords with context snippets |
| **Language Detection** | Optional (requires langdetect) |
| **SQLite Storage** | All results in portable database |
| **Tor Integration** | Routes via 127.0.0.1:9050 with `--tor` |
| **Configurable Delays** | Seconds between requests (`--delay`) |

### Usage Examples
```bash
# Standard OSINT recon
python sentinel_crawler.py --url "https://target.com" \
  --keywords "confidential" "password" "admin" \
  --db target_scan.db

# Dark web / stealth mode
python sentinel_crawler.py --url "http://exampleonion.onion" \
  --keywords "leak" "database" --tor --delay 2.0

# Deep fast scan
python sentinel_crawler.py --url "https://target.com" \
  --keywords "admin" "confidential" --depth 3 --threads 10 \
  --db scan_results.db
```

### CLI Parameters

| Flag | Purpose | Default |
|---|---|---|
| `--depth` | Max crawl depth | 2 |
| `--max` | Max pages to crawl | 100 |
| `--delay` | Seconds between requests | 1.0 |
| `--threads` | Concurrent threads | 5 |
| `--tor` | Enable Tor proxy | Off |
| `--db` | Output SQLite filename | (required) |

### Team Usage Potential
- **Target reconnaissance**: Map website structure and discover hidden pages
- **Keyword leak detection**: Scan competitors' exposed directories for confidential terms
- **Dark web monitoring**: Crawl .onion forums for mentions of client/team names
- **Attack surface mapping**: Identify exposed admin panels, config files, debug endpoints
- **Evidence preservation**: Capture page snapshots with context snippets

### Pros
- Single Python file — lightweight and portable
- SQLite storage (easy querying, no DB server needed)
- Dual-mode: surface web + anonymous dark web
- Configurable throttling (delay, depth, threads)
- MD5 deduplication
- Minimal dependencies (stdlib + optional pysocks/langdetect)
- Context snippets on keyword hits

### Cons
- **Alpha-stage software** — bugs and rough edges likely
- Single-file design (hard to maintain/extend)
- No authentication/cookie support (cannot crawl logged-in content)
- No JavaScript rendering (misses SPAs/dynamic content)
- Tor dependency is external (user manages Tor daemon)
- SQLite-only output (no JSON/CSV export)
- Static delay (no adaptive backoff on 429 responses)
- Small community (2 forks, 4 stars)

---

## 5. OSINT-D2 — Agentic OSINT Profiling Platform

### What It Is
An **LLM-driven autonomous OSINT platform** that transforms usernames and emails into structured identity dossiers. Unlike simple scripted lookups, its AI agent autonomously decides which tools to invoke and pivots across discovered identities. Produces **6-dimension cognitive profiles** with classified-style PDF reports.

**Creator**: Doble-2 (angelcalderon.dev)
**Language**: Python 93%, HTML 7%
**License**: MIT
**Stars**: 170 | **Forks**: 29 | **Latest**: v2.0.1 (June 2026)

### Installation
```bash
git clone https://github.com/Doble-2/osint-d2
cd osint-d2
poetry install
poetry run osint-d2 doctor setup-ai

# System deps for PDFs:
# Ubuntu: libcairo2 libpango-1.0-0 libpangoft2-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info
# macOS: brew install cairo pango gdk-pixbuf libffi
```

### Architecture (Hexagonal / Ports-and-Adapters)
```
src/
├── core/                          # Domain logic (framework-agnostic)
│   ├── domain/models.py           # PersonEntity, SocialProfile, AnalysisReport
│   ├── services/identity_pipeline.py
│   ├── services/agent_engine.py   # Agentic AI loop (function calling)
│   ├── services/agent_tools.py    # Tool definitions
│   └── services/trust_anchor.py   # False-positive filtering
├── adapters/                      # External integrations
│   ├── ai_analyst.py              # LLM interaction (OpenAI SDK)
│   ├── http_client.py             # Async HTTP + proxy
│   ├── sherlock_runner.py         # ~400 sites
│   ├── specific_scrapers.py       # GitHub, GitLab, Twitch, etc.
│   └── report_exporter.py         # PDF/HTML/JSON
└── cli/main.py                    # Typer commands + wizard
```

### 5 AI Agent Tools

| Tool | Function |
|---|---|
| `scan_username` | Scans 18+ social networks |
| `scan_email` | Gravatar, PGP keyservers + pivot local-part as username |
| `fetch_url` | Scrape URLs for social links, emails, phones, metadata |
| `breach_check` | HaveIBeenPwned query (requires `--breach-check`) |
| `generate_report` | Submit 6-dimension intelligence report (ends investigation) |

### 6-Dimension Cognitive Profiling

| Dimension | What It Covers |
|---|---|
| **Identity** | Real name, aliases, emails, phone numbers, demographics |
| **Geo-temporal** | Location inference, timezone, activity patterns, sleep schedule |
| **Psychological (OCEAN)** | Openness, Conscientiousness, Extraversion, Agreeableness, Neuroticism |
| **Technical/Professional** | Tech stack, seniority level, professional archetype |
| **Ideology** | Political/ethical leanings, values, cultural affiliations |
| **OpSec** | Attack surface, social engineering susceptibility, exposure risks |

### Commands

| Command | Description |
|---|---|
| `wizard` | Interactive guided workflow |
| `scan` | Lightweight username sweep (18+ networks) |
| `scan-email` | Email-centric scan with local-part pivot |
| `hunt` | Full pipeline: usernames + email + Sherlock + AI + PDF |
| `agent` | Autonomous AI investigation (LLM decides everything) |
| `analyze` | Re-run AI on previously exported JSON |
| `doctor` | Environment diagnostics, AI setup |

### AI Providers
| Preset | Model |
|---|---|
| `deepseek` | `deepseek-chat` **(recommended)** |
| `groq` | `llama-3.1-70b-versatile` |
| `groq-fast` | `llama-3.1-8b-instant` |
| `openrouter` | `openai/gpt-4o-mini` |
| `huggingface` | `meta-llama/Llama-3.1-8B-Instruct` |

### Team Usage Potential
- **Person of Interest profiling**: Full identity dossier on targets
- **Social media footprint audit**: Map all accounts across 30+ platforms
- **Phishing target assessment**: Evaluate OpSec risk for employees
- **Competitor analyst identification**: Profile individuals behind competitor LinkedIn/X accounts
- **Due diligence**: Background checks on business partners / vendors

### Pros
- Autonomous investigation (AI agent discovers and pivots)
- 6-dimension profiling goes beyond simple "what accounts exist"
- Trust anchors reduce false positives (major pain point in OSINT)
- ScrapingAnt residential proxies bypass anti-bot blocks
- Offline heuristic fallback without AI key
- 5 language support (EN, ES, PT, AR, RU)
- Classified-style PDF reports with confidence meters
- Clean hexagonal architecture (testable, extensible)
- PyInstaller portable binaries

### Cons
- AI dependency for best results (adds cost/external dependency)
- WeasyPrint native deps cause installation issues
- Proxy lock-in (ScrapingAnt only, no generic SOCKS5)
- OpenAI-compatible only (no local Ollama/llama.cpp documented)
- Social platform scraping is fragile (Instagram blocks, rate limits)
- No Docker image
- Limited email sources (Gravatar, PGP keyservers, HIBP)
- No web UI (CLI-only)
- False positives acknowledged for correlation

---

## 6. Awesome OSINT Arsenal — 751+ Tools Master Catalog

### What It Is
A **curated OSINT and recon toolkit for Kali Linux** with a one-command installer. It organizes 751+ tools across **50 categories** into shell scripts and a JSON manifest, enabling bulk or selective deployment. Not original tools — it's a deployment wrapper for existing open-source tools.

**Creator**: rawfilejson
**Language**: Shell 100%
**Stars**: 1,000 | **Forks**: 182
**Updates**: 27 commits, no versioned releases

### Structure
```
install.sh       # Central one-command installer
tools.json       # Tool manifest/metadata registry
osint.sh         # Core OSINT tools (SOCMINT, GEOINT, data gathering)
redteam.sh       # Offensive security tooling
blueteam.sh      # Defensive tooling
forensics.sh     # Digital forensics tools
hardware.sh      # Hardware investigation tools
labs.sh          # Lab/practice environment tooling
extras.sh        # Supplementary additions
termux.sh        # Android Termux installer variant
```

### Tool Category Breakdown

| Category | Count |
|---|---|
| Online Platforms | 461+ |
| CLI Tools | 165+ |
| GitHub Repos | 117+ |
| Breach Engines | 39+ |
| AI Tools | 25+ |
| Blue Team | 24+ |
| Training | 21+ |
| Red Team | 35+ |
| Forensics | 16+ |
| Dark Web | 15+ |
| Bug Bounty | 12+ |
| **Georgian OSINT Arsenal** | 500+ (country-specific) |

### 50 Categories (Condensed)

| Domain | Categories Included |
|---|---|
| **Recon & Discovery** | Username/Social OSINT, Email OSINT, Phone OSINT, Domain/IP OSINT, Geo OSINT, Image/Video OSINT, Facial Recognition, Social Media Monitoring |
| **Breaches & Leaks** | Data Breach Search Engines, WikiLeaks/DDoSecrets, Password Cracking |
| **Dark Web & Privacy** | Dark Web Search Engines, Anonymous Tools |
| **Offensive Security** | Web App OSINT, Social Engineering, Vuln Scanning, Network Tools, Mobile Hacking |
| **Intelligence** | AI-Powered OSINT, Financial Intelligence, Vehicle/Property Records, Metadata Forensics |
| **Surveillance** | IP Camera OSINT, Google Dorking, Credential Dorking, IP Tracking |
| **Community** | Telegram OSINT Bots, Russian OSINT Services, Social Media Searcher Platforms |
| **Toolkits** | Termux Hacking, Kali Linux Toolkit, All-in-One Frameworks, Wordlist Generation |
| **Hardware & OS** | Hardware Hacking, OSINT Operating Systems |
| **Developer** | OSINT APIs, Browser Extensions, Learning Resources, Awesome Lists |
| **Red & Blue** | Red Team, Blue Team, Threat Intel Platforms |
| **Forensics & Training** | Digital Forensics, CTF Platforms, Bug Bounty, Training Labs |
| **Country-Specific** | Georgian OSINT Arsenal (500+ tools) |

### Team Usage Potential
- **Tool discovery**: Find the right tool for any OSINT task across 50 categories
- **Quick deployment**: One-command install of entire OSINT stack on Kali
- **Reference catalog**: Use tools.json as searchable inventory
- **Termux mobile ops**: Android OSINT toolkit via termux.sh
- **Training setup**: Rapidly provision learning environments from labs.sh

### Pros
- Largest curated OSINT collection (751+ tools)
- 50 categories cover entire OSINT spectrum
- One-command installer (install.sh)
- Category-specific scripts for selective installs
- Termux support for mobile OSINT
- tools.json enables programmatic access
- 1,000 stars indicates community validation

### Cons
- **Kali Linux only** (not cross-platform)
- No versioned releases
- Not original tools — wrapper/deployment only
- License not stated on main page
- 27 commits suggests limited maintenance activity
- Quality varies across 751 tools (no curation filter)
- Georgian OSINT section is highly niche

---

## 7. DeHashed.com — Breach Intelligence Search Engine

### What It Is
DeHashed is a **credential intelligence and OSINT search engine** that aggregates data from thousands of compromised databases. It enables searching across **24+ billion records** from **24,000+ data sources** with multi-field queries (email, username, password, IP, name, phone, address, VIN, domain). Supports wildcards, regex, and mixed operators.

### Core Services

| Service | Description |
|---|---|
| **Search** | 24B+ records across email, username, password, IP, name, phone, address, VIN, domain |
| **Monitoring** | Real-time alerts via SMS/email/webhook when new credentials match |
| **API** | REST API with JSON/CSV, ~$0.02/query, key-based auth |
| **WHOIS** | Domain registration, 10+ year historical, reverse WHOIS (launched Apr 2025) |

### Pricing

| Tier | Price | Features |
|---|---|---|
| **Free** | $0 | Web search only, 5 results/query, 10 monitor tasks |
| **Starter** | $19/mo or $190/yr | Unlimited web searches, API access |
| **Professional** | $99/mo or $990/yr | Unlimited searches/API, bulk export, priority support |
| **Enterprise** | Custom | Custom limits, SLA, dedicated account manager |

API credits: ~$0.02/query. Rate limits: 50-1,000 requests/day by tier. Max 10,000 results per query. WHOIS requires separate credit purchases.

### Team Usage Potential
- **Employee exposure audits**: Check work emails against breaches
- **Password reuse detection**: Search passwords to find linked accounts
- **Domain breach monitoring**: Monitor @company.com emails continuously
- **Incident response**: Quickly identify scope of credential compromise
- **WHOIS investigation**: Domain ownership and historical registration data

### Pros
- Largest breach database (24B+ records, 24K+ sources)
- Multi-field search (email, IP, phone, VIN, address, name)
- Continuous monitoring with alerts
- REST API for integration
- WHOIS with 10+ year history
- Used by law enforcement and Fortune 500

### Cons
- Paid subscription required to see full results (cleartext passwords)
- API pricing adds up at scale
- No dark web forum search
- No raw file downloads (parsed records only)
- 10,000 result cap per query

---

## 8. Intelligence X (IntelX.io) — Dark Web & Leak Search Engine

### What It Is
IntelX is a **selector-based intelligence search engine** covering surface web, dark web (Tor + I2P), stealer logs, paste sites, WikiLeaks, Sci-Hub, WHOIS, and DNS. It does NOT accept free-text keywords — only structured selectors (email, domain, IP, CIDR, phone, crypto addresses, etc.).

### Data Sources (Buckets)

| Bucket | Type |
|---|---|
| Pastes, Leaks, Leaks COMB, Stealer Logs | **Premium (PRO)** |
| Darknet: Tor, Darknet: I2P | **Premium (PRO)** |
| WHOIS, DNS, Usenet | **Premium (PRO)** |
| WikiLeaks, Public Leaks, Dumpster, Sci-Hub | **Free** |

### Pricing

| Plan | Price/Year | Features |
|---|---|---|
| **Free** | $0 | 50 selector searches/day |
| **Researcher** | €2,500 | 200 lookups/day, 25 phonebook/day, priority email |
| **API** | €7,000 | 100 phonebook/day, programmatic access |
| **Identity Portal** | €10,000 | Line-by-line leak view, reverse lookups, stealer logs |
| **Enterprise** | €20,000 | 2,500+ phonebook/day, team access, SLA |

### Phonebook Feature
Enumerates emails and domains without knowing the full selector:
- Find all `@example.com` emails
- Discover related domains and infrastructure

### API Selectors Supported
Email, domain (incl. wildcards like `*.example.com`), URL, IPv4/IPv6, phone, Bitcoin, Ethereum, MAC address, IPFS hash, credit card, SSN, IBAN, UUID, simhash

### SDK Support
Official SDK for: Python (PyPI), PHP, Go, Maltego transforms, HTML/JS

### Team Usage Potential
- **Deep dive investigations**: Selector-based precision searching
- **Cryptocurrency tracing**: Bitcoin/Ethereum address analysis
- **Dark web monitoring**: Tor + I2P bucket searches
- **Infrastructure mapping**: DNS, WHOIS, IP/CIDR queries
- **Academic research**: Sci-Hub bucket access
- **Stealer log analysis**: Identify compromised sessions and cookies

### Pros
- Uniquely broad coverage (surface + Tor + I2P + stealer logs + Sci-Hub)
- Selector-based precision (ideal for targeted intelligence)
- Rich metadata (timestamps, categories, file types)
- Phonebook enumeration feature
- Website screenshots as evidence
- Official SDK in 5 languages

### Cons
- **No keyword search** — selectors only (major limitation for exploration)
- 50 lookups/day free tier is very restrictive
- Pricing opaque and expensive (€2,500+/yr)
- Login-gated (no anonymous access)
- Concurrent search throttling
- Restricted search terms
- CAPTCHA on login

---

## 9. GeoSpy.ai — AI Visual Geolocation Intelligence

### What It Is
GeoSpy is an **AI-powered visual geolocation platform** that determines where a photo was taken by analyzing the **image's pixels alone** — no EXIF/GPS metadata required. Uses Visual Place Recognition (VPR) model "Superbolt" against a database of **46M+ street-level images**.

**Developer**: Graylark Technologies Inc. (founded 2023, Boston)
**CEO**: Daniel Heinen
**Status**: Public access shut down Jan 2025; now government/enterprise only

### Product Lineup

| Product | Audience | Accuracy | Monthly Cost |
|---|---|---|---|
| **GeoSpy Plus** | OSINT hobbyists | City/region level | SHUT DOWN |
| **GeoSpy Pro** | Law enforcement, govt | Within a few feet | ~$500/mo |
| **GeoSpy Vision** | Enterprise (coming) | Object/vehicle/address ID | TBD |
| **API** | Developers | Varies by tier | $60-500/mo |

### How It Works
1. Upload an image (no metadata needed)
2. AI analyzes: vegetation, architecture, road surfaces, signage, lighting, shadows, spatial relationships, cloud patterns, sun position
3. Superbolt VPR model compares against 46M+ street-level images
4. Returns geolocation estimate (up to meter-level in ideal conditions)

### Real-World Use Cases
- **Law enforcement**: Fugitive caught in 20 minutes (published case study)
- **Journalism**: Verify photo locations for disinformation investigation
- **Threat intelligence**: Track sanctioned cybercriminal groups
- **Military OSINT**: Track tank/vehicle movements in conflict zones
- **Fraud detection**: Verify rental listing photos against claimed locations
- **Crime mapping**: Geolocate crime-related social media posts

### Team Usage Potential
- **Photo verification**: Confirm where investigation photos were taken
- **Location intelligence**: Extract location from stripped-metadata images
- **Disinformation analysis**: Debunk fake location claims
- **Pattern analysis**: Identify recurring locations in threat actor imagery
- **Evidence enrichment**: Add geolocation context to investigation dossiers

### Pros
- No EXIF/metadata required (works on bare images)
- Fast results (seconds per query)
- Up to meter-level precision claimed
- 10,000+ cases solved (real-world validation)
- Works on low-resolution and surveillance footage
- Analyzes vegetation, architecture, signage, sun position globally

### Cons
- **Public access shut down** — now government/enterprise only
- No public pricing (enterprise licensing only)
- Accuracy varies by location type (urban good, generic landscapes poor)
- No independent benchmark data available
- No API documentation publicly available
- Ethical concerns: mass surveillance, stalking risk
- Potential for false arrests from inaccurate geolocation
- Costs $500/mo for Pro tier

---

## 10. Master OSINT Workflow: Unified Pipeline

This workflow integrates all tools into a cohesive investigation pipeline for JACOB Team operations.

### Phase 0: Preparation & Environment Setup

```
[Setup]
  |
  +-- Deploy Kali VM (or provision existing)
  |     `-- ./install.sh from awesome-osint-arsenal (selective categories)
  |
  +-- Configure Tor
  |     `-- Install Tor daemon, configure ControlPort 9051
  |     `-- Install OnionClaw (as standalone or OpenClaw skill)
  |
  +-- Configure API Keys
  |     `-- DeHashed (Starter/Professional tier)
  |     `-- IntelX (Researcher or API tier)
  |     `-- DeepSeek/OpenAI (for DeepDive + OSINT-D2 AI)
  |     `-- Leaker .env with 13 source keys
  |     `-- ScrapingAnt (for OSINT-D2 residential proxy)
  |     `-- GeoSpy Pro (if government/LE access available)
  |
  +-- Configure OSINT-D2
  |     `-- poetry run osint-d2 doctor setup-ai
  |
  +-- Start DeepDive server
        `-- python3 server/app.py (background)
```

### Phase 1: Target Identification & Surface Recon

```
[Objective: Seed data collection on target]
  |
  +-- OSINT-D2 agent mode (autonomous reconnaissance)
  |     `-- osint-d2 agent "<target>" --breach-check --sources
  |
  +-- DeHashed / IntelX (manual selector searches)
  |     `-- email, domain, IP, phone selectors
  |
  +-- Leaker (batch passive leak enumeration)
  |     `-- leaker email target@example.com --db phase1.db -j
  |     `-- leaker domain targetdomain.com -V -M
  |
  +-- OnionClaw check_engines.py (verify dark web access)
  |
  OUTPUTS:
  - Known emails, usernames, domains
  - Breach exposure summary
  - Initial social media accounts
```

### Phase 2: Deep Search & Dark Web

```
[Objective: Surface hidden information]
  |
  +-- OnionClaw autonomous investigation
  |     `-- pipeline.py --mode threat_intel --query "<target>" --max 50
  |     `-- Or manual: search.py -> fetch.py -> ask.py
  |
  +-- IntelX deep selector search (paid tier)
  |     `-- All premium buckets (Tor, I2P, stealer logs, COMB)
  |     `-- Phonebook enumeration for domain
  |
  +-- DeHashed monitoring setup
  |     `-- Configure watch on domain/email
  |
  +-- The Collector (Tor stealth crawl)
  |     `-- python sentinel_crawler.py --url "<target-site>" \
  |          --keywords "confidential" "password" "admin" \
  |          --tor --depth 2 --db deep_scan.db
  |
  OUTPUTS:
  - Dark web mentions of target
  - Hidden services / .onion links
  - Stealer logs with target data
  - Crawled page content with keyword hits
```

### Phase 3: Relationship Mapping & Visualization

```
[Objective: Visualize connections and patterns]
  |
  +-- DeepDive investigation graph
  |     `-- Seed with primary target name/company/event
  |     `-- Import Phase 1+2 JSON data as document corpus
  |     `-- CLI: /deepdive expand, /deepdive money, /deepdive gaps
  |     `-- AI agent query: "Show me all financial connections"
  |
  +-- OSINT-D2 advanced profiling (if targets are individuals)
  |     `-- osint-d2 hunt --usernames <derived-usernames> \
  |          --emails <found-emails> --sherlock --strict \
  |          --export-pdf --export-json
  |
  +-- Cross-reference findings
  |     `-- DeepDive fuzzy matching across investigation nodes
  |     `-- OSINT-D2 trust anchors to filter false positives
  |
  OUTPUTS:
  - 3D relationship graph (DeepDive)
  - 6-dimension cognitive profile (OSINT-D2 PDF)
  - Sankey money flow diagram
  - Cross-investigation link report
```

### Phase 4: Physical Intelligence (if applicable)

```
[Objective: Geolocation and physical world context]
  |
  +-- GeoSpy Pro (if access available)
  |     `-- Upload photographs associated with target
  |     `-- Extract location from bare images
  |     `-- Create location timeline
  |
  +-- OSINT-D2 geo-temporal profiling
  |     `-- Derived timezone, activity patterns, sleep schedule
  |
  OUTPUTS:
  - Photo geolocation estimates
  - Location timeline
  - Activity pattern analysis
```

### Phase 5: Analysis, Report & Export

```
[Objective: Produce actionable intelligence report]
  |
  +-- DeepDive HTML report generation
  |     `-- /deepdive report
  |     `-- Print-to-PDF for distribution
  |
  +-- OSINT-D2 PDF dossier (if individual profiling)
  |     `-- Classified-style report with confidence meters
  |     `-- Footprint matrix with clickable URLs
  |     `-- Breach exposure tables
  |
  +-- IntelX evidence preservation
  |     `-- Download documents, screenshots, file exports
  |
  +-- The Collector SQLite analysis
  |     `-- Query crawled content for patterns
  |     `-- SQL: SELECT * FROM pages WHERE content LIKE '%<key>%';
  |
  +-- Cross-tool synthesis
  |     `-- Merge DeepDive + OSINT-D2 + Leaker findings
  |     `-- Identify gaps flagged by DeepDive's "gaps" command
  |
  OUTPUTS:
  - Final intelligence report (PDF or Obsidian)
  - Machine-readable JSON/JSONL for automation
  - 3D graph archive
  - SQLite evidence database
  - Monitor configuration for ongoing watch
```

### Ongoing: Continuous Monitoring

```
[Objective: Maintain watch on targets over time]
  |
  +-- DeHashed Monitoring
  |     `-- SMS/email/webhook alerts on new exposures
  |
  +-- IntelX recurrent searches
  |     `-- Re-check selectors periodically
  |
  +-- OnionClaw watch jobs (if SICRY engine supports)
  |     `-- Periodic dark web re-scans
  |
  +-- DeepDive periodic expansion
  |     `-- Automated overnight graph expansion runs
```

### Tool Selection Matrix by Investigation Type

| Investigation Type | Primary Tool | Secondary | Supporting |
|---|---|---|---|
| **Credential breach** | Leaker + DeHashed | IntelX | OnionClaw (dark web) |
| **Person of Interest** | OSINT-D2 | DeepDive | GeoSpy (photos) |
| **Corporate intelligence** | DeepDive | DeHashed WHOIS | IntelX |
| **Dark web monitoring** | OnionClaw | The Collector | IntelX |
| **Photo geolocation** | GeoSpy | OSINT-D2 (geo-temporal) | - |
| **Full-spectrum recon** | All combined | - | Arsenal catalog |

### Cost Estimate for Full Pipeline

| Component | Monthly Cost |
|---|---|
| DeHashed Starter/Professional | $19-99 |
| IntelX Researcher (annual) | ~$208/mo |
| DeepSeek API (AI inference) | $10-50 |
| ScrapingAnt Proxy | $0 (free tier) or $50+ |
| Leaker source APIs (various) | $50-200 |
| GeoSpy Pro (if accessible) | $500 |
| Infrastructure (VPS/Kali) | $10-30 |
| **Total (without GeoSpy)** | **~$100-400/mo** |
| **Total (with GeoSpy)** | **~$600-900/mo** |

---

## Recommendations for JACOB Team

### Immediate (This Week)
1. **Deploy OnionClaw** as OpenClaw skill on investigation workstation — instant dark web access with 18 search engines
2. **Set up Leaker** with free-tier sources (ProxyNova, Hudson Rock — no API key needed) for quick credential checks
3. **Install awesome-osint-arsenal** selectively — start with OSINT, Breach, and Dark Web categories
4. **Create DeHashed account** (Starter tier $19/mo) for continuous monitoring

### Short-Term (This Month)
5. **Deploy DeepDive** on Kali VM with DeepSeek AI — start building investigation graphs
6. **Configure OSINT-D2** with ScrapingAnt proxy for residential IP reputation
7. **Integrate The Collector** into dark web crawl pipeline (post-OnionClaw deep fetch)
8. **Set up IntelX Researcher account** (~€2,500/yr) if budget allows for serious investigations

### Strategic (Within Quarter)
9. **Build automated pipeline**: Chain OnionClaw -> Leaker -> DeepDive for unattended investigation runs
10. **Establish GeoSpy access** through appropriate channels if government/LE partnerships exist
11. **Create investigation templates**: Standard operating procedures for each investigation type
12. **Develop cross-tool data format**: Normalize JSON output schemas across all tools for pipeline integration

### Tools to Pair Together
- **OnionClaw + Leaker**: Dark web credential hunting pipeline
- **DeepDive + OSINT-D2**: Relationship graph + cognitive profiling
- **The Collector + OnionClaw**: Deep crawl after surface reconnaissance
- **DeHashed + IntelX**: Complement breach databases with dark web sources
- **All + awesome-osint-arsenal**: Reference catalog for specialized tasks

---

*End of SCOPE Deep Dive Report — 2026-06-30*
