from datetime import datetime, timedelta, timezone
from jose import jwt
from passlib.context import CryptContext

SECRET_KEY = "chave_secreta_desenvolvimento_mude_em_producao"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verificar_senha(senha_pura: str, senha_hash: str) -> bool:
    return pwd_context.verify(senha_pura, senha_hash)

def gerar_hash_senha(senha_pura: str) -> str:
    return pwd_context.hash(senha_pura)

def criar_token_acesso(dados: dict) -> str:
    conteudo = dados.copy()
    expiracao = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    conteudo.update({"exp": expiracao})
    return jwt.encode(conteudo, SECRET_KEY, algorithm=ALGORITHM)