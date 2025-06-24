from pydantic import BaseModel
from enum import Enum


class TipoAtividadeEnum(str, Enum):
    TRILHA = "trilha"
    CACHOEIRA = "cachoeira"
    ESCALADA = "escalada"


class AtividadeModel(BaseModel):
    tipo: TipoAtividadeEnum
    nome: str
    tempo: int
    localizacao: str
    imagem: str
    parque_id: str
