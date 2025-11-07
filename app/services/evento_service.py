from app.config.database_config import eventos_collection, db
from bson import ObjectId
from fastapi import HTTPException
from app.models.evento_model import EventoModel
from datetime import datetime
import re
from typing import List, Optional

def _serialize_many(cursor) -> List[dict]:
    items = list(cursor)
    for e in items:
        e["_id"] = str(e["_id"])
    return items

def criar_evento(evento: EventoModel):
    if not ObjectId.is_valid(evento.parque_id):
        raise HTTPException(status_code=400, detail="ID inválido")
    if not db.parques.find_one({"_id": ObjectId(evento.parque_id)}):
        raise HTTPException(status_code=404, detail="❌ Parque não encontrado, impossível cadastrar evento.")
    evento_dict = evento.dict()
    inserted = eventos_collection.insert_one(evento_dict).inserted_id
    evento_dict["_id"] = str(inserted)
    return {"message": "✅ Evento cadastrado com sucesso!", "evento": evento_dict}

def buscar_evento(evento_id: str):
    if not ObjectId.is_valid(evento_id):
        raise HTTPException(status_code=400, detail="ID inválido")
    evento = eventos_collection.find_one({"_id": ObjectId(evento_id)})
    if not evento:
        raise HTTPException(status_code=404, detail="❌ Evento não encontrado")
    evento["_id"] = str(evento["_id"])
    return evento

def listar_eventos_por_parque(parque_id: str, limit: int = 0):
    cur = eventos_collection.find({"parque_id": parque_id}).sort("data", 1)
    if limit > 0:
        cur = cur.limit(limit)
    return {"eventos": _serialize_many(cur)}

def listar_eventos(
    parque_id: Optional[str] = None,
    start: Optional[datetime] = None,
    end: Optional[datetime] = None,
    skip: int = 0,
    limit: int = 0,
    sort: str = "asc",
):
    query = {}
    if parque_id:
        query["parque_id"] = parque_id
    if start or end:
        query["data"] = {}
        if start: query["data"]["$gte"] = start
        if end:   query["data"]["$lte"] = end

    order = 1 if sort.lower() == "asc" else -1
    cur = eventos_collection.find(query).sort("data", order)
    if skip > 0: cur = cur.skip(skip)
    if limit > 0: cur = cur.limit(limit)

    return {"eventos": _serialize_many(cur)}

def listar_eventos_recentes(limit: int = 5, parque_id: str | None = None, parque_nome: str | None = None):
    from datetime import datetime
    import re
    query_base = {}
    if parque_nome and not parque_id:
        regex = re.compile(f"^{re.escape(parque_nome)}$", re.IGNORECASE)
        parque = db.parques.find_one({"nome": regex})
        if parque:
            parque_id = str(parque["_id"])
    if parque_id:
        query_base["parque_id"] = parque_id

    # tenta próximos
    q_upcoming = {**query_base, "data": {"$gte": datetime.utcnow()}}
    cur = eventos_collection.find(q_upcoming).sort("data", 1).limit(limit)
    itens = list(cur)
    if not itens:
        # fallback: últimos 5 (passados inclusive)
        cur = eventos_collection.find(query_base).sort("data", -1).limit(limit)
        itens = list(cur)

    for e in itens:
        e["_id"] = str(e["_id"])
    return {"eventos": itens}

def atualizar_evento(evento_id: str, evento: EventoModel):
    if not ObjectId.is_valid(evento_id):
        raise HTTPException(status_code=400, detail="ID inválido")
    if not eventos_collection.find_one({"_id": ObjectId(evento_id)}):
        raise HTTPException(status_code=404, detail="❌ Evento não encontrado")
    eventos_collection.update_one({"_id": ObjectId(evento_id)}, {"$set": evento.dict()})
    return {"message": f"✅ Evento '{evento_id}' atualizado com sucesso!"}

def excluir_evento(evento_id: str):
    if not ObjectId.is_valid(evento_id):
        raise HTTPException(status_code=400, detail="ID inválido")
    if not eventos_collection.find_one({"_id": ObjectId(evento_id)}):
        raise HTTPException(status_code=404, detail="❌ Evento não encontrado")
    eventos_collection.delete_one({"_id": ObjectId(evento_id)})
    return {"message": f"✅ Evento '{evento_id}' deletado com sucesso!"}
