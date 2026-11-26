import os
import threading
import time
import webbrowser

from core.runtime import add_project_venv_to_path, find_available_port

add_project_venv_to_path()
import uvicorn
from dotenv import load_dotenv

load_dotenv()


def open_browser(port: int) -> None:
    time.sleep(1.2)
    url = f"http://localhost:{port}"
    print(f"\n[Trình duyệt] Đang mở giao diện An Nhiên Tâm Lý tại: {url}\n")
    try:
        webbrowser.open(url)
    except Exception as e:
        print(f"[Lưu ý] Không thể tự động mở trình duyệt: {e}. Vui lòng click vào link: {url}")


if __name__ == "__main__":
    preferred_port = int(os.getenv("PORT", "8000"))
    port = find_available_port(preferred_port)

    print("=" * 65)
    print("   AN NHIÊN TÂM LÝ — HỆ THỐNG TRỢ LÝ THAM VẤN CẢM XÚC")
    print("=" * 65)
    print(f"👉 GIAO DIỆN WEB UI:    http://localhost:{port}")
    print(f"👉 XEM TÀI LIỆU API:    http://localhost:{port}/docs")
    print("=" * 65)
    print("🌿 Nhấn giữ Ctrl + Click vào link trên hoặc mở trình duyệt web!")
    print("=" * 65 + "\n")

    threading.Thread(target=open_browser, args=(port,), daemon=True).start()
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=True, log_level="info", server_header=False)

