---
name: python-facebook-sdk
description: Building a Python SDK wrapper for Facebook Graph API using requests/httpx, async support, pagination handling
metadata:
  type: skill
  category: facebook-api
  owner: lyra
---

# Python Facebook Graph API SDK

> A clean, typed SDK wrapper for the Facebook Graph API.

---

## SDK Architecture

```
facebook_sdk/
├── __init__.py          # Public API
├── client.py            # Base HTTP client
├── page.py              # Page operations
├── post.py              # Post operations
├── comment.py           # Comment operations
├── media.py             # Photo/video operations
├── insights.py          # Analytics operations
├── conversation.py      # Message operations
├── models.py            # Pydantic response models
├── errors.py            # Custom exceptions
├── token_manager.py     # Token refresh logic
└── utils.py             # Pagination, rate limiting
```

---

## Base Client

### Sync Client (requests)

```python
"""client.py — Base HTTP Client (sync)"""

import os
import time
import logging
import requests
from typing import Optional, Dict, Any
from .errors import FacebookAPIError, RateLimitError, TokenExpiredError

logger = logging.getLogger("facebook_sdk")

class FacebookClient:
    """Synchronous Facebook Graph API client."""
    
    BASE_URL = "https://graph.facebook.com"
    
    def __init__(
        self,
        access_token: Optional[str] = None,
        api_version: str = "v21.0",
        timeout: int = 30,
        max_retries: int = 3,
    ):
        self.access_token = access_token or os.environ.get("FB_PAGE_TOKEN")
        self.api_version = api_version or os.environ.get("FB_API_VERSION", "v21.0")
        self.timeout = timeout
        self.max_retries = max_retries
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": f"FacebookSDK/Python/{api_version}"
        })
        
        # Rate limit tracking
        self._call_timestamps: list[float] = []
        self._max_calls_per_hour = 190
    
    def _build_url(self, endpoint: str) -> str:
        endpoint = endpoint.lstrip("/")
        return f"{self.BASE_URL}/{self.api_version}/{endpoint}"
    
    def _handle_response(self, resp: requests.Response) -> dict:
        """Process API response and raise typed errors."""
        if resp.status_code == 200:
            data = resp.json()
            # Check for error in response body
            if "error" in data:
                self._raise_error(data["error"], resp.status_code)
            return data
        
        try:
            error_data = resp.json().get("error", {})
        except (ValueError, KeyError):
            error_data = {}
        
        self._raise_error(error_data, resp.status_code)
    
    def _raise_error(self, error: dict, status_code: int):
        code = error.get("code", 0)
        message = error.get("message", "Unknown error")
        subcode = error.get("error_subcode")
        fbtrace = error.get("fbtrace_id", "")
        
        if code == 190:
            raise TokenExpiredError(message, code, subcode, fbtrace)
        elif code in (4, 17, 32, 341, 368, 613):
            raise RateLimitError(message, code, subcode, fbtrace, status_code)
        else:
            raise FacebookAPIError(message, code, subcode, fbtrace, status_code)
    
    def _check_rate_limit(self):
        """Ensure we don't exceed rate limits."""
        now = time.time()
        self._call_timestamps = [t for t in self._call_timestamps if now - t < 3600]
        
        if len(self._call_timestamps) >= self._max_calls_per_hour:
            oldest = min(self._call_timestamps)
            wait = 3600 - (now - oldest)
            if wait > 0:
                logger.warning(f"⏳ Rate limit reached — waiting {wait:.0f}s")
                time.sleep(wait)
    
    def _update_rate_limits(self, headers: Dict[str, str]):
        """Parse and log rate limit headers."""
        for header in ["x-app-usage", "x-page-usage"]:
            value = headers.get(header)
            if value and hasattr(self, "_on_rate_limit_update"):
                self._on_rate_limit_update(header, value)
    
    def request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        data: Optional[Dict] = None,
        files: Optional[Dict] = None,
    ) -> dict:
        """Make an API request with retry logic."""
        url = self._build_url(endpoint)
        params = params or {}
        
        if self.access_token:
            params["access_token"] = self.access_token
        
        self._check_rate_limit()
        
        last_error = None
        for attempt in range(self.max_retries):
            try:
                resp = self.session.request(
                    method=method,
                    url=url,
                    params=params,
                    json=data if data and not files else None,
                    data=data if files else None,
                    files=files,
                    timeout=self.timeout,
                )
                self._call_timestamps.append(time.time())
                self._update_rate_limits(resp.headers)
                
                logger.debug(
                    f"{method} {endpoint} → {resp.status_code} "
                    f"({time.time() - self._call_timestamps[-1]:.2f}s)"
                )
                
                return self._handle_response(resp)
                
            except (requests.ConnectionError, requests.Timeout) as e:
                last_error = e
                wait = 2 ** attempt
                logger.warning(f"⏳ Connection error, retrying in {wait}s (attempt {attempt + 1})")
                time.sleep(wait)
            except RateLimitError as e:
                # Extract retry-after from headers
                wait = min(2 ** attempt * 30, 300)  # max 5 min
                logger.warning(f"⏳ Rate limited, waiting {wait}s (attempt {attempt + 1})")
                time.sleep(wait)
                last_error = e  # Don't swallow rate limit errors
                if attempt == self.max_retries - 1:
                    raise
        
        raise FacebookAPIError(
            f"Request failed after {self.max_retries} retries: {last_error}",
            status_code=0
        )
    
    # Convenience methods
    def get(self, endpoint: str, params: Optional[Dict] = None) -> dict:
        return self.request("GET", endpoint, params=params)
    
    def post(self, endpoint: str, data: Optional[Dict] = None, files: Optional[Dict] = None) -> dict:
        return self.request("POST", endpoint, data=data, files=files)
    
    def delete(self, endpoint: str, params: Optional[Dict] = None) -> dict:
        return self.request("DELETE", endpoint, params=params)
```

### Async Client (httpx)

```python
"""async_client.py — Async HTTP Client"""

import os
import asyncio
import logging
import httpx
from typing import Optional, Dict, Any
from .errors import FacebookAPIError, RateLimitError, TokenExpiredError

logger = logging.getLogger("facebook_sdk")

class AsyncFacebookClient:
    """Asynchronous Facebook Graph API client using httpx."""
    
    BASE_URL = "https://graph.facebook.com"
    
    def __init__(
        self,
        access_token: Optional[str] = None,
        api_version: str = "v21.0",
        timeout: int = 30,
        max_retries: int = 3,
        max_connections: int = 10,
    ):
        self.access_token = access_token or os.environ.get("FB_PAGE_TOKEN")
        self.api_version = api_version or os.environ.get("FB_API_VERSION", "v21.0")
        self.timeout = timeout
        self.max_retries = max_retries
        
        self.client = httpx.AsyncClient(
            timeout=httpx.Timeout(timeout),
            limits=httpx.Limits(
                max_connections=max_connections,
                max_keepalive_connections=max_connections,
            ),
            headers={"User-Agent": f"FacebookSDK/Python/{api_version}/async"},
        )
        
        # Rate limit tracking
        self._call_timestamps: list[float] = []
        self._max_calls_per_hour = 190
        self._lock = asyncio.Lock()
    
    async def _build_url(self, endpoint: str) -> str:
        endpoint = endpoint.lstrip("/")
        return f"{self.BASE_URL}/{self.api_version}/{endpoint}"
    
    async def _check_rate_limit(self):
        async with self._lock:
            now = time.time()
            self._call_timestamps = [t for t in self._call_timestamps if now - t < 3600]
            
            if len(self._call_timestamps) >= self._max_calls_per_hour:
                oldest = min(self._call_timestamps)
                wait = 3600 - (now - oldest)
                if wait > 0:
                    logger.warning(f"⏳ Rate limit reached — waiting {wait:.0f}s")
                    await asyncio.sleep(wait)
    
    async def request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        data: Optional[Dict] = None,
        files: Optional[Dict] = None,
    ) -> dict:
        """Make async API request with retry logic."""
        url = await self._build_url(endpoint)
        params = params or {}
        
        if self.access_token:
            params["access_token"] = self.access_token
        
        await self._check_rate_limit()
        
        last_error = None
        for attempt in range(self.max_retries):
            try:
                async with self.client.stream(
                    method=method,
                    url=url,
                    params=params,
                    json=data if data and not files else None,
                    data=data if files else None,
                    files=files,
                ) as resp:
                    await resp.aread()
                    async with self._lock:
                        self._call_timestamps.append(time.time())
                    
                    return self._handle_response(resp)
                    
            except (httpx.ConnectError, httpx.TimeoutException) as e:
                last_error = e
                wait = 2 ** attempt
                await asyncio.sleep(wait)
            except RateLimitError:
                wait = min(2 ** attempt * 30, 300)
                await asyncio.sleep(wait)
                last_error = None  # Retry after backoff
                if attempt == self.max_retries - 1:
                    raise
        
        raise FacebookAPIError(
            f"Async request failed after {self.max_retries} retries",
            status_code=0
        )
    
    def _handle_response(self, resp: httpx.Response) -> dict:
        """Process async response."""
        if resp.status_code == 200:
            data = resp.json()
            if "error" in data:
                self._raise_error(data["error"])
            return data
        
        try:
            error_data = resp.json().get("error", {})
        except (ValueError, KeyError):
            error_data = {}
        
        self._raise_error(error_data)
    
    async def close(self):
        await self.client.aclose()
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, *args):
        await self.close()
```

---

## Error Handling

```python
"""errors.py — Custom exceptions"""

class FacebookAPIError(Exception):
    """Base exception for Facebook API errors."""
    def __init__(self, message: str, code: int = 0, subcode: int = None,
                 fbtrace_id: str = "", status_code: int = 0):
        self.code = code
        self.subcode = subcode
        self.fbtrace_id = fbtrace_id
        self.status_code = status_code
        super().__init__(self._format_message(message))
    
    def _format_message(self, message: str) -> str:
        parts = [f"[{self.code}]" if self.code else ""]
        if self.subcode:
            parts.append(f"({self.subcode})")
        parts.append(message)
        parts.append(f"(trace: {self.fbtrace_id})" if self.fbtrace_id else "")
        return " ".join(filter(None, parts))

class TokenExpiredError(FacebookAPIError):
    """Token has expired or is invalid."""
    pass

class RateLimitError(FacebookAPIError):
    """API rate limit exceeded."""
    pass

class PermissionError(FacebookAPIError):
    """Insufficient permissions."""
    pass
```

---

## Response Models

```python
"""models.py — Pydantic models for API responses"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class PageInfo(BaseModel):
    id: str
    name: str
    about: Optional[str] = None
    fan_count: Optional[int] = None
    link: Optional[str] = None
    username: Optional[str] = None
    access_token: Optional[str] = None

class Post(BaseModel):
    id: str
    message: Optional[str] = None
    created_time: Optional[str] = None
    permalink_url: Optional[str] = None
    full_picture: Optional[str] = None
    is_published: Optional[bool] = None
    shares: Optional[dict] = None
    comments: Optional[dict] = None
    likes: Optional[dict] = None

class Comment(BaseModel):
    id: str
    message: Optional[str] = None
    from_field: Optional[dict] = Field(None, alias="from")
    created_time: Optional[str] = None
    like_count: Optional[int] = None
    parent: Optional[dict] = None
    attachment: Optional[dict] = None
    
    class Config:
        populate_by_name = True
        allow_population_by_field_name = True

class InsightMetric(BaseModel):
    name: str
    period: str
    values: List[dict]
    title: Optional[str] = None
    description: Optional[str] = None

class PaginatedResponse(BaseModel):
    data: List[dict]
    paging: Optional[dict] = None
```

---

## Pagination Handler

```python
"""utils.py — Pagination utilities"""

from typing import Iterator, List, Optional, Dict, Any
import logging

logger = logging.getLogger("facebook_sdk")

class Paginator:
    """
    Handle cursor-based pagination for Facebook Graph API.
    
    Usage:
        client = FacebookClient(token)
        paginator = Paginator(client)
        for post in paginator.all_pages(f"{page_id}/posts", params={"fields": "id,message"}):
            print(post)
    """
    
    def __init__(self, client, max_pages: int = 100):
        self.client = client
        self.max_pages = max_pages
    
    def all_pages(
        self,
        endpoint: str,
        params: Optional[Dict] = None,
    ) -> Iterator[dict]:
        """Iterate over all pages of a paginated endpoint."""
        params = params or {}
        params["limit"] = params.get("limit", 100)
        
        page_count = 0
        url = endpoint
        
        while url and page_count < self.max_pages:
            data = self.client.get(url, params=params if page_count == 0 else {})
            page_count += 1
            
            # Yield items
            for item in data.get("data", []):
                yield item
            
            # Check for next page
            paging = data.get("paging", {})
            url = paging.get("next")
            
            # Clear params after first request (cursor in URL)
            params = {}
        
        if page_count >= self.max_pages:
            logger.warning(f"Reached max pages ({self.max_pages}) for {endpoint}")
    
    def all_pages_async(self, client, endpoint: str, params: Optional[Dict] = None):
        """Async version — requires AsyncFacebookClient."""
        # Similar pattern with async/await
        pass


class BatchPaginator:
    """
    Collect all items from all pages into a list.
    Warning: Can be memory-intensive for large datasets.
    """
    
    def collect_all(self, client, endpoint: str, params: Optional[Dict] = None) -> List[dict]:
        results = []
        for item in Paginator(client).all_pages(endpoint, params):
            results.append(item)
        return results
```

---

## Domain Operations

### Page Operations

```python
"""page.py — Page management"""

from typing import Optional, List
from .client import FacebookClient
from .models import PageInfo, PaginatedResponse

class PageAPI:
    """Operations on Facebook Pages."""
    
    def __init__(self, client: FacebookClient):
        self.client = client
    
    def get_info(self, page_id: str, fields: Optional[List[str]] = None) -> dict:
        """Get page information."""
        params = {}
        if fields:
            params["fields"] = ",".join(fields)
        return self.client.get(f"{page_id}", params=params)
    
    def get_posts(
        self,
        page_id: str,
        fields: Optional[List[str]] = None,
        limit: int = 25,
        before: Optional[str] = None,
        after: Optional[str] = None,
    ) -> dict:
        """Get page posts with cursor-based pagination."""
        params = {
            "limit": limit,
        }
        if fields:
            params["fields"] = ",".join(fields)
        if before:
            params["before"] = before
        if after:
            params["after"] = after
        return self.client.get(f"{page_id}/posts", params=params)
    
    def create_post(
        self,
        page_id: str,
        message: str,
        link: Optional[str] = None,
        published: bool = True,
        scheduled_publish_time: Optional[int] = None,
    ) -> dict:
        """Create a new page post."""
        data = {
            "message": message,
            "published": str(published).lower(),
        }
        if link:
            data["link"] = link
        if scheduled_publish_time:
            data["published"] = "false"
            data["scheduled_publish_time"] = scheduled_publish_time
        return self.client.post(f"{page_id}/posts", data=data)
    
    def get_insights(
        self,
        page_id: str,
        metrics: List[str],
        period: str = "day",
        since: Optional[str] = None,
        until: Optional[str] = None,
    ) -> dict:
        """Get page insights."""
        params = {
            "metric": ",".join(metrics),
            "period": period,
        }
        if since:
            params["since"] = since
        if until:
            params["until"] = until
        return self.client.get(f"{page_id}/insights", params=params)
```

### Post Operations

```python
"""post.py — Post management"""

from typing import Optional, List
from .client import FacebookClient

class PostAPI:
    """Operations on Facebook Page Posts."""
    
    def __init__(self, client: FacebookClient):
        self.client = client
    
    def get(self, post_id: str, fields: Optional[List[str]] = None) -> dict:
        """Get a single post."""
        params = {}
        if fields:
            params["fields"] = ",".join(fields)
        return self.client.get(post_id, params=params)
    
    def get_comments(
        self,
        post_id: str,
        fields: Optional[List[str]] = None,
        order: str = "chronological",
        filter: str = "toplevel",
        limit: int = 50,
    ) -> dict:
        """Get comments on a post."""
        params = {
            "order": order,
            "filter": filter,
            "limit": limit,
        }
        if fields:
            params["fields"] = ",".join(fields)
        return self.client.get(f"{post_id}/comments", params=params)
    
    def create_comment(self, post_id: str, message: str) -> dict:
        """Reply to a post."""
        return self.client.post(f"{post_id}/comments", data={"message": message})
    
    def get_likes(self, post_id: str, summary: bool = True, limit: int = 100) -> dict:
        """Get likes on a post."""
        return self.client.get(f"{post_id}/likes", params={
            "summary": str(summary).lower(),
            "limit": limit,
        })
```

### Media Operations

```python
"""media.py — Photo and video uploads"""

from typing import Optional
from .client import FacebookClient

class MediaAPI:
    """Photo and video operations for Facebook Pages."""
    
    def __init__(self, client: FacebookClient):
        self.client = client
    
    def upload_photo(
        self,
        page_id: str,
        url: Optional[str] = None,
        file_path: Optional[str] = None,
        message: Optional[str] = None,
        published: bool = True,
    ) -> dict:
        """Upload photo to page."""
        if url:
            data = {"url": url, "published": str(published).lower()}
            if message:
                data["message"] = message
            return self.client.post(f"{page_id}/photos", data=data)
        
        elif file_path:
            with open(file_path, "rb") as f:
                files = {"source": f}
                data = {"published": str(published).lower()}
                if message:
                    data["message"] = message
                return self.client.post(f"{page_id}/photos", data=data, files=files)
        
        raise ValueError("Must provide either url or file_path")
    
    def upload_video(
        self,
        page_id: str,
        file_url: Optional[str] = None,
        file_path: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
    ) -> dict:
        """Upload video to page."""
        data = {}
        if file_url:
            data["file_url"] = file_url
        elif file_path:
            data["file_path"] = file_path
        else:
            raise ValueError("Must provide either file_url or file_path")
        
        if title:
            data["title"] = title
        if description:
            data["description"] = description
        
        return self.client.post(f"{page_id}/videos", data=data)
```

---

## Usage Example

```python
"""example.py — Complete usage example"""

from facebook_sdk import FacebookClient, PageAPI, PostAPI, MediaAPI
from facebook_sdk.errors import TokenExpiredError, RateLimitError

# Initialize client
client = FacebookClient(
    access_token="EAA...",  # Or set FB_PAGE_TOKEN env var
    api_version="v21.0",
)

# Work with a page
page = PageAPI(client)
page_info = page.get_info("123456789", fields=["id", "name", "fan_count"])
print(f"Page: {page_info['name']} ({page_info['fan_count']} fans)")

# Create a post
post_api = PostAPI(client)
new_post = page.create_post(
    page_id="123456789",
    message="Hello from our Python SDK! 🤖",
    link="https://example.com",
)
post_id = new_post["id"]
print(f"Created post: {post_id}")

# Get comments
comments = post_api.get_comments(post_id, limit=10)
for comment in comments.get("data", []):
    print(f"  {comment.get('from', {}).get('name')}: {comment.get('message')}")

# Upload photo
media = MediaAPI(client)
photo = media.upload_photo(
    page_id="123456789",
    url="https://example.com/photo.jpg",
    message="Check out this photo!",
)

# Error handling
try:
    insights = page.get_insights(
        page_id="123456789",
        metrics=["page_impressions", "page_engaged_users"],
        period="day",
        since="2026-07-01",
        until="2026-07-24",
    )
except TokenExpiredError as e:
    print(f"🔐 Token expired: {e}")
    # Trigger token refresh
except RateLimitError as e:
    print(f"⏳ Rate limited: {e}")
    # Implement backoff
```

---

## Async Usage Example

```python
"""async_example.py"""

import asyncio
from facebook_sdk.async_client import AsyncFacebookClient

async def main():
    async with AsyncFacebookClient(
        access_token="EAA...",
        api_version="v21.0",
        max_connections=10,
    ) as client:
        
        # Multiple concurrent requests
        tasks = [
            client.get("me", params={"fields": "id,name"}),
            client.get("123456789", params={"fields": "id,name,fan_count"}),
            client.get("123456789/posts", params={"limit": 5}),
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for result in results:
            if isinstance(result, Exception):
                print(f"❌ Error: {result}")
            else:
                print(f"✅ Data: {result}")

asyncio.run(main())
```

---

## Installation & Configuration

```bash
# Install dependencies
pip install requests httpx pydantic python-dotenv

# Or use requirements.txt
# requests>=2.31.0
# httpx>=0.27.0
# pydantic>=2.0.0
# python-dotenv>=1.0.0
```

**`.env` configuration:**
```bash
FB_PAGE_TOKEN=EAA...
FB_USER_TOKEN=EAA...
FB_APP_ID=123456789
FB_APP_SECRET=abc123...
FB_API_VERSION=v21.0
```

---

## Error Handling Patterns

```python
# Pattern 1: Specific error handling
try:
    result = client.get("me/photos")
except TokenExpiredError:
    refresh_token()
except RateLimitError:
    wait_and_retry()
except FacebookAPIError as e:
    if e.code == 100:
        fix_parameters(e)
    else:
        escalate_to_zion(e)

# Pattern 2: Retry with backoff (already built into client)
# client.max_retries = 3 by default

# Pattern 3: Circuit breaker for persistent failures
from pybreaker import CircuitBreaker

breaker = CircuitBreaker(fail_max=5, reset_timeout=60)

@breaker
def safe_api_call():
    return client.get("me")

try:
    result = safe_api_call()
except CircuitBreakerError:
    logger.error("Circuit breaker open — Facebook API may be down")
```

---

## Logging Configuration

```python
import logging

# Structured JSON logging for production
logging.basicConfig(
    level=logging.INFO,
    format='{"time":"%(asctime)s","name":"%(name)s","level":"%(levelname)s","message":"%(message)s"}',
    datefmt="%Y-%m-%dT%H:%M:%S",
)

# Log levels per module
logging.getLogger("facebook_sdk").setLevel(logging.DEBUG)  # debug in dev
logging.getLogger("httpx").setLevel(logging.WARNING)  # quiet httpx
logging.getLogger("urllib3").setLevel(logging.WARNING)  # quiet urllib3
```

---

## Testing the SDK

```python
"""test_client.py — Testing with mocked responses"""

import pytest
from unittest.mock import Mock, patch
from facebook_sdk import FacebookClient
from facebook_sdk.errors import TokenExpiredError, RateLimitError

@pytest.fixture
def client():
    return FacebookClient(access_token="test_token")

@patch("requests.Session.request")
def test_get_success(mock_request, client):
    """Test successful GET request."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"id": "123", "name": "Test"}
    mock_response.headers = {}
    mock_request.return_value = mock_response
    
    result = client.get("me", params={"fields": "id,name"})
    assert result["id"] == "123"
    assert result["name"] == "Test"

@patch("requests.Session.request")
def test_token_expired(mock_request, client):
    """Test token expiration handling."""
    mock_response = Mock()
    mock_response.status_code = 400
    mock_response.json.return_value = {
        "error": {
            "code": 190,
            "message": "Invalid OAuth 2.0 Access Token"
        }
    }
    mock_response.headers = {}
    mock_request.return_value = mock_response
    
    with pytest.raises(TokenExpiredError):
        client.get("me")

@patch("requests.Session.request")
def test_rate_limited(mock_request, client):
    """Test rate limit handling."""
    mock_response = Mock()
    mock_response.status_code = 403
    mock_response.json.return_value = {
        "error": {
            "code": 613,
            "message": "Calls to this api have exceeded the rate limit."
        }
    }
    mock_response.headers = {
        "x-app-usage": '{"call_count": 95, "total_time": 12}'
    }
    mock_request.return_value = mock_response
    
    with pytest.raises(RateLimitError):
        client.get("me/posts")
```

---

## SDK Development Checklist

```
□ 1.  Base client: requests + httpx (sync + async)
□ 2.  Error handling: typed exceptions for all error codes
□ 3.  Token management: auto-inject, auto-refresh on 401
□ 4.  Rate limiting: in-memory counter, header tracking, throttle
□ 5.  Pagination: cursor-based iterator, batch support
□ 6.  Retry: exponential backoff + jitter, max retries config
□ 7.  Logging: structured JSON, token sanitized, latency tracked
□ 8.  Testing: pytest + mock responses, VCR.py for real recordings
□ 9.  Documentation: README, docstrings, usage examples
□ 10. Version management: env-based version, migration helpers
```
