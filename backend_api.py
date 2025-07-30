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
    """
    Crea una nueva reserva asignando un ID incremental.

    La reserva debe ser un diccionario con claves como nombre, origen, destino,
    fecha, mascota y asiento. No se realiza validación aquí porque se asume
    que el cliente (dashboard) ya aplicó las reglas de negocio. Si se
    necesitan validaciones server‑side, pueden añadirse aquí.
    """
    nueva_reserva["id"] = max((r["id"] for r in reservas), default=0) + 1
    reservas.append(nueva_reserva)
    with open(BASE_DIR / "json_extended.json", "w", encoding="utf-8") as f:
        json.dump(reservas, f, ensure_ascii=False, indent=2)
    return nueva_reserva


@app.put("/reservas/{reserva_id}")
def actualizar_reserva(reserva_id: int, reserva_actualizada: Dict):
    """Actualiza una reserva existente.

    Se permite actualización parcial: los campos no incluidos se mantienen.
    """
    for idx, r in enumerate(reservas):
        if r["id"] == reserva_id:
            # fusionar campos existentes con los actualizados, preservando el ID
            reservas[idx] = {**r, **reserva_actualizada, "id": reserva_id}
            with open(BASE_DIR / "json_extended.json", "w", encoding="utf-8") as f:
                json.dump(reservas, f, ensure_ascii=False, indent=2)
            return reservas[idx]
    raise HTTPException(status_code=404, detail="Reserva no encontrada")


@app.delete("/reservas/{reserva_id}")
def eliminar_reserva(reserva_id: int):
    """
    Elimina una reserva por ID.
    """
    for r in list(reservas):  # convert to list copy for safe removal
        if r["id"] == reserva_id:
            reservas.remove(r)
            with open(BASE_DIR / "json_extended.json", "w", encoding="utf-8") as f:
                json.dump(reservas, f, ensure_ascii=False, indent=2)
            return {"mensaje": "Reserva eliminada"}
    raise HTTPException(status_code=404, detail="Reserva no encontrada")
