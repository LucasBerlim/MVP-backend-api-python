from app.config.database_config import db
from bson import ObjectId
from fastapi import HTTPException
from app.models.parque_model import ParqueModel


def criar_parque(parque: ParqueModel):
    parque_dict = parque.dict()
    parque_dict["_id"] = str(db.parques.insert_one(parque_dict).inserted_id)
    return {"message": "✅ Parque cadastrado com sucesso!", "parque": parque_dict}


def buscar_parque(parque_id: str):
    if not ObjectId.is_valid(parque_id):
        raise HTTPException(status_code=400, detail="ID inválido")
    parque = db.parques.find_one({"_id": ObjectId(parque_id)})
    if not parque:
        raise HTTPException(status_code=404, detail="❌ Parque não encontrado")

    parque["_id"] = str(parque["_id"])
    return parque


def listar_parques():
    parques = list(db.parques.find({}))

    for parque in parques:
        parque["_id"] = str(parque["_id"])

    return {"parques": parques}


def atualizar_parque(parque_id: str, parque: ParqueModel):
    if not ObjectId.is_valid(parque_id):
        raise HTTPException(status_code=400, detail="ID inválido")
    parque_db = db.parques.find_one({"_id": ObjectId(parque_id)})

    if not parque_db:
        raise HTTPException(status_code=404, detail="❌ Parque não encontrado")

    db.parques.update_one({"_id": ObjectId(parque_id)}, {"$set": parque.dict()})
    return {"message": f"✅ Parque '{parque_id}' atualizado com sucesso!"}


def excluir_parque(parque_id: str):
    if not ObjectId.is_valid(parque_id):
        raise HTTPException(status_code=400, detail="ID inválido")
    parque_db = db.parques.find_one({"_id": ObjectId(parque_id)})

    if not parque_db:
        raise HTTPException(status_code=404, detail="❌ Parque não encontrado")

    db.eventos.delete_many({"parque_id": parque_id})
    db.atividades.delete_many({"parque_id": parque_id})
    db.parques.delete_one({"_id": ObjectId(parque_id)})
    return {"message": f"✅ Parque '{parque_id}' deletado com sucesso!"}


def buscar_parque_por_nome(nome_parque: str):
    parque = db.parques.find_one({"nome": nome_parque})

    if parque:
        return {
            "_id": str(parque["_id"]),
            "nome": parque["nome"],
            "localizacao": parque.get("localizacao", ""),
            "endereco": parque.get("endereco", ""),
            "imagem": parque.get("imagem", "")
        }

    return {"message": "Parque não encontrado"}
