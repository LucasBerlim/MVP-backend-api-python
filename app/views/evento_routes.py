# app/views/evento_routes.py
from fastapi import APIRouter, Depends, Query
from typing import Optional
from app.models.evento_model import EventoModel
from app.services.evento_service import (
    criar_evento, buscar_evento, listar_eventos_por_parque,
    atualizar_evento, excluir_evento, listar_eventos_recentes, listar_eventos
)
from app.services.parque_service import listar_parques_basico
from app.services.auth_service import is_admin

from datetime import datetime

router = APIRouter()

@router.post("/eventos", dependencies=[Depends(is_admin)])
def post_evento(evento: EventoModel):
    return criar_evento(evento)

@router.get("/eventos/recentes")
def get_eventos_recentes(
    limit: int = Query(default=5, ge=1, le=100),
    parque_id: Optional[str] = None,
    parque_nome: Optional[str] = None
):
    return listar_eventos_recentes(limit=limit, parque_id=parque_id, parque_nome=parque_nome)

@router.get("/eventos/parque/{parque_id}")
def get_eventos_por_parque(parque_id: str, limit: int = Query(default=0, ge=0, le=100)):
    return listar_eventos_por_parque(parque_id, limit=limit)

@router.get("/eventos/{evento_id}")
def get_evento(evento_id: str):
    return buscar_evento(evento_id)

@router.put("/eventos/{evento_id}", dependencies=[Depends(is_admin)])
def put_evento(evento_id: str, evento: EventoModel):
    return atualizar_evento(evento_id, evento)

@router.get("/eventos")
def get_eventos(
    parque_id: Optional[str] = None,
    start: Optional[str] = Query(default=None, description="ISO datetime"),
    end: Optional[str] = Query(default=None, description="ISO datetime"),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=0, ge=0, le=1000),
    sort: str = Query(default="asc", pattern="^(asc|desc)$"),
):
    s_dt = datetime.fromisoformat(start) if start else None
    e_dt = datetime.fromisoformat(end) if end else None
    return listar_eventos(parque_id=parque_id, start=s_dt, end=e_dt, skip=skip, limit=limit, sort=sort)

@router.delete("/eventos/{evento_id}", dependencies=[Depends(is_admin)])
def del_evento(evento_id: str):
    return excluir_evento(evento_id)

@router.get("/parques")
def get_parques():
    return listar_parques_basico()
