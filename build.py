"""Genera el ejecutable autónomo con PyInstaller: python build.py"""
import os
import sys

import PyInstaller.__main__

ROOT = os.path.dirname(os.path.abspath(__file__))
name = sys.argv[1] if len(sys.argv) > 1 else "QuantumFlightDispatcher"

PyInstaller.__main__.run([
    os.path.join(ROOT, "launcher.py"), "--onefile", "--noconfirm", "--name", name,
    "--add-data", f"{os.path.join(ROOT, 'static')}{os.pathsep}static",
    "--collect-all", "qiskit", "--collect-submodules", "uvicorn",
])
