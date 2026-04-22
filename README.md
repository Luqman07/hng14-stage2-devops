# hng14-stage2-devops

A containerized job processing system with a CI/CD pipeline.

## Services

- **frontend** (Node.js/Express) — Job submission UI on port 3000
- **api** (Python/FastAPI) — Job creation and status API on port 8000
- **worker** (Python) — Background job processor
- **redis** — Shared queue and job state store (internal only)

## Prerequisites

- Docker >= 24
- Docker Compose >= 2.20
- Git

## Quick Start

```bash
# 1. Clone the repo
git clone <your-fork-url>
cd hng14-stage2-devops

# 2. Create your .env file from the example
cp .env.example .env
# Edit .env and set a strong REDIS_PASSWORD

# 3. Bring the stack up
docker compose up -d --build

# 4. Check all services are healthy
docker compose ps
```

## What a Successful Startup Looks Like

```
NAME       STATUS
redis      Up (healthy)
api        Up (healthy)
worker     Up (healthy)
frontend   Up (healthy)
```

Open http://localhost:3000 in your browser. Click **Submit New Job** — the job should transition from `queued` → `completed` within a few seconds.

## Environment Variables

See `.env.example` for all required variables. Never commit `.env`.

| Variable        | Description                        |
|-----------------|------------------------------------|
| REDIS_HOST      | Redis service hostname             |
| REDIS_PORT      | Redis port (default 6379)          |
| REDIS_PASSWORD  | Redis auth password                |
| QUEUE_NAME      | Job queue name (default `jobs`)    |
| API_URL         | Internal API URL for the frontend  |
| PORT            | Frontend port (default 3000)       |

## Stopping the Stack

```bash
docker compose down -v
```
