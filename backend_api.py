from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
from typing import List, Dict
from pathlib import Path

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent
with open(BASE_DIR / "json_extended.json", encoding="utf-8") as f:
    reservas: List[Dict] = json.load(f)

@app.get("/")
def root():
    return {"mensaje": "API de reservas de Andesmar: consulta /docs para más detalles"}

@app.get("/reservas")
def listar_reservas():
    return reservas

@app.get("/reservas/{reserva_id}")
def obtener_reserva(reserva_id: int):
    for r in reservas:
        if r["id"] == reserva_id:
            return r
    raise HTTPException(status_code=404, detail="Reserva no encontrada")

@app.post("/reservas")
def crear_reserva(nueva_reserva: Dict):
    nueva_reserva["id"] = max((r["id"] for r in reservas), default=0) + 1
    reservas.append(nueva_reserva)
    with open(BASE_DIR / "json_extended.json", "w", encoding="utf-8") as f:
        json.dump(reservas, f, ensure_ascii=False, indent=2)
    return nueva_reserva
