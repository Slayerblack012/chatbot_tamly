import re
import unicodedata
from typing import Any, Dict, Iterable

CRISIS_PATTERNS = (
    r"\bngu khong day nua\b",
    r"\bkhong muon ton tai nua\b",
    r"\bmuon bien mat\b",
    r"\bkhong muon song nua\b",
    r"\bkhong muon song\b",
    r"\bket thuc cuoc doi\b",
    r"\bket thuc cuoc song\b",
    r"\bmuon chet\b",
    r"\btu tu\b",
    r"\btu hai\b",
    r"\btu lam dau\b",
    r"\bcat tay\b",
    r"\btu lam ton thuong\b",
    r"\btu lam hai ban than\b",
    r"\bkhong o day\b",
    r"\bkhong o day nua\b",
    r"\bkhong co minh\b",
    r"\bngoi khong day nua\b",
    r"\bi wish i were dead\b",
    r"\bi want to disappear\b",
    r"\bkill myself\b",
    r"\bsuicid",
)

EXPLICIT_DENIAL_PATTERNS = (
    r"\bkhong co y dinh tu tu\b",
    r"\bkhong co y dinh tu hai\b",
    r"\bkhong nghi den viec tu tu\b",
    r"\bkhong nghi den viec tu hai\b",
    r"\bkhong muon tu tu\b",
    r"\bkhong muon tu hai\b",
)

CRISIS_RESPONSE = """**Hỗ trợ ngay:** gọi **111** để được hỗ trợ bảo vệ trẻ em; gọi **115** nếu bạn đang gặp nguy hiểm hoặc cần cấp cứu. Bạn cũng có thể liên hệ **Đường dây Ngày Mai: 096 306 1414**.

**Bạn có đang định làm đau mình ngay lúc này, hoặc đã chuẩn bị cách thực hiện chưa? Bạn đang ở một mình không?**

Nếu nguy hiểm đang ở ngay trước mắt, hãy gọi 115 hoặc đến khoa cấp cứu gần nhất, và báo ngay cho một người lớn đáng tin cậy ở cạnh bạn. Bạn có thể trả lời ngắn gọn: “đang nguy hiểm” hoặc “đang an toàn”. Mình sẽ tiếp tục ở đây cùng bạn."""


def normalize_crisis_text(text: str) -> str:
    normalized = unicodedata.normalize("NFD", text.lower())
    without_marks = "".join(
        char for char in normalized if unicodedata.category(char) != "Mn"
    )
    return without_marks.replace("đ", "d")


def is_crisis_message(text: str) -> bool:
    normalized = normalize_crisis_text(text)
    for pattern in EXPLICIT_DENIAL_PATTERNS:
        normalized = re.sub(pattern, " ", normalized)
    return any(re.search(pattern, normalized) for pattern in CRISIS_PATTERNS)


def latest_user_message(messages: Iterable[Dict[str, Any]]) -> str:
    for message in reversed(list(messages)):
        if message.get("role") == "user":
            content = message.get("content", "")
            return content if isinstance(content, str) else str(content)
    return ""
