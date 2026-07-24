---
name: facebook-api-debugging
description: How to debug Facebook API calls — Graph API Explorer, error codes, rate limiting detection, request tracing
metadata:
  type: skill
  category: facebook-api
  owner: lyra
---

# Facebook API Debugging Guide

> Every error code has a story. Learn to read it.

---

## Debugging Toolkit

### Tool 1: Graph API Explorer (Quick Debug)
```
Tools → Graph API Explorer
https://developers.facebook.com/tools/explorer/
```

**Use for:**
- Test endpoint with different tokens
- Inspect raw response JSON
- Discover available fields interactively
- Get short-lived tokens for testing

**Pro tip:** Use "Get Token" → "Page Token" to test page-specific endpoints. Switch tokens to verify permission issues.

### Tool 2: Access Token Debugger
```
Tools → Access Token Debugger
https://developers.facebook.com/tools/debug/accesstoken/
```

**Use for:**
- Check token validity and expiry
- Verify granted permissions/scopes
- Identify which app issued the token
- Check which user/page token belongs to

### Tool 3: Webhooks Dashboard
```
App Dashboard → Webhooks → Logs
https://developers.facebook.com/apps/{app-id}/webhooks/
```

**Use for:**
- View webhook delivery history
- Check for delivery failures
- Inspect webhook payloads
- Retry failed deliveries

### Tool 4: App Dashboard Insights
```
App Dashboard → Insights → API Calls
```

**Use for:**
- View aggregate API usage metrics
- Identify error rate spikes
- Track API call volume trends
- Find rate limiting events

---

## Error Code Reference

### Authentication & Token Errors

| Code | Subcode | Description | Debug Steps |
|------|---------|-------------|-------------|
| 190 | — | Invalid OAuth 2.0 Access Token | [1] Debug token at /debug_token [2] Check expiry [3] Re-authenticate |
| 190 | 458 | User changed password | User must re-login — token invalidated |
| 190 | 459 | App logged out by user | User revoked app — need re-authentication |
| 190 | 460 | Token expired | Refresh token immediately |
| 190 | 463 | Session has expired | Need new login session |
| 190 | 464 | Token was revoked | User revoked token — notify user |
| 190 | 467 | App secret changed | Update app secret in .env |

**Debug Flow for Code 190:**
```
1. Debug token: GET /debug_token?input_token={token}
2. If expired → Refresh or re-authenticate
3. If valid but failing → Check endpoint requires different token type
4. If app secret issue → Check FB_APP_SECRET matches developer console
```

### Permission Errors

| Code | Description | Debug Steps |
|------|-------------|-------------|
| 200 | Permission not granted | [1] Check permissions in /debug_token [2] Re-login with required scope |
| 200 (sub 33) | Not friends with user | Privacy setting — cannot access |
| 200 (sub 372) | Page needs `pages_show_list` | Grant `pages_show_list` permission |
| 200 (sub 298) | Session key invalid | Not using proper access_token |
| 210 | User not visible | Privacy settings — user blocks access |
| 240 | Requires Facebook Login | Need user token, not app token |

### Rate Limit Errors

| Code | Description | Debug Steps |
|------|-------------|-------------|
| 4 | Application request limit reached | [1] Check x-app-usage header [2] Reduce frequency [3] Use batch requests |
| 17 | API rate limit exceeded (user) | [1] Check x-business-use-case-usage [2] Wait for reset |
| 32 | Page rate limit exceeded | [1] Check x-page-usage [2] Reduce page-level calls |
| 341 | Feed action limit reached | Too many posts/comments — wait before more actions |
| 368 | Temporarily blocked | Repeat action too fast — wait 15-60 min |
| 613 | Calls to this API exceeded limit | [1] Implement backoff [2] Check burst limits |

**Rate Limit Detection Checklist:**
```
□ Check x-app-usage header in response
□ Check x-page-usage header in response
□ Check x-business-use-case-usage header
□ Monitor response_code in logs — 403 with code 613
□ Track call_count per endpoint per time window
□ Alert when call_count > 70% of limit
```

### Validation & Parameter Errors

| Code | Description | Debug Steps |
|------|-------------|-------------|
| 100 | Invalid parameter | [1] Check field names (case-sensitive) [2] Check data types [3] Validate required fields |
| 100 (sub 33) | Invalid format | JSON body malformed — check Content-Type header |
| 100 (sub 34) | Missing required field | Add required fields to request |
| 100 (sub 148) | Unsupported field | Field removed in this API version — check migration guide |
| 2500 | Batch request error | One or more batch requests failed — check individual responses |

**Common 100 Errors & Fixes:**
```python
# ❌ Wrong field name
"fields": "created-time"  # hyphen instead of underscore

# ✅ Correct
"fields": "created_time"

# ❌ Missing required field
POST /{page-id}/photos (no url or source)

# ✅ Required
"url": "https://example.com/photo.jpg"

# ❌ Wrong data type
"published": "true"  # string instead of boolean

# ✅ Correct
"published": True
```

---

## Request Tracing

### Logging Pattern (Sanitized)

```python
import logging
import time
import json

logger = logging.getLogger("facebook_api")

class APITracer:
    """Trace every Facebook API call with sanitized logging."""
    
    def __init__(self):
        self.session = requests.Session()
        self.stats = {
            "total_calls": 0,
            "total_latency": 0,
            "error_count": 0,
            "rate_limited_count": 0,
        }
    
    def call(self, method, url, **kwargs):
        start = time.time()
        
        # Log request (sanitized — mask token)
        debug_url = url.replace(kwargs.get("params", {}).get("access_token", ""), "***")
        logger.debug(f"→ {method} {debug_url}")
        
        try:
            resp = self.session.request(method, url, **kwargs)
            latency = time.time() - start
            
            # Log response
            logger.info(
                f"← {resp.status_code} | {latency:.2f}s | {resp.request.method} {resp.request.path_url}"
            )
            
            # Log rate limit headers
            self._log_rate_limits(resp.headers)
            
            # Track stats
            self.stats["total_calls"] += 1
            self.stats["total_latency"] += latency
            
            if resp.status_code == 429 or resp.status_code == 403:
                error_data = resp.json().get("error", {})
                if error_data.get("code") in (4, 17, 32, 613, 341, 368):
                    self.stats["rate_limited_count"] += 1
                    logger.warning(f"⚠️ RATE LIMITED | code={error_data['code']} | {error_data.get('message', '')}")
            
            if not resp.ok:
                self.stats["error_count"] += 1
                error_data = resp.json().get("error", {})
                logger.error(f"❌ API ERROR | code={error_data.get('code')} | {error_data.get('message', '')}")
            
            return resp
            
        except Exception as e:
            latency = time.time() - start
            self.stats["error_count"] += 1
            logger.error(f"💥 REQUEST FAILED | {type(e).__name__}: {e} | {latency:.2f}s")
            raise
    
    def _log_rate_limits(self, headers):
        for header in ["x-app-usage", "x-page-usage", "x-business-use-case-usage"]:
            value = headers.get(header)
            if value:
                logger.debug(f"  {header}: {value}")
                # Check thresholds
                try:
                    usage = json.loads(value)
                    if isinstance(usage, dict):
                        call_pct = usage.get("call_count", 0) / 100  # normalize
                        if call_pct > 0.7:
                            logger.warning(f"⚠️ {header} at {call_pct:.0%} capacity")
                except (json.JSONDecodeError, TypeError):
                    pass
```

---

## Debugging Specific Scenarios

### Scenario 1: "Post failed to publish"
```
Error: (#100) The parameter message is required
```

**Debug Flow:**
```
1. Check request body — is `message` included?
2. Check for empty string vs null
3. If message exists → check for disallowed characters
4. Try with simple message first: "Test"
5. Check if page is published (not unpublished)
6. Check page posting eligibility (Page Quality)
```

### Scenario 2: "Can't upload photo"
```
Error: (#100) The parameter url is required
```

**Debug Flow:**
```
1. Check `url` parameter — accessible URL?
2. Check URL returns image content type
3. Check file size limit (25MB photos, 1GB videos)
4. Try `source` parameter instead of `url` (multipart upload)
5. Check page permissions — `pages_manage_posts`
```

### Scenario 3: "Comments not showing"
```
Error: 200 OK but empty data array
```

**Debug Flow:**
```
1. Check pagination — maybe comments on next page
2. Check `filter=toplevel` — are these replies?
3. Check post exists and is visible
4. Check order parameter — chronological vs reverse
5. Check `summary=true` to get total_count
```

### Scenario 4: "Webhook not receiving events"
```
No POST received to callback URL
```

**Debug Flow:**
```
1. Check subscription in App Dashboard → Webhooks
2. Verify callback URL is HTTPS and reachable
3. Test with Graph API Explorer "Test Webhook" button
4. Check verify token matches
5. Check server logs for incoming requests (maybe blocked by firewall)
6. Check ngrok tunnel (if testing locally)
7. Check subscription fields — subscribed to correct events?
```

### Scenario 5: "Intermittent 500 errors"
```
Error: (#1) An unknown error occurred
```

**Debug Flow:**
```
1. Check Facebook status page (https://developers.facebook.com/status/)
2. Retry with exponential backoff — 500s are often transient
3. Check if specific to an endpoint or all endpoints
4. Check if specific to time of day (load-related)
5. Implement circuit breaker pattern
```

---

## Rate Limiting Detection & Response

### Headers to Monitor

```python
def check_rate_limit_headers(headers: dict) -> dict:
    """Parse Facebook rate limit headers and return status."""
    result = {}
    
    # App-level usage (percentage of limit used)
    app_usage = headers.get("x-app-usage")
    if app_usage:
        try:
            usage = json.loads(app_usage)
            call_pct = usage.get("call_count", 0) / 100
            result["app_level"] = {
                "usage_pct": call_pct,
                "status": "ok" if call_pct < 0.7 else "warning" if call_pct < 0.9 else "critical"
            }
        except json.JSONDecodeError:
            pass
    
    # Page-level usage
    page_usage = headers.get("x-page-usage")
    if page_usage:
        try:
            usage = json.loads(page_usage)
            call_pct = usage.get("call_count", 0) / 100
            result["page_level"] = {
                "usage_pct": call_pct,
                "status": "ok" if call_pct < 0.7 else "warning" if call_pct < 0.9 else "critical"
            }
        except json.JSONDecodeError:
            pass
    
    # Business-level usage
    business_usage = headers.get("x-business-use-case-usage")
    if business_usage:
        try:
            usage = json.loads(business_usage)
            if isinstance(usage, list):
                for item in usage:
                    for key, val in item.items():
                        if isinstance(val, dict):
                            call_pct = val.get("call_count", 0)
                            result[key] = {
                                "usage_pct": call_pct / 100,
                                "status": "ok" if call_pct < 70 else "warning" if call_pct < 90 else "critical"
                            }
        except json.JSONDecodeError:
            pass
    
    return result
```

### Auto-Throttle Implementation

```python
class RateLimitAwareClient:
    """Client that automatically throttles when approaching rate limits."""
    
    def __init__(self, max_per_hour: int = 190):
        self.max_per_hour = max_per_hour
        self.call_timestamps: list[float] = []
    
    def _is_throttled(self) -> bool:
        """Check if we're approaching rate limit."""
        now = time.time()
        # Keep only last hour
        self.call_timestamps = [t for t in self.call_timestamps if now - t < 3600]
        return len(self.call_timestamps) >= self.max_per_hour
    
    def _wait_if_needed(self):
        """Wait until rate limit window resets."""
        if self._is_throttled():
            oldest = min(self.call_timestamps)
            wait = 3600 - (time.time() - oldest)
            if wait > 0:
                logger.warning(f"⏳ Rate limit approaching — waiting {wait:.0f}s")
                time.sleep(wait)
    
    def call(self, *args, **kwargs):
        self._wait_if_needed()
        self.call_timestamps.append(time.time())
        return self.session.request(*args, **kwargs)
```

---

## Quick Debug Protocol

When GEMMY, KOMHAS, or SALMON reports an API issue:

```
1. ⏱️ TIMING
   When did it happen? Frequency? First time or recurring?

2. 🔍 ENDPOINT
   Which endpoint? Which parameters? Full URL (without token)?

3. 📋 RESPONSE
   Full error JSON? HTTP status code? Rate limit headers?

4. 🔐 TOKEN
   Which token type? Expiry? Permissions? (/debug_token)

5. 🔄 REPRODUCE
   Can you reproduce in Graph API Explorer?

6. 📊 PATTERN
   Single user or all users? Specific page or all pages?

7. 📢 ESCALATE
   Rate limiting? → Implement throttle
   Permission error? → Re-login
   API deprecation? → Escalate to ZION
   Facebook outage? → Monitor status page
```

---

## Debugging Quick Reference Card

```
┌─────────────────────────────────────────────────────────┐
│  DEBUG FLOW                                             │
│                                                         │
│  ERROR ─→ Inspect error code + subcode                  │
│    │                                                     │
│    ├─ code 190  ─→ Debug token → Refresh / Re-auth      │
│    ├─ code 100  ─→ Validate params → Check fields       │
│    ├─ code 200  ─→ Check permissions → Re-login         │
│    ├─ code 4,17,32,613 → Rate limited → Backoff         │
│    ├─ code 368  ─→ Temporarily blocked → Wait           │
│    ├─ code 1    ─→ Unknown → Retry → Check FB status    │
│    └─ 5xx       ─→ Server error → Retry → Escalate      │
│                                                         │
│  FIRST THINGS TO CHECK:                                 │
│  □ Token valid? (debug_token)                           │
│  □ Permissions correct? (scopes in debug_token)         │
│  □ API version current? (not deprecated)                │
│  □ Rate limit headers? (x-*-usage)                      │
│  □ Can reproduce in Explorer?                           │
└─────────────────────────────────────────────────────────┘
```
