from fastapi import APIRouter, Depends
from app.models.parque_model import ParqueModel
from app.services.parque_service import (
    criar_parque, buscar_parque, listar_parques,
    atualizar_parque, excluir_parque, buscar_parque_por_nome
)
from app.services.auth_service import is_admin

router = APIRouter()


@router.get("/parques/nome")
def get_parque_por_nome(nome: str):
    return buscar_parque_por_nome(nome)


@router.post("/parques", dependencies=[Depends(is_admin)])
def post_parque(parque: ParqueModel):
    return criar_parque(parque)


@router.get("/parques/{parque_id}")
def get_parque(parque_id: str):
    return buscar_parque(parque_id)


@router.get("/parques")
def get_all_parques():
    return listar_parques()


@router.put("/parques/{parque_id}", dependencies=[Depends(is_admin)])
def update_parque(parque_id: str, parque: ParqueModel):
    return atualizar_parque(parque_id, parque)


@router.delete("/parques/{parque_id}", dependencies=[Depends(is_admin)])
def delete_parque(parque_id: str):
    return excluir_parque(parque_id)
