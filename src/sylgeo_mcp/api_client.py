"""Async HTTP client for the Sylgeo API.

Handles authentication, request formatting, and error handling for all
Sylgeo API endpoints. The client is designed to be used as an async
context manager or via individual method calls.

Configuration:
    SYLGEO_API_KEY  — Required. Your API key from https://sylgeo.com/dashboard/api-keys
    SYLGEO_API_URL  — Optional. Override the base URL (default: https://api.sylgeo.com)
"""

from __future__ import annotations

import logging
import os
from typing import Any

import httpx

from sylgeo_mcp import __version__

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DEFAULT_BASE_URL = "https://api.sylgeo.com"
REQUEST_TIMEOUT = 60.0  # seconds


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _get_api_key() -> str:
    """Return the Sylgeo API key or raise a clear error."""
    key = os.environ.get("SYLGEO_API_KEY", "").strip()
    if not key:
        raise EnvironmentError(
            "SYLGEO_API_KEY environment variable is not set. "
            "Get your API key at https://sylgeo.com/dashboard/api-keys"
        )
    return key


def _get_base_url() -> str:
    """Return the API base URL, respecting the optional override."""
    return os.environ.get("SYLGEO_API_URL", DEFAULT_BASE_URL).rstrip("/")


def _default_headers(api_key: str) -> dict[str, str]:
    """Build the default headers sent with every request."""
    return {
        "Authorization": f"Bearer {api_key}",
        "X-MCP-Client": f"sylgeo-mcp/{__version__}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }


# ---------------------------------------------------------------------------
# Client
# ---------------------------------------------------------------------------


class SylgeoClient:
    """Async wrapper around the Sylgeo REST API.

    Usage::

        client = SylgeoClient()
        result = await client.scan_brand("example.com")
    """

    def __init__(self) -> None:
        self._api_key = _get_api_key()
        self._base_url = _get_base_url()
        self._headers = _default_headers(self._api_key)

    # -- internal helpers ---------------------------------------------------

    async def _request(
        self,
        method: str,
        path: str,
        *,
        json_body: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Execute an HTTP request and return the parsed JSON response.

        On HTTP or network errors the method returns a structured error dict
        instead of raising, so the MCP tool can always return something useful
        to the AI assistant.
        """
        url = f"{self._base_url}{path}"
        logger.debug("%s %s", method, url)

        try:
            async with httpx.AsyncClient(
                timeout=REQUEST_TIMEOUT,
                headers=self._headers,
            ) as http:
                response = await http.request(method, url, json=json_body)

                if response.status_code == 401:
                    return {
                        "error": "authentication_failed",
                        "message": (
                            "Invalid or expired API key. "
                            "Check your SYLGEO_API_KEY or get a new one at "
                            "https://sylgeo.com/dashboard/api-keys"
                        ),
                    }

                if response.status_code == 404:
                    return {
                        "error": "not_found",
                        "message": (
                            f"Resource not found at {path}. "
                            "The domain may not have been scanned yet."
                        ),
                    }

                if response.status_code == 429:
                    return {
                        "error": "rate_limited",
                        "message": (
                            "API rate limit exceeded. Please wait a moment "
                            "and try again, or upgrade your plan at "
                            "https://sylgeo.com/pricing"
                        ),
                    }

                if response.status_code >= 400:
                    # Try to extract a message from the response body
                    try:
                        body = response.json()
                        detail = body.get("detail") or body.get("message") or str(body)
                    except Exception:
                        detail = response.text[:500]
                    return {
                        "error": "api_error",
                        "status_code": response.status_code,
                        "message": detail,
                    }

                return response.json()  # type: ignore[no-any-return]

        except httpx.TimeoutException:
            logger.warning("Request to %s timed out", url)
            return {
                "error": "timeout",
                "message": (
                    f"Request to {path} timed out after {REQUEST_TIMEOUT}s. "
                    "The scan may still be running — try checking results later."
                ),
            }
        except httpx.HTTPError as exc:
            logger.exception("HTTP error calling %s", url)
            return {
                "error": "http_error",
                "message": f"HTTP error: {exc}",
            }
        except Exception as exc:
            logger.exception("Unexpected error calling %s", url)
            return {
                "error": "unexpected_error",
                "message": f"Unexpected error: {exc}",
            }

    # -- public API ---------------------------------------------------------

    async def scan_brand(self, domain: str) -> dict[str, Any]:
        """Start a full AI visibility scan for *domain*.

        Initiates an asynchronous scan across ChatGPT, Claude, Gemini, and
        Perplexity. Use :meth:`get_visibility_score` to retrieve results
        once the scan completes.

        Args:
            domain: The domain to scan (e.g. ``"example.com"``).

        Returns:
            API response dict with scan ID and status.
        """
        return await self._request(
            "POST",
            "/api/scanner/run",
            json_body={"domain": domain},
        )

    async def get_visibility_score(self, domain: str) -> dict[str, Any]:
        """Retrieve the latest visibility scores for *domain*.

        Args:
            domain: The domain to look up (e.g. ``"example.com"``).

        Returns:
            Dict with overall score, per-model breakdown, mention count,
            and sentiment analysis.
        """
        return await self._request("GET", f"/api/scanner/results/{domain}")

    async def analyze_website(self, domain: str) -> dict[str, Any]:
        """Analyze a website's GEO readiness.

        Checks robots.txt configuration for AI crawlers, schema markup,
        content structure, and other GEO signals.

        Args:
            domain: The bare domain (e.g. ``"example.com"``).

        Returns:
            Analysis results with scores and findings.
        """
        return await self._request(
            "POST",
            "/api/analyze/website",
            json_body={"url": f"https://{domain}"},
        )

    async def get_recommendations(self, domain: str) -> dict[str, Any]:
        """Fetch prioritized GEO optimization recommendations for *domain*.

        Args:
            domain: The domain to get recommendations for.

        Returns:
            Dict containing action items with estimated impact scores.
        """
        return await self._request("GET", f"/api/analyze/recommendations/{domain}")

    async def get_competitors(self, domain: str) -> dict[str, Any]:
        """Get competitive AI visibility data for *domain*.

        Args:
            domain: The domain whose competitors to compare.

        Returns:
            Dict with competitor list, GEO scores, mention rates, and
            ranking differences.
        """
        return await self._request("GET", f"/api/competitors/{domain}")

    async def get_scan_history(self, domain: str) -> dict[str, Any]:
        """Retrieve historical scan data and score trends for *domain*.

        Args:
            domain: The domain to get history for.

        Returns:
            Dict with timestamped scan results and trend data.
        """
        return await self._request("GET", f"/api/scanner/history/{domain}")

    async def get_prompts(self, domain: str) -> dict[str, Any]:
        """List the AI search prompts currently tracked for *domain*.

        These are the actual queries tested across ChatGPT, Claude, Gemini,
        and Perplexity during each scan.

        Args:
            domain: The domain to get prompts for.

        Returns:
            Dict with prompt list and associated metadata.
        """
        return await self._request("GET", f"/api/prompts/{domain}")
