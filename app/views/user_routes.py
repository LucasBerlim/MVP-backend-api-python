from fastapi import APIRouter, HTTPException
from app.config.database_config import users_collection
from app.models.user_model import UserModel, LoginModel
import bcrypt
import jwt
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY:
    raise ValueError("❌ SECRET_KEY não encontrada! Verifique o arquivo .env.")


@router.post("/register")
def register(user: UserModel):
    hashed_pw = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt())
    users_collection.insert_one({
        "email": user.email,
        "password": hashed_pw.decode(),
        "role": user.role,
        "active": True
    })
    return {"message": f"✅ Usuário '{user.email}' registrado com sucesso como {user.role}!"}


@router.post("/login")
def login(user: LoginModel):
    user_db = users_collection.find_one({"email": user.email})

    if not user_db or not bcrypt.checkpw(user.password.encode(), user_db["password"].encode()):
        raise HTTPException(status_code=401, detail="❌ Credenciais inválidas")

    token = jwt.encode(
        {"email": user.email, "role": user_db["role"]},
        SECRET_KEY,
        algorithm="HS256"
    )

    print(f"✅ Token gerado: {token}")
    print(f"🔑 SECRET_KEY usada na geração: {SECRET_KEY}")

    return {"token": token, "role": user_db["role"], "active": user_db["active"]}
