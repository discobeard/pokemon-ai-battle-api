import boto3
import pytest
from moto import mock_aws

from pokemon_battle.handlers import authorizer

SECRET = "correct-horse-battery-staple"
METHOD_ARN = "arn:aws:execute-api:eu-west-2:123456789012:abc123/prod/GET/health"


@pytest.fixture(autouse=True)
def shared_secret(monkeypatch):
    """Store the shared secret in a fake Secrets Manager and point the authorizer at it."""
    monkeypatch.setenv("AWS_DEFAULT_REGION", "eu-west-2")
    with mock_aws():
        secret = boto3.client("secretsmanager").create_secret(
            Name="/pokemon-ai-battle/api-shared-secret", SecretString=SECRET
        )
        monkeypatch.setenv("SHARED_SECRET_ARN", secret["ARN"])
        # The secret is cached per container; clear it so each test sees its own fake.
        authorizer._shared_secret.cache_clear()
        yield


def authorize(token):
    event = {"type": "TOKEN", "methodArn": METHOD_ARN}
    if token is not None:
        event["authorizationToken"] = token
    return authorizer.handler(event, None)


def test_correct_token_is_allowed_across_the_whole_api():
    result = authorize(f"Bearer {SECRET}")

    [statement] = result["policyDocument"]["Statement"]
    assert statement["Effect"] == "Allow"
    assert statement["Action"] == "execute-api:Invoke"
    # Covers every route, so a cached decision doesn't deny the next route called.
    assert statement["Resource"] == "arn:aws:execute-api:eu-west-2:123456789012:abc123/prod/*/*"


@pytest.mark.parametrize(
    "token",
    [
        pytest.param("Bearer wrong-secret", id="wrong secret"),
        pytest.param(f"Bearer {SECRET}x", id="secret with extra characters"),
        pytest.param(SECRET, id="missing Bearer prefix"),
        pytest.param(f"Basic {SECRET}", id="wrong scheme"),
        pytest.param("Bearer ", id="empty token"),
        pytest.param(None, id="missing header"),
    ],
)
def test_anything_but_the_correct_bearer_token_is_unauthorized(token):
    with pytest.raises(Exception, match="^Unauthorized$"):
        authorize(token)
