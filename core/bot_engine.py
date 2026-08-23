import logging
import os
from typing import Any, AsyncGenerator, Dict, Generator, List, Optional

from dotenv import load_dotenv
from google import genai
from google.genai import types

from core.prompts import BASE_COUNSELOR_PERSONA, MODE_PROMPTS, SUMMARY_PROMPT

# Cấu hình logging
logger = logging.getLogger("an_nhien.bot_engine")

# Tìm nạp file .env ở thư mục gốc của dự án
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
if os.path.exists(env_path):
    load_dotenv(dotenv_path=env_path)
else:
    load_dotenv()

DEFAULT_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")
FALLBACK_MODELS = [
    "gemini-3.5-flash-lite",
    "gemini-flash-lite-latest",
    "gemini-3.1-flash-lite",
    "gemini-3.5-flash",
    "gemini-3.6-flash",
]


def sanitize_messages_for_gemini(raw_messages: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """
    Chuẩn hóa và gộp các tin nhắn liên tiếp cùng vai trò (role alternation).
    Ngăn chặn lỗi Gemini 400 "Please ensure that multiturn requests alternate between user and model".
    """
    if not raw_messages:
        return []

    clean: List[Dict[str, str]] = []
    for m in raw_messages:
        role = "user" if m.get("role") == "user" else "model"
        content = str(m.get("content", "")).strip()
        if not content:
            continue

        if clean and clean[-1]["role"] == role:
            # Gộp hai tin cùng role lại với nhau
            clean[-1]["content"] += f"\n\n{content}"
        else:
            clean.append({"role": role, "content": content})

    return clean


class CounselorEngine:
    """Quản lý kết nối và tạo phản hồi từ Gemini cho Trợ lý An Nhiên (Hỗ trợ Async & Sync)."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.client: Optional[genai.Client] = None
        self.active_model: str = DEFAULT_MODEL
        if self.api_key:
            self._init_client()

    def _init_client(self) -> None:
        """Khởi tạo Google GenAI Client (an toàn, không crash server nếu lỗi key ban đầu)."""
        try:
            if self.api_key and self.api_key.strip():
                self.client = genai.Client(api_key=self.api_key.strip())
                logger.info("Khởi tạo Google GenAI Client thành công.")
            else:
                self.client = None
        except Exception as e:
            self.client = None
            logger.error(f"Lỗi khởi tạo Google GenAI Client: {e}")

    def reload(self) -> bool:
        """Thử nạp lại API key từ môi trường."""
        self.api_key = os.getenv("GEMINI_API_KEY")
        self._init_client()
        return self.is_ready()

    def is_ready(self) -> bool:
        """Kiểm tra xem Client đã sẵn sàng hoạt động hay chưa."""
        return self.client is not None

    def build_system_instruction(
        self, mode: str = "empathy", mood_context: Optional[Dict[str, Any]] = None
    ) -> str:
        """Tạo prompt hệ thống kết hợp chế độ trò chuyện và bối cảnh tâm trạng người dùng."""
        prompt = BASE_COUNSELOR_PERSONA

        # Thêm chỉ dẫn theo chế độ
        mode_instruction = MODE_PROMPTS.get(mode, MODE_PROMPTS["empathy"])
        prompt += f"\n\n{mode_instruction}"

        # Thêm bối cảnh cảm xúc nếu có
        if mood_context and isinstance(mood_context, dict):
            mood_name = str(mood_context.get("mood_name", "Chưa xác định"))[:50]
            try:
                stress_level = max(1, min(10, int(mood_context.get("stress_level", 5))))
            except (ValueError, TypeError):
                stress_level = 5
            raw_note = str(mood_context.get("note", "")).strip()[:500]

            context_str = f"""
[BỐI CẢNH TÂM TRẠNG HIỆN TẠI CỦA NGƯỜI DÙNG]:
- Cảm xúc tự nhận diện: {mood_name}
- Mức độ căng thẳng / áp lực (thang điểm 1-10): {stress_level}/10
"""
            if raw_note:
                context_str += f"- Ghi chú riêng của người dùng: '{raw_note}'\n"
            context_str += "Hãy lưu ý trạng thái này để điều chỉnh mức độ vỗ về, hỏi han sao cho tinh tế và phù hợp nhất."
            prompt += f"\n\n{context_str}"

        return prompt

    def _prepare_history_and_latest(
        self, messages: List[Dict[str, str]]
    ) -> tuple[List[types.Content], str]:
        """Tách lịch sử hội thoại thành danh sách types.Content và tin nhắn user mới nhất."""
        clean = sanitize_messages_for_gemini(messages)
        if not clean:
            return [], ""

        if clean[-1]["role"] == "user":
            latest_user_message = clean[-1]["content"]
            prior_messages = clean[:-1]
        else:
            latest_user_message = "Xin chào An Nhiên"
            prior_messages = clean

        history_contents: List[types.Content] = []
        for msg in prior_messages:
            history_contents.append(
                types.Content(
                    role=msg["role"],
                    parts=[types.Part(text=msg["content"])]
                )
            )

        return history_contents, latest_user_message

    def _get_candidate_models(self, preferred_model: Optional[str] = None) -> List[str]:
        """Tạo danh sách các model để thử nghiệm theo thứ tự ưu tiên."""
        primary = preferred_model or self.active_model or DEFAULT_MODEL
        candidates = [primary]
        for m in FALLBACK_MODELS:
            if m not in candidates:
                candidates.append(m)
        return candidates

    async def async_stream_chat(
        self,
        messages: List[Dict[str, str]],
        mode: str = "empathy",
        mood_context: Optional[Dict[str, Any]] = None,
        model_name: Optional[str] = None,
        temperature: float = 0.8,
    ) -> AsyncGenerator[str, None]:
        """
        Async generator streaming câu trả lời từ Gemini qua client.aio (Non-blocking Event Loop).
        """
        if not self.is_ready():
            yield "⚠️ *Chưa tìm thấy API Key trong cấu hình hệ thống.*"
            return

        if not messages:
            return

        clamped_temp = max(0.0, min(2.0, float(temperature)))
        system_instruction = self.build_system_instruction(mode, mood_context)
        history_contents, latest_user_message = self._prepare_history_and_latest(messages)

        models_to_try = self._get_candidate_models(model_name)
        last_err: Optional[Exception] = None
        has_yielded: bool = False

        for target_model in models_to_try:
            try:
                logger.debug(f"Đang thử kết nối async chat với model: {target_model}")
                chat = self.client.aio.chats.create(
                    model=target_model,
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        temperature=clamped_temp,
                        max_output_tokens=1500,
                    ),
                    history=history_contents if history_contents else None,
                )

                stream = await chat.send_message_stream(message=latest_user_message)
                async for chunk in stream:
                    if chunk.text:
                        has_yielded = True
                        yield chunk.text

                # Thành công: Cập nhật active_model đệm
                self.active_model = target_model
                return
            except Exception as exc:
                last_err = exc
                logger.warning(f"Lỗi khi gọi model {target_model}: {exc}")
                # Nếu đã xuất token ra client rồi thì KHÔNG fallback sang model khác để tránh lặp text
                if has_yielded:
                    logger.error("Sự cố stream ngắt quãng giữa chừng khi đã gửi dữ liệu.")
                    yield "\n\n*(Kết nối gặp gián đoạn tạm thời.)*"
                    return
                continue

        # Nếu toàn bộ các model fallback đều thất bại trước khi gửi bất kỳ chunk nào
        err_str = str(last_err).lower() if last_err else ""
        if any(kw in err_str for kw in ["429", "resource_exhausted", "quota", "rate limit", "too many requests"]):
            yield """**An Nhiên xin lỗi bạn nhé.**

Hiện tại mình đang cần vài phút tĩnh dưỡng và nạp lại năng lượng do số lượng cuộc trò chuyện trong phiên vượt quá giới hạn của hệ thống.

Trong lúc chờ đợi, bạn hãy thử hít thở thật sâu, uống một ngụm nước ấm hoặc ghé qua mục Thư Giãn & Tĩnh Tâm để thả lỏng một chút nhé. Mình sẽ sớm quay lại cùng bạn."""
        else:
            yield "\n\n*(An Nhiên đang gặp gián đoạn kết nối tạm thời. Bạn hãy thử gửi lại sau giây lát nhé.)*"

    def stream_chat(
        self,
        messages: List[Dict[str, str]],
        mode: str = "empathy",
        mood_context: Optional[Dict[str, Any]] = None,
        model_name: Optional[str] = None,
        temperature: float = 0.8,
    ) -> Generator[str, None, None]:
        """
        Sync generator streaming câu trả lời (Dành cho CLI main.py).
        """
        if not self.is_ready():
            yield "⚠️ *Chưa tìm thấy API Key trong cấu hình hệ thống.*"
            return

        if not messages:
            return

        clamped_temp = max(0.0, min(2.0, float(temperature)))
        system_instruction = self.build_system_instruction(mode, mood_context)
        history_contents, latest_user_message = self._prepare_history_and_latest(messages)

        models_to_try = self._get_candidate_models(model_name)
        last_err: Optional[Exception] = None
        has_yielded = False

        for target_model in models_to_try:
            try:
                chat = self.client.chats.create(
                    model=target_model,
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        temperature=clamped_temp,
                        max_output_tokens=1500,
                    ),
                    history=history_contents if history_contents else None,
                )

                stream = chat.send_message_stream(message=latest_user_message)
                for chunk in stream:
                    if chunk.text:
                        has_yielded = True
                        yield chunk.text

                self.active_model = target_model
                return
            except Exception as exc:
                last_err = exc
                if has_yielded:
                    yield "\n\n*(Kết nối gặp gián đoạn tạm thời.)*"
                    return
                continue

        err_str = str(last_err).lower() if last_err else ""
        if any(kw in err_str for kw in ["429", "resource_exhausted", "quota", "rate limit", "too many requests"]):
            yield "**An Nhiên xin lỗi bạn nhé.**\n\nHiện tại hệ thống đang vượt quá giới hạn tải tạm thời. Bạn hãy thử lại sau giây lát nhé."
        else:
            yield "\n\n*(An Nhiên đang gặp gián đoạn kết nối tạm thời. Bạn hãy thử gửi lại sau giây lát nhé.)*"

    async def async_generate_session_summary(
        self, messages: List[Dict[str, str]], model_name: Optional[str] = None
    ) -> str:
        """Tạo tóm tắt và lời nhắn nhủ chữa lành (Bản Async)."""
        if not self.is_ready() or len(messages) < 2:
            return "Phiên trò chuyện còn ngắn, hãy trò chuyện thêm một chút để An Nhiên có thể đúc kết cho bạn nhé!"

        clean = sanitize_messages_for_gemini(messages)
        conversation_text = ""
        for m in clean:
            speaker = "Người dùng" if m["role"] == "user" else "An Nhiên"
            conversation_text += f"{speaker}: {m['content']}\n"

        prompt = f"{SUMMARY_PROMPT}\n\n[NỘI DUNG CUỘC TRÒ CHUYỆN]:\n{conversation_text}"
        models_to_try = self._get_candidate_models(model_name)

        for target_model in models_to_try:
            try:
                chat = self.client.aio.chats.create(
                    model=target_model,
                    config=types.GenerateContentConfig(
                        temperature=0.5,
                        max_output_tokens=800,
                    ),
                )
                response = await chat.send_message(message=prompt)
                if response.text:
                    self.active_model = target_model
                    return response.text
            except Exception as e:
                logger.warning(f"Lỗi khi tạo summary với model {target_model}: {e}")
                continue

        return "Không thể tạo tóm tắt lúc này."

    def generate_session_summary(
        self, messages: List[Dict[str, str]], model_name: Optional[str] = None
    ) -> str:
        """Tạo tóm tắt và lời nhắn nhủ chữa lành (Bản Sync)."""
        if not self.is_ready() or len(messages) < 2:
            return "Phiên trò chuyện còn ngắn, hãy trò chuyện thêm một chút để An Nhiên có thể đúc kết cho bạn nhé!"

        clean = sanitize_messages_for_gemini(messages)
        conversation_text = ""
        for m in clean:
            speaker = "Người dùng" if m["role"] == "user" else "An Nhiên"
            conversation_text += f"{speaker}: {m['content']}\n"

        prompt = f"{SUMMARY_PROMPT}\n\n[NỘI DUNG CUỘC TRÒ CHUYỆN]:\n{conversation_text}"
        models_to_try = self._get_candidate_models(model_name)

        for target_model in models_to_try:
            try:
                chat = self.client.chats.create(
                    model=target_model,
                    config=types.GenerateContentConfig(
                        temperature=0.5,
                        max_output_tokens=800,
                    ),
                )
                response = chat.send_message(message=prompt)
                if response.text:
                    self.active_model = target_model
                    return response.text
            except Exception:
                continue

        return "Không thể tạo tóm tắt lúc này."
