import io
import sys

from core.bot_engine import CounselorEngine
from core.prompts import get_time_greeting

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    except Exception:
        pass

WELCOME_BANNER = f"""
{'=' * 65}
   AN NHIEN TAM LY - Nguoi Ban Dong Hanh Cam Xuc
   {get_time_greeting()}

   [Goi y]: Chay 'python run.py' de mo Giao Dien Web.
   - Go 'thoat' hoac 'exit' de ket thuc.
   - Go 'mode empathy', 'mode cbt', hoac 'mode mindfulness' de doi phong cach.
{'=' * 65}
"""


def main() -> None:
    engine = CounselorEngine()
    if not engine.is_ready():
        print("\n[Loi] Chua tim thay GEMINI_API_KEY trong moi truong hoac file .env.")
        print("Huong dan: tao file .env cung thu muc voi noi dung:")
        print("GEMINI_API_KEY=your_gemini_api_key_here\n")
        return

    print(WELCOME_BANNER)
    messages = []
    current_mode = "empathy"

    while True:
        try:
            user_input = input("\nBạn: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\nAn Nhiên: Chúc bạn luôn an yên và nhẹ lòng. Hẹn gặp lại bạn nhé.")
            break

        if not user_input:
            continue

        if user_input.lower() in ("thoat", "thoát", "exit", "quit"):
            print("\nAn Nhiên: Tạm biệt bạn, chúc bạn một ngày thật nhiều bình an.")
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

