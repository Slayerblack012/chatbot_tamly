import socket
import threading
import time
import webbrowser

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
    url = f"http://127.0.0.1:{port}"
    print(f"\nĐang mở giao diện An Nhiên Tâm Lý tại: {url}\n")
    try:
        webbrowser.open(url)
    except Exception as e:
        print(f"Không thể tự động mở trình duyệt: {e}. Vui lòng mở thủ công tại: {url}")


if __name__ == "__main__":
    port = find_available_port(8000)

    print("=" * 65)
    print("   AN NHIEN TAM LY - NGUOI BAN DONG HANH CAM XUC")
    print("=" * 65)
    print(f"Đang khởi động tại http://127.0.0.1:{port} ...")

    threading.Thread(target=open_browser, args=(port,), daemon=True).start()
    uvicorn.run("server:app", host="127.0.0.1", port=port, reload=True, log_level="info", server_header=False)


