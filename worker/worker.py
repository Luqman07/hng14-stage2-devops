import redis
import time
import os
import signal
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

r = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    password=os.getenv("REDIS_PASSWORD", None),
    decode_responses=True,
)

QUEUE_NAME = os.getenv("QUEUE_NAME", "jobs")

running = True


def shutdown_handler(signum, frame):
    global running
    logger.info("Shutting down worker...")
    running = False


signal.signal(signal.SIGTERM, shutdown_handler)
signal.signal(signal.SIGINT, shutdown_handler)


def process_job(job_id):
    logger.info(f"Processing job {job_id}")
    time.sleep(2)  # simulate work
    r.hset(f"job:{job_id}", "status", "completed")
    logger.info(f"Done: {job_id}")


while running:
    job = r.brpop(QUEUE_NAME, timeout=5)
    if job:
        _, job_id = job
        try:
            process_job(job_id)
        except Exception as e:
            logger.error(f"Error processing job {job_id}: {e}")
            r.hset(f"job:{job_id}", "status", "failed")
