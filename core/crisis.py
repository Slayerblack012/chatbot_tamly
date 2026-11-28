import re
import unicodedata
from typing import Any, Dict, Iterable

EXPLICIT_DENIAL_PATTERNS = (
    r"\bkhong co y dinh tu tu\b",
    r"\bkhong co y dinh tu hai\b",
    r"\bkhong nghi den viec tu tu\b",
    r"\bkhong nghi den viec tu hai\b",
    r"\bkhong muon tu tu\b",
    r"\bkhong muon tu hai\b",
)

# Safe colloquial patterns / academic study contexts in Vietnamese teen speech
SAFE_PATTERNS = (
    r"kho muon chet",
    r"doi muon chet",
    r"cuoi chet",
    r"nao chet luon",
    r"chet chac roi",
    r"chet hoai khong qua",
    r"co giet minh qua",
    r"phong chong tu tu",
    r"bai thuyet trinh ve.*tu tu",
    r"poster ve.*suc khoe",
    r"nhan vat chinh.*mat",
    r"phim.*mat",
    r"truyen.*mat",
    r"ngu mot giac that da",
    r"ngu bu.*suong",
    r"di tu qua",
    r"muon tron khoi thanh pho",
    r"het pin.*cham het",
    r"muon don tho",
    r"doi xiu",
    r"tuc muon xiu",
    r"met muon xiu",
    r"tieu doi.*quen lam bai",
)

CRISIS_PATTERNS = (
    # Direct suicidal ideation / attempts
    r"\bkhong muon song\b",
    r"\bchua tung muon song\b",
    r"\bsong chi nua\b",
    r"\bsong lam gi nua\b",
    r"\bchet di cho roi\b",
    r"\bchet di la xong\b",
    r"\bmuon chet that\b",
    r"\bmuon chet\b",
    r"\bchet di\b",
    r"\btu tu\b",
    r"\btu sat\b",
    r"\bkhong con ly do gi de song\b",
    r"\bmuon ket thuc tat ca\b",
    r"\bket thuc moi thu\b",
    r"\bket thuc cuoc doi\b",
    r"\bket thuc cuoc song\b",
    r"\bthu tuyet menh\b",
    r"\bdung tren san thuong\b",
    r"\blam dieu dai dot\b",
    r"\btung thu tu tu\b",
    r"\bk muon song\b",
    r"\bko muon song\b",
    r"\buong thuoc ngu\b",
    # Indirect / subtle risk signs
    r"\bngu luon khong day\b",
    r"\bngu khong day\b",
    r"\bngu 1 giac that dai.*mai mai\b",
    r"\bngu mot giac.*bien mat\b",
    r"\bnham mat la mong khong phai mo ra\b",
    r"\bmoi nguoi se on hon khi khong co minh\b",
    r"\bse nhe nhom khi khong co minh\b",
    r"\bkhong co minh\b",
    r"\bchi la ganh nang\b",
    r"\bla ganh nang cho\b",
    r"\bneu mai minh khong con nua\b",
    r"\bneu ngay mai khong thay minh online\b",
    r"\bdung tim minh\b",
    r"\bneu minh chet thi\b",
    r"\bviet thu tam biet\b",
    r"\bdem do quy cho het\b",
    r"\bcho het ban be.*khong can nua\b",
    r"\bxoa het tai khoan.*don dep\b",
    r"\bmuon di dau that xa.*khong bao gio quay ve\b",
    r"\bdi luon cho ranh\b",
    r"\bmet moi voi cuoc doi nay lam roi\b",
    r"\bkhong muon ton tai nua\b",
    r"\bcha muon ton tai\b",
    r"\bmuon bien mat\b",
    r"\bneu minh bien mat\b",
    r"\bchua tung duoc sinh ra\b",
    r"\bkhong ai can minh het\b",
    r"\bkhong ai can minh\b",
    r"\bco hay khong co cung vay\b",
    r"\bkhong o day nua\b",
    r"\bkhong o day\b",
    r"\bkhong con loi thoat\b",
    r"\blan cuoi minh noi chuyen\b",
    r"\bchac day la lan cuoi\b",
    r"\bcam on vi da nghe minh.*tam biet\b",
    r"\bdung lai mai mai\b",
    r"\bmai la ngay cuoi minh di hoc\b",
    r"\bnghi toi cai chet.*binh yen\b",
    r"\bsap duoc gap lai.*da mat\b",
    r"\bgap lai.*ong.*mat\b",
    r"\bmoi chuyen se som ket thuc thoi\b",
    r"\bdua thua trong nha\b",
    r"\bdem nguoc toi ngay minh ra di\b",
    r"\bdem nay la dem cuoi\b",
    r"\btoi nay la dem cuoi\b",
    r"\bcuoc song vo nghia.*khong muon co gang\b",
    r"\bsong met qua.*dung lai\b",
    r"\btat ca dung lai\b",
    # Other crises: self-harm, assault, sexual coercion, threats, friend in danger
    r"\btu lam dau\b",
    r"\btu lam minh bi thuong\b",
    r"\btu lam ton thuong\b",
    r"\btu hai\b",
    r"\brach tay\b",
    r"\bcat tay\b",
    r"\bvua lam dieu dai dot\b",
    r"\bdoa tung anh\b",
    r"\bbat.*gui anh nhay cam\b",
    r"\bchup anh nhay cam\b",
    r"\bba.*say ruou.*danh\b",
    r"\bbi danh dap\b",
    r"\bchan duong danh\b",
    r"\bhen.*gap rieng.*dung noi\b",
    r"\bhen minh ra gap rieng\b",
    r"\bdung cham co the\b",
    r"\bdoa giet\b",
    r"\bban than.*muon tu tu\b",
    r"\bem minh.*nhot trong phong.*muon chet\b",
    r"\bban minh dang story tam biet\b",
    r"\bi wish i were dead\b",
    r"\bi want to disappear\b",
    r"\bkill myself\b",
    r"\bsuicid",
)

CRISIS_RESPONSE = """**Hỗ trợ ngay:** gọi **111** để được hỗ trợ bảo vệ trẻ em; gọi **115** nếu bạn đang gặp nguy hiểm hoặc cần cấp cứu. Bạn cũng có thể liên hệ **Đường dây Ngày Mai: 096 306 1414**.

**Bạn có đang định làm đau mình ngay lúc này, hoặc đã chuẩn bị cách thực hiện chưa? Bạn đang ở một mình không?**

Nếu nguy hiểm đang ở ngay trước mắt, hãy gọi 115 hoặc đến khoa cấp cứu gần nhất, và báo ngay cho một người lớn đáng tin cậy ở cạnh bạn. Bạn có thể trả lời ngắn gọn: “đang nguy hiểm” hoặc “đang an toàn”. Mình sẽ tiếp tục ở đây cùng bạn."""


def normalize_crisis_text(text: str) -> str:
    normalized = unicodedata.normalize("NFD", text.lower())
    without_marks = "".join(
        char for char in normalized if unicodedata.category(char) != "Mn"
    )
    t = without_marks.replace("đ", "d")
    slang_map = [
        (r"\bk\b", "khong"),
        (r"\bko\b", "khong"),
        (r"\bkhg\b", "khong"),
        (r"\bnx\b", "nua"),
        (r"\bmun\b", "muon"),
        (r"\bmik\b", "minh"),
        (r"\bmk\b", "minh"),
        (r"\btui\b", "toi"),
        (r"\bwa\b", "qua"),
        (r"\br\b", "roi"),
    ]
    for p, rep in slang_map:
        t = re.sub(p, rep, t)
    return t


def is_crisis_message(text: str) -> bool:
    if not text or not isinstance(text, str):
        return False
    normalized = normalize_crisis_text(text)
    for pattern in EXPLICIT_DENIAL_PATTERNS:
        normalized = re.sub(pattern, " ", normalized)
    for sp in SAFE_PATTERNS:
        if re.search(sp, normalized):
            return False
    return any(re.search(pattern, normalized) for pattern in CRISIS_PATTERNS)


def latest_user_message(messages: Iterable[Dict[str, Any]]) -> str:
    for message in reversed(list(messages)):
        if message.get("role") == "user":
            content = message.get("content", "")
            return content if isinstance(content, str) else str(content)
    return ""
