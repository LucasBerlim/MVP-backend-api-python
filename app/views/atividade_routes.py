from fastapi import APIRouter, Depends
from app.models.atividade_model import AtividadeModel
from app.services.atividade_service import (
    criar_atividade, buscar_atividade, listar_atividades_por_parque,
    atualizar_atividade, excluir_atividade
)
from app.services.auth_service import is_admin

router = APIRouter()


@router.post("/atividades", dependencies=[Depends(is_admin)])
def post_atividade(atividade: AtividadeModel):
    return criar_atividade(atividade)


@router.get("/atividades/{atividade_id}")
def get_atividade(atividade_id: str):
    return buscar_atividade(atividade_id)


@router.get("/atividades/parque/{parque_id}")
def get_atividades_por_parque(parque_id: str):
    return listar_atividades_por_parque(parque_id)


@router.put("/atividades/{atividade_id}", dependencies=[Depends(is_admin)])
def update_atividade(atividade_id: str, atividade: AtividadeModel):
    return atualizar_atividade(atividade_id, atividade)


@router.delete("/atividades/{atividade_id}", dependencies=[Depends(is_admin)])
def delete_atividade(atividade_id: str):
    return excluir_atividade(atividade_id)
