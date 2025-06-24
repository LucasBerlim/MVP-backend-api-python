from pydantic import BaseModel, Field


class UserModel(BaseModel):
    email: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)
    role: str = Field(..., pattern="^(usuario|administrador)$")
    active: bool = Field(default=True)


class LoginModel(BaseModel):
    email: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)
