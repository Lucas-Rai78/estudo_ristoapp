from sqlalchemy.orm import Session
from src.modules.usuarios.models import Usuario

class UsuarioRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def buscar_por_email(self, email: str):
        return self.db.query(Usuario).filter(Usuario.email == email).first()

    def criar(self, nome: str, email: str, senha_hash: str):
        usuario = Usuario(
            nome=nome,
            email=email,
            senha_hash=senha_hash,
        )

        self.db.add(usuario)
        self.db.commit()
        self.db.refresh(usuario)

        return usuario