import os, jwt, bcrypt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.config.database_config import users_collection
from dotenv import load_dotenv

load_dotenv()
security = HTTPBearer()
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("❌ SECRET_KEY não encontrada! Verifique seu .env.")

def get_current_user(token: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=["HS256"])
        email = payload.get("email")
        if not email:
            raise HTTPException(status_code=401, detail="❌ Token inválido (sem e-mail).")
        user = users_collection.find_one({"email": email})
        if not user:
            raise HTTPException(status_code=401, detail="❌ Usuário não encontrado.")
        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="❌ Token expirado.")
    except Exception:
        raise HTTPException(status_code=401, detail="❌ Token inválido.")

def issue_token(email: str, role: str):
    return jwt.encode({"email": email, "role": role}, SECRET_KEY, algorithm="HS256")
