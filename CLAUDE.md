# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies
uv pip install -r requirements.txt
uv pip install -r requirements-dev.txt

# Run the server
uvicorn main:app --reload

# Run tests (fast mode skips the 0.05s CPU priming sleep)
FAST_TEST=1 pytest -q

# Run a single test
FAST_TEST=1 pytest test_main.py::test_function_name -q

# Lint and format
black .
flake8 .
mypy .
```

## Architecture

This is a FastAPI-based Linux process monitor. The current MVP is intentionally minimal — a single file (`main.py`) with one endpoint.

**`GET /metrics?limit=N`** (default 5, max 50): Returns system CPU/memory percentages and the top N processes by CPU usage via `psutil`. The endpoint performs a non-blocking async sleep to prime `psutil`'s CPU counters; this sleep is skipped when `FAST_TEST=1` is set.

### Planned expansion (per README)
- Richer metrics: disk, load averages, network I/O
- WebSocket/SSE for real-time streaming
- Vue + Tailwind frontend dashboard
- PostgreSQL/TimescaleDB for historical storage
- Anomaly detection and alerting
- Process management actions (terminate, renice) with RBAC
- AI/ML layer for predictive modeling and natural language queries
- Future env vars will use the `APM_` prefix
