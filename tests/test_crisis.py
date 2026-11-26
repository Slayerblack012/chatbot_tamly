import time

from core.crisis import CRISIS_RESPONSE, is_crisis_message


def test_indirect_crisis_phrases_with_and_without_diacritics():
    phrases = (
        "Mình muốn ngủ không dậy nữa",
        "Mọi người sẽ nhẹ nhõm khi không có mình",
        "Mình không muốn tồn tại nữa",
        "Mình muốn biến mất",
        "Mọi chuyện sẽ ổn khi mình không ở đây",
        "toi muon bien mat",
    )
    assert all(is_crisis_message(phrase) for phrase in phrases)


def test_explicit_denial_does_not_match_but_other_risk_still_does():
    assert not is_crisis_message("Mình không có ý định tự tử.")
    assert is_crisis_message("Mình không có ý định tự tử nhưng muốn biến mất.")
    assert is_crisis_message("Mình không muốn sống nữa.")


def test_crisis_detection_is_under_500ms():
    started = time.perf_counter()
    assert is_crisis_message("Mọi chuyện sẽ ổn khi mình không ở đây")
    assert time.perf_counter() - started < 0.5


def test_crisis_template_leads_with_hotlines_and_direct_safety_check():
    hotline_position = min(
        CRISIS_RESPONSE.index("111"),
        CRISIS_RESPONSE.index("115"),
        CRISIS_RESPONSE.index("096 306 1414"),
    )
    question_position = CRISIS_RESPONSE.index("Bạn có đang định làm đau mình ngay lúc này")
    assert hotline_position < question_position
    assert "Bạn đang ở một mình không?" in CRISIS_RESPONSE
