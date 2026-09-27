"""Health check: confirms the API, the authorizer and Lambda wiring all work end to end."""

import json


def handler(event, context):
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            # Lambda proxy integrations must set CORS headers themselves; the API's
            # preflight config only covers OPTIONS requests.
            "Access-Control-Allow-Origin": "*",
        },
        "body": json.dumps({"status": "ok"}),
    }
