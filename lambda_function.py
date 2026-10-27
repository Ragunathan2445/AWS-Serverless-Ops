
import json
import logging
from datetime import datetime, timezone

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    records = event.get("Records", [])
    results = []

    for record in records:
        try:
            message = json.loads(record["body"])
            job_id = message.get("job_id", "unknown")
            action = message.get("action", "process")

            logger.info(
                "Processing job_id=%s action=%s",
                job_id,
                action,
            )

            if message.get("simulate_failure") is True:
                raise ValueError("Simulated job failure")

            results.append({
                "job_id": job_id,
                "status": "success",
                "processed_at": datetime.now(
                    timezone.utc
                ).isoformat(),
            })

        except Exception:
            logger.exception("Job processing failed")
            raise

    return {
        "statusCode": 200,
        "body": json.dumps({
            "processed_count": len(results),
            "results": results,
        }),
    }
