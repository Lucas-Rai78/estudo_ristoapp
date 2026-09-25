from pydantic import BaseModel, EmailStr, Field

# DTO para cadastro
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

class LoginResponse(BaseModel):
    accessToken: str
    user: AuthUser

class RegisterResponse(BaseModel):
    user: AuthUser