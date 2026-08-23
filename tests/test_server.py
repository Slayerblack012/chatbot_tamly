"""Unit and Integration tests for FastAPI Server."""

import base64
import json

import pytest
from fastapi import HTTPException
from starlette.testclient import TestClient

from server import app, b64_decode_json, b64_encode_text, check_rate_limit, get_client_ip, request_history

client = TestClient(app)


def test_b64_encode_and_decode():
    original = {"hello": "xin chào", "numbers": [1, 2, 3]}
    encoded = b64_encode_text(json.dumps(original))
    decoded = b64_decode_json(encoded)
    assert decoded == original


def test_b64_decode_invalid():
    with pytest.raises(HTTPException) as exc_info:
        b64_decode_json("!!!invalid_base64!!!")
    assert exc_info.value.status_code == 400


def test_security_headers_and_csp():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.headers.get("X-Content-Type-Options") == "nosniff"
    assert response.headers.get("X-Frame-Options") == "SAMEORIGIN"
    assert response.headers.get("X-XSS-Protection") == "1; mode=block"
    assert "Content-Security-Policy" in response.headers
    csp = response.headers.get("Content-Security-Policy")
    assert "default-src 'self'" in csp
    assert "script-src" in csp


def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data


def test_knowledge_endpoint():
    response = client.get("/api/knowledge")
    assert response.status_code == 200
    data = response.json()
    assert "d" in data
    decoded_raw = base64.b64decode(data["d"]).decode("utf-8")
    knowledge = json.loads(decoded_raw)
    assert "distortions" in knowledge
    assert "articles" in knowledge
    assert "quizzes" in knowledge
    assert "phq9" in knowledge["quizzes"]
    assert "gad7" in knowledge["quizzes"]


def test_index_serves_html():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")
    assert "An Nhiên Tâm Lý" in response.text


def test_chat_invalid_payload():
    response = client.post("/api/chat", json={"p": "invalid_payload"})
    assert response.status_code == 400


def test_chat_empty_messages():
    payload = b64_encode_text(json.dumps({"messages": []}))
    response = client.post("/api/chat", json={"p": payload})
    assert response.status_code == 400


def test_rate_limit_function():
    test_ip = "192.168.1.99"
    request_history[test_ip] = []

    # 45 requests should pass
    for _ in range(45):
        check_rate_limit(test_ip)

    # 46th request should raise 429
    with pytest.raises(HTTPException) as exc:
        check_rate_limit(test_ip)
    assert exc.value.status_code == 429

    # Clean up
    request_history.pop(test_ip, None)


def test_get_client_ip_proxy_header(monkeypatch):
    class DummyRequest:
        def __init__(self, forwarded=None, host="127.0.0.1"):
            self.headers = {"X-Forwarded-For": forwarded} if forwarded else {}
            self.client = type("Client", (), {"host": host})()

    # When TRUST_PROXY_HEADERS is False (default) -> should return socket IP
    monkeypatch.setattr("server.TRUST_PROXY_HEADERS", False)
    req = DummyRequest(forwarded="203.0.113.195", host="192.168.1.50")
    assert get_client_ip(req) == "192.168.1.50"

    # When TRUST_PROXY_HEADERS is True -> should trust X-Forwarded-For
    monkeypatch.setattr("server.TRUST_PROXY_HEADERS", True)
    req = DummyRequest(forwarded="203.0.113.195, 70.41.3.18", host="192.168.1.50")
    assert get_client_ip(req) == "203.0.113.195"
