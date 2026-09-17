# Estágio de build com uv
FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim AS builder

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

WORKDIR /app

# Copia apenas as definições de dependências para aproveitar cache de build
COPY pyproject.toml uv.lock ./

# Instala as dependências congeladas sem instalar o próprio projeto ainda
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

# Estágio final de execução
FROM python:3.14-slim-bookworm

WORKDIR /app

# Copia o ambiente virtual gerado pelo uv
COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Copia o código da aplicação e configurações do Alembic
COPY alembic.ini ./
COPY alembic ./alembic
COPY src ./src
COPY main.py ./

EXPOSE 8000

# Executa o Uvicorn apontando para a instância do FastAPI
CMD ["fastapi", "dev", "./src/main.py", "--host", "0.0.0.0"]