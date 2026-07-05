"""Sample AWS Lambda function triggered on S3 audio upload."""

import json
import logging
import os
from datetime import datetime, timezone

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    """
    Lambda handler for S3 PutObject events.
    Logs upload metadata for Clinical Speech Intelligence Platform.
    """
    records = event.get("Records", [])
    results = []

    for record in records:
        bucket = record["s3"]["bucket"]["name"]
        key = record["s3"]["object"]["key"]
        size = record["s3"]["object"].get("size", 0)

        metadata = {
            "event": "audio_upload",
            "bucket": bucket,
            "key": key,
            "size_bytes": size,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "platform": os.environ.get("PLATFORM_NAME", "csip"),
        }

        logger.info("Audio upload detected: %s", json.dumps(metadata))
        results.append(metadata)

    return {
        "statusCode": 200,
        "body": json.dumps({"processed": len(results), "records": results}),
    }
