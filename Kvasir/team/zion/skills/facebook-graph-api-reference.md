---
name: facebook-graph-api-reference
description: Key Facebook Graph API endpoints — /me, /{page-id}/posts, /{post-id}/comments, insights, permissions, token types (Page, User, App)
metadata:
  type: skill
  category: facebook-api
  owner: zion
---

# Facebook Graph API Reference

## Endpoint Reference

### 1. Identity & Profile

#### GET /me
Get current user/profile tied to the access token.

```
GET graph.facebook.com/{api-version}/me
  ?access_token={token}
  &fields=id,name,email,picture
```

**Response:**
```json
{
  "id": "123456789",
  "name": "John Doe",
  "email": "john@example.com",
  "picture": {
    "data": {
      "height": 50,
      "is_silhouette": false,
      "url": "https://platform-lookaside.fbsbx.com/...",
      "width": 50
    }
  }
}
```

**Error:**
```json
{
  "error": {
    "message": "Invalid OAuth 2.0 Access Token",
    "type": "OAuthException",
    "code": 190,
    "fbtrace_id": "ABC123"
  }
}
```

---

### 2. Page Management

#### GET /{page-id}
Get page information.

```
GET graph.facebook.com/{api-version}/{page-id}
  ?access_token={page-token}
  &fields=id,name,about,fan_count,rating_count,link,username
```

#### GET /{page-id}/posts
Get page posts (published + scheduled).

```
GET graph.facebook.com/{api-version}/{page-id}/posts
  ?access_token={page-token}
  &fields=id,message,created_time,permalink_url,full_picture,shares,comments.limit(2){message,from}
  &limit=25
  &before={cursor}  (pagination: previous)
  &after={cursor}   (pagination: next)
```

**Response:**
```json
{
  "data": [
    {
      "id": "123_456",
      "message": "Hello world!",
      "created_time": "2026-07-24T10:00:00+0000",
      "permalink_url": "https://www.facebook.com/...",
      "full_picture": "https://scontent.fbom1-1.fna.fbcdn.net/..."
    }
  ],
  "paging": {
    "cursors": {
      "before": "QVFI...",
      "after": "QVFI..."
    },
    "next": "https://graph.facebook.com/v21.0/..."
  }
}
```

#### POST /{page-id}/posts
Create a new page post.

```
POST graph.facebook.com/{api-version}/{page-id}/posts
  ?access_token={page-token}
  &message=Hello%20world
  &link=https://example.com
  &published=true
```

**Response:**
```json
{
  "id": "123_789"
}
```

#### POST /{page-id}/photos
Upload a photo to the page.

```
POST graph.facebook.com/{api-version}/{page-id}/photos
  ?access_token={page-token}
  &url=https://example.com/photo.jpg
  &message=Check%20this%20out
  &published=true
```

#### POST /{page-id}/videos
Upload a video to the page.

```
POST graph.facebook.com/{api-version}/{page-id}/videos
  ?access_token={page-token}
  &file_url=https://example.com/video.mp4
  &title=My%20Video
  &description=Video%20description
```

---

### 3. Engagement

#### GET /{post-id}/comments
Get comments on a post.

```
GET graph.facebook.com/{api-version}/{post-id}/comments
  ?access_token={page-token}
  &fields=id,message,from,created_time,like_count,parent
  &order=chronological
  &filter=toplevel  (top-level comments only, omit for all)
  &limit=50
```

#### POST /{post-id}/comments
Reply to a post or comment.

```
POST graph.facebook.com/{api-version}/{post-id}/comments
  ?access_token={page-token}
  &message=Thanks%20for%20your%20feedback
```

#### GET /{post-id}/likes
Get likes on a post.

```
GET graph.facebook.com/{api-version}/{post-id}/likes
  ?access_token={page-token}
  &fields=id,name
  &limit=100
  &summary=true
```

**Response with summary:**
```json
{
  "data": [...],
  "summary": {
    "total_count": 542
  }
}
```

#### GET /{page-id}/feed
Get all posts (from page + others who posted on page).

```
GET graph.facebook.com/{api-version}/{page-id}/feed
  ?access_token={page-token}
  &fields=id,message,from,created_time,type
  &limit=25
```

---

### 4. Insights & Analytics

#### GET /{page-id}/insights
Get page analytics metrics.

```
GET graph.facebook.com/{api-version}/{page-id}/insights
  ?access_token={page-token}
  &metric=page_impressions,page_impressions_unique,page_fans,page_engaged_users,page_post_engagements
  &period=day
  &since=2026-07-01
  &until=2026-07-24
```

**Response:**
```json
{
  "data": [
    {
      "name": "page_impressions",
      "period": "day",
      "values": [
        {"value": 1500, "end_time": "2026-07-01T07:00:00+0000"},
        {"value": 2300, "end_time": "2026-07-02T07:00:00+0000"}
      ],
      "title": "Page Impressions",
      "description": "Number of times any page content..."
    }
  ]
}
```

#### Available Insights Metrics

| Metric | Description | Period |
|--------|-------------|--------|
| `page_impressions` | Total impressions | day/week/month |
| `page_impressions_unique` | Unique users reached | day/week/month |
| `page_fans` | Total page likes | day |
| `page_fans_gross` | New likes | day |
| `page_engaged_users` | Users who engaged | day |
| `page_post_engagements` | Total post engagements | day |
| `page_consumptions` | Clicks on page content | day |
| `page_impressions_paid` | Paid impressions | day |
| `page_impressions_organic` | Organic impressions | day |
| `page_fan_adds` | New page likes (net) | day |

---

### 5. Conversations / Messages

#### GET /{page-id}/conversations
Get page conversations (requires `pages_messaging` permission).

```
GET graph.facebook.com/{api-version}/{page-id}/conversations
  ?access_token={page-token}
  &fields=id,snippet,message_count,updated_time,messages.limit(1){message,from,created_time}
  &limit=25
```

#### GET /{conversation-id}/messages
Get messages in a conversation.

```
GET graph.facebook.com/{api-version}/{conversation-id}/messages
  ?access_token={page-token}
  &fields=message,from,created_time,attachments
  &limit=100
```

---

### 6. Media

#### GET /{page-id}/albums
Get page photo albums.

```
GET graph.facebook.com/{api-version}/{page-id}/albums
  ?access_token={page-token}
  &fields=id,name,description,count,cover_photo
  &limit=25
```

#### GET /{album-id}/photos
Get photos from an album.

```
GET graph.facebook.com/{api-version}/{album-id}/photos
  ?access_token={page-token}
  &fields=id,images,name,created_time
  &limit=50
```

---

## Permissions Reference

### Common Permissions

| Permission | Access | Expiry | Notes |
|-----------|--------|--------|-------|
| `pages_manage_posts` | Create/edit/delete page posts | With page token | Required for content publishing |
| `pages_read_engagement` | Read page metrics + engagement | With page token | Read-only insight data |
| `pages_manage_metadata` | Update page settings/profile | With page token | Required by SALMON for profile updates |
| `pages_messaging` | Read/manage conversations | With page token | Messenger automation |
| `public_profile` | Basic user info (name, pic) | With user token | Minimal access |
| `email` | User email | With user token | Optional for CRM |
| `pages_show_list` | List managed pages | With user token | Required to discover page IDs |
| `pages_read_user_content` | Read user content on pages | With user token | For moderation |

### Permission Review Process
- Standard access: auto-approved for most permissions
- Advanced access: requires business verification + use case review
- `pages_messaging` may require app review for some features

---

## Token Types

### Page Token
- Short-lived: 1 hour
- Long-lived: 60 days (extend via `GET /{page-id}?fields=access_token`)
- Never-expire: re-login page every 60 days to refresh
- Scope: specific page only

### User Token
- Short-lived: 1-2 hours
- Long-lived: 60 days (via `GET /oauth/access_token?grant_type=fb_exchange_token`)
- Cannot be extended forever — user must re-login
- Scope: all permissions user granted

### App Token
- Format: `{app-id}|{app-secret}`
- No expiry
- Use: server-to-server, no user context
- Cannot call user-specific or page-specific endpoints

---

## API Versioning

| Version | Status | Current | Code Migration Due |
|---------|--------|---------|-------------------|
| v21.0 | **Current** | Live | — |
| v20.0 | Deprecated Apr 2026 | Grace period | Q3 2026 |
| v19.0 | Deprecated Apr 2025 | End of life | Already migrated |
| v22.0 | Beta | Test | Q1 2027 |

### Version Call Format
```
# Via URL path
GET graph.facebook.com/v21.0/me

# Via env variable (recommended)
API_VERSION=${FB_API_VERSION:-v21.0}
```

### Breaking Changes to Watch
- Field removals (check changelog each version)
- Permission requirement changes
- Rate limit adjustments
- Response format changes (e.g., `paging` → `pagination`)

---

## Rate Limits

| Limit Type | Threshold | Reset |
|-----------|-----------|-------|
| User-level | 200 calls/user/hour | Sliding window |
| App-level | 4800 calls/user/day | UTC midnight |
| Page-level | Varies by page size | Sliding window |
| Burst | 100 calls/5 minutes | Sliding window |
| Batch calls | 50 requests/batch | Counts as 1 call |

### Rate Limit Headers (Monitor These)
```
x-business-use-case-usage: [{"type": "api", "call_count": 45, "total_cputime": 0.5, "total_time": 1.2}]
x-app-usage: {"call_count": 12, "total_cputime": 0.2, "total_time": 0.5}
x-page-usage: {"call_count": 34, "total_cputime": 1.1, "total_time": 2.3}
```

### When Rate Limited (HTTP 403 / code 613)
```json
{
  "error": {
    "message": "(#613) Calls to this api have exceeded the rate limit.",
    "type": "OAuthException",
    "code": 613,
    "error_subcode": 2500,
    "fbtrace_id": "DEF456"
  }
}
```

---

## Quick Reference: Common Endpoint Patterns

| Purpose | Method | Endpoint | Key Fields |
|---------|--------|----------|-----------|
| Identify user | GET | `/me` | `id,name,email` |
| List pages | GET | `/me/accounts` | `id,name,access_token,category` |
| Get posts | GET | `/{page-id}/posts` | `message,created_time,permalink_url` |
| Create post | POST | `/{page-id}/posts` | `message,link,published` |
| Get comments | GET | `/{post-id}/comments` | `message,from,created_time` |
| Reply | POST | `/{post-id}/comments` | `message` |
| Get likes | GET | `/{post-id}/likes` | `summary=true` |
| Upload photo | POST | `/{page-id}/photos` | `url,message` |
| Upload video | POST | `/{page-id}/videos` | `file_url,title` |
| Get insights | GET | `/{page-id}/insights` | `metric,period,since,until` |
| Get conversations | GET | `/{page-id}/conversations` | `snippet,message_count` |

---

## Error Codes Quick Reference

| Code | Meaning | Action |
|------|---------|--------|
| 1 | Generic error | Retry or check request |
| 100 | Invalid parameter | Check field names and values |
| 190 | Invalid/expired token | Refresh access token |
| 200 | Permission denied | Check granted permissions |
| 210 | User not visible | Privacy settings |
| 341 | Feed action limit | Rate limiting active |
| 368 | Temporarily blocked | Wait and reduce frequency |
| 613 | Rate limit hit | Implement backoff |
| 80004 | Application limit reached | Check app-level usage |
