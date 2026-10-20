"""Quantum Flight Dispatcher: API de comparación clásica y Grover."""

import sys
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from optimizer import compare_searches

ROOT = Path(getattr(sys, "_MEIPASS", Path(__file__).parent))
app = FastAPI(title="Quantum Flight Dispatcher")
app.mount("/static", StaticFiles(directory=ROOT / "static"), name="static")

class Flight(BaseModel):
    code: str
    start: int = Field(ge=0, le=23)
    end: int = Field(ge=1, le=24)
    aircraft: str
    allowed_gates: list[int]

class SearchRequest(BaseModel):
    flights: list[Flight] = Field(min_length=2, max_length=10)
    shots: int = Field(default=1024, ge=128, le=8192)

@app.get("/", include_in_schema=False)
def index(): return FileResponse(ROOT / "static" / "index.html")

@app.get("/health")
def health():
    import qiskit
    return {"status": "ok", "qiskit": qiskit.__version__}

@app.post("/api/compare")
def compare(request: SearchRequest):
    flights = [f.model_dump() for f in request.flights]
    if any(f["end"] <= f["start"] for f in flights):
        raise HTTPException(400, "La hora final debe ser posterior a la inicial.")
    if any(any(g not in (0, 1) for g in f["allowed_gates"]) for f in flights):
        raise HTTPException(400, "La demostración utiliza las puertas A y B.")
    try: return compare_searches(flights, request.shots)
    except ValueError as exc: raise HTTPException(400, str(exc)) from exc

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


