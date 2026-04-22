# FIXES.md

## api/main.py
- **Line 7**: Hardcoded Redis host `"localhost"`. Changed to `os.getenv('REDIS_HOST', 'redis')` so it resolves correctly inside Docker.
- **Added**: `/health` endpoint required for container health checks and the `depends_on: condition: service_healthy` chain.

## worker/worker.py
- **Line 6**: Redis connection used `"localhost"`, which fails in Docker. Replaced with `os.getenv("REDIS_HOST", "redis")`.
- **Line 6**: No Redis password support. Added `password=os.getenv("REDIS_PASSWORD", None)`.
- **Line 15**: Hardcoded queue name `"job"` did not match the API's queue name `"jobs"`. Replaced with `os.getenv("QUEUE_NAME", "jobs")`.
- **Line 13**: Infinite loop with no signal handling prevented graceful container shutdown. Added `SIGTERM`/`SIGINT` handlers and a `running` flag.
- **Line 18**: Manual `.decode()` on Redis responses. Enabled `decode_responses=True` on the Redis client instead.

## frontend/app.js
- **Line 6**: Hardcoded API URL `"localhost"` breaks Docker networking. Replaced with `process.env.API_URL || "http://api:8000"`.
- **Lines 11, 20**: Axios requests had no timeout, causing potential hangs. Added `timeout: 5000` via `axios.create`.
- **Lines 13, 22**: Errors were silently swallowed. Added `err.message` in the JSON error response.
- **Added**: `/health` route for container health checks.
- **Line 27**: Hardcoded port `3000`. Replaced with `process.env.PORT || 3000`.

## frontend/eslintrc.json
- **Filename**: File was named `eslintrc.json` (missing leading dot). ESLint cannot discover it without the dot. Renamed to `.eslintrc.json`.

## docker-compose.yaml
- **frontend.depends_on**: Used list syntax (`- api:`) instead of map syntax (`api:`), causing a YAML parse error and the `condition: service_healthy` to be ignored. Fixed to proper map syntax.
- **redis service**: Missing `command` to start Redis with password auth (`--requirepass`). Without it, the `redis-cli -a` healthcheck always fails and authenticated clients are rejected.
- **api service**: Missing `QUEUE_NAME` environment variable. The API uses `QUEUE_NAME` to push jobs; without it the env var is undefined inside the container.
- **api healthcheck**: Used `curl` which is not present in the `python:3.12-slim-bookworm` image. Replaced with a Python `urllib.request` one-liner.

## .env.example
- **REDIS_PASSWORD**: Contained a real password value (`supersecretpassword123`). Replaced with placeholder `your_redis_password_here`.
- **Missing variables**: `API_URL` and `PORT` were used by the frontend service but absent from `.env.example`. Added both.

## frontend/Dockerfile
- **Line 7**: `npm ci --omit=dev` fails on two counts: `--omit` flag not supported by the npm version bundled in `node:18-alpine`, and `npm ci` requires a `package-lock.json` which is absent. Changed to `npm install --only=production`.

## api/conftest.py (new file)
- **Missing**: No `conftest.py` existed, so `import main` in `tests/test_api.py` raised `ModuleNotFoundError` when pytest was invoked from any directory other than `api/`. Added `conftest.py` that inserts the `api/` directory into `sys.path`.

## .github/workflows/pipeline.yml
- **Line 16**: `action/setup-python` (typo — missing `s`). Corrected to `actions/setup-python@v4`. This caused the lint and test jobs to fail immediately.
- **Line 44**: Same `action/setup-python` typo in the test job.
- **build job**: Incomplete — no Docker build/push steps. Added full multi-image build with SHA and `latest` tags pushed to a local registry service container.
- **Missing jobs**: `security-scan`, `integration-test`, and `deploy` jobs were entirely absent. Added all three with correct `needs:` ordering to enforce `lint → test → build → security-scan → integration-test → deploy`.
- **hadolint step**: Missing `dockerfile:` input, so it only linted the default `Dockerfile` path. Added separate steps for all three Dockerfiles.

## README.md
- File contained only the repo name. Added prerequisites, startup commands, environment variable reference, and description of a successful startup.
