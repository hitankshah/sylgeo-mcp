"""Sylgeo MCP Server — expose Sylgeo GEO tools via the Model Context Protocol.

This module registers all MCP tools, prompts, and resources and starts
the server over the stdio transport.  It is the entry point used by
``uvx sylgeo-mcp`` and the ``sylgeo-mcp`` console script.

Environment variables:
    SYLGEO_API_KEY  — Required. Your Sylgeo API key.
    SYLGEO_API_URL  — Optional. Override the API base URL.
"""

from __future__ import annotations

import logging
import sys

from mcp.server.fastmcp import FastMCP

from sylgeo_mcp.api_client import SylgeoClient

# ---------------------------------------------------------------------------
# Logging — always to stderr so we never pollute the MCP JSON-RPC stream.
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger("sylgeo_mcp")

# ---------------------------------------------------------------------------
# Server instance
# ---------------------------------------------------------------------------

mcp = FastMCP(
    "Sylgeo",
    description=(
        "AI Visibility Intelligence — check and improve your brand's "
        "presence across ChatGPT, Claude, Gemini & Perplexity."
    ),
)

# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------


@mcp.tool()
async def scan_brand_visibility(domain: str) -> dict:
    """Run a full AI visibility scan across ChatGPT, Claude, Gemini & Perplexity.

    Returns mention rates, rankings, and sentiment for each model.
    The scan runs in the background — use check_visibility_score to get results.

    Args:
        domain: The domain to scan (e.g. "example.com").
    """
    logger.info("Starting brand visibility scan for %s", domain)
    client = SylgeoClient()
    return await client.scan_brand(domain)


@mcp.tool()
async def check_visibility_score(domain: str) -> dict:
    """Get the current GEO and AEO visibility scores for a domain.

    Shows overall score, per-model breakdown, mention count, and sentiment analysis.

    Args:
        domain: The domain to check (e.g. "example.com").
    """
    logger.info("Checking visibility score for %s", domain)
    client = SylgeoClient()
    return await client.get_visibility_score(domain)


@mcp.tool()
async def analyze_website_geo(url: str) -> dict:
    """Analyze a website's GEO readiness.

    Checks robots.txt for AI crawlers, schema markup, content structure,
    and generates optimization prompts. URL should be like 'https://example.com'.

    Args:
        url: Full URL to analyze (e.g. "https://example.com").
    """
    # Strip protocol prefix so the API client can add it back consistently.
    domain = url.removeprefix("https://").removeprefix("http://").strip("/")
    logger.info("Analyzing website GEO readiness for %s", domain)
    client = SylgeoClient()
    return await client.analyze_website(domain)


@mcp.tool()
async def get_geo_recommendations(domain: str) -> dict:
    """Get actionable recommendations to improve your brand's AI visibility.

    Returns prioritized action items with estimated impact scores.

    Args:
        domain: The domain to get recommendations for (e.g. "example.com").
    """
    logger.info("Fetching GEO recommendations for %s", domain)
    client = SylgeoClient()
    return await client.get_recommendations(domain)


@mcp.tool()
async def compare_competitors(domain: str) -> dict:
    """Compare your brand's AI visibility against tracked competitors.

    Shows GEO scores, mention rates, and ranking differences for each competitor.

    Args:
        domain: Your domain to compare (e.g. "example.com").
    """
    logger.info("Comparing competitors for %s", domain)
    client = SylgeoClient()
    return await client.get_competitors(domain)


@mcp.tool()
async def get_scan_history(domain: str) -> dict:
    """Get historical scan data and score trends for a domain.

    Shows how your AI visibility has changed over time across all models.

    Args:
        domain: The domain to get history for (e.g. "example.com").
    """
    logger.info("Fetching scan history for %s", domain)
    client = SylgeoClient()
    return await client.get_scan_history(domain)


@mcp.tool()
async def get_tracked_prompts(domain: str) -> dict:
    """Get the list of AI search prompts being tracked for a domain.

    These are the actual queries tested across ChatGPT, Claude, Gemini & Perplexity.

    Args:
        domain: The domain to get prompts for (e.g. "example.com").
    """
    logger.info("Fetching tracked prompts for %s", domain)
    client = SylgeoClient()
    return await client.get_prompts(domain)


# ---------------------------------------------------------------------------
# Prompt templates
# ---------------------------------------------------------------------------


@mcp.prompt()
def geo_audit(domain: str) -> str:
    """Run a complete GEO audit for a domain.

    Walks you through a full website analysis, visibility scan, score check,
    and actionable recommendations.

    Args:
        domain: The domain to audit (e.g. "example.com").
    """
    return (
        f"Perform a complete GEO audit for {domain}. "
        "First analyze the website, then run a visibility scan, "
        "check the scores, and provide recommendations."
    )


@mcp.prompt()
def competitor_analysis(domain: str) -> str:
    """Run a competitive AI visibility analysis.

    Compares a domain against its tracked competitors and highlights gaps.

    Args:
        domain: The domain to analyze (e.g. "example.com").
    """
    return (
        f"Run a competitive AI visibility analysis for {domain}. "
        "Compare against tracked competitors and identify gaps."
    )


@mcp.prompt()
def content_optimization(domain: str) -> str:
    """Analyze content for AI visibility optimization.

    Checks current scores, identifies content gaps, and provides specific
    recommendations for improving AI search performance.

    Args:
        domain: The domain to optimize (e.g. "example.com").
    """
    return (
        f"Analyze {domain}'s content for AI visibility optimization. "
        "Check current scores, identify content gaps, and provide "
        "specific recommendations."
    )


# ---------------------------------------------------------------------------
# Resources
# ---------------------------------------------------------------------------


@mcp.resource("sylgeo://docs/getting-started")
def getting_started() -> str:
    """Getting started guide for Sylgeo MCP."""
    return """\
# Getting Started with Sylgeo MCP

Sylgeo MCP lets AI coding assistants check and improve your brand's
visibility across AI search engines (ChatGPT, Claude, Gemini, Perplexity).

## Quick Start

1. **Get your API key** at https://sylgeo.com/dashboard/api-keys
2. **Set the environment variable**:
   ```
   export SYLGEO_API_KEY="your-api-key"
   ```
3. **Start using tools** — ask your AI assistant to:
   - *"Scan my brand visibility for example.com"*
   - *"Analyze example.com for GEO readiness"*
   - *"Compare my AI visibility against competitors"*

## Available Tools

| Tool | Description |
|------|-------------|
| `scan_brand_visibility` | Run a full AI visibility scan |
| `check_visibility_score` | Get current GEO/AEO scores |
| `analyze_website_geo` | Analyze website GEO readiness |
| `get_geo_recommendations` | Get optimization action items |
| `compare_competitors` | Compare against competitors |
| `get_scan_history` | View historical score trends |
| `get_tracked_prompts` | List tracked AI search prompts |

## Typical Workflow

1. Run `scan_brand_visibility` to start a scan
2. Use `check_visibility_score` to see results
3. Call `get_geo_recommendations` for action items
4. Use `compare_competitors` to benchmark against rivals
"""


@mcp.resource("sylgeo://docs/what-is-geo")
def what_is_geo() -> str:
    """Explainer: What is Generative Engine Optimization (GEO)?"""
    return """\
# What is GEO (Generative Engine Optimization)?

**GEO** is the practice of optimizing your brand's content so it appears
in AI-generated answers — the responses produced by ChatGPT, Claude,
Gemini, Perplexity, and other large-language-model-powered search tools.

## Why GEO Matters

Traditional SEO focuses on ranking in Google's blue links. But users
increasingly ask AI assistants for recommendations, comparisons, and
answers. If your brand isn't mentioned in those AI responses, you're
invisible to a fast-growing audience.

## Key GEO Metrics

| Metric | What It Measures |
|--------|-----------------|
| **Mention Rate** | How often your brand appears in AI answers |
| **Ranking Position** | Where you appear in recommendation lists |
| **Sentiment** | Whether mentions are positive, neutral, or negative |
| **Citation Rate** | How often AI links back to your content |

## GEO vs SEO vs AEO

- **SEO** — Optimize for traditional search engine results pages
- **AEO** (Answer Engine Optimization) — Optimize for featured snippets and voice assistants
- **GEO** — Optimize for AI-generated answers across LLM-powered tools

GEO builds on SEO and AEO but adds strategies specific to how language
models retrieve and synthesize information, such as:

- Structured data and schema markup that LLMs can parse
- Authoritative, citable content that models prefer to reference
- Consistent brand mentions across high-quality sources
- `robots.txt` and `llms.txt` configuration for AI crawlers

## How Sylgeo Helps

Sylgeo scans the major AI models with real prompts related to your
industry, measures how often and how favorably your brand is mentioned,
and gives you actionable recommendations to improve your AI visibility.
"""


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main() -> None:
    """Run the Sylgeo MCP server with stdio transport."""
    logger.info("Starting Sylgeo MCP server")
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
