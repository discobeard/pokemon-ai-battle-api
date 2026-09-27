import json

from pokemon_battle.handlers import health


def test_health_reports_ok_with_cors_header():
    response = health.handler({}, None)

    assert response["statusCode"] == 200
    assert json.loads(response["body"]) == {"status": "ok"}
    assert response["headers"]["Access-Control-Allow-Origin"] == "*"
