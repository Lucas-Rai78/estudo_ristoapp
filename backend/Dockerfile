FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY pyproject.toml uv.lock ./

# Instala dependencias fora de /app para nao ser sobrescrito pelo volume mount
ENV UV_PROJECT_ENVIRONMENT=/opt/venv
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

ENV PATH="/opt/venv/bin:$PATH"

EXPOSE 8000

CMD ["fastapi", "dev", "./src/main.py", "--host", "0.0.0.0"]