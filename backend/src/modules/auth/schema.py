from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=72)

class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=72)

class AuthUser(BaseModel):
    id: str
    name: str
    email: EmailStr

    class Config:
        from_attributes = True

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: AuthUser

class RegisterResponse(BaseModel):
    message: str = "Usuário cadastrado com sucesso"
    user: AuthUser