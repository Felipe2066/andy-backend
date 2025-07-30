@app.get("/")
def root():
    return {"mensaje": "API de reservas de Andesmar: consulta /docs para más detalles"}
from fastapi import FastAPI, HTTPException
import json
from typing import List, Dict

app = FastAPI()

# Cargar reservas desde el archivo JSON
with open("json_extended.json", encoding="utf-8") as f:
    reservas: List[Dict] = json.load(f)

@app.get("/reservas")
def listar_reservas():
    """Devuelve todas las reservas"""
    return reservas

@app.get("/reservas/{reserva_id}")
def obtener_reserva(reserva_id: int):
    """Devuelve una reserva por ID"""
    for r in reservas:
        if r["id"] == reserva_id:
            return r
    raise HTTPException(status_code=404, detail="Reserva no encontrada")

@app.post("/reservas")
def crear_reserva(nueva_reserva: Dict):
    """Crea una nueva reserva"""
    nueva_reserva["id"] = max((r["id"] for r in reservas), default=0) + 1
    reservas.append(nueva_reserva)
    # Persistir en disco
    with open("json_extended.json", "w", encoding="utf-8") as f:
        json.dump(reservas, f, ensure_ascii=False, indent=2)
    return nueva_reserva
