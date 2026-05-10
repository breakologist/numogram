# Honcho Configuration

Local Honcho instance providing cross-session memory and user modelling for Hermes Agent.

## Architecture

- **API**: `http://localhost:8000` (v3, POST-based)
- **Workspace**: `hermes`
- **Peer**: `etym`
- **Database**: pgvector/pg15 (Docker: `honcho-database-1`)
- **Cache**: Redis 8.2 (Docker: `honcho-redis-1`)
- **Metrics**: Prometheus on `:9090`, Grafana on `:3000`

### Containers

| Container | Image | Role |
|-----------|-------|------|
| `honcho` | honcho-honcho | Main API server |
| `honcho-deriver-1` | honcho-deriver | Background memory formation |
| `honcho-database-1` | pgvector/pgvector:pg15 | Vector + relational storage |
| `honcho-redis-1` | redis:8.2 | Queue + cache |
| `honcho-prometheus-1` | prom/prometheus:v3.2.1 | Metrics collection |

## Configuration

### Location
- **Compose**: `~/honcho/docker-compose.yml` (main API + DB + Redis + Prometheus + Grafana)
- **Environment**: `~/honcho/.env`
- **Deriver**: Standalone container (not in compose), recreated manually with fixed health check

### LLM Provider (2026-05-10)
- **Provider**: `custom` (OpenAI-compatible via Nous Portal)
- **Endpoint**: `https://inference-api.nousresearch.com/v1`
- **Model**: `deepseek/deepseek-v4-pro`
- **Auth**: Nous subscription key (OAuth-derived, synced from Hermes Agent's `NOUS_PORTAL_API_KEY`)
- **Embeddings**: Google Gemini (`LLM_EMBEDDING_PROVIDER=gemini`)
- **Summary**: Google Gemini (`SUMMARY_PROVIDER=google`)
- **Backup**: Local Ollama — `hf.co/bartowski/NousResearch_Hermes-4-14B-GGUF:latest` via `host.docker.internal:11434`

### Key .env Variables
```bash
DERIVER_PROVIDER=custom
DERIVER_MODEL=deepseek/deepseek-v4-pro
LLM_OPENAI_COMPATIBLE_BASE_URL=https://inference-api.nousresearch.com/v1
LLM_OPENAI_COMPATIBLE_API_KEY=<synced from ~/.hermes/.env NOUS_PORTAL_API_KEY>
LLM_EMBEDDING_PROVIDER=gemini
SUMMARY_PROVIDER=google
```

All dialectic levels (`minimal` through `max`) also use `custom` provider with `deepseek/deepseek-v4-pro`.

### Session Strategy
- `sessionStrategy: per-directory`
- `memoryMode: hybrid`
- `writeFrequency: async`
- `recallMode: hybrid`

## Health Check Fix (2026-05-10)

The deriver health check historically showed `unhealthy` despite the deriver functioning correctly. Root cause: the baked-in health check probes `localhost:8000/openapi.json` from inside the deriver container, where nothing listens on port 8000. The Honcho API is on the `honcho` container on the Docker network.

**Fix**: Recreate the deriver container with `--health-cmd` pointing to `honcho:8000` instead of `localhost:8000`.

```bash
docker run -d \
  --name honcho-deriver-1 \
  --network honcho_default \
  --restart unless-stopped \
  --health-cmd 'python -c "import urllib.request; urllib.request.urlopen(\"http://honcho:8000/openapi.json\")" || exit 1' \
  ... \
  honcho-deriver
```

## Model Config Fix (2026-05-10)

Previous model `x-ai/grok-4.1-fast` was failing with `NotFoundError` (model unavailable). Switched all 11 occurrences to `deepseek/deepseek-v4-pro` across deriver and all 5 dialectic levels. API key was also a placeholder (`nous-sub`) — updated to the active Nous subscription key from Hermes Agent.

## User Model Priming (2026-05-10)

The Honcho representation was thin (surface-level task observations from April 15-21, 2026). Fed 13 structured messages into session `cron-memory-consolidation`:
- 3 rich profile summaries (working style, projects, numogram/AQ systems)
- 10 explicit single-trait observations (empirical values, wiki preference, bug enjoyment, audio/DSP identity, cross-domain synthesis, etc.)

These provide the deriver with explicit material to derive deeper observations.

## API Notes

- All listing endpoints use **POST** (not GET) — `GET` returns 405
- Session list: `POST /v3/workspaces/{ws}/sessions/list`
- Messages list: `POST /v3/workspaces/{ws}/sessions/{id}/messages/list`
- Message create: `POST /v3/workspaces/{ws}/sessions/{id}/messages`
  - Requires `{"messages": [{"content": "...", "peer_id": "..."}]}` wrapper
  - No `role` field — peer identity is via `peer_id` only
- Dialectic chat: `POST /v3/workspaces/{ws}/peers/{peer_id}/chat`
  - Body: `{"query": "...", "reasoning_level": "low|medium|high|max"}`
- Queue status: `GET /v3/workspaces/{ws}/queue/status`
- Peer representation: `POST /v3/workspaces/{ws}/peers/{peer_id}/representation`

## Pitfalls

- `docker compose restart` does NOT reload `.env` — use `--force-recreate`
- Provider name MUST be `custom` for OpenAI-compatible endpoints (NOT `openai_compatible`)
- Deriver health check baked into image points to `localhost` — must override
- Setting only one of `BACKUP_PROVIDER`/`BACKUP_MODEL` crashes both deriver AND honcho main (Pydantic validation)
- Invalid deriver config can crash the honcho main container too (shared config module)

## Session History

Honcho spans two Hermes Agent installations:
- **March 2026**: Local models only (Qwen2.5-14B-Instruct-Heretic via llama.cpp)
- **April 2026 onward**: Cloud models via Nous subscription (deepseek-v4-pro)
- 22 sessions, oldest: 2026-03-24, newest: 2026-05-10
- Largest session: `etym` (2,354 messages — early AQ/Numogram work archaeology)

## Related

- `~/honcho/docker-compose.yml` — main service definitions
- `~/honcho/.env` — environment configuration
- `~/.hermes/.env` — Hermes Agent env (source of `NOUS_PORTAL_API_KEY`)
- `~/.hermes/honcho.json` — Honcho client config for Hermes Agent
- Skill: `honcho-context-posting` — SDK and raw HTTP patterns
- Skill: `honcho-custom-provider` — LLM provider configuration
- Skill: `honcho-deriver-custom-llm` — Custom endpoint setup
