# 🔬 Advanced OSINT Toolkit — SCOPE & PRISM

> อัปเดต 2026-06-30 · 100+ เครื่องมือขั้นสูง

---

## 🏆 All-in-One Platforms

| Tool | Type | ใช้สำหรับ |
|------|------|----------|
| [The_Collector](https://github.com/VolkanSah/The_Collector) | Open Source | Web crawler + Tor stealth + SQLite |
| [DeepDive](https://github.com/Sinndarkblade/deepdive) | Open Source | Autonomous 3D graph — คน เงิน บริษัท เหตุการณ์ |
| [OSINT-D2](https://github.com/Doble-2/osint-d2) | Open Source | AI agent — 30+ platforms, 6-dimension profiling |
| [red-team-osint-tool](https://github.com/POWDER-RANGER/red-team-osint-tool) | Open Source | Full pipeline — WHOIS, email, social, dark web |
| [JARVIS](https://github.com/affaan-m/JARVIS) | Open Source | Real-time face recognition + social scraping |

---

## 🕵️ People Search & Identity

| Tool | Type | ใช้สำหรับ |
|------|------|----------|
| **PimEyes** | Freemium | Reverse face search — หาใบหน้าบนเน็ต |
| **FaceCheck.id** | Freemium | Facial recognition + social profile matching |
| **Search4Faces** | Free | Search faces across VK, TikTok, Instagram |
| **Epieos** | Free | Email/phone reverse lookup + Google account info |
| **WhatsMyName** | Free | Username search across 500+ sites |
| **Social Mapper** | Open Source | Facial recognition across LinkedIn, Instagram, Twitter, Facebook |

---

## 💧 Breach & Leak Intelligence

| Tool | Type | ใช้สำหรับ |
|------|------|----------|
| **DeHashed** | Paid | Billions of records — email, phone, IP, VIN, crypto |
| **LeakRadar** | Freemium | 497B+ leak lines — stealer logs, combolists |
| **CheckLeaked.cc** (Apify) | Freemium | 6 sources in one — DeHashed, Snusbase, LeakCheck, GHunt |
| **leaker CLI** | Open Source | 13 sources in one — v1.6.7 June 2026 |
| **BreachHunter** | Open Source | DeHashed API automation |
| **SPIA Privacy Auditor** (Apify) | Freemium | 60+ sources — surface + deep + dark web |
| **IntelX / Phonebook.cz** | Freemium | 121B records — domains, emails, URLs |
| **Hudson Rock** | Paid | Infostealer logs — 30M+ infected computers |
| **Constella** | Enterprise | 1.5T identities — infostealer logs |

---

## 🌐 Dark Web Intelligence

| Tool | Type | ใช้สำหรับ |
|------|------|----------|
| [OnionClaw](https://github.com/christinminor459/OnionClaw) | Open Source | AI agent Tor access — 18 search engines |
| [phantomx39/Scraper](https://github.com/phantomx39/Scraper) | Open Source | Dark web scraper + LLM analysis |
| **Ahmia** | Free | Tor hidden service search |
| **Tor66** | Free | .onion search engine |
| **DarkSearch** | Free | Dark web search |
| **NexVision** | Paid ($18K/yr) | 120K+ new Tor sites daily |
| **DarkOwl** | Paid | Largest commercial dark web index |

---

## 📍 Geolocation & Imagery

| Tool | Type | ใช้สำหรับ |
|------|------|----------|
| **GeoSpy** | Free | AI-powered image geolocation |
| **Picarta.ai** | Free | Photo geolocation |
| **SunCalc** | Free | Sun/shadow timing analysis |
| **Sentinel Hub** | Free | Satellite imagery |
| **Google Earth Pro** | Free | Historical imagery + measurements |
| **Overpass Turbo** | Free | OpenStreetMap data mining |
| **ShadowMap** | Free | Shadow analysis for geolocation |

---

## 📱 Social Media OSINT

| Tool | Type | ใช้สำหรับ |
|------|------|----------|
| **Osintgram** | Open Source | Instagram deep analysis |
| **Instaloader** | Open Source | Instagram content + metadata download |
| **Twint** | Open Source | Twitter scraping (no API) |
| **Tookie-osint** | Open Source | TikTok username + content analysis |

---

## 🧩 Awesome Lists & Toolkits

| Resource | เนื้อหา |
|----------|--------|
| [Awesome-OSINT-Arsenal](https://github.com/rawfilejson/awesome-osint-arsenal) | 751+ tools, 50 categories, one-command installer |
| [Awesome-OSINT-List](https://github.com/Astrosp/Awesome-OSINT-List) | 50+ subcategories — SOCMINT, GEOINT, Dark Web |
| [Bellingcat Toolkit](https://bellingcat.gitbook.io/toolkit) | คู่มือ OSINT ระดับมืออาชีพ |
| [OSINT Navigator](https://navigator.indicator.media) | 150+ tools จัดหมวดหมู่ |
| [Awesome-AI-OSINT](https://github.com/ubikron/awesome-osint-chrome-extensions) | AI-powered OSINT + Chrome extensions |
| [WarTrace](https://github.com/4lp1ne/WarTrace) | Geolocation + Facial Recognition + War Crimes |

---

## 🔄 OSINT Workflow ขั้นเทพ

```
1. Username → Sherlock (400+ sites) + WhatsMyName (500+)
2. Email → Holehe + Epieos + GHunt + IntelX
3. Phone → PhoneInfoga + Truecaller
4. Face → PimEyes + FaceCheck + Search4Faces
5. Breach → leaker CLI (13 sources) + DeHashed + LeakRadar
6. Domain → Amass + theHarvester + crt.sh + Shodan
7. Dark Web → OnionClaw + Ahmia + DarkSearch
8. Geolocation → GeoSpy + Picarta + SunCalc + Sentinel
9. Graph → Maltego + DeepDive (3D)
10. Report → OSINT-D2 (AI agent + PDF dossier)
```

---

## 📊 Tool Comparison — เลือกใช้ตามสถานการณ์

| สถานการณ์ | เครื่องมือหลัก | เครื่องมือรอง |
|-----------|-------------|------------|
| หาตัวตนจาก username | Sherlock + Maigret | WhatsMyName |
| หาจาก email | Epieos + Holehe | GHunt + IntelX |
| หาจากรูปหน้า | PimEyes | FaceCheck + Search4Faces |
| ตรวจสอบ data leak | leaker CLI (13 sources) | DeHashed + LeakRadar |
| ขุด dark web | OnionClaw | Ahmia + DarkSearch |
| หาพิกัดจากภาพ | GeoSpy | Picarta + SunCalc |
| คนหาย/บุคคล | Sherlock → Epieos → PimEyes → LeakRadar |
| สอบสวนองค์กร | Amass → theHarvester → Maltego → IntelX |

---

## 🎯 Assignments

- 🔬 **SCOPE**: ศึกษา DeepDive, leaker CLI, OnionClaw, GeoSpy, Maltego
- 🔍 **PRISM**: ศึกษา Sherlock, Epieos, SPIA, Osintgram, PimEyes

---

> 📅 2026-06-30 · JACOB Team OSINT Division
