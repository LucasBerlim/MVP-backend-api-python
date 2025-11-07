from pydantic import BaseModel, EmailStr, constr

class UpdateProfileModel(BaseModel):
    name: constr(strip_whitespace=True, min_length=1)

class UpdateEmailModel(BaseModel):
    email: EmailStr
    current_password: constr(min_length=1)

class ChangePasswordModel(BaseModel):
    current_password: constr(min_length=1)
    new_password: constr(min_length=6)
