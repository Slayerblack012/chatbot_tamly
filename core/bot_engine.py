import os
from typing import Generator, Optional, Dict, Any, List
from dotenv import load_dotenv
from google import genai
from google.genai import types

from core.prompts import BASE_COUNSELOR_PERSONA, MODE_PROMPTS, SUMMARY_PROMPT

# Tìm nạp file .env ở thư mục gốc của dự án
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
if os.path.exists(env_path):
    load_dotenv(dotenv_path=env_path)
else:
    load_dotenv()

DEFAULT_MODEL = "gemini-3.5-flash-lite"
FALLBACK_MODELS = ["gemini-3.5-flash-lite", "gemini-flash-lite-latest", "gemini-3.1-flash-lite", "gemini-3.5-flash", "gemini-3.6-flash"]


class CounselorEngine:
    """Quản lý kết nối và tạo phản hồi từ Gemini cho Trợ lý An Nhiên (Chuẩn Chat API)."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.client = None
        if self.api_key:
            self._init_client()

    def _init_client(self) -> None:
        """Khởi tạo Google GenAI Client."""
        try:
            self.client = genai.Client(api_key=self.api_key)
        except Exception as e:
            self.client = None
            raise RuntimeError(f"Không thể khởi tạo Client: {e}")

    def update_api_key(self, new_key: str) -> bool:
        """Cập nhật API Key."""
        if not new_key or not new_key.strip():
            return False
        self.api_key = new_key.strip()
        try:
            self._init_client()
            return True
        except Exception:
            return False

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
        if mood_context:
            mood_name = mood_context.get("mood_name", "Chưa xác định")
            stress_level = mood_context.get("stress_level", 5)
            note = mood_context.get("note", "")
            
            context_str = f"""
[BỐI CẢNH TÂM TRẠNG HIỆN TẠI CỦA NGƯỜI DÙNG]:
- Cảm xúc tự nhận diện: {mood_name}
- Mức độ căng thẳng / áp lực (thang điểm 1-10): {stress_level}/10
"""
            if note:
                context_str += f"- Ghi chú riêng của người dùng: '{note}'\n"
            context_str += "Hãy lưu ý trạng thái này để điều chỉnh mức độ vỗ về, hỏi han sao cho tinh tế và phù hợp nhất."
            prompt += f"\n\n{context_str}"

        return prompt

    def stream_chat(
        self,
        messages: List[Dict[str, str]],
        mode: str = "empathy",
        mood_context: Optional[Dict[str, Any]] = None,
        model_name: str = DEFAULT_MODEL,
        temperature: float = 0.8,
    ) -> Generator[str, None, None]:
        """Gửi lịch sử hội thoại và stream câu trả lời theo chuẩn Chat.send_message_stream (Không cảnh báo AFC)."""
        if not self.is_ready():
            yield "⚠️ *Chưa tìm thấy API Key trong cấu hình hệ thống.*"
            return

        if not messages:
            return

        system_instruction = self.build_system_instruction(mode, mood_context)

        # Tách tin nhắn gần nhất và lịch sử trước đó
        latest_user_message = ""
        history_contents: List[types.Content] = []

        if messages[-1]["role"] == "user":
            latest_user_message = messages[-1]["content"]
            prior_messages = messages[:-1]
        else:
            prior_messages = messages

        for msg in prior_messages:
            role = "user" if msg["role"] == "user" else "model"
            history_contents.append(
                types.Content(
                    role=role,
                    parts=[types.Part(text=msg["content"])]
                )
            )

        models_to_try = [model_name] + [m for m in FALLBACK_MODELS if m != model_name]
        last_err = None

        for target_model in models_to_try:
            try:
                # Sử dụng Chat session chính thống từ Google GenAI SDK
                chat = self.client.chats.create(
                    model=target_model,
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        temperature=temperature,
                        max_output_tokens=1500,
                    ),
                    history=history_contents if history_contents else None,
                )

                stream = chat.send_message_stream(message=latest_user_message)
                for chunk in stream:
                    if chunk.text:
                        yield chunk.text
                return
            except Exception as exc:
                last_err = exc
                continue

        # Kiểm tra xem có phải lỗi do hết Quota / Rate limit không
        err_str = str(last_err).lower() if last_err else ""
        if any(kw in err_str for kw in ["429", "resource_exhausted", "quota", "rate limit", "too many requests"]):
            yield """☕ **An Nhiên xin lỗi bạn nhé...**

Hiện tại mình đang cần vài phút tĩnh dưỡng và nạp lại năng lượng do số lượng cuộc trò chuyện trong phiên vượt quá giới hạn token của hệ thống.

🌿 Trong lúc chờ đợi, bạn hãy thử hít thở thật sâu, uống một ngụm nước ấm hoặc ghé qua tab **🧘 Thư Giãn & Tĩnh Tâm** để thả lỏng cơ thể một chút nhé.

Mình sẽ sớm hồi phục và quay lại đồng hành cùng bạn ngay sau vài phút nữa! 💛✨"""
        else:
            yield "\n\n*(An Nhiên đang gặp gián đoạn kết nối tạm thời. Bạn hãy thử gửi lại sau giây lát nhé.)*"

    def generate_session_summary(
        self, messages: List[Dict[str, str]], model_name: str = DEFAULT_MODEL
    ) -> str:
        """Tạo tóm tắt và lời nhắn nhủ chữa lành qua Chat.send_message."""
        if not self.is_ready() or len(messages) < 2:
            return "Phiên trò chuyện còn ngắn, hãy trò chuyện thêm một chút để An Nhiên có thể đúc kết cho bạn nhé!"

        conversation_text = ""
        for m in messages:
            speaker = "Người dùng" if m["role"] == "user" else "An Nhiên"
            conversation_text += f"{speaker}: {m['content']}\n"

        prompt = f"{SUMMARY_PROMPT}\n\n[NỘI DUNG CUỘC TRÒ CHUYỆN]:\n{conversation_text}"

        models_to_try = [model_name] + [m for m in FALLBACK_MODELS if m != model_name]
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
                return response.text if response.text else "Không thể tạo tóm tắt lúc này."
            except Exception:
                continue

        return "Không thể tạo tóm tắt lúc này."
