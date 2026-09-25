from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.core.database import Base, engine
from src.modules.auth.router import router as auth_router

# Gera automaticamente as tabelas no banco de dados ao iniciar
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Gerenciador de Produtos API")

# Habilita o CORS para aceitar requisições do frontend em Vue 3
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)

@app.get("/")
def status_api():
    return {"status": "API rodando perfeitamente"}

from src.modules.auth.router import router as auth_router

app.include_router(auth_router)