import glob
import os
import socket
import sys
import threading
import time
import webbrowser

# Tự động nạp gói thư viện từ .venv nếu người dùng chạy bằng python hệ thống
_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
_VENV_DIR = os.path.join(_BASE_DIR, ".venv")
if os.path.isdir(_VENV_DIR):
    for _sp in glob.glob(os.path.join(_VENV_DIR, "lib", "python*", "site-packages")):
        if _sp not in sys.path:
            sys.path.insert(0, _sp)

import uvicorn


def is_port_available(port: int, host: str = "127.0.0.1") -> bool:
    """Kiểm tra xem cổng mạng (port) có đang sẵn sàng sử dụng hay không."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind((host, port))
            return True
        except OSError:
            return False


def find_available_port(preferred: int = 8000, max_attempts: int = 20) -> int:
    """Tự động tìm cổng còn trống nếu cổng 8000 đang bị tiến trình khác chiếm dụng."""
    for port in range(preferred, preferred + max_attempts):
        if is_port_available(port):
            return port
    return preferred


def open_browser(port: int) -> None:
    time.sleep(1.2)
    url = f"http://localhost:{port}"
    print(f"\n[Trình duyệt] Đang mở giao diện An Nhiên Tâm Lý tại: {url}\n")
    try:
        webbrowser.open(url)
    except Exception as e:
        print(f"[Lưu ý] Không thể tự động mở trình duyệt: {e}. Vui lòng click vào link: {url}")


if __name__ == "__main__":
    port = find_available_port(8000)

    print("=" * 65)
    print("   AN NHIÊN TÂM LÝ — HỆ THỐNG TRỢ LÝ THAM VẤN CẢM XÚC")
    print("=" * 65)
    print(f"👉 GIAO DIỆN WEB UI:    http://localhost:{port}")
    print(f"👉 XEM TÀI LIỆU API:    http://localhost:{port}/docs")
    print("=" * 65)
    print(f"🌿 Nhấn giữ Ctrl + Click vào link trên hoặc mở trình duyệt web!")
    print("=" * 65 + "\n")

    threading.Thread(target=open_browser, args=(port,), daemon=True).start()
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=True, log_level="info", server_header=False)


