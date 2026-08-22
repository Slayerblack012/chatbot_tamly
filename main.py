"""
Giao diện dòng lệnh (CLI) cho An Nhiên Edu-Psychology Platform.
Để chạy giao diện Web chuyên nghiệp, vui lòng chạy lệnh:
    python run.py
"""

import sys
import os
from core.bot_engine import CounselorEngine, DEFAULT_MODEL
from core.prompts import get_time_greeting

import io

# Cấu hình UTF-8 cho Windows Terminal
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    except Exception:
        pass

WELCOME_BANNER = f"""
{'=' * 65}
   🌿 AN NHIÊN TÂM LÝ - Người Bạn Đồng Hành Cảm Xúc
   {get_time_greeting()}
   
   💡 Mẹo: Chạy 'python run.py' để mở Giao Diện Web 'An Nhiên Tâm Lý' cực đẹp!
   - Gõ 'thoat' hoặc 'exit' để kết thúc.
   - Gõ 'mode empathy', 'mode cbt', hoặc 'mode mindfulness' để đổi phong cách.
{'=' * 65}
"""


def main() -> None:
    engine = CounselorEngine()
    if not engine.is_ready():
        print("\n[Lỗi] Chưa tìm thấy GEMINI_API_KEY trong môi trường hoặc file .env.")
        print("Hướng dẫn: tạo file .env cùng thư mục với nội dung:")
        print("GEMINI_API_KEY=your_gemini_api_key_here\n")
        return

    print(WELCOME_BANNER)
    messages = []
    current_mode = "empathy"

    while True:
        try:
            user_input = input("\nBạn: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\nAn Nhiên: Chúc bạn luôn an yên và nhẹ lòng. Hẹn gặp lại bạn nhé! 🕊️")
            break

        if not user_input:
            continue

        if user_input.lower() in ("thoat", "thoát", "exit", "quit"):
            print("\nAn Nhiên: Tạm biệt bạn, chúc bạn một ngày thật nhiều bình an và yêu thương! 🕊️")
            break

        if user_input.lower().startswith("mode"):
            parts = user_input.split()
            if len(parts) > 1 and parts[1] in ("empathy", "cbt", "mindfulness"):
                current_mode = parts[1]
                print(f"[Hệ thống] Đã chuyển sang chế độ: {current_mode}")
            else:
                print("[Hệ thống] Các chế độ hợp lệ: 'mode empathy', 'mode cbt', 'mode mindfulness'")
            continue

        messages.append({"role": "user", "content": user_input})

        print("\nAn Nhiên: ", end="", flush=True)
        full_reply = ""
        try:
            for chunk in engine.stream_chat(messages=messages, mode=current_mode):
                print(chunk, end="", flush=True)
                full_reply += chunk
            print()
        except Exception as exc:
            print(f"\n[Lỗi] Không thể kết nối: {exc}")
            messages.pop()
            continue

        if full_reply:
            messages.append({"role": "model", "content": full_reply})


if __name__ == "__main__":
    main()
