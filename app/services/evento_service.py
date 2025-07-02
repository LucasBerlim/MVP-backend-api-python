from app.config.database_config import eventos_collection, db
from bson import ObjectId
from fastapi import HTTPException
from app.models.evento_model import EventoModel


def criar_evento(evento: EventoModel):
    if not ObjectId.is_valid(evento.parque_id):
        raise HTTPException(status_code=400, detail="ID inválido")
    parque = db.parques.find_one({"_id": ObjectId(evento.parque_id)})

    if not parque:
        raise HTTPException(status_code=404, detail="❌ Parque não encontrado, impossível cadastrar evento.")

    evento_dict = evento.dict()
    evento_dict["_id"] = str(eventos_collection.insert_one(evento_dict).inserted_id)
    return {"message": "✅ Evento cadastrado com sucesso!", "evento": evento_dict}


def buscar_evento(evento_id: str):
    if not ObjectId.is_valid(evento_id):
        raise HTTPException(status_code=400, detail="ID inválido")
    evento = eventos_collection.find_one({"_id": ObjectId(evento_id)})
    if not evento:
        raise HTTPException(status_code=404, detail="❌ Evento não encontrado")

    evento["_id"] = str(evento["_id"])
    return evento


def listar_eventos_por_parque(parque_id: str):
    eventos = list(eventos_collection.find({"parque_id": parque_id}))

    if not eventos:
        raise HTTPException(status_code=404, detail="❌ Nenhum evento encontrado para esse parque.")

    for evento in eventos:
        evento["_id"] = str(evento["_id"])

    return {"eventos": eventos}


def atualizar_evento(evento_id: str, evento: EventoModel):
    if not ObjectId.is_valid(evento_id):
        raise HTTPException(status_code=400, detail="ID inválido")
    evento_db = eventos_collection.find_one({"_id": ObjectId(evento_id)})

    if not evento_db:
        raise HTTPException(status_code=404, detail="❌ Evento não encontrado")

    eventos_collection.update_one({"_id": ObjectId(evento_id)}, {"$set": evento.dict()})
    return {"message": f"✅ Evento '{evento_id}' atualizado com sucesso!"}


def excluir_evento(evento_id: str):
    if not ObjectId.is_valid(evento_id):
        raise HTTPException(status_code=400, detail="ID inválido")
    evento_db = eventos_collection.find_one({"_id": ObjectId(evento_id)})

    if not evento_db:
        raise HTTPException(status_code=404, detail="❌ Evento não encontrado")

    eventos_collection.delete_one({"_id": ObjectId(evento_id)})
    return {"message": f"✅ Evento '{evento_id}' deletado com sucesso!"}
