"""API Gateway TOKEN authorizer.

Allows a request only if its `Authorization: Bearer <token>` header matches the
shared secret held in Secrets Manager. Any other request is rejected with 401.
"""

import hmac
import os
from functools import cache

import boto3

BEARER_PREFIX = "Bearer "


@cache
def _shared_secret() -> str:
    """Fetch the shared secret once per Lambda container and reuse it for warm invocations."""
    client = boto3.client("secretsmanager")
    response = client.get_secret_value(SecretId=os.environ["SHARED_SECRET_ARN"])
    return response["SecretString"]


def _api_wide_resource(method_arn: str) -> str:
    """Widen a method ARN to cover every method and path in the same API stage.

    API Gateway caches the returned policy per token, not per route. If the policy
    only allowed the method that was called, the cached policy would deny the next
    route called with the same token until the cache expired.
    """
    # method_arn looks like: arn:aws:execute-api:{region}:{account}:{api_id}/{stage}/{verb}/{path}
    api_and_stage = "/".join(method_arn.split("/")[:2])
    return f"{api_and_stage}/*/*"


def handler(event, context):
    token = event.get("authorizationToken") or ""
    supplied = token[len(BEARER_PREFIX):] if token.startswith(BEARER_PREFIX) else ""

    # compare_digest takes the same time whether the first or last character differs,
    # so response timing can't be used to guess the secret one character at a time.
    if not supplied or not hmac.compare_digest(supplied.encode(), _shared_secret().encode()):
        # API Gateway turns this exact message into a 401 response.
        raise Exception("Unauthorized")

    return {
        "principalId": "operator",
        "policyDocument": {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": "execute-api:Invoke",
                    "Effect": "Allow",
                    "Resource": _api_wide_resource(event["methodArn"]),
                }
            ],
        },
    }
