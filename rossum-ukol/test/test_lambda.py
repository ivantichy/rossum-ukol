import json
from fastapi.testclient import TestClient
from lambda_function import app  # type: ignore


client = TestClient(
    app, raise_server_exceptions=False
)  # raise_server_exceptions=False - this actually catches unhandled exceptions and returns HTTP/50x response codes


def test_service_http_401(mock_requests):
    response = client.get('export/1234/5678')
    assert response.status_code == 401


def test_service_basic_auth(mock_requests):
    response = client.get('export/1234/5678', auth=("user", "rossum"))
    assert response.status_code == 200


def test_service_failed(mock_requests):
    response = client.get('export/1234/56789', auth=("user", "rossum"))
    assert response.status_code == 200
    assert json.loads(response.content).get("success") == False


def test_service_success(mock_requests):
    response = client.get('export/1234/5678', auth=("user", "rossum"))
    assert response.status_code == 200
    assert json.loads(response.content).get("success") == True
