from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.security import verificar_senha, gerar_hash_senha, criar_token_acesso
from src.modules.auth.schema import (
    UserCreate,
    UserLogin,
    AuthUser,
    LoginResponse,
    RegisterResponse,
)
from src.modules.usuarios.models import Usuario

router = APIRouter(prefix="/auth", tags=["Autenticação e Cadastro"])

# 1. Endpoint de Cadastro
@router.post("/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
def registrar_usuario(usuario_data: UserCreate, db: Session = Depends(get_db)):
    usuario_existente = db.query(Usuario).filter(Usuario.email == usuario_data.email).first()
    if usuario_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="EMAIL_ALREADY_EXISTS"
        )

    novo_usuario = Usuario(
        nome=usuario_data.name,
        email=usuario_data.email,
        senha_hash=gerar_hash_senha(usuario_data.password)
    )

    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)

    return RegisterResponse(
        user=AuthUser(
            id=str(novo_usuario.id),
            name=novo_usuario.nome,
            email=novo_usuario.email
        )
    )

# 2. Endpoint de Login
@router.post("/login", response_model=LoginResponse)
def login(usuario_data: UserLogin, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == usuario_data.email).first()

    if not usuario or not verificar_senha(usuario_data.password, usuario.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="INVALID_CREDENTIALS"
        )

    access_token = criar_token_acesso(dados={"sub": str(usuario.id)})

    return LoginResponse(
        accessToken=access_token,
        user=AuthUser(
            id=str(usuario.id),
            name=usuario.nome,
            email=usuario.email
        )
    )