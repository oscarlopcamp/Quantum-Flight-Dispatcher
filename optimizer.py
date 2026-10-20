"""Oráculo de puertas y ejecución de Grover con Qiskit."""
from math import floor, pi, sqrt
from time import perf_counter

def overlaps(a, b): return a["start"] < b["end"] and b["start"] < a["end"]
def decode(state, count): return [(state >> i) & 1 for i in range(count)]

def is_valid(assignment, flights):
    if any(assignment[i] not in f["allowed_gates"] for i, f in enumerate(flights)): return False
    return all(assignment[i] != assignment[j] or not overlaps(flights[i], flights[j])
               for i in range(len(flights)) for j in range(i + 1, len(flights)))

def valid_states(flights):
    return [s for s in range(1 << len(flights)) if is_valid(decode(s, len(flights)), flights)]

def classical_search(flights):
    started = perf_counter()
    for state in range(1 << len(flights)):
        if is_valid(decode(state, len(flights)), flights):
            return {"state": state, "evaluations": state + 1,
                    "time_ms": round((perf_counter() - started) * 1000, 4)}

def grover_search(flights, marked, shots):
    import numpy as np
    from qiskit import QuantumCircuit
    from qiskit.circuit.library import DiagonalGate
    from qiskit.quantum_info import Statevector
    started = perf_counter(); qubits = len(flights); space = 1 << qubits
    iterations = max(1, floor(pi / 4 * sqrt(space / len(marked))))
    phases = np.ones(space, dtype=complex); phases[marked] = -1
    qc = QuantumCircuit(qubits); qc.h(range(qubits))
    for _ in range(iterations):
        qc.append(DiagonalGate(phases), range(qubits)); qc.h(range(qubits)); qc.x(range(qubits))
        qc.h(qubits - 1); qc.mcx(list(range(qubits - 1)), qubits - 1); qc.h(qubits - 1)
        qc.x(range(qubits)); qc.h(range(qubits))
    probs = Statevector.from_instruction(qc).probabilities()
    counts = np.bincount(np.random.default_rng(7).choice(space, shots, p=probs), minlength=space)
    selected = int(np.argmax(counts)); ranking = np.argsort(probs)[::-1][:8]
    return {"state": selected, "oracle_queries": iterations, "qubits": qubits,
            "time_ms": round((perf_counter() - started) * 1000, 4),
            "success_probability": round(float(probs[marked].sum()) * 100, 2),
            "valid_result": selected in marked,
            "top_states": [{"bits": format(int(s), f"0{qubits}b")[::-1],
                            "probability": round(float(probs[s]) * 100, 3), "valid": int(s) in marked}
                           for s in ranking]}

def compare_searches(flights, shots=1024):
    marked = valid_states(flights)
    if not marked: raise ValueError("No existe una asignación válida con estas restricciones.")
    classical = classical_search(flights); quantum = grover_search(flights, marked, shots)
    chosen = quantum["state"] if quantum["valid_result"] else marked[0]
    iterations = quantum["oracle_queries"]; space = 1 << len(flights)
    return {"search_space": space, "valid_solutions": len(marked), "classical": classical,
            "quantum": quantum, "theoretical_classical_worst": space,
            "theoretical_grover": iterations,
            "theoretical_reduction_percent": round((1 - iterations / space) * 100, 2),
            "assignment": [{**f, "gate": "B" if decode(chosen, len(flights))[i] else "A"}
                           for i, f in enumerate(flights)]}
