"""Unit tests for CounselorEngine, message sanitization, role merging, and prompts."""

from core.bot_engine import (
    AUTH_FAILURE_MESSAGE,
    QUOTA_FALLBACK_MESSAGE,
    STREAM_STOP_MESSAGE,
    TEMPORARY_FALLBACK_MESSAGE,
    CounselorEngine,
    is_auth_error,
    is_quota_error,
    sanitize_messages_for_gemini,
)
from core.prompts import BASE_COUNSELOR_PERSONA, get_time_greeting


def test_sanitize_messages_role_merging():
    # Test merging consecutive user messages
    raw = [
        {"role": "user", "content": "Tin 1"},
        {"role": "user", "content": "Tin 2"},
        {"role": "model", "content": "Phản hồi 1"},
        {"role": "model", "content": "Phản hồi 2"},
        {"role": "user", "content": "Tin 3"}
    ]
    cleaned = sanitize_messages_for_gemini(raw)
    assert len(cleaned) == 3
    assert cleaned[0]["role"] == "user"
    assert "Tin 1\n\nTin 2" in cleaned[0]["content"]
    assert cleaned[1]["role"] == "model"
    assert "Phản hồi 1\n\nPhản hồi 2" in cleaned[1]["content"]
    assert cleaned[2]["role"] == "user"
    assert cleaned[2]["content"] == "Tin 3"


def test_sanitize_messages_empty():
    assert sanitize_messages_for_gemini([]) == []
    assert sanitize_messages_for_gemini([{"role": "user", "content": "   "}]) == []


def test_counselor_engine_system_instruction():
    engine = CounselorEngine(api_key="TEST_DUMMY_KEY")
    inst = engine.build_system_instruction(
        mode="cbt",
        mood_context={
            "mood_name": "Lo âu",
            "stress_level": 8,
            "note": "Áp lực thi tốt nghiệp"
        }
    )
    assert "An Nhiên Tâm Lý" in inst
    assert "Lo âu" in inst
    assert "8/10" in inst
    assert "Áp lực thi tốt nghiệp" in inst


def test_counselor_engine_candidate_models():
    engine = CounselorEngine(api_key="TEST_DUMMY_KEY")
    candidates = engine._get_candidate_models("gemini-3.6-flash")
    assert candidates[0] == "gemini-3.6-flash"
    assert len(candidates) >= 3


def test_time_greeting():
    greeting = get_time_greeting()
    assert isinstance(greeting, str)
    assert len(greeting) > 0


def test_persona_contains_crisis_instructions():
    assert "111" in BASE_COUNSELOR_PERSONA
    assert "115" in BASE_COUNSELOR_PERSONA
    assert "096 306 1414" in BASE_COUNSELOR_PERSONA


def test_quota_and_auth_error_detection():
    assert is_quota_error("RESOURCE_EXHAUSTED: 429 quota exceeded")
    assert is_auth_error("401 UNAUTHENTICATED: invalid API key")
    assert not is_quota_error("network timeout")


def test_public_fallback_messages_are_user_friendly():
    assert "hết lượt" in QUOTA_FALLBACK_MESSAGE
    assert "API Key" in AUTH_FAILURE_MESSAGE
    assert "gửi lại" in TEMPORARY_FALLBACK_MESSAGE
    assert "gửi lại" in STREAM_STOP_MESSAGE
