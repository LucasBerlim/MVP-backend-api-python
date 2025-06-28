import jwt
import os
import logging
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)

load_dotenv()

security = HTTPBearer()

SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY:
    raise ValueError("❌ SECRET_KEY não encontrada! Verifique seu arquivo .env.")


def is_admin(token: HTTPAuthorizationCredentials = Depends(security)):
    try:

        if not SECRET_KEY:
            logging.error("❌ SECRET_KEY não foi carregada corretamente!")
            raise HTTPException(status_code=500, detail="Erro interno: chave de segurança não encontrada.")

        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=["HS256"])

        role = payload.get("role")
        if not role:
            logging.error("❌ Campo 'role' ausente no token!")
            raise HTTPException(status_code=400, detail="❌ Token inválido: campo 'role' ausente.")

        if role != "administrador":
            logging.warning("❌ Acesso negado! Usuário sem permissão.")
            raise HTTPException(status_code=403, detail="❌ Acesso negado, apenas administradores podem acessar.")

        logging.info("✅ Token validado com sucesso!")
        return payload

    except jwt.ExpiredSignatureError:
        logging.warning("❌ Token expirado!")
        raise HTTPException(status_code=401, detail="❌ Token expirado.")

    except jwt.DecodeError:
        logging.error("❌ Erro ao decodificar token!")
        raise HTTPException(status_code=401, detail="❌ Token inválido.")

    except jwt.InvalidTokenError:
        logging.error("❌ Token inválido!")
        raise HTTPException(status_code=401, detail="❌ Token inválido.")

    except Exception as e:
        logging.error(f"❌ Erro inesperado na validação do token: {str(e)}")
        raise HTTPException(status_code=500, detail="❌ Erro interno ao validar token.")
