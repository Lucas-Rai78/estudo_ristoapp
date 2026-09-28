from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.modules.auth.schema import UserCreate, UserLogin, LoginResponse, RegisterResponse
from src.modules.auth.service import AuthService

router = APIRouter(prefix="/auth", tags=["Autenticação e Cadastro"])

@router.post("/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
def registrar_usuario(usuario_data: UserCreate, db: Session = Depends(get_db)):
    return AuthService.registrar_usuario(usuario_data, db)

@router.post("/login", response_model=LoginResponse)
def login(usuario_data: UserLogin, db: Session = Depends(get_db)):
    return AuthService.autenticar_usuario(usuario_data, db)