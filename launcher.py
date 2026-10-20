"""Punto de entrada del ejecutable: arranca el servidor y abre el navegador."""
import socket
import threading
import webbrowser

import uvicorn

from main import app

def free_port(preferred=8000):
    for port in (preferred, 0):
        with socket.socket() as s:
            try: s.bind(("127.0.0.1", port)); return s.getsockname()[1]
            except OSError: continue

if __name__ == "__main__":
    port = free_port()
    url = f"http://127.0.0.1:{port}"
    print(f"Quantum Flight Dispatcher en {url} (cierra esta ventana para salir)")
    threading.Timer(1.5, webbrowser.open, [url]).start()
    uvicorn.run(app, host="127.0.0.1", port=port, log_level="warning")
