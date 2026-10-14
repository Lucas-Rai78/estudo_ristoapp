from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from src.modules.auth.database.repository import UsuarioRepository
from src.modules.auth.schema import UserCreate, UserLogin, AuthUser, LoginResponse, RegisterResponse
from src.core.security import verificar_senha, gerar_hash_senha, criar_token_acesso

class AuthService:
    @staticmethod
    def registrar_usuario(usuario_data: UserCreate, db: Session) -> RegisterResponse:
        repo = UsuarioRepository(db)

        usuario_existente = repo.buscar_por_email(usuario_data.email)
        if usuario_existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="EMAIL_ALREADY_EXISTS"
            )

        novo_usuario = repo.criar(
            nome=usuario_data.name,
            email=usuario_data.email,
            senha_hash=gerar_hash_senha(usuario_data.password)
        )

        return RegisterResponse(
            user=AuthUser(
                id=str(novo_usuario.id),
                name=novo_usuario.nome,
                email=novo_usuario.email
            )
        )

    @staticmethod
    def autenticar_usuario(usuario_data: UserLogin, db: Session) -> LoginResponse:
        repo = UsuarioRepository(db)
        usuario = repo.buscar_por_email(usuario_data.email)

        if not usuario or not verificar_senha(
            usuario_data.password,
            usuario.senha_hash
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="INVALID_CREDENTIALS"
            )

        access_token = criar_token_acesso(data={"sub": str(usuario.id)})

        return LoginResponse(
            access_token=access_token,
            token_type="bearer",
            user=AuthUser(
                id=str(usuario.id),
                name=usuario.nome,
                email=usuario.email
            )
        )