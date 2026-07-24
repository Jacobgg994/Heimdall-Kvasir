# FLARE Learning Report: Ad Platform Foundation

**Date:** 2026-06-30
**Specialist:** FLARE — Social Media & Ads Specialist
**Focus:** Thailand market, multi-platform ad strategy

---

## Table of Contents

1. [Platform API Overview](#1-platform-api-overview)
2. [Thailand Market Ad Benchmarks (CPM, CPC, CTR)](#2-thailand-market-ad-benchmarks)
3. [Budget Allocation Strategy](#3-budget-allocation-strategy)
4. [Audience Targeting Guide](#4-audience-targeting-guide)
5. [Creative Best Practices per Platform](#5-creative-best-practices-per-platform)
6. [Platform Comparison Matrix](#6-platform-comparison-matrix)
7. [Key Takeaways](#7-key-takeaways)

---

## 1. Platform API Overview

### 1.1 Meta Marketing API

**Source:** developers.facebook.com/docs/marketing-apis/

The Meta Marketing API provides programmatic access to Facebook, Instagram, and Messenger advertising infrastructure. It supports the full ad management lifecycle.

**Core Capabilities:**
- **Campaign Management:** Full CRUD for campaigns, ad sets, and ads across the traditional hierarchy (Campaign > Ad Set > Ad)
- **Buying Types:** Auction (default), Reach & Frequency (reserved), and Target Cost bidding
- **Campaign Objectives:** Awareness (Brand Awareness, Reach), Consideration (Traffic, Engagement, App Installs, Video Views, Lead Generation, Messages), Conversion (Conversions, Catalog Sales, Store Traffic)
- **Optimization Goals:** Impressions, Reach, Landing Page Views, Link Clicks, Event Responses, Valuable Actions, Offsite Conversions, Value (ROAS), App Installs, etc.
- **Bid Strategies:** Lowest Cost (default), Cost Cap, Bid Cap, Target Cost, and Minimum ROAS
- **Server-Side Tracking:** Conversions API (CAPI) for sending web, app, and offline events directly from servers

**SDK Access:**
- Python: `facebook_business` (pip installable)
- Key classes: `FacebookAdsApi`, `FacebookSession`, `AdAccount`, `Campaign`, `EdgeIterator`
- Object hierarchy inherits from `AbstractCrudObject` with `api_get`, `api_create`, `api_update`, `api_delete`
- Multiple access tokens supported via separate `FacebookSession` instances
- Batch operations available via `FacebookAdsApiBatch`

### 1.2 TikTok Ads API

**Source:** business-api.tiktok.com/portal/docs

TikTok's business API (formerly at ads.tiktok.com/marketing_api/docs, now at business-api.tiktok.com) provides the full advertising management layer for TikTok's ecosystem including TikTok Shop.

**Core Capabilities:**
- **Campaign Management:** Create and manage campaigns, ad groups, and ads
- **Campaign Objectives:** Reach, Traffic, App Installs, Video Views, Lead Generation, Conversions, Catalog Sales
- **Ad Formats:** In-Feed Ads, Spark Ads (boosted organic posts), TopView (first thing users see on app open), Branded Hashtag Challenge, Branded Effects, Shopping Ads, Live Shopping Ads
- **Bidding Strategies:** Lowest Cost, Cost Cap, Bid Cap, Target CPA
- **Budget Types:** Daily budget and Lifetime budget
- **Creative Management:** Video and image ad creation, Spark Ads integration with organic content
- **Reporting:** Full performance analytics with demographic, geographic, and device-level breakdowns

**TikTok Shop Integration:**
- Shopping Ads with direct product tagging
- Live Shopping Ads for real-time selling events
- Catalog management for e-commerce

### 1.3 Google Ads API

**Source:** developers.google.com/google-ads/api/docs/start

The Google Ads API is the programmatic interface for managing large or complex Google Ads accounts and campaigns. It covers the full Google advertising ecosystem.

**Campaign Types Supported:**
- **Search Ads:** Traditional text ad campaigns on search results
- **Performance Max:** Fully automated cross-inventory campaigns (Search, Display, YouTube, Gmail, Maps, Discovery)
- **Display Ads:** Image and responsive ads across the Google Display Network
- **Video / YouTube Ads:** Skippable in-stream, non-skippable, bumper, in-feed, and Shorts
- **Shopping Ads:** Product-based campaigns with Merchant Center integration
- **Demand Gen:** Visual storytelling campaigns on YouTube Shorts, Discover, Gmail
- **App Campaigns:** Automated cross-property mobile app promotion
- **Local Services, Hotel Ads, Smart Campaigns, Dynamic Search Ads**

**Bidding Strategies:**
- Smart Bidding: Maximize Conversions, Maximize Conversion Value, Target CPA, Target ROAS, Enhanced CPC
- Manual CPC, CPM, CPV
- Portfolio bidding (cross-campaign)
- Bid modifiers by device, location, schedule
- Seasonality adjustments and data exclusions

**Targeting Options:**
- Location targeting (multiple granularity levels)
- Audience management: Remarketing, Custom Audiences, Lookalike Segments, Customer Match
- Demographic, keyword, placement, and topic targeting
- Audience signals for Performance Max campaigns

**Reporting:**
- GAQL (Google Ads Query Language) for flexible querying
- Search and SearchStream (streaming for large results)
- Segmentation by time, device, conversion category
- Optimization score, recommendations, and change history

**Authentication:**
- OAuth 2.0 with service account and user-based workflows
- Developer token system with defined access levels
- Python client library: `google-ads` (pip install, Python 3.9+)
- Multi-party approval for managed accounts

### 1.4 Reddit Ads API

**Status:** The github.com/reddit-ads-api organization was 404 at time of review. Reddit's advertising platform exists (ads.reddit.com) but a dedicated Python SDK is not publicly available as a standalone open-source package. Reddit Ads API access requires application approval and uses standard REST endpoints.

---

## 2. Thailand Market Ad Benchmarks

### 2.1 Comprehensive Benchmark Table

| Platform | Format | CPM (THB) | CPM (USD) | CPC (THB) | CPC (USD) | CTR | Notes |
|---|---|---|---|---|---|---|---|
| **Meta (FB/IG)** | All Formats | 50-150 | $1.50-4.50 | 2-8 | $0.06-0.24 | 1-2% | Thailand is 2-3x cheaper than US |
| **Meta (FB/IG)** | Brand Awareness | 30-80 | $0.90-2.40 | — | — | 0.8-1.5% | Lowest CPM format |
| **Meta (FB/IG)** | Retargeting | — | $6-12 | — | $0.40-0.90 | 1.5-3% | Higher CTR, higher CPM |
| **TikTok** | In-Feed Ads | 50-200 | $1.50-6.00 | 1-5 | $0.03-0.15 | 0.9-1.3% | Cheapest CPC in market |
| **TikTok** | Spark Ads | 40-150 | $1.20-4.50 | 1-4 | $0.03-0.12 | 2.4% | Best CTR uplift |
| **TikTok** | Shopping Ads | 60-180 | $1.80-5.50 | 2-6 | $0.06-0.18 | — | For TikTok Shop |
| **TikTok** | Live Shopping | — | — | 1-3 | $0.03-0.09 | — | Live selling events |
| **Google Search** | Low Competition | — | — | 5-20 | $0.15-0.60 | ~3.1% | Food, local services |
| **Google Search** | Medium Competition | — | — | 20-50 | $0.60-1.50 | ~3.1% | E-com, real estate, edu |
| **Google Search** | High Competition | — | — | 50-150+ | $1.50-4.50+ | ~3.1% | Insurance, legal, finance |
| **Google Display** | All | 30-150 | $0.85-4.25 | 3-15 | $0.09-0.45 | 0.46-0.60% | Intent targeting matters |
| **LINE Ads** | Display/Broadcast | ~15 | ~$0.42 | ~8 | ~$0.22 | 0.18% | Lowest CPM; low CTR |
| **LINE Ads** | Video View | — | — | CPV: ~1.22 THB | — | — | Cost per 6s view |

### 2.2 Key Market Dynamics

**Thailand has 56M social media users (78% of population):**
- Facebook: ~49M users
- LINE: ~54M MAU (80% smartphone penetration)
- TikTok: ~96.3% reach among Thai adults 18+
- Instagram: ~22M users

**Cost Trends:**
- Meta Thailand CPM is 2-3x cheaper than US ($1.50-4.50 vs $8-15) but RISING YoY
- TikTok offers the cheapest CPC in market (1-5 THB)
- Google Search CPC is 3-10x cheaper than US averages
- LINE has the lowest CPM (~15 THB) but very low CTR (0.18%)
- All platforms seeing 9-10% CPC inflation YoY as Thai businesses shift budgets digital

**Seasonality:**
- Q4 CPMs average 26% higher than Q1
- Black Friday week: 2-3x normal CPMs
- Thai-specific peaks: Songkran (April), payday cycles, 9.9, 11.11, Mother's Day

---

## 3. Budget Allocation Strategy

### 3.1 The 70/20/10 Framework

The most widely recommended approach for multi-platform allocation:

| Allocation | Purpose | Thailand Application |
|---|---|---|
| **70% — Proven Channels** | Core strategies delivering reliable ROAS | Meta (retargeting + prospecting) + Google Search |
| **20% — Emerging Opportunities** | Promising but not fully proven | TikTok expansion, LINE Ads scaling |
| **10% — Experiments** | High-risk, high-reward tests | New formats, Spark Ads testing, niche platforms |

**Minimum threshold:** 70/20/10 only works with total monthly budget above ~100,000 THB (~$3,000). Below that, single-platform concentration outperforms.

### 3.2 Revenue-Based Allocation

| Stage | % of Revenue for Ads | Notes |
|---|---|---|
| Launch (M1-3) | 25-35% of projected revenue | Heavy investment for market entry |
| Growth (M4-12) | 18-22% of revenue | Scale what works, test new channels |
| Maturity (M13+) | 12-18% of revenue | Efficiency focus, brand maintenance |

### 3.3 Thailand-Specific Allocation Model

For a Thai-market brand with 500K-2M THB monthly budget:

| Platform | Share | Rationale |
|---|---|---|
| **Meta (FB/IG)** | 35-40% | Largest reach, best retargeting, stable ROAS |
| **Google Search** | 20-25% | Intent capture, highest conversion intent |
| **TikTok** | 20-25% | Lowest CPC, fastest growth in Thai market |
| **LINE Ads** | 5-10% | Mass awareness, CRM integration |
| **Google Display + YouTube** | 5-10% | Video awareness, retargeting |
| **Creative Testing Reserve** | 10-15% | Set aside from platform budgets |

### 3.4 Creative Production Budget

One of the most common blind spots: allocate **10-20% of paid media budget specifically to creative production and testing.**

- TikTok needs: 3-5 new creatives per ad group per 7-14 days
- Meta needs: 3-4 new variants per ad set per 7-10 days
- Google needs: RSAs with 15 headlines + 4 descriptions refreshed quarterly

### 3.5 Mistakes to Avoid

1. **Equal distribution (33/33/33)** across platforms — asymmetric allocation always wins
2. **Over-indexing on last-click ROI** — underinvests in upper-funnel (TikTok, LINE)
3. **Rigid annual budgets** — review quarterly; Thai market shifts fast
4. **Not accounting for creative production costs** in media budget
5. **Ignoring platform-specific seasonality** — Songkran, 9.9, 11.11, payday cycles

---

## 4. Audience Targeting Guide

### 4.1 The 2026 Targeting Paradigm Shift

**Creative is now the primary targeting signal.** Platform AI (Advantage+, Performance Max, Smart Audience) reads visual cues from ads to find buyers. Audience definitions serve as **starting suggestions**, not hard constraints.

Key forces:
- Post-iOS 14.5 signal loss (global opt-in ~25%)
- First-party data is the new currency
- Server-side tracking (CAPI, Enhanced Conversions) is mandatory
- Broad + AI targeting outperforms manual lookalikes on mature accounts

### 4.2 Audience Types by Platform

| Type | Meta | Google | TikTok | LINE |
|---|---|---|---|---|
| **Demographic** | Age, gender, location, language | Age, gender, parental status, household income | Age, gender, location | Age, gender, province |
| **Interest/Behavior** | 1,000+ detailed interests, digital activities, purchase behavior | Custom Affinity, Custom Intent (search terms, URLs) | Interest categories, device, OS, network | Minimal (limited compared to others) |
| **Custom/Retargeting** | Website visitors (pixel), CRM, app users, engagement (video, lead form) | Website visitors, YouTube engagers, Customer Match email list | Website visitors, app activity, video engagers, Spark Engagement | LINE Tag (website pixel), OA followers |
| **Lookalike/Similar** | 1-10% lookalike; value-based lookalike (LTV-weighted) | Similar Segments, Performance Max audience signals | Smart Audience (Narrow/Balanced/Broad), Video Engagement Lookalike | Not available |
| **AI/Broad** | Advantage+ Audience (recommended default) | Optimized Targeting, Performance Max | Auto-targeting with AI optimization | — |

### 4.3 Lookalike Best Practices

**Meta Lookalikes:**
- Seed with micro-segments (2,000 repeat buyers = 30-50% better ROAS than 87K all-time list)
- Use rolling 7-14 day windows, not 90-day static lists
- Value-based lookalikes (LTV-weighted) consistently beat flat purchase-based
- Test 1% vs 3% vs 5% — sweet spot is often 2-3% layered with interest/behavior
- Use CAPI to restore 15-30% of lost iOS match quality

**TikTok Smart Audience:**
- Broader tiers (3-5%) often outperform tight 1% on TikTok
- Min seed: 1,000 matched users
- Video Engagement lookalikes (6s views, past 30 days) perform best for conversion
- Spark Ads + lookalike targeting = best performance combination

**Google Similar Segments:**
- Auto-generated from remarketing lists (min 500-1,000 users)
- Performance Max: upload customer email lists as audience signals
- Custom Intent audiences (competitor URLs + search terms) for niche targeting

### 4.4 Thailand-Specific Targeting Notes

- **Bangkok vs. provincial targeting matters:** City-by-city logic often beats national averages. Bangkok, Chiang Mai, Phuket, and secondary cities can behave like different markets
- **Thai consumer habits:** Value-conscious — price signals in targeting creative work well
- **Language:** Thai-language creative with local references outperforms translated content by significant margins (case study: 1.2% CTR translation vs 3.9% local = 35% CPA drop)
- **PDPA compliance required** for using customer data in lookalike/retargeting audiences

### 4.5 Funnel-Based Multi-Platform Strategy

| Funnel Stage | Primary Platform | Secondary | Goal |
|---|---|---|---|
| **Awareness (Top)** | TikTok (+ Spark Ads) | LINE Ads, YouTube | Reach, views, engagement |
| **Consideration (Mid)** | Meta (FB/IG) | Google Display, YouTube | Traffic, engagement, lead gen |
| **Conversion (Bottom)** | Google Search | Meta Retargeting, TikTok | Sales, leads, signups |
| **Retention/Retarget** | Meta (custom audiences) | LINE OA, Google | Repeat purchases, LTV |

---

## 5. Creative Best Practices Per Platform

### 5.1 Meta (Facebook & Instagram) Creative

**The Winning Formula (Video):**

| Time | Content | Why |
|---|---|---|
| 0-3 sec | Hook — visual surprise, bold claim, problem statement | Stop the scroll or lose them |
| 3-15 sec | Value — demonstrate product/service benefit | Hold interest |
| 15-22 sec | Social proof — testimonial, results data | Build trust |
| 22-30 sec | CTA — clear next step with urgency | Convert |

**Key Rules:**
- Hook in the first 3 seconds — 90% of ad recall impact is in first 6 seconds
- Show product within first 5 seconds
- Design for sound-off — captions boost view time by 12%
- Keep under 30 sec for cold audiences; longer for retargeting
- Rotate creative every 7-10 days — ad fatigue hits faster in 2026
- UGC-style ads outperform polished brand creative by 2-3x in Thailand

**Format Specs:**

| Placement | Aspect Ratio | Resolution | Max Duration |
|---|---|---|---|
| Feed (video) | 4:5 | 1080x1350 | <30 sec rec |
| Stories/Reels | 9:16 | 1080x1920 | 15-60 sec |
| Carousel | 1:1 | 1080x1080 | 2-10 cards |
| Image (feed) | 4:5 | 1080x1350 | — |

**Image Best Practices:**
- Static images = testing weapon (fastest way to validate concepts)
- Lead with bold visual or unexpected element
- Key value prop in first 125 characters of primary text
- UGC customer photos add authenticity

**Carousel Structure:**
1. Hook — stop the scroll
2. Explain — problem or value
3. Prove — social proof or evidence
4. Close — CTA with urgency

**The 60-30-10 Testing Rule:**
- 60%: Scaling winning ads
- 30%: Winner variations (new hooks, formats)
- 10%: Brand-new concepts and tests

### 5.2 TikTok Creative

**The Hook (0-3 seconds) is Everything:**
- 90% of ad recall impact captured within first 6 seconds
- 63% of highest-performing ads place core message in first 3 seconds
- 45% of people who watch first 3 seconds watch 30+ seconds

**Top-Performing Hook Types:**
1. Bold question — "Why is every dermatologist recommending this?"
2. Pattern interrupt — unexpected visual or sound
3. Problem-first — "Stop scrolling if you have XYZ problem"
4. Before/after reveal — transformation in first frame
5. Social proof — "2 million people bought this last month"
6. Price-led — "Under $20 and works better than..." (critical for Thailand)

**Spark Ads Advantage:**
- Engagement rate: +142% vs standard in-feed
- Conversion rate: +43%
- Watch time: +24%
- CPA reduction: -37%
- CVR: 2.6% vs 1.8% for standard in-feed

**Thailand-Specific Creative Tips:**
- Local Thai creators outperform big lifestyle names
- Price signals early: show pricing/discount in first few seconds
- Cultural hooks that work: routine fix, value proof, social proof
- Local holidays matter: Songkran, payday, 9.9, 11.11
- Full localization (Thai audio + subtitles + local pricing) is mandatory, not optional

**Creative Velocity:**
- TikTok creative burns out in ~7 days (4x faster than Meta)
- Keep 3-5 diverse creatives per ad group running simultaneously
- Modular approach: 3 hooks x 2 body variations x 2 CTAs = 12 variants from one production

**Technical Specs:**
- Aspect ratio: 9:16 (vertical)
- Optimal length for conversions: 21-34 seconds (hook in first 1.7s)
- Sound-on creative converts 28% better than sound-off
- Best posting time: 6pm-10pm local time (CTR lifts 38% vs daily avg)
- Optimal frequency: 4 impressions/user/week

### 5.3 Google Ads Creative

**Responsive Search Ads (RSAs):**

| Asset | Max | Character Limit | Strategy |
|---|---|---|---|
| Headlines | 15 | 30 each | Cover 5 angles: keyword match, benefit, proof, differentiator, CTA |
| Descriptions | 4 | 90 each | Each standalone: benefit, social proof, offer, CTA |

**Headline Strategy (don't write 15 of the same):**
- 2-3 keyword match headlines (mirror search intent)
- 3-4 benefit headlines ("Lower CPA in 30 Days")
- 2-3 proof headlines (numbers, certifications)
- 2-3 differentiator headlines ("No Long-Term Contracts")
- 1-2 CTA headlines ("Get a Free Audit")

**Critical 2026 Insights:**
- **Ad Strength is NOT a performance metric** — it measures structural completeness only
- Human-written RSAs outperform AI-generated ones by 214% at same Ad Strength
- **2 RSAs per ad group** = sweet spot (~6.6% conversion lift from second RSA)
- Pin sparingly — only pin 1 headline to position 1, leave rest unpinned
- Sweet spot for description length: 61-70 characters

**Display Ads (Responsive):**
- Provide maximum assets — more combinations = better ML testing
- Avoid text overlays on images (Google adds headlines automatically)
- 1.91:1 (landscape) and 1:1 (square) required; 4:5 (portrait) recommended
- Video is increasingly valuable for display campaigns

**YouTube/Video:**
- Hook in first 5 seconds (before skip button)
- Brand within first 5 seconds
- Music/voiceover increases conversions by 20%+
- Skippable in-stream: 15-30 sec recommended
- Shorts: safe zone center 1080x1420px (bottom 480px = UI overlay)

**Message Match (CRITICAL):**
- Lead benefit in ad headline MUST appear in landing page H1 — same words, not synonyms
- 83% of landing page visits come from mobile
- Fix the "drift" between click and first view before touching bids

### 5.4 LINE Creative

**LINE OA Content Strategy:**
- Every message should feel useful, not like an ad
- If every message feels like an ad, followers go quiet
- Block Rate (<5%) is the #1 metric to watch

**LINE Ad Formats:**
- Display Ads: static image across chat list, VOOM, LINE News, partner apps
- Video Ads: 6-15 sec for awareness; 9:16 vertical for VOOM
- Smart Channel: premium placement at top of chat list
- Sponsored Stickers: mass Friend adds (budget: 1.5-5M THB)

**LINE OA as CRM (not just broadcast):**
- Rich Menu = mini-website (promotions, store locator, chat, loyalty)
- Welcome Flow: Day 1 coupon, Day 3 content, Day 7 special offer
- Segmentation via Chat Tags (move away from mass broadcasts)
- Step Messages: timed sequences with branching logic
- LINE Tag: website pixel for retargeting + conversion measurement

**Key KPIs:**
- Block Rate: <5%
- Open Rate: >35-40%
- CTR: >10%
- Cost per Friend Add: 5-30 THB

### 5.5 Thailand-Specific Cross-Platform Creative Insights

- UGC content outperforms polished brand content by 2-3x across all platforms
- Thai-language, culturally relevant creative is non-negotiable
- Price/value signals early in creative (Thai shoppers are value-conscious)
- Mobile-first (vertical 9:16 is priority for TikTok, Reels, LINE, YouTube Shorts)
- Local creators > imported content — even translated UGC underperforms native Thai content
- Creative velocity beats perfection on every platform

---

## 6. Platform Comparison Matrix

| Dimension | Meta (FB/IG) | TikTok | Google Ads | LINE Ads |
|---|---|---|---|---|
| **Reach in Thailand** | 49M FB, 22M IG | ~96% adult reach | 56M internet users | 54M MAU |
| **Best For** | Full-funnel (awareness to conversion) | Discovery + engagement | Intent capture + conversion | Mass awareness + CRM |
| **CPM (THB)** | 50-150 | 40-200 | 30-150 (Display) | ~15 |
| **CPC (THB)** | 2-8 | 1-6 | 5-150+ (Search); 3-15 (Display) | ~8 |
| **CTR** | 1-2% | 0.9-2.4% | 3.1% (Search); 0.5% (Display) | 0.18% |
| **Conversion Intent** | Medium | Medium-low | Highest (Search) | Lowest |
| **Targeting Granularity** | Excellent | Good | Excellent | Limited |
| **Creative Velocity Required** | Medium (7-10 day refresh) | High (7 day refresh) | Low-medium | Medium |
| **API/SDK Availability** | Python SDK, REST API | REST API | Python SDK, REST API | REST API, Messaging API |
| **Thailand Cost Efficiency** | High (2-3x cheaper than US) | Highest (cheapest CPC in market) | High (3-10x cheaper than US) | Highest CPM efficiency |
| **Best Objective** | Conversions, retargeting | Reach, video views, conversions | Search intent, lead gen | Awareness, CRM retention |
| **PDPA Readiness** | Mature (CAPI, server-side) | Developing | Mature (Enhanced Conversions) | Basic |

---

## 7. Key Takeaways

### For Thailand Market Strategy

1. **Meta remains the workhorse** — largest reach, best targeting, proven ROAS. Start here.
2. **TikTok is the growth engine** — lowest CPC in market, fastest-growing e-commerce platform (TikTok Shop at 33% market share), critical for reaching Gen Z and millennial Thai consumers.
3. **Google Search captures intent** — essential for bottom-funnel conversion. High CPC but highest conversion rates.
4. **LINE is the retention layer** — 54M MAU with lowest CPM. Use for CRM, mass awareness, and OA-based retention. The LY Ads migration (April 2026-March 2027) is critical to track.
5. **LINE Ads are for awareness only** — CTR is very low (0.18%). Do not use for direct response.

### Budget Principles

- 70/20/10 rule for allocation across proven/emerging/experimental
- Asymmetric allocation beats equal distribution
- Include 10-20% of budget for creative production (often forgotten)
- Review and reallocate monthly, not annually
- Below $3K/month total: single-platform concentration wins

### The One Thing That Matters Most in 2026

**Creative is the new targeting.** Platform AI reads your creative content to find the right audience. On Meta (Advantage+), Google (Performance Max), and TikTok (Smart Audience), the quality and diversity of your creative assets determine performance more than audience definitions ever did.

This means:
- Invest in creative velocity before audience granularity
- Test hooks before scaling budgets
- Localize fully for Thailand (not just translate)
- UGC > polished brand content (2-3x ROI difference)
- Refresh before fatigue sets in (7-14 day cadence on social platforms)

---

*Report compiled by FLARE based on live API documentation, market benchmarks, and 2026 industry research.*

**Sources:**
- Meta Marketing API documentation (developers.facebook.com)
- Facebook Python Business SDK (github.com/facebook/facebook-python-business-sdk)
- TikTok Business API (business-api.tiktok.com)
- Google Ads API documentation (developers.google.com/google-ads/api/docs/start)
- Google Ads Python Client Library (github.com/googleads/google-ads-python)
- Sphere Agency — Google Ads Pricing Thailand 2026
- Sphere Agency — TikTok Ads Cost Thailand 2026
- Yes Web Design Studio — Facebook & Instagram Ads Guide for Thai Businesses 2026
- MCIX Agency — Meta Ads Creative Testing Framework for Thailand
- MCIX Agency — TikTok Spark Ads Thailand Strategy
- MCIX Agency — LINE Ads Thailand Guide for Consumer Brands 2026
- Audience-IQ — LINE Advertising Deep Dive
- Phoenix Media — Costs of Facebook, Google, and LINE Ads in Thailand 2024
- 6W Research — Thailand Social Networking Advertising Market 2025-2031
- The Yolk Media — Meta Ads Creative Playbook 2026
- AI Advantage Agency — Facebook Ad Creative for Ecommerce 2026
- AdBacklog — Google, Facebook, TikTok Ads Benchmarks 2025
- Hallam — Budgeting for Paid Media in 2026
- Helium 10 — How to Allocate Advertising Budget Across Channels 2026
- Search Engine Journal — PPC Budget Rebalancing 2026
