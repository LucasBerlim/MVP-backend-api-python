from fastapi import APIRouter, Depends
from app.models.evento_model import EventoModel
from app.services.evento_service import (
    criar_evento, buscar_evento, listar_eventos_por_parque,
    atualizar_evento, excluir_evento
)
from app.services.auth_service import is_admin

router = APIRouter()


@router.post("/eventos", dependencies=[Depends(is_admin)])
def post_evento(evento: EventoModel):
    return criar_evento(evento)


@router.get("/eventos/{evento_id}")
def get_evento(evento_id: str):
    return buscar_evento(evento_id)


@router.get("/eventos/parque/{parque_id}")
def get_eventos_por_parque(parque_id: str):
    return listar_eventos_por_parque(parque_id)


@router.put("/eventos/{evento_id}", dependencies=[Depends(is_admin)])
def update_evento(evento_id: str, evento: EventoModel):
    return atualizar_evento(evento_id, evento)


@router.delete("/eventos/{evento_id}", dependencies=[Depends(is_admin)])
def delete_evento(evento_id: str):
    return excluir_evento(evento_id)
