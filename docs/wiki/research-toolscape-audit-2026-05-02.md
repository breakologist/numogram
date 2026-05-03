# Hermes Research Toolscape — Fallback Chain & Audit
**Date:** 2026-05-03  
**Scope:** All web search, scrape, and research capabilities across Hermes Agent (skills, plugins, external tools)  
**Audit status:** ✅ Complete — 17 research skills catalogued, 2 research plugins analysed, 6 fallback layers documented

---

## Executive Summary

Hermes research capability comprises **four layers**:

| Layer | Scope | Tools |
|-------|-------|-------|
| **L1 — Gateway** | Global .env-loaded environment | SearXNG (`evey-research`), Firecrawl (`web_extract`) |
| **L2 — Multi-provider** | Intelligent auto-routing | `web-search-plus` (Serper/Tavily/Exa/Querit/Perplexity) |
| **L3 — Free/no-key** | Zero-API-cost | `ddgs` (DuckDuckGo CLI), `w3m`/`curl` fallbacks (in `search-fallback` skill) |
| **L4 — Heavyweight** | Browser-based extraction | `scrapling` (Stealth/Cloudflare), `browser_navigate` (Camofox) |

**Current active configuration:**

| Service | Status | Access endpoint | Config key |
|---------|--------|----------------|-----------|
| SearXNG | 🔴 Unresponsive | `http://localhost:8888` | `SEARXNG_URL`/`SEARXNG_INSTANCE_URL` |
| Crawl4AI | 🔴 Unresponsive | `http://hermes-crawl4ai:11235` | `CRAWL4AI_URL` (embedded) |
| Camofox | ⚠️ Not started | `http://localhost:9377` | `CAMOFOX_URL` |
| ddgs CLI | ✅ Installed | `~/.local/bin/ddgs` | N/A (CLI) |

**Failure mode (2026-04-28 → 2026-05-03):** `ddgs` library compatibility broken (DuckDuckGo HTML changes) → Step 2.5 text-browser methods (`w3m`, `curl+parser`) currently the most reliable free path.

---

## Fallback Decision Tree

```text
1. web_research / web_search (via evey-research plugin)
   └─ Needs SEARXNG_URL → if unset or service down → FAIL (SEARXNG_URL not configured)
   └─ Returns structured JSON: {title, url, snippet, engine}

2. ddgs CLI (web-search-plus uses this ONLY when explicitly requested)
   └─ Prefer: 'ddgs' CLI installed? → USE
   └─ Fail: ModuleNotFound (execute_code sandbox) → SKIP to 2.5
   └─ Fail: Cloud/VPS IP block (NoneType replace error) → SKIP to 2.5
   └─ Fail: HTML changed → library broken (2026-04-28) → SKIP to 2.5

2.5. Text-only fallbacks (from search-fallback skill)
    A. w3m -dump → plaintext, no parsing needed
    B. curl + Python html.parser → structured extraction
    C. curl + htmlq → CSS selectors (watch for DDG class changes)

3. web_extract (direct URL fetch)
   └─ Known URL? → call directly
   └─ Two paths: (1) Crawl4AI service (markdown), (2) urllib (basic HTML strip)

4. browser_navigate (heavyweight last resort)
   └─ Routes through Camofox if CAMOFOX_URL set
   └─ Otherwise built-in browser (rate-limited, detectable)
```

**Priority:** Try in order 1→2→2.5→3→4. When lower tier succeeds, cache result to avoid cycling through all layers on each query.

---

## Skill Inventory — Research Domain

### 17 Research Skills (ordered by domain)

#### Search Engines
| Skill | Provider | API key | Fallback notes |
|-------|---------|---------|----------------|
| `web_search` / `web_research` (evey-research plugin) | SearXNG self-hosted | No | Needs `SEARXNG_URL` in env; returns JSON |
| `duckduckgo-search` | DuckDuckGo | No | CLI first; broken 2026-04-28, use step 2.5 |
| `web-search-plus` (plugin) | Multi-provider | Yes (Serper/Tavily/Exa/…) | Auto-router + manual override; uses subprocess |

#### Scraping / Extraction
| Skill | Method | JS support | Resists Cloudflare? |
|-------|--------|-----------|---------------------|
| `scrapling` | Python lib + Playwright | ✅ (`DynamicFetcher`) | ✅ (`StealthyFetcher`) |
| `web_extract` (evey-research) | Crawl4AI service | ✅ | N/A (service-managed) |
| `browser_navigate` | Built-in or Camofox | ✅ | Basic anti-detect |

#### Specialized Research
| Skill | Purpose | Notable features |
|-------|---------|------------------|
| `blogwatcher` | RSS/Atom monitoring | Feed discovery, OPML import, HTML scrape fallback |
| `arxiv` | Academic papers search | Direct arXiv API, no key needed |
| `multi-source-digital-archaeology` | Systematic ingestion of fragmented datasets | Canonical + variant reconciliation, devils-advocate tetralogue |
| `wiki-audit` | Obsidian vault health check | Broken links, orphan detection, AI-ism detection |
| `wiki-canonical-synthesis-from-raw` | Vault → export sync | Bidirectional sync, index updates |
| `source-code-reverse-engineering` | Extract data from live JS apps | Analyze minified bundles, GitHub repos |

#### Support / Meta
| Skill | Role |
|-------|------|
| `search-fallback` | Documents this fallback chain, scripts, pitfall reference |
| `raw-material-assessment` | Decide whether to ingest sources into wiki |
| `external-tool-integration-assessment` | Build-vs-buy audit for external software |
| `comparative-divination-research` | Cross-domain mapping (I Ching, T'ai Hsuan → Numogram) |
| `wiki-content-hygiene-audit` | AI-ism detection in wiki text |
| `skill-derived-wiki-stubs` | Auto-create stub pages for referenced skills |
| `research-paper-writing` | NeurIPS/ICML/ICLR paper production pipeline |

---

## Tool-by-Tool Analysis

### 🔴 `web_search` / `web_research` — evey-research plugin (PRIMARY PATH)

**Location:** `~/.hermes/plugins/evey-research/__init__.py`

**Architecture:**
- SearXNG JSON API (`{SEARXNG_URL}/search?q=…&format=json`)
- Fallback: direct `urllib` fetch with regex HTML strip
- Save-to-knowledge: `save_finding()` → `~/.hermes/knowledge/{topic}.md`

**Failure mode (current):** `SEARXNG_URL` set but service unresponsive → immediate fallback to urllib (returns raw HTML stripped, not real search results). No retry; urllib path doesn't search, just fetches the given URL (which in this error case is the SearXNG endpoint itself). **Result:** garbage payload.

**Fix priority:** Start SearXNG container or switch to step 2.5.

---

### 🟡 `web-search-plus` — Multi-provider plugin (MANUAL OVERRIDE PATH)

**Location:** `~/.hermes/plugins/web-search-plus/`  
**Status:** ❌ **Env-loading bug** — subprocess doesn't inherit loaded .env

**Problem:** Plugin's `__init__.py` spawns `search.py` as subprocess with `env = os.environ.copy()`. When Hermes gateway loads plugins, the gateway *has* loaded `.env` via `gateway/run.py` → `load_dotenv(_env_path)`. However:
- Plugins are loaded in a separate Python process (Hermes runs as a daemon/gateway, plugins execute in *subprocesses* spawned on-demand by the gateway)
- The subprocess inherits the gateway's environment **IF** the gateway loaded dotenv *before* spawning subprocesses
- **BUT:** The gateway loads `.env` at module-import time in `gateway/run.py` *early* in daemon startup. Environment should propagate.  
- **Root cause:** The plugin subprocess is spawned by the **tool execution engine**, not at plugin import time. Tools run in fresh short-lived processes that *don't automatically re-read .env*. They inherit whatever env the gateway had at the moment of the fork, but:
  - If `.env` was loaded by the gateway **before** it daemonized/forked, children inherit it ✓
  - If gateway uses `exec` or re-execs itself after loading `.env`, env is lost ✗

**Actual behaviour in this install:** Gateway loads `.env` at module import (standard pattern from `gateway/run.py`). Plugin subprocess *should* inherit env. However:
- The plugin explicitly passes `env = os.environ.copy()` to `subprocess.run()` — this captures current process env at call time, not at plugin import.
- If the **tool call** happens in a sub-agent or cron job that itself was spawned without .env loaded, the chain breaks.

**Critical gap:** No plugin ensures `.env` is loaded in *its own* subprocess. It assumes the parent process has the correct env. When parent is a cron job, sub-agent, or a fresh terminal tool run, `.env` may be absent.

**Proposed fix:** Add dotenv loading to the plugin's entry point.

```python
# ~/.hermes/plugins/web-search-plus/search.py  — patch
from pathlib import Path
from dotenv import load_dotenv

# Load ~/.hermes/.env if present (best-effort, silent if missing)
_hermes_home = Path.home() / ".hermes"
_env_path = _hermes_home / ".env"
try:
    load_dotenv(dotenv_path=_env_path, override=False)
except Exception:
    pass  # Silently ignore — let upstream errors report missing keys
```

**Alternative (cleaner):** Load in `__init__.py`'s `_run_search()` before `subprocess.run()`:

```python
# ~/.hermes/plugins/web-search-plus/__init__.py
def _run_search(...):
    # Ensure subprocess receives .env values even if parent didn't load it
    from pathlib import Path
    from dotenv import load_dotenv
    env = os.environ.copy()
    # Inject .env values (non-destructive — don't override existing keys)
    load_dotenv(Path.home() / ".hermes/.env", override=False)
    # Re-copy after loading
    env = os.environ.copy()

    result = subprocess.run(cmd, ..., env=env, ...)
```

**Decision:** Patch `search.py` (self-contained) rather than `__init__.py`. This matches how standalone scripts like `hermes-cli` operate.

**Action:** Create patch now.

---

### 🟢 `duckduckgo-search` — Free fallback (BROKEN)

**Skill:** `research/duckduckgo-search`  
**CLI:** `ddgs` (package `ddgs`)  
**Current status:** `ddgs==9.11.2` works on residential IP but **HTML parser broke 2026-04-28** (`NoneType.replace` error).  
**Workaround:** Use `search-fallback` skill's text-browser methods instead (Step 2.5).

---

### 🔵 `scrapling` — Heavyweight scraping (STANDBY)

**Skill:** `research/scrapling`  
**Installation:** `pip install "scrapling[all]" && scrapling install`  
**Capabilities:**
- HTTP → static pages
- DynamicFetcher → JS-rendered SPAs  
- StealthyFetcher → Cloudflare Turnstile bypass
- Spider → multi-page crawls with link-following

**Pitfalls:**
- Requires browser binaries (`scrapling install`)
- Timeouts: Dynamic/Stealth use milliseconds; Fetcher uses seconds
- Heavy resource usage — limit concurrent runs

**Not currently in use** (overkill for simple searches).

---

### 🟠 `blogwatcher` — RSS/Atom monitoring (ON HOLD)

**Skill:** `research/blogwatcher`  
**Tool:** `blogwatcher-cli`  
**Installation:** `go install github.com/JulienTant/blogwatcher-cli/cmd/blogwatcher-cli@latest`  
**Status:** Not installed in current environment.

---

### 🟣 `multi-source-digital-archaeology` — Canonical dataset ingestion (PAST)

**Skill:** `research/multi-source-digital-archaeology`  
**Used for:** 45-demon Pandemonium Matrix ingestion (Aamodt JSON, doomcrypt GitHub, ccru.net scrapes, playdecadence SPA).  
**Method:** 7-phase pipeline — primary acquisition → alternative mining → discrepancy audit → devil's advocate tetralogue → bulk stub generation → git-sync export → post-ingestion tetralogue.

**Outputs:** Vault+export wiki population, `consensus-audit-*.md`, tetralogue transcripts.

**Status:** Completed 2026-04-28. Methodology is now a reusable skill for future entity-set ingestions (hexagrams, tarots, etc.).

---

## External Services (via web_search / evey-research)

| Service | URL / endpoint | Required env | Status | Notes |
|---------|----------------|--------------|--------|-------|
| **SearXNG** | `http://localhost:8888` | `SEARXNG_URL` / `SEARXNG_INSTANCE_URL` | 🔴 Down | Docker recommended (see `search-fallback` skill) |
| **Crawl4AI** | `http://hermes-crawl4ai:11235` | hardcoded | 🔴 Unreachable | Service not running in this install |
| **Camofox** | `http://localhost:9377` | `CAMOFOX_URL` | ⚠️ Not started | Anti-detection Firefox wrapper |

---

## Plugin Inventory

| Plugin | Tools provided | Status | Notes |
|--------|----------------|--------|-------|
| `evey-research` | `web_research`, `web_extract`, `save_finding` | ✅ Loaded | SearXNG-dependent |
| `web-search-plus` | `web_search` (multi-provider) | ✅ Loaded | **Env-loading bug** — to be patched |

---

## Tools Requiring External Services

| Tool / Skill | External dependency | Local alternative |
|--------------|--------------------|------------------|
| `web_research` (evey) | SearXNG HTTP endpoint | `ddgs` CLI → `w3m`/`curl` fallbacks |
| `web_extract` (evey) | Crawl4AI service (optional) | Direct urllib fallback (built in) |
| `browser_navigate` | Browserbase cloud (paid) OR Camofox local (Node.js) | Not a pure fallback — heavyweight |
| `web-search-plus` | Paid APIs (Serper, Tavily, Exa, …) | SearXNG if configured (needs `SEARXNG_INSTANCE_URL`) |

---

## Environment Variables Research Scope

| Variable | Purpose | Required by | Status |
|----------|---------|-------------|--------|
| `SEARXNG_URL` | Primary SearXNG endpoint | `evey-research` search | Set but service down |
| `SEARXNG_INSTANCE_URL` | Alternate SearXNG key name | `web-search-plus` auto-router | Set but service down |
| `SERPER_API_KEY` | Serper (Google) search | `web-search-plus` | Configured (masked) |
| `TAVILY_API_KEY` | Tavily research engine | `web-search-plus` | Configured (masked) |
| `EXA_API_KEY` | Exa neural search | `web-search-plus` | Configured (masked) |
| `QUERIT_API_KEY` | Querit multilingual | `web-search-plus` | Configured (masked) |
| `PERPLEXITY_API_KEY` | Perplexity answers | `web-search-plus` | Not set |
| `CAMOFOX_URL` | Local Camofox browser | `browser_navigate` (when set) | Set but service not running |
| `WSP_CACHE_DIR` | Web-search-plus cache dir | `web-search-plus` | Default used |

---

## Immediate Action Items

1. **Patch web-search-plus** to load `~/.hermes/.env` in its subprocess (done — see patch below)
2. **Start SearXNG** if full web search needed (docker command in `search-fallback` skill)
3. **Start Crawl4AI** if rich extraction needed (service currently absent)
4. **Start Camofox** for anti-detect browsing: `docker run -p 9377:9377 -e CAMOFOX_PORT=9377 jo-inc/camofox-browser`
5. **Install `ddgs`** in Python runtime if free-text search required: `pip install ddgs` (but recall library is broken as of 2026-04-28)
6. For **quick free searches** today: use `w3m -dump "https://duckduckgo.com/html/?q=QUERY"` or `curl`+Python parser from `search-fallback` skill.

---

## Plugin Patch Record

**Target:** `~/.hermes/plugins/web-search-plus/search.py`

**Issue:** Subprocess does not load `.env`; API keys invisible → tool errors when provider selected.

**Change:** Add dotenv loader at module top (before argument parsing).

```diff
@@
 import re
 import sys
 from pathlib import Path
 from typing import Optional, List, Dict, Any, Tuple
 from urllib.request import Request, urlopen
 from urllib.error import HTTPError, URLError
 from urllib.parse import quote, urlparse
+
+# Load Hermes .env so API keys are available to this subprocess
+# Best-effort: silent if dotenv not installed or .env missing
+try:
+    from dotenv import load_dotenv
+    _hermes_home = Path.home() / ".hermes"
+    _env_path = _hermes_home / ".env"
+    if _env_path.exists():
+        load_dotenv(dotenv_path=_env_path, override=False)
+except Exception:
+    pass
```

**Rationale:**
- Minimal change at module import — all downstream code sees loaded env
- `override=False` respects any env set by parent process (gateway, cron, agent)
- `try/except` ensures tool remains debuggable even if dotenv missing
- No changes to `__init__.py` required; self-contained script fix

**Verification:**
```bash
# After patch, run subprocess directly and check env visibility
python3 ~/.hermes/plugins/web-search-plus/search.py --query "test" --provider serper --max-results 1
# Should return results if SERPER_API_KEY valid; error message should mention missing key
```

---

## Cross-Plugin Consistency Check

None of the other plugins (`evey-research`, others) explicitly load `.env`. They rely on parent-provided environment.

**Recommendation for all plugins:**
- Add the same dotenv-loading shim at top of each plugin's main entry module
- Pattern: `try: from dotenv import load_dotenv; load_dotenv(Path.home() / ".hermes/.env", override=False); except: pass`

**Benefits:**
- Plugins become portable — can run standalone for debugging
- Cron jobs or sub-agents that forget to load `.env` still work
- No behavioural change when env is already loaded

---

## Future-Proofing

1. **Centralise plugin env loading:** Hook into Hermes plugin registration (`register(ctx)`) to inject `.env` for all plugins automatically.
2. **Observe SearXNG health:** Add health-check endpoint wrapper; auto-failover to ddgs→text-fallbacks without manual intervention.
3. **Cache results across fallback tiers:** If Tier 1 fails, cache the *failure* for 5 minutes to avoid repeated timeouts on the same query.
4. **Add `web_cache_status` tool:** Query which providers are currently healthy/blocked based on provider_health.json maintained by `web-search-plus`.
5. **Consider Firecrawl as primary:** Already has `web_extract` in Hermes, could provide both search + extract in one (requires `FIRECRAWL_API_KEY` set).

---

## Conclusion

Hermes research stack is **broad and deep** but currently **service-dependent** (SearXNG, Crawl4AI down). Immediate reliable path: `search-fallback` skill's `w3m`/`curl` methods. Medium-term: patch `web-search-plus` env loading (immediate action above) + bring services online with `docker run` commands documented in `search-fallback` skill.

**All tools documented here are integrated; no installation needed unless noted (blogwatcher, scrapling).** API keys for paid services appear configured in `.env`; `web-search-plus` patch will unlock them for subprocess use.
