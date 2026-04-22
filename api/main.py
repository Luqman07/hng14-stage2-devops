from fastapi import FastAPI, HTTPException
import redis
import uuid
import os

app = FastAPI()

def get_redis():
    return redis.Redis(
        host=os.getenv("REDIS_HOST", "redis"),
        port=int(os.getenv("REDIS_PORT", 6379)),
        password=os.getenv("REDIS_PASSWORD", None),
        decode_responses=True
    )

r = get_redis()

QUEUE_NAME = os.getenv("QUEUE_NAME", "jobs")

@app.get("/health")
def health_check():
    r.ping()  # Check if Redis is reachable
    return {"status": "healthy"}

@app.post("/jobs")
def create_job():
    job_id = str(uuid.uuid4())
    r.lpush(QUEUE_NAME, job_id)
    r.hset(f"job:{job_id}", "status", "queued")
    return {"job_id": job_id}

@app.get("/jobs/{job_id}")
def get_job(job_id: str):
    status = r.hget(f"job:{job_id}", "status")
    if not status:
        raise HTTPException(status_code=404, detail="Job not found")
    return {"job_id": job_id, "status": status}