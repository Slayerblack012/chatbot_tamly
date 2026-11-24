import socket
import sys
from pathlib import Path


def add_project_venv_to_path(project_root: Path | None = None) -> None:
    root = project_root or Path(__file__).resolve().parent.parent
    virtualenv = root / ".venv"
    site_packages = [
        virtualenv / "Lib" / "site-packages",
        *virtualenv.glob("lib/python*/site-packages"),
    ]

    for path in site_packages:
        if path.is_dir():
            resolved_path = str(path.resolve())
            if resolved_path not in sys.path:
                sys.path.insert(0, resolved_path)


def is_port_available(port: int, host: str = "0.0.0.0") -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        try:
            server_socket.bind((host, port))
            return True
        except OSError:
            return False


def find_available_port(preferred: int = 8000, max_attempts: int = 20) -> int:
    for port in range(preferred, preferred + max_attempts):
        if is_port_available(port):
            return port
    return preferred
