from fastapi import APIRouter, HTTPException
from app.config.database_config import users_collection
from app.models.user_model import UserModel, LoginModel
from app.models.user_model import (
    UserModel,
    LoginModel,
    PasswordResetRequestModel,
    PasswordResetModel,
)
from app.services.mail_service import send_email
from datetime import datetime, timedelta
import secrets
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
    usuario_existente = users_collection.find_one({"email": user.email})
    if usuario_existente:
        raise HTTPException(status_code=400, detail="❌ Email já cadastrado!")

    hashed_pw = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt())
    users_collection.insert_one({
        "email": user.email,
        "password": hashed_pw.decode(),
        "role": user.role,
        "active": True,
        "reset_token": None,
        "reset_token_expires": None,
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

    return {"token": token, "role": user_db["role"], "active": user_db["active"]}


@router.post("/admins/password-reset-request")
def password_reset_request(data: PasswordResetRequestModel):
    user_db = users_collection.find_one({"email": data.email, "role": "administrador"})
    if not user_db:
        raise HTTPException(status_code=404, detail="❌ Administrador não encontrado")

    token = secrets.token_urlsafe(32)
    expires = datetime.utcnow() + timedelta(hours=1)

    users_collection.update_one(
        {"_id": user_db["_id"]},
        {"$set": {"reset_token": token, "reset_token_expires": expires}}
    )

    send_email(data.email, "Redefinição de Senha", f"Seu token para redefinição de senha: {token}")

    return {"message": "✅ Instruções de redefinição enviadas por email"}


@router.post("/admins/password-reset")
def password_reset(data: PasswordResetModel):
    user_db = users_collection.find_one({"reset_token": data.token})
    if not user_db:
        raise HTTPException(status_code=404, detail="❌ Token inválido")

    expires = user_db.get("reset_token_expires")
    if not expires or expires < datetime.utcnow():
        raise HTTPException(status_code=400, detail="❌ Token expirado")

    hashed_pw = bcrypt.hashpw(data.new_password.encode(), bcrypt.gensalt()).decode()
    users_collection.update_one(
        {"_id": user_db["_id"]},
        {
            "$set": {
                "password": hashed_pw,
                "reset_token": None,
                "reset_token_expires": None,
            }
        },
    )

    return {"message": "✅ Senha redefinida com sucesso"}
