from fastapi import APIRouter, HTTPException, Depends
from app.config.database_config import users_collection
from app.models.profile_models import UpdateProfileModel, UpdateEmailModel, ChangePasswordModel
from app.services.auth_helpers import get_current_user, issue_token
import bcrypt

router = APIRouter(prefix="/me", tags=["me"])

@router.get("")
def get_me(user=Depends(get_current_user)):
    return {
        "email": user.get("email"),
        "name": user.get("name"),
        "role": user.get("role"),
        "active": user.get("active", True),
    }

@router.put("/profile")
def update_profile(body: UpdateProfileModel, user=Depends(get_current_user)):
    users_collection.update_one({"_id": user["_id"]}, {"$set": {"name": body.name}})
    return {"message": "✅ Nome atualizado com sucesso", "name": body.name}

@router.put("/email")
def update_email(body: UpdateEmailModel, user=Depends(get_current_user)):
    # 1) confere senha atual
    if not bcrypt.checkpw(body.current_password.encode(), user["password"].encode()):
        raise HTTPException(status_code=401, detail="❌ Senha atual incorreta.")
    # 2) e-mail único
    if users_collection.find_one({"email": body.email}):
        raise HTTPException(status_code=400, detail="❌ E-mail já está em uso.")
    # 3) atualiza e emite novo token
    users_collection.update_one({"_id": user["_id"]}, {"$set": {"email": body.email}})
    new_token = issue_token(body.email, user["role"])
    return {
        "message": "✅ E-mail atualizado com sucesso",
        "email": body.email,
        "token": new_token,
        "role": user["role"],
        "active": user.get("active", True),
    }

@router.put("/password")
def change_password(body: ChangePasswordModel, user=Depends(get_current_user)):
    if not bcrypt.checkpw(body.current_password.encode(), user["password"].encode()):
        raise HTTPException(status_code=401, detail="❌ Senha atual incorreta.")
    new_hash = bcrypt.hashpw(body.new_password.encode(), bcrypt.gensalt()).decode()
    users_collection.update_one({"_id": user["_id"]}, {"$set": {"password": new_hash}})
    return {"message": "✅ Senha alterada com sucesso"}
