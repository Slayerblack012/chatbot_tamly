"""
Khởi chạy Nền tảng An Nhiên Edu-Psychology Platform:
- Chạy FastAPI Server trên cổng 8000
- Tự động mở trình duyệt web tại http://127.0.0.1:8000
- Không cần cài đặt Streamlit, không hỏi email, khởi động trong 1 giây!

Cách dùng:
    python run.py
"""

import sys
import os
import time
import threading
import webbrowser
import uvicorn

def open_browser():
    time.sleep(1.2)
    url = "http://127.0.0.1:8000"
    print(f"\n🕊️ Đang mở giao diện An Nhiên Edu-Psychology tại: {url}\n")
    try:
        webbrowser.open(url)
    except Exception as e:
        print(f"Không thể tự động mở trình duyệt: {e}. Bạn hãy mở link thủ công: {url}")

if __name__ == "__main__":
    print("=" * 65)
    print("   🌿 AN NHIÊN TÂM LÝ - NGƯỜI BẠN ĐỒNG HÀNH CẢM XÚC")
    print("=" * 65)
    print("Đang khởi động tại http://127.0.0.1:8000 ...")

    # Mở trình duyệt trong luồng riêng
    threading.Thread(target=open_browser, daemon=True).start()

    # Chạy Uvicorn server
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=False, log_level="info")
