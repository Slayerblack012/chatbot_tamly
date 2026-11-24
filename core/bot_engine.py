import logging
import os
from typing import Any, AsyncGenerator, Dict, Generator, List, Optional

from core.runtime import add_project_venv_to_path

add_project_venv_to_path()

from dotenv import load_dotenv
from google import genai
from google.genai import types

from core.prompts import BASE_COUNSELOR_PERSONA, MODE_PROMPTS, SUMMARY_PROMPT

logger = logging.getLogger("an_nhien.bot_engine")

env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
if os.path.exists(env_path):
    load_dotenv(dotenv_path=env_path)
else:
    load_dotenv()

DEFAULT_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
FALLBACK_MODELS = [
    "gemini-3.8-flash",
    "gemini-3.5-flash-lite",
    "gemini-3.6-flash",
    "gemini-3.7-flash",
]

QUOTA_FALLBACK_MESSAGE = """**An Nhiên xin lỗi bạn nhé.**

Mình đang tạm hết lượt phản hồi do giới hạn sử dụng của dịch vụ AI trong lúc này. Đây không phải lỗi ở tin nhắn của bạn; bạn có thể thử lại sau ít phút, hoặc quay lại mục Thư Giãn & Tĩnh Tâm để nghỉ ngơi trong lúc chờ nhé.

Nếu bạn cần hỗ trợ khẩn cấp, hãy liên hệ 115 hoặc dịch vụ cấp cứu phù hợp tại khu vực của bạn."""

AUTH_FAILURE_MESSAGE = "An Nhiên hiện chưa thể kết nối an toàn vì thông tin API Key cần được cập nhật. Bạn vui lòng thử lại sau ít phút nhé."
TEMPORARY_FALLBACK_MESSAGE = "Mình đang gặp một chút gián đoạn nhỏ trong lúc phản hồi. Bạn gửi lại hoặc nhấn gửi một lần nữa nhé, mình vẫn ở đây để tiếp tục cùng bạn."
PARTIAL_REPLY_FALLBACK = "Mình vừa dừng phần còn lại của câu trả lời do kết nối không ổn định. Hãy gửi lại câu hỏi này, hoặc nhấn gửi lại lần nữa để mình phản hồi hoàn chỉnh nhé."
CHAT_MAX_OUTPUT_TOKENS = 2048


def is_quota_error(error: Exception | str) -> bool:
    err_text = str(error).lower()
    return any(
        keyword in err_text
        for keyword in (
            "429",
            "resource_exhausted",
            "quota",
            "rate limit",
            "too many requests",
            "billing",
        )
    )


def is_auth_error(error: Exception | str) -> bool:
    err_text = str(error).lower()
    return any(
        keyword in err_text
        for keyword in (
            "api_key",
            "api key",
            "unauthorized",
            "permission_denied",
            "invalid_argument",
            "invalid key",
            "401",
            "403",
        )
    )


def is_model_unavailable_error(error: Exception | str) -> bool:
    err_text = str(error).lower()
    return any(
        keyword in err_text
        for keyword in (
            "model not found",
            "model_not_found",
            "not_found",
            "not found",
            "unsupported model",
            "model is not supported",
            "not supported for generatecontent",
        )
    )


def is_model_overloaded_error(error: Exception | str) -> bool:
    err_text = str(error).lower()
    return any(
        keyword in err_text
        for keyword in (
            "503",
            "unavailable",
            "high demand",
            "temporarily unavailable",
            "overloaded",
            "try again later",
        )
    )


def get_fallback_message(error: Exception | str | None) -> str:
    if is_quota_error(error or ""):
        return QUOTA_FALLBACK_MESSAGE
    if is_auth_error(error or ""):
        return AUTH_FAILURE_MESSAGE
    return TEMPORARY_FALLBACK_MESSAGE


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
            clean[-1]["content"] += f"\n\n{content}"
        else:
            clean.append({"role": role, "content": content})

    return clean


class CounselorEngine:
    """Quản lý kết nối và tạo phản hồi từ Gemini cho Trợ lý An Nhiên (Hỗ trợ Async & Sync)."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.api_keys = self._get_api_keys(api_key)
        self.client: Optional[genai.Client] = None
        self.active_model: str = DEFAULT_MODEL
        self._init_client()

    @staticmethod
    def _get_api_keys(explicit_key: Optional[str] = None) -> List[str]:
        """Nạp danh sách API key dự phòng từ cấu hình môi trường."""
        raw_keys = os.getenv("GEMINI_API_KEYS") or explicit_key or os.getenv("GEMINI_API_KEY") or ""
        separators = raw_keys.replace(",", "\n").replace(";", "\n").splitlines()
        return list(dict.fromkeys(key.strip().strip('"').strip("'") for key in separators if key.strip()))

    def _init_client(self) -> None:
        """Khởi tạo Google GenAI Client an toàn và thử lần lượt các API key."""
        if not hasattr(self, "api_keys"):
            self.api_keys = self._get_api_keys(self.api_key)

        for key in self.api_keys:
            try:
                candidate = genai.Client(api_key=key)
                self.api_key = key
                self.client = candidate
                logger.info("Khởi tạo Google GenAI Client thành công.")
                return
            except Exception:
                logger.warning("Không thể khởi tạo một API key Gemini; thử key dự phòng.")

        self.client = None

    def _try_next_api_key(self) -> bool:
        """Chuyển sang API key tiếp theo sau khi key hiện tại bị từ chối hoặc hết quota."""
        if not self.api_keys:
            return False

        try:
            current_index = self.api_keys.index(self.api_key)
        except (ValueError, AttributeError):
            current_index = -1

        next_index = current_index + 1
        if next_index >= len(self.api_keys):
            return False

        next_key = self.api_keys[next_index]
        try:
            self.client = genai.Client(api_key=next_key)
            self.api_key = next_key
            logger.warning("Đã chuyển sang API key Gemini dự phòng.")
            return True
        except Exception as exc:
            logger.warning("API key Gemini dự phòng không thể khởi tạo: %s", exc)
            return False

    def reload(self) -> bool:
        """Thử nạp lại API key từ môi trường."""
        raw_keys = os.getenv("GEMINI_API_KEYS") or os.getenv("GEMINI_API_KEY") or ""
        self.api_key = raw_keys.strip().strip('"').strip("'")
        self.api_keys = self._get_api_keys(self.api_key)
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

        mode_instruction = MODE_PROMPTS.get(mode, MODE_PROMPTS["empathy"])
        prompt += f"\n\n{mode_instruction}"

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
        temperature: float = 0.65,
    ) -> AsyncGenerator[str, None]:
        """
        Async generator streaming câu trả lời từ Gemini qua client.aio (Non-blocking Event Loop).
        """
        if not self.is_ready():
            yield "*Chưa tìm thấy API Key trong cấu hình hệ thống.*"
            return

        if not messages:
            return

        clamped_temp = max(0.0, min(2.0, float(temperature)))
        system_instruction = self.build_system_instruction(mode, mood_context)
        history_contents, latest_user_message = self._prepare_history_and_latest(messages)

        models_to_try = self._get_candidate_models(model_name)
        last_err: Optional[Exception] = None
        has_yielded: bool = False
        overload_fallbacks = 0

        for target_model in models_to_try:
            try:
                logger.debug(f"Đang thử kết nối async chat với model: {target_model}")
                chat = self.client.aio.chats.create(
                    model=target_model,
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        temperature=clamped_temp,
                        max_output_tokens=CHAT_MAX_OUTPUT_TOKENS,
                    ),
                    history=history_contents if history_contents else None,
                )

                stream = await chat.send_message_stream(message=latest_user_message)
                async for chunk in stream:
                    if chunk.text:
                        has_yielded = True
                        yield chunk.text

                self.active_model = target_model
                return
            except Exception as exc:
                last_err = exc
                if has_yielded:
                    if is_model_overloaded_error(exc):
                        logger.warning(
                            "Model %s quá tải sau khi đã gửi một phần câu trả lời: %s",
                            target_model,
                            exc,
                        )
                    else:
                        logger.error(
                            "Sự cố stream ngắt quãng giữa chừng khi đã gửi dữ liệu.",
                            exc_info=True,
                        )
                    yield PARTIAL_REPLY_FALLBACK
                    return
                logger.warning(f"Lỗi khi gọi model {target_model}: {exc}")
                if is_quota_error(exc):
                    self._try_next_api_key()
                elif is_auth_error(exc):
                    if not self._try_next_api_key():
                        break
                elif is_model_overloaded_error(exc):
                    if overload_fallbacks >= 1:
                        break
                    overload_fallbacks += 1
                elif not is_model_unavailable_error(exc):
                    break
                continue

        logger.error(f"Tất cả model Gemini đều thất bại: {last_err}")
        yield get_fallback_message(last_err)

    def stream_chat(
        self,
        messages: List[Dict[str, str]],
        mode: str = "empathy",
        mood_context: Optional[Dict[str, Any]] = None,
        model_name: Optional[str] = None,
        temperature: float = 0.65,
    ) -> Generator[str, None, None]:
        """
        Sync generator streaming câu trả lời (Dành cho CLI main.py).
        """
        if not self.is_ready():
            yield "*Chưa tìm thấy API Key trong cấu hình hệ thống.*"
            return

        if not messages:
            return

        clamped_temp = max(0.0, min(2.0, float(temperature)))
        system_instruction = self.build_system_instruction(mode, mood_context)
        history_contents, latest_user_message = self._prepare_history_and_latest(messages)

        models_to_try = self._get_candidate_models(model_name)
        last_err: Optional[Exception] = None
        has_yielded = False
        overload_fallbacks = 0

        for target_model in models_to_try:
            try:
                chat = self.client.chats.create(
                    model=target_model,
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        temperature=clamped_temp,
                        max_output_tokens=CHAT_MAX_OUTPUT_TOKENS,
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
                    if is_model_overloaded_error(exc):
                        logger.warning(
                            "Model %s quá tải sau khi đã gửi một phần câu trả lời: %s",
                            target_model,
                            exc,
                        )
                    else:
                        logger.error(
                            "Sự cố stream ngắt quãng giữa chừng khi đã gửi dữ liệu.",
                            exc_info=True,
                        )
                    yield PARTIAL_REPLY_FALLBACK
                    return
                logger.warning(f"Lỗi khi gọi model {target_model}: {exc}")
                if is_quota_error(exc):
                    self._try_next_api_key()
                elif is_auth_error(exc):
                    if not self._try_next_api_key():
                        break
                elif is_model_overloaded_error(exc):
                    if overload_fallbacks >= 1:
                        break
                    overload_fallbacks += 1
                elif not is_model_unavailable_error(exc):
                    break
                continue

        yield get_fallback_message(last_err)

    @staticmethod
    def _build_summary_prompt(messages: List[Dict[str, str]]) -> str:
        clean = sanitize_messages_for_gemini(messages)
        conversation = "\n".join(
            f"{'Người dùng' if message['role'] == 'user' else 'An Nhiên'}: {message['content']}"
            for message in clean
        )
        return f"{SUMMARY_PROMPT}\n\n[NỘI DUNG CUỘC TRÒ CHUYỆN]:\n{conversation}"

    async def async_generate_session_summary(
        self, messages: List[Dict[str, str]], model_name: Optional[str] = None
    ) -> str:
        """Tạo tóm tắt và lời nhắn nhủ chữa lành (Bản Async)."""
        if not self.is_ready() or len(messages) < 2:
            return "Phiên trò chuyện còn ngắn, hãy trò chuyện thêm một chút để An Nhiên có thể đúc kết cho bạn nhé!"

        prompt = self._build_summary_prompt(messages)
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

        prompt = self._build_summary_prompt(messages)
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
            except Exception as exc:
                logger.warning("Lỗi khi tạo summary với model %s: %s", target_model, exc)
                continue

        return "Không thể tạo tóm tắt lúc này."

