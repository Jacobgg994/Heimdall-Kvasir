---
name: token-management
description: How to generate, store, refresh, and rotate Facebook access tokens safely
metadata:
  type: skill
  category: facebook-api
  owner: zion
---

# Token Management — Facebook Access Tokens

> Never expose tokens in code, logs, or commits.

---

## Token Types

### 1. Page Token
**Scope**: Specific Facebook Page
**Short-lived**: ~1 hour
**Long-lived**: ~60 days
**Never-expire**: Requires page re-login every 60 days

```
📋 Uses: Post to page, read page insights, manage page comments
```

### 2. User Token
**Scope**: User's granted permissions
**Short-lived**: ~1-2 hours
**Long-lived**: ~60 days
**Renewal**: User must re-login

```
📋 Uses: Discover pages (/me/accounts), user profile, email
```

### 3. App Token
**Format**: `{app-id}|{app-secret}`
**Expiry**: Never expires
**Scope**: App-level only (no user/page context)

```
📋 Uses: Server-to-server calls, app analytics
```

---

## Token Generation

### Step 1: Get Short-Lived User Token
```
# Via Graph API Explorer (manual)
https://developers.facebook.com/tools/explorer/

# Via OAuth dialog (programmatic)
GET https://www.facebook.com/v21.0/dialog/oauth
  ?client_id={app-id}
  &redirect_uri={redirect-uri}
  &scope=pages_manage_posts,pages_read_engagement,public_profile
  &response_type=token
```

### Step 2: Exchange for Long-Lived User Token
```
GET graph.facebook.com/v21.0/oauth/access_token
  ?grant_type=fb_exchange_token
  &client_id={app-id}
  &client_secret={app-secret}
  &fb_exchange_token={short-lived-token}
```

**Response:**
```json
{
  "access_token": "EAA...long-lived-token...ZD",
  "token_type": "bearer",
  "expires_in": 5184000  (60 days in seconds)
}
```

### Step 3: Get Page Tokens
```
GET graph.facebook.com/v21.0/me/accounts
  ?access_token={long-lived-user-token}
```

**Response:**
```json
{
  "data": [
    {
      "id": "123456789",
      "name": "My Page",
      "access_token": "EAA...page-token...ZD",
      "category": "Software"
    }
  ]
}
```

---

## Token Storage (Production)

### DO NOT
```
# ❌ NEVER in code
FB_PAGE_TOKEN = "EAA..."

# ❌ NEVER in logs
logger.info(f"Token: {token}")

# ❌ NEVER in git
# .env files committed to repo
```

### DO — Environment Variables
```bash
# .env (in .gitignore!)
FB_APP_ID=123456789
FB_APP_SECRET=abc123def456
FB_PAGE_TOKEN=EAA...
FB_USER_TOKEN=EAA...
FB_API_VERSION=v21.0
```

```python
import os
from dotenv import load_dotenv

load_dotenv()

FB_PAGE_TOKEN = os.environ["FB_PAGE_TOKEN"]
FB_APP_ID = os.environ["FB_APP_ID"]
```

### DO — Encrypted Vault
```python
# Example with python-dotenv + system keyring
import keyring

def get_token(page_id: str) -> str:
    """Get encrypted token from system keyring."""
    return keyring.get_password("facebook-page-tokens", page_id)

def set_token(page_id: str, token: str):
    """Store encrypted token in system keyring."""
    keyring.set_password("facebook-page-tokens", page_id, token)
```

---

## Token Refresh

### Check Token Validity
```
GET graph.facebook.com/v21.0/debug_token
  ?input_token={token-to-check}
  &access_token={app-token}
```

**Response:**
```json
{
  "data": {
    "app_id": "123456789",
    "type": "PAGE",
    "application": "My App",
    "expires_at": 1761331200,  (timestamp)
    "is_valid": true,
    "issued_at": 1739808000,
    "scopes": ["pages_manage_posts", "pages_read_engagement"],
    "user_id": "987654321",
    "page_id": "123456789"
  }
}
```

### Refresh Logic (Python)

```python
import os
import time
import requests
from datetime import datetime, timedelta

class TokenManager:
    def __init__(self):
        self.api_version = os.environ["FB_API_VERSION"]
        self.app_id = os.environ["FB_APP_ID"]
        self.app_secret = os.environ["FB_APP_SECRET"]
    
    def debug_token(self, token: str) -> dict:
        url = f"https://graph.facebook.com/{self.api_version}/debug_token"
        resp = requests.get(url, params={
            "input_token": token,
            "access_token": f"{self.app_id}|{self.app_secret}"
        })
        resp.raise_for_status()
        return resp.json()["data"]
    
    def token_expires_in_days(self, token: str) -> int:
        info = self.debug_token(token)
        expires_at = info.get("expires_at", 0)
        if expires_at == 0:
            return -1  # never expires (app token)
        remaining = expires_at - int(time.time())
        return max(0, remaining // 86400)
    
    def needs_refresh(self, token: str, days_before: int = 7) -> bool:
        remaining = self.token_expires_in_days(token)
        return remaining < days_before and remaining >= 0
    
    def refresh_user_token(self, current_token: str) -> str:
        """Exchange for a new long-lived user token."""
        url = f"https://graph.facebook.com/{self.api_version}/oauth/access_token"
        resp = requests.get(url, params={
            "grant_type": "fb_exchange_token",
            "client_id": self.app_id,
            "client_secret": self.app_secret,
            "fb_exchange_token": current_token
        })
        resp.raise_for_status()
        return resp.json()["access_token"]
    
    def refresh_page_token(self, user_token: str, page_id: str) -> str:
        """Get fresh page token via /me/accounts."""
        url = f"https://graph.facebook.com/{self.api_version}/me/accounts"
        resp = requests.get(url, params={
            "access_token": user_token
        })
        resp.raise_for_status()
        accounts = resp.json()["data"]
        for account in accounts:
            if account["id"] == page_id:
                return account["access_token"]
        raise ValueError(f"Page {page_id} not found in accounts")
```

---

## Scheduled Refresh

### Daily Token Health Check (Cron)
```bash
# crontab — run daily at 02:00
0 2 * * * cd /path/to/app && python -m scripts.check_tokens
```

### Check Script
```python
# scripts/check_tokens.py
import os
from token_manager import TokenManager

tm = TokenManager()

pages = {
    "page_1": os.environ["FB_PAGE_1_ID"],
    "page_2": os.environ["FB_PAGE_2_ID"],
}

for name, page_id in pages.items():
    token = os.environ[f"FB_PAGE_{name.upper()}_TOKEN"]
    days = tm.token_expires_in_days(token)
    
    if days < 0:
        print(f"[OK] {name}: App token (never expires)")
    elif days > 14:
        print(f"[OK] {name}: {days} days remaining")
    elif days > 7:
        print(f"[WARN] {name}: {days} days remaining — refresh soon")
    else:
        print(f"[ALERT] {name}: {days} days remaining — REFRESH NOW")
```

---

## Token Rotation (Emergency)

### If Token is Compromised
1. **Immediately rotate**: Generate new token via Graph API Explorer
2. **Revoke old token**:
   ```
   DELETE graph.facebook.com/v21.0/me/permissions
     ?access_token={compromised-token}
   ```
3. **Reset app secret** (Extreme): Facebook Developer Console → App → Settings → Basic → Reset App Secret
4. **Audit logs**: Check for unauthorized API calls
5. **Notify JIMMY**: Report scope of exposure

### Automated Rotation (Scheduled)
```python
def rotate_all_tokens():
    """Rotate all page tokens every 45 days."""
    tm = TokenManager()
    user_token = os.environ["FB_USER_TOKEN"]
    
    # Refresh user token
    new_user_token = tm.refresh_user_token(user_token)
    
    # Get fresh page tokens
    url = f"https://graph.facebook.com/{tm.api_version}/me/accounts"
    resp = requests.get(url, params={"access_token": new_user_token})
    accounts = resp.json()["data"]
    
    for account in accounts:
        # Store fresh token securely
        set_token(account["id"], account["access_token"])
    
    # Update env variable for user token
    set_token("user", new_user_token)
    print(f"✅ Rotated {len(accounts)} page tokens + 1 user token")
```

---

## Token Security Checklist

```
□ 1.  All tokens stored in environment variables or encrypted vault
□ 2.  .env added to .gitignore — never committed
□ 3.  Logs are sanitized — no token output (use "Bearer ***")
□ 4.  Token refresh runs daily via cron
□ 5.  Alert 14 days before token expiry
□ 6.  Auto-refresh 7 days before token expiry
□ 7.  Emergency rotation script accessible
□ 8.  App secret stored separately from app ID
□ 9.  Token debug tool available for manual check
□ 10. Rate limit headers monitored alongside token health
```

---

## Common Token Issues

| Symptom | Error Code | Cause | Fix |
|---------|-----------|-------|-----|
| `Invalid OAuth Access Token` | 190 | Token expired | Refresh token |
| `Invalid OAuth 2.0 Access Token` | 190 subcode 458 | User changed password | Re-authenticate user |
| `(#200) Permission error` | 200 | Token lacks scope | Re-login with correct scope |
| `Error validating access token` | 190 subcode 467 | App secret changed | Update app secret |
| `Session has expired` | 190 subcode 463 | Token revoked by user | Re-authenticate |
| `Unsupported get request` | 100 | Page ID mismatch | Check which page token belongs to |
