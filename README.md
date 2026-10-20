# Quantum Flight Dispatcher

Demostración visual de asignación de puertas mediante búsqueda clásica y Grover en Qiskit.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Abre <http://localhost:8000>. Cada qubit representa la puerta A o B de un vuelo. El oráculo marca asignaciones compatibles y Grover amplifica su probabilidad. La reducción presentada es teórica: `O(N)` contra `O(sqrt(N/M))`; el tiempo de Qiskit es una simulación clásica.

Pruebas: `python -m unittest discover -s tests -v`.
