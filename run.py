"""
Khoi chay Nen tang An Nhien Tam Ly:
- Chay FastAPI Server tren cong 8000
- Tu dong mo trinh duyet web tai http://127.0.0.1:8000

Cach dung:
    python run.py
"""

import threading
import time
import webbrowser

import uvicorn


def open_browser():
    time.sleep(1.2)
    url = "http://127.0.0.1:8000"
    print(f"\nDang mo giao dien An Nhien Tam Ly tai: {url}\n")
    try:
        webbrowser.open(url)
    except Exception as e:
        print(f"Khong the tu dong mo trinh duyet: {e}. Vui long mo thu cong tai: {url}")


if __name__ == "__main__":
    print("=" * 65)
    print("   AN NHIEN TAM LY - NGUOI BAN DONG HANH CAM XUC")
    print("=" * 65)
    print("Dang khoi dong tai http://127.0.0.1:8000 ...")

    # Mo trinh duyet trong luong rieng
    threading.Thread(target=open_browser, daemon=True).start()

    # Chay Uvicorn server voi server_header=False
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=False, log_level="info", server_header=False)
