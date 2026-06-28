# Sylgeo MCP Server

[![PyPI](https://img.shields.io/pypi/v/sylgeo-mcp)](https://pypi.org/project/sylgeo-mcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**Check your brand's AI visibility across ChatGPT, Claude, Gemini & Perplexity — right from your coding workflow.**

Sylgeo MCP is a [Model Context Protocol](https://modelcontextprotocol.io/) server that gives AI coding assistants access to Sylgeo's Generative Engine Optimization (GEO) tools. Ask your assistant to scan your brand, analyze your website, compare competitors, and get actionable recommendations — all without leaving your editor.

---

## Quick Start

### 1. Get Your API Key

Sign up and grab your key at **[sylgeo.com/dashboard/api-keys](https://sylgeo.com/dashboard/api-keys)**.

### 2. Install in Your AI Assistant

#### Claude Code

```bash
claude mcp add sylgeo-mcp -- uvx sylgeo-mcp
```

Then set your API key:

```bash
export SYLGEO_API_KEY="your-api-key-here"
```

#### Cursor

Add to `.cursor/mcp.json` in your project root:

```json
{
  "mcpServers": {
    "sylgeo": {
      "command": "uvx",
      "args": ["sylgeo-mcp"],
      "env": {
        "SYLGEO_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

#### Windsurf

Add to your Windsurf MCP config:

```json
{
  "mcpServers": {
    "sylgeo": {
      "command": "uvx",
      "args": ["sylgeo-mcp"],
      "env": {
        "SYLGEO_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

#### Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "sylgeo": {
      "command": "uvx",
      "args": ["sylgeo-mcp"],
      "env": {
        "SYLGEO_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

---

## Available Tools

All tools require a valid `SYLGEO_API_KEY`.

| Tool | Description |
|------|-------------|
| **`scan_brand_visibility`** | Run a full AI visibility scan across ChatGPT, Claude, Gemini & Perplexity. Returns mention rates, rankings, and sentiment. |
| **`check_visibility_score`** | Get current GEO and AEO visibility scores with per-model breakdown. |
| **`analyze_website_geo`** | Analyze a website's GEO readiness — robots.txt, schema markup, content structure. |
| **`get_geo_recommendations`** | Get prioritized action items with estimated impact scores. |
| **`compare_competitors`** | Compare your AI visibility against tracked competitors. |
| **`get_scan_history`** | View historical scan data and score trends over time. |
| **`get_tracked_prompts`** | List the AI search prompts being tracked for your domain. |

## Prompt Templates

| Prompt | Description |
|--------|-------------|
| **`geo_audit`** | Full GEO audit — analyze website, run scan, check scores, provide recommendations. |
| **`competitor_analysis`** | Competitive AI visibility analysis with gap identification. |
| **`content_optimization`** | Content analysis with specific optimization recommendations. |

## Resources

| URI | Description |
|-----|-------------|
| `sylgeo://docs/getting-started` | Getting started guide |
| `sylgeo://docs/what-is-geo` | What is GEO (Generative Engine Optimization)? |

---

## Example Usage

Once installed, just ask your AI assistant:

> **"Scan the AI visibility for my domain example.com"**

The assistant will call `scan_brand_visibility` and then `check_visibility_score` to show your results.

> **"How does my site compare to competitors?"**

The assistant will call `compare_competitors` and present a comparison table.

> **"Run a full GEO audit for example.com"**

Using the `geo_audit` prompt template, the assistant will walk through a complete audit:
1. Analyze website GEO readiness
2. Run a visibility scan
3. Check scores
4. Provide recommendations

> **"What prompts are being tracked for my domain?"**

The assistant will call `get_tracked_prompts` to show which AI search queries are being monitored.

---

## Configuration

| Environment Variable | Required | Description |
|---------------------|----------|-------------|
| `SYLGEO_API_KEY` | **Yes** | Your Sylgeo API key ([get one here](https://sylgeo.com/dashboard/api-keys)) |
| `SYLGEO_API_URL` | No | Override the API base URL (default: `https://api.sylgeo.com`) |

---

## Development

```bash
# Clone the repo
git clone https://github.com/sylgeo/sylgeo-mcp.git
cd sylgeo-mcp

# Install in development mode
pip install -e ".[dev]"

# Run the server locally
SYLGEO_API_KEY="your-key" python -m sylgeo_mcp.server
```

### Testing with MCP Inspector

```bash
npx @modelcontextprotocol/inspector uvx sylgeo-mcp
```

---

## What is GEO?

**Generative Engine Optimization (GEO)** is the practice of optimizing your brand's content to appear in AI-generated answers — the responses from ChatGPT, Claude, Gemini, Perplexity, and other LLM-powered search tools.

Traditional SEO focuses on Google's blue links. GEO focuses on getting your brand mentioned, recommended, and cited by AI assistants.

Learn more → [sylgeo.com](https://sylgeo.com)

---

## License

MIT — see [LICENSE](LICENSE) for details.
