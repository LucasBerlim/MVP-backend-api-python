from pydantic import BaseModel


class ParqueModel(BaseModel):
    nome: str
    localizacao: str
    endereco: str


class ParqueNomeRequest(BaseModel):
    nome: str
