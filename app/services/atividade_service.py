from app.config.database_config import atividades_collection, db
from bson import ObjectId
from fastapi import HTTPException
from app.models.atividade_model import AtividadeModel, TipoAtividadeEnum


def criar_atividade(atividade: AtividadeModel):
    if atividade.tipo not in TipoAtividadeEnum.__members__.values():
        raise HTTPException(status_code=400, detail="❌ Tipo de atividade inválido. Escolha entre 'trilha', 'cachoeira' ou 'escalada'.")

    if not ObjectId.is_valid(atividade.parque_id):
        raise HTTPException(status_code=400, detail="ID inválido")
    parque = db.parques.find_one({"_id": ObjectId(atividade.parque_id)})

    if not parque:
        raise HTTPException(status_code=404, detail="❌ Parque não encontrado, impossível cadastrar atividade.")

    atividade_dict = atividade.dict()
    atividade_dict["_id"] = str(atividades_collection.insert_one(atividade_dict).inserted_id)
    return {"message": "✅ Atividade cadastrada com sucesso!", "atividade": atividade_dict}


def buscar_atividade(atividade_id: str):
    if not ObjectId.is_valid(atividade_id):
        raise HTTPException(status_code=400, detail="ID inválido")
    atividade = atividades_collection.find_one({"_id": ObjectId(atividade_id)})
    if not atividade:
        raise HTTPException(status_code=404, detail="❌ Atividade não encontrada")

    atividade["_id"] = str(atividade["_id"])
    return atividade


def listar_atividades_por_parque(parque_id: str, tipo: TipoAtividadeEnum = None):
    filtro = {"parque_id": parque_id}
    if tipo:
        filtro["tipo"] = tipo.value

    atividades = list(atividades_collection.find(filtro))

    if not atividades:
        raise HTTPException(status_code=404, detail="❌ Nenhuma atividade encontrada para esse parque.")

    for atividade in atividades:
        atividade["_id"] = str(atividade["_id"])

    return {"atividades": atividades}


def atualizar_atividade(atividade_id: str, atividade: AtividadeModel):
    if atividade.tipo not in TipoAtividadeEnum.__members__.values():
        raise HTTPException(status_code=400, detail="❌ Tipo de atividade inválido. Escolha entre 'trilha', 'cachoeira' ou 'escalada'.")

    if not ObjectId.is_valid(atividade_id):
        raise HTTPException(status_code=400, detail="ID inválido")
    atividade_db = atividades_collection.find_one({"_id": ObjectId(atividade_id)})

    if not atividade_db:
        raise HTTPException(status_code=404, detail="❌ Atividade não encontrada")

    atividades_collection.update_one({"_id": ObjectId(atividade_id)}, {"$set": atividade.dict()})
    return {"message": f"✅ Atividade '{atividade_id}' atualizada com sucesso!"}


def excluir_atividade(atividade_id: str):
    if not ObjectId.is_valid(atividade_id):
        raise HTTPException(status_code=400, detail="ID inválido")
    atividade_db = atividades_collection.find_one({"_id": ObjectId(atividade_id)})

    if not atividade_db:
        raise HTTPException(status_code=404, detail="❌ Atividade não encontrada")

    atividades_collection.delete_one({"_id": ObjectId(atividade_id)})
    return {"message": f"✅ Atividade '{atividade_id}' deletada com sucesso!"}
