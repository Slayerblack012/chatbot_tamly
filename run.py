import threading
import time
import webbrowser

import uvicorn


def open_browser() -> None:
    time.sleep(1.2)
    url = "http://127.0.0.1:8000"
    print(f"\nĐang mở giao diện An Nhiên Tâm Lý tại: {url}\n")
    try:
        webbrowser.open(url)
    except Exception as e:
        print(f"Không thể tự động mở trình duyệt: {e}. Vui lòng mở thủ công tại: {url}")


if __name__ == "__main__":
    print("=" * 65)
    print("   AN NHIEN TAM LY - NGUOI BAN DONG HANH CAM XUC")
    print("=" * 65)
    print("Đang khởi động tại http://127.0.0.1:8000 ...")

    threading.Thread(target=open_browser, daemon=True).start()
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True, log_level="info", server_header=False)

