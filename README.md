# Quantum Flight Dispatcher

Demostración visual de asignación de puertas mediante búsqueda clásica y Grover en Qiskit.

## Descargar y ejecutar (sin instalar Python)

1. Ve a [Releases](https://github.com/oscarlopcamp/Quantum-Flight-Dispatcher/releases/latest) y descarga el archivo de tu sistema:
   - Windows: `QuantumFlightDispatcher-windows.exe`
   - macOS (Apple Silicon): `QuantumFlightDispatcher-macos-arm64`
   - Linux: `QuantumFlightDispatcher-linux`
2. Ejecútalo. Se abrirá el navegador en la aplicación; cierra la ventana de la terminal para salir.

Notas:
- **macOS**: el binario no está firmado. La primera vez haz clic derecho → *Abrir*, o ejecuta `xattr -d com.apple.quarantine QuantumFlightDispatcher-macos-arm64 && chmod +x QuantumFlightDispatcher-macos-arm64`.
- **Linux**: `chmod +x QuantumFlightDispatcher-linux && ./QuantumFlightDispatcher-linux`.
- **Windows**: SmartScreen puede avisar; pulsa *Más información* → *Ejecutar de todas formas*.
- El primer arranque tarda unos segundos mientras se descomprime.

## Desarrollo

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Abre <http://localhost:8000>. Cada qubit representa la puerta A o B de un vuelo. El oráculo marca asignaciones compatibles y Grover amplifica su probabilidad. La reducción presentada es teórica: `O(N)` contra `O(sqrt(N/M))`; el tiempo de Qiskit es una simulación clásica.

Pruebas: `python -m unittest discover -s tests -v`.

## Publicar una release

Crea y sube un tag; GitHub Actions compila los ejecutables de Windows, macOS y Linux y los adjunta a la release:

```bash
git tag v1.0.0
git push origin v1.0.0
```

Para compilar en local: `pip install pyinstaller && python build.py` (el ejecutable queda en `dist/`).
