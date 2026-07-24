---
name: webhook-setup
description: Facebook webhook configuration for real-time page events, callback URL setup, verify token
metadata:
  type: skill
  category: facebook-api
  owner: zion
---

# Webhook Setup — Facebook Real-Time Events

> Receive real-time updates when things happen on your Facebook Pages.

---

## Overview

Facebook Webhooks deliver real-time HTTP POST notifications when subscribed events occur (new post, comment, lead, etc.). No polling needed — the event comes to you.

```
┌──────────┐     POST     ┌────────────┐
│ Facebook │ ───────────→ │ Your Server │
│  Graph   │   (event)    │  (callback) │
│   API    │ ← ─────────── │            │
└──────────┘    OK 200    └────────────┘
```

---

## Architecture

### Webhook Flow
```
1. Facebook → POST /webhook/callback  (event notification)
2. Server responds 200 OK within 5 seconds
3. Server processes event (or queues for async processing)
4. Facebook retries with exponential backoff if no 200
```

### When to Use Webhooks vs Polling

| Scenario | Webhook | Polling |
|----------|---------|---------|
| New page posts | ✅ | Redundant |
| Comments on posts | ✅ | Redundant |
| Page likes | ✅ | Can poll insights |
| Message/conversation | ✅ | Can poll `/conversations` |
| Leadgen leads | ✅ | Must use webhook |
| Historical data | ❌ | ✅ Use GET |
| High frequency (>100/min) | ✅ Low latency | ❌ Rate limit risk |
| Testing/development | ❌ | ✅ Simpler to debug |

---

## Setup Steps

### Step 1: Configure Webhook in Facebook App

1. **Go to**: Facebook Developer Console → [Your App] → Webhooks
2. **Add Product**: If not visible, add "Webhooks" from product catalog
3. **Select Page**: Click "Subscribe to this object" → "Page"

### Step 2: Callback URL Setup

```
https://your-server.com/webhook/facebook
```

**Requirements:**
- HTTPS only (valid SSL cert — Let's Encrypt, Cloudflare, etc.)
- Respond with `hub.challenge` on GET verification
- Respond within 5 seconds on POST events
- Port 443 (standard HTTPS)

### Step 3: Verify Token

Generate a unique verify token (long, random, never reused):

```python
import secrets

# Generate once — store in .env
verify_token = secrets.token_urlsafe(32)
print(verify_token)
# Example: "x7gR3kL9pQ2mN5vB8wC1zX4yA6dF0jH8"
```

**Store in environment:**
```bash
FB_WEBHOOK_VERIFY_TOKEN=x7gR3kL9pQ2mN5vB8wC1zX4yA6dF0jH8
```

### Step 4: Verification Endpoint (GET)

```python
# fastapi_example.py
from fastapi import FastAPI, Query, HTTPException
import os

app = FastAPI()
VERIFY_TOKEN = os.environ["FB_WEBHOOK_VERIFY_TOKEN"]

@app.get("/webhook/facebook")
async def verify_webhook(
    hub_mode: str = Query(alias="hub.mode"),
    hub_verify_token: str = Query(alias="hub.verify_token"),
    hub_challenge: str = Query(alias="hub.challenge"),
):
    """
    Facebook sends GET request to verify callback URL.
    Must respond with hub.challenge value if verify_token matches.
    """
    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        return int(hub_challenge)  # Return challenge as plain text
    raise HTTPException(status_code=403, detail="Verify token mismatch")
```

### Step 5: Event Handler (POST)

```python
from fastapi import Request

@app.post("/webhook/facebook")
async def handle_webhook(request: Request):
    """Receive real-time events from Facebook."""
    body = await request.json()
    
    # Verify this is for Page
    if body.get("object") != "page":
        return {"status": "ignored"}
    
    # Process each entry
    for entry in body.get("entry", []):
        page_id = entry.get("id")
        timestamp = entry.get("time")
        
        # Handle changes based on field
        for change in entry.get("changes", []):
            field = change.get("field")
            value = change.get("value")
            
            if field == "feed":
                await handle_feed_event(page_id, value)
            elif field == "comments":
                await handle_comment_event(page_id, value)
            elif field == "conversations":
                await handle_message_event(page_id, value)
            elif field == "leadgen":
                await handle_lead_event(page_id, value)
            elif field == "likes":
                await handle_like_event(page_id, value)
    
    # MUST respond 200 within 5 seconds
    return {"status": "ok"}
```

---

## Event Types

### Feed (New Post)
```json
{
  "field": "feed",
  "value": {
    "item": "post",
    "post_id": "123_456",
    "message": "New post content",
    "created_time": 1721812800,
    "is_published": true,
    "photo_ids": ["789012"],
    "video_ids": []
  }
}
```

### Comments
```json
{
  "field": "comments",
  "value": {
    "item": "comment",
    "post_id": "123_456",
    "comment_id": "789_012",
    "from_id": "user_123",
    "from_name": "John Doe",
    "message": "Great post!",
    "created_time": 1721812900,
    "parent_id": null
  }
}
```

### Conversations (Messages)
```json
{
  "field": "conversations",
  "value": {
    "item": "message",
    "conversation_id": "mcid_123",
    "message_id": "mid_456",
    "sender_id": "user_789",
    "message": "Hello, I have a question",
    "created_time": 1721813000
  }
}
```

### Leadgen (Leads)
```json
{
  "field": "leadgen",
  "value": {
    "leadgen_id": "lead_123",
    "page_id": "page_456",
    "form_id": "form_789",
    "created_time": 1721813100
  }
}
```

### Page Likes
```json
{
  "field": "likes",
  "value": {
    "item": "like",
    "user_id": "user_123",
    "user_name": "John Doe"
  }
}
```

---

## Subscription Management

### Subscribe to Page Events
```
POST graph.facebook.com/v21.0/{app-id}/subscriptions
  ?access_token={app-token}
  &object=page
  &callback_url=https://your-server.com/webhook/facebook
  &verify_token={verify-token}
  &fields=feed,comments,conversations,leadgen,likes
```

### List Subscriptions
```
GET graph.facebook.com/v21.0/{app-id}/subscriptions
  ?access_token={app-token}
```

### Unsubscribe
```
DELETE graph.facebook.com/v21.0/{app-id}/subscriptions
  ?access_token={app-token}
  &object=page
```

---

## Server Implementation Patterns

### Pattern A: FastAPI (Recommended)
```python
from fastapi import FastAPI, Request, HTTPException, Query
import os
import json
import hmac
import hashlib

app = FastAPI()
VERIFY_TOKEN = os.environ["FB_WEBHOOK_VERIFY_TOKEN"]
APP_SECRET = os.environ["FB_APP_SECRET"]

@app.get("/webhook/facebook")
async def verify(hub_mode: str = Query(alias="hub.mode"),
                 hub_verify_token: str = Query(alias="hub.verify_token"),
                 hub_challenge: str = Query(alias="hub.challenge")):
    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        return int(hub_challenge)
    raise HTTPException(403, "Token mismatch")

@app.post("/webhook/facebook")
async def webhook(request: Request):
    body = await request.body()
    
    # Optional: Verify signature (recommended for production)
    signature = request.headers.get("x-hub-signature-256", "")
    if not verify_signature(body, signature):
        raise HTTPException(401, "Invalid signature")
    
    data = json.loads(body)
    
    if data.get("object") != "page":
        return {"status": "ignored"}
    
    # Process in background — respond 200 immediately
    import asyncio
    asyncio.create_task(process_events(data))
    
    return {"status": "ok"}

def verify_signature(payload: bytes, signature: str) -> bool:
    """Verify request came from Facebook."""
    expected = "sha256=" + hmac.new(
        APP_SECRET.encode(), payload, hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature)
```

### Pattern B: Flask
```python
from flask import Flask, request, abort
import os

app = Flask(__name__)
VERIFY_TOKEN = os.environ["FB_WEBHOOK_VERIFY_TOKEN"]

@app.route("/webhook/facebook", methods=["GET"])
def verify():
    if request.args.get("hub.mode") == "subscribe" and \
       request.args.get("hub.verify_token") == VERIFY_TOKEN:
        return request.args["hub.challenge"], 200
    abort(403)

@app.route("/webhook/facebook", methods=["POST"])
def webhook():
    data = request.json
    if data.get("object") == "page":
        # Process events
        pass
    return {"status": "ok"}, 200
```

### Pattern C: Django
```python
# views.py
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os

VERIFY_TOKEN = os.environ["FB_WEBHOOK_VERIFY_TOKEN"]

@csrf_exempt
def facebook_webhook(request):
    if request.method == "GET":
        if request.GET.get("hub.mode") == "subscribe" and \
           request.GET.get("hub.verify_token") == VERIFY_TOKEN:
            return HttpResponse(request.GET["hub.challenge"])
        return HttpResponse(status=403)
    
    elif request.method == "POST":
        data = json.loads(request.body)
        # Process events
        return JsonResponse({"status": "ok"})
```

---

## Event Processing Best Practices

### 1. Respond Fast (5-second rule)
```python
# GOOD: Respond 200 immediately, process async
asyncio.create_task(process_events(data))
return {"status": "ok"}

# BAD: Blocking the response
await slow_processing(data)
return {"status": "ok"}
```

### 2. Idempotent Processing
```python
processed_ids = set()  # Redis or DB-backed

async def process_events(data):
    for entry in data.get("entry", []):
        for change in entry.get("changes", []):
            # Use idempotency key
            event_id = f"{entry['id']}_{change.get('value', {}).get('post_id', '')}"
            if event_id in processed_ids:
                continue
            processed_ids.add(event_id)
            # Process event...
```

### 3. Queue for Heavy Processing
```python
# Use Redis queue, RabbitMQ, or in-memory queue
async def webhook_handler(data):
    await queue.enqueue("process_webhook_event", data)
    return {"status": "ok"}
```

### 4. Dead Letter Queue for Failures
```python
MAX_RETRIES = 3

async def process_with_retry(event_data, retry_count=0):
    try:
        await process_event(event_data)
    except Exception as e:
        if retry_count < MAX_RETRIES:
            await asyncio.sleep(2 ** retry_count)  # exponential backoff
            await process_with_retry(event_data, retry_count + 1)
        else:
            await dead_letter_queue.put(event_data)
```

---

## Webhook Verification & Security

### Facebook App Secret Proof (appsecret_proof)
Every webhook POST can include `X-Hub-Signature-256` header. Verify it:

```python
def verify_webhook_signature(payload: bytes, signature: str, app_secret: str) -> bool:
    expected = "sha256=" + hmac.new(
        app_secret.encode(), payload, hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature)
```

### IP Whitelist (Optional)
Facebook webhooks come from known IP ranges. Whitelist them for extra security:
```
https://developers.facebook.com/docs/graph-api/webhooks/getting-started#ip-addresses
```

---

## Testing Webhooks

### Facebook Test Tool
1. **Graph API Explorer**: Send test POST to your webhook
2. **Webhooks Dashboard**: Developer Console → Webhooks → "Test" button
3. **Page changes**: Perform real action on page (post, comment) → webhook fires

### Local Development (ngrok)
```bash
# Expose local server to internet
ngrok http 8000

# Output:
# Forwarding https://abc123.ngrok.io → http://localhost:8000

# Use https://abc123.ngrok.io/webhook/facebook as callback URL
```

### Webhook Simulator (Python Test)
```python
import requests
import json

def simulate_webhook(callback_url, event_type="feed"):
    """Send a test webhook event to your callback."""
    payload = {
        "object": "page",
        "entry": [{
            "id": "test_page_123",
            "time": 1721812800,
            "changes": [{
                "field": event_type,
                "value": {
                    "item": "post",
                    "post_id": "test_123_456",
                    "message": "Test webhook event",
                    "created_time": 1721812800,
                    "is_published": True
                }
            }]
        }]
    }
    resp = requests.post(callback_url, json=payload)
    return resp.status_code, resp.text

# Test
code, text = simulate_webhook("https://abc123.ngrok.io/webhook/facebook")
print(f"Status: {code}, Response: {text}")
```

---

## Webhook Setup Checklist

```
□ 1.  Callback URL uses HTTPS with valid SSL certificate
□ 2.  Verify token generated (secrets.token_urlsafe(32))
□ 3.  GET endpoint returns hub.challenge on matching verify_token
□ 4.  POST endpoint responds 200 within 5 seconds
□ 5.  Signature verification implemented (X-Hub-Signature-256)
□ 6.  Events processed asynchronously (not blocking response)
□ 7.  Idempotency key prevents duplicate processing
□ 8.  Dead letter queue for failed events (max 3 retries)
□ 9.  ngrok available for local development
□ 10. Subscribed to relevant fields only (not all fields)
□ 11. Monitoring on webhook response time and error rate
□ 12. Fallback polling strategy if webhook misses events
```

---

## Fallback: Polling Strategy

If webhooks are unreliable, implement polling as backup:

```python
import requests
import time

class WebhookFallback:
    """Poll for missed events if webhook gaps detected."""
    
    def __init__(self, page_id, token, interval=300):
        self.page_id = page_id
        self.token = token
        self.interval = interval
        self.last_check = int(time.time())
    
    def poll_missed_events(self):
        """Check for events since last poll."""
        since = self.last_check
        self.last_check = int(time.time())
        
        url = f"https://graph.facebook.com/v21.0/{self.page_id}/feed"
        params = {
            "access_token": self.token,
            "since": since,
            "fields": "id,message,created_time,comments{id,message,created_time}",
            "limit": 100
        }
        
        resp = requests.get(url, params=params)
        if resp.status_code == 200:
            return resp.json().get("data", [])
        return []
```

---

## Rate Limits & Webhook

- Webhook events do NOT count toward API rate limits
- Maximum 1 webhook subscription per app per object type
- Facebook may batch multiple events into a single POST
- Webhook delivery expected within seconds (but not guaranteed SLA)
- If server is down, Facebook retries with exponential backoff up to ~24 hours
