# AI-Powered Linux Process Manager

Lightweight FastAPI service that will evolve into a full AI‑assisted Linux process and system resource manager. This initial commit delivers a minimal `/metrics` API and a testing scaffold; the broader design (see accompanying Design & Implementation PDF) envisions real‑time monitoring, intelligent anomaly detection, historical analytics, and a web UI.

## 1. Vision (High Level)

Provide operators and developers with:

- Real‑time system & per‑process metrics (CPU, memory, disk, load, etc.)
- Intelligent insights (future: trend analysis, anomaly detection, suggestions)
- Web dashboard + API + (future) WebSocket streaming
- Extensible plugin layer (future) for data collectors & actions (e.g. restart / throttle)
- Optional persistence backend for historical queries & ML features

## 2. Current Minimal Functionality (MVP in this repo state)

Endpoint implemented:

- `GET /metrics?limit=N`  (default `limit=5`) returns:

```json
{
 "cpu_percent": <float>,
 "memory_percent": <float>,
 "processes": [ {"pid": int, "name": str, "cpu": float, "memory": float, "status": str}, ... ]
}
```

Technical notes:

- Uses non‑blocking priming of per‑process CPU stats + short sleep (skipped when `FAST_TEST=1`).
- Query parameter `limit` (1–50) controls number of top CPU processes returned.

## 3. Planned Roadmap (From Design Document)

Short‑term:

1. Add richer system metrics (disk, load averages, uptime, network I/O).
2. Introduce structured response models (Pydantic) & OpenAPI examples.
3. WebSocket / SSE streaming channel for push updates.
4. Basic frontend (likely Vue + Tailwind) consuming streaming metrics.

Medium‑term:

1. Historical storage (PostgreSQL / Timescale) with retention policies.
2. Alert rules & anomaly detection (statistical + ML baseline models).
3. Process management actions (terminate, nice adjustment) with RBAC.
4. Authentication & API keys / OAuth.

Long‑term / AI layer:

1. Predictive resource usage modeling.
2. Natural language query interface ("Why is memory high?").
3. Recommendation engine (e.g. suggest service restarts or scaling steps).

## 4. Architecture (Incremental Outline)

| Layer | Current | Future Expansion |
|-------|---------|------------------|
| API   | FastAPI monolith (`main.py`) | Modular routers (metrics, processes, admin) |
| Data Collection | psutil inline | Async tasks + plugin collectors |
| Streaming | (none) | WebSocket/SSE broadcasting hub |
| Persistence | (none) | PostgreSQL (metrics, events), Redis (caching) |
| AI / Analytics | (none) | Background workers (Celery / RQ) + model store |
| Frontend | placeholder | SPA dashboard + charts + live process table |

## 5. Directory Layout (Minimal Now)

```text
ai-process-manager/
├── main.py               # FastAPI app (metrics endpoint)
├── test_main.py          # Basic pytest test
├── requirements.txt      # Runtime deps (FastAPI, Uvicorn, psutil)
├── requirements-dev.txt  # Dev tools (pytest, black, flake8, mypy)
├── frontend/             # (empty placeholder for future UI)
└── README.md             # This document
```

## 6. Installation & Run

Runtime dependencies:

```bash
uv pip install -r requirements.txt
```

Run development server:

```bash
uvicorn main:app --reload
```

Access: `http://127.0.0.1:8000/metrics` (optionally `?limit=10`).

## 7. Testing

Install dev dependencies & run tests (fast mode skips sleep):

```bash
uv pip install -r requirements-dev.txt
FAST_TEST=1 pytest -q
```

Expected test output: 1 passing test validating structure of `/metrics` response.

## 8. Configuration (Planned)

Will adopt environment variables (prefix `APM_`) for: port, intervals, CORS, feature toggles, DB connection, and performance limits. (Not yet implemented in minimal version.)

## 9. API Examples

Example request:

```bash
curl 'http://127.0.0.1:8000/metrics?limit=3'
```

Example truncated response:

```json
{
 "cpu_percent": 14.2,
 "memory_percent": 62.5,
 "processes": [
  {"pid": 1234, "name": "python", "cpu": 37.5, "memory": 1.2, "status": "running"},
  {"pid": 222,  "name": "nginx",  "cpu": 12.0, "memory": 0.3, "status": "sleeping"},
  {"pid": 77,   "name": "dockerd","cpu":  5.0, "memory": 0.8, "status": "sleeping"}
 ]
}
```

## 10. Development Guidelines (Initial)

Formatting / lint:

```bash
black .
flake8 .
mypy .
```

Future additions: pre-commit hooks, type-enforced API models, CI pipeline.

## 11. Contributing (Future State)

Will define issue templates, contribution guidelines, and code ownership once core modules are added. Early contributions: adding extra metrics or WebSocket prototype.

## 12. Security Considerations (Planned)

- Will restrict process control endpoints with auth.
- Avoid exposing full command lines or usernames unless authorized.
- Rate limiting & CORS tightening when frontend origin known.
