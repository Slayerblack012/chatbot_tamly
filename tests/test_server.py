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


def test_b64_decode_rejects_non_object_json():
    encoded = b64_encode_text(json.dumps(["not", "an object"]))
    with pytest.raises(HTTPException) as exc_info:
        b64_decode_json(encoded)
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
    assert "facilities" in knowledge
    assert len(knowledge["facilities"]) >= 5
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


def test_chat_rejects_non_object_messages():
    payload = b64_encode_text(json.dumps({"messages": ["invalid"]}))
    response = client.post("/api/chat", json={"p": payload})
    assert response.status_code == 400


def test_summary_rejects_invalid_conversation_roles():
    payload = b64_encode_text(json.dumps({
        "messages": [
            {"role": "user", "content": "Tin một"},
            {"role": "user", "content": "Tin hai"},
        ]
    }))
    response = client.post("/api/summary", json={"p": payload})
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


def test_tts_rejects_empty_text():
    response = client.post("/api/tts", json={"text": ""})
    assert response.status_code == 400


def test_tts_response_is_not_cached(monkeypatch):
    import httpx

    class FakeResponse:
        status_code = 200
        content = b"fake_mp3_content_bytes" * 30

    class FakeClient:
        def __init__(self, *args, **kwargs):
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, *args):
            return None

        async def get(self, *args, **kwargs):
            return FakeResponse()

    monkeypatch.setattr(httpx, "AsyncClient", FakeClient)
    response = client.post("/api/tts", json={"text": "test phrase"})
    assert response.status_code == 200
    assert response.headers["content-type"] == "audio/mpeg"
    assert response.content == FakeResponse.content


def test_facilities_endpoint():
    response = client.get("/api/facilities")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["count"] == 6
    assert len(data["data"]) == 6

    # Filter by bien_hoa location
    res_bh = client.get("/api/facilities?location=bien_hoa")
    assert res_bh.status_code == 200
    data_bh = res_bh.json()
    assert data_bh["status"] == "success"
    assert data_bh["count"] == 6
    for item in data_bh["data"]:
        assert item["location"] == "bien_hoa"
        verification = item["verification"]
        if verification["address_verified"]:
            assert item["address"] is not None
        else:
            assert item["address"] is None
        if verification["phone_verified"]:
            assert item["phone"] is not None
        else:
            assert item["phone"] is None

    minh_tri = next(item for item in data_bh["data"] if item["id"] == "pk_tamly_minhtri")
    assert minh_tri["phone"] == "0251 3685 676"
    assert minh_tri["email"] == "minhtricare@gmail.com"

    central_hospital = next(item for item in data_bh["data"] if item["id"] == "bv_tamthan_tw2")
    assert central_hospital["address"].startswith("Số 1310")
    assert central_hospital["phone"] == "0251 3822 965"
    assert central_hospital["timing"] is None
    assert central_hospital["reported_timing"] == "Khám ngoại trú theo lịch bác sĩ, thứ Hai - thứ Sáu"


def test_crisis_chat_bypasses_ai_and_returns_safety_response(monkeypatch):
    import server
    from core.crisis import CRISIS_RESPONSE

    async def forbidden_provider_call(*args, **kwargs):
        raise AssertionError("Crisis responses must not call the AI provider")

    monkeypatch.setattr(server.engine, "async_stream_chat", forbidden_provider_call)
    payload = b64_encode_text(json.dumps({
        "messages": [{"role": "user", "content": "Mọi người sẽ nhẹ nhõm khi không có mình"}]
    }))
    response = client.post("/api/chat", json={"p": payload})
    assert response.status_code == 200
    assert "text/event-stream" in response.headers["content-type"]
    assert b64_encode_text(CRISIS_RESPONSE) in response.text


def test_privacy_delete_receipt_and_shared_data_apis_removed():
    response = client.delete("/api/privacy/data")
    assert response.status_code == 200
    assert response.json()["server_records_deleted"] == 0
    assert response.json()["server_retains_health_records"] is False

    assert client.get("/api/sessions").status_code == 404
    assert client.get("/api/moods").status_code == 404
    assert client.get("/api/quizzes/results").status_code == 404


def test_unlicensed_audio_is_not_served():
    response = client.get("/static/audio/rain.mp3")
    assert response.status_code == 404


def test_accessibility_and_privacy_controls_are_present():
    response = client.get("/")
    assert 'role="alert" aria-live="assertive"' in response.text
    assert 'id="btn-hard-delete-history"' in response.text
    assert 'id="audio-rain" preload="none"' in response.text

