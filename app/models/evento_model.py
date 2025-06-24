from pydantic import BaseModel
from datetime import datetime


class EventoModel(BaseModel):
    nome: str
    descricao: str
    data: datetime
    localizacao: str
    parque_id: str
