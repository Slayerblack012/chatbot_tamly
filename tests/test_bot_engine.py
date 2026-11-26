"""Unit tests for CounselorEngine, message sanitization, role merging, and prompts."""

import asyncio

from core.bot_engine import (
    AUTH_FAILURE_MESSAGE,
    PARTIAL_REPLY_FALLBACK,
    QUOTA_FALLBACK_MESSAGE,
    TEMPORARY_FALLBACK_MESSAGE,
    CounselorEngine,
    is_auth_error,
    is_model_overloaded_error,
    is_model_unavailable_error,
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
    assert "Bạn là An Nhiên" in inst
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


def test_persona_is_short_nonjudgmental_and_non_diagnostic():
    assert "150 từ" in BASE_COUNSELOR_PERSONA
    assert "không phán xét" in BASE_COUNSELOR_PERSONA
    assert "Không khuyên nghỉ học 1-2 ngày" in BASE_COUNSELOR_PERSONA
    assert "không chẩn đoán" in BASE_COUNSELOR_PERSONA


def test_provider_exception_content_is_not_logged(caplog):
    private_marker = "PRIVATE_MESSAGE_FOR_LOG_TEST"

    class FakeChat:
        async def send_message_stream(self, message):
            raise RuntimeError(private_marker)

    class FakeChats:
        def create(self, **kwargs):
            return FakeChat()

    class FakeAio:
        chats = FakeChats()

    class FakeClient:
        aio = FakeAio()

    engine = CounselorEngine(api_key="TEST_DUMMY_KEY")
    engine.client = FakeClient()

    async def collect_response():
        return [
            chunk
            async for chunk in engine.async_stream_chat(
                [{"role": "user", "content": private_marker}]
            )
        ]

    asyncio.run(collect_response())

    assert private_marker not in caplog.text


def test_quota_and_auth_error_detection():
    assert is_quota_error("RESOURCE_EXHAUSTED: 429 quota exceeded")
    assert is_auth_error("401 UNAUTHENTICATED: invalid API key")
    assert not is_quota_error("network timeout")


def test_model_fallback_only_for_model_availability_errors():
    assert is_model_unavailable_error("model not found")
    assert is_model_unavailable_error("404 NOT_FOUND")
    assert is_model_unavailable_error("Unsupported model")
    assert not is_model_unavailable_error("network timeout")
    assert is_model_overloaded_error("503 UNAVAILABLE: high demand")
    assert is_model_overloaded_error("temporarily unavailable")
    assert not is_model_overloaded_error("network timeout")


def test_public_fallback_messages_are_user_friendly():
    assert "hết lượt" in QUOTA_FALLBACK_MESSAGE
    assert "API Key" in AUTH_FAILURE_MESSAGE
    assert "gửi lại" in TEMPORARY_FALLBACK_MESSAGE
    assert "phản hồi hoàn chỉnh" in PARTIAL_REPLY_FALLBACK
