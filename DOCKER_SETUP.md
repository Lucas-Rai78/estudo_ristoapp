# Docker Setup - RistoApp (Desenvolvimento)

Ambiente Docker configurado para desenvolvimento local com hot-reload.

---

## Quickstart

```bash
# Subir tudo (frontend + backend + banco)
docker compose up --build

# Parar tudo
docker compose down
```

**Acesse:**
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- Swagger Docs: http://localhost:8000/docs

---

## Servicos

| Servico | Tecnologia | Porta | Hot-reload |
|---------|-----------|-------|------------|
| **frontend** | Vue 3 + Vite | 5173 | Sim (src/, public/, index.html) |
| **backend** | FastAPI + uv | 8000 | Sim (src/, main.py, alembic/) |
| **db** | PostgreSQL 16 | 5432 | N/A |

---

## Banco de Dados

- **User:** `ristoapp`
- **Password:** `ristoapp_dev_password`
- **Database:** `ristoapp`
- **Connection string:** `postgresql+psycopg://ristoapp:ristoapp_dev_password@db:5432/ristoapp`

### Acesso direto
```bash
docker compose exec db psql -U ristoapp -d ristoapp
```

### Migracoes (Alembic)
```bash
docker compose exec backend alembic upgrade head
docker compose exec backend alembic revision --autogenerate -m "descricao"
```

---

## Banco Externo (Neon, Supabase, etc.)

Para usar um banco externo ao inves do container local:

```bash
DATABASE_URL="postgresql+psycopg://user:pass@host/db" docker compose up --build
```

O servico `db` ainda sobe, mas o backend usara a URL fornecida.

---

## Volumes Montados (Hot-reload)

**Backend** - alteracoes refletem automaticamente:
- `./backend/src` -> `/app/src`
- `./backend/main.py` -> `/app/main.py`
- `./backend/alembic` -> `/app/alembic`
- `./backend/alembic.ini` -> `/app/alembic.ini`

> Dependencias Python ficam em `/opt/venv` (fora de `/app`), entao o volume mount nao as sobrescreve. Para atualizar deps, rode `docker compose up --build`.

**Frontend** - alteracoes refletem automaticamente:
- `./frontend/src` -> `/app/src`
- `./frontend/public` -> `/app/public`
- `./frontend/index.html` -> `/app/index.html`

> `node_modules` fica dentro do container. Para atualizar deps, rode `docker compose up --build`.

---

## Comandos Uteis

```bash
# Logs de um servico
docker compose logs -f backend
docker compose logs -f frontend

# Status dos containers
docker compose ps

# Shell dentro de um container
docker compose exec backend bash
docker compose exec frontend sh

# Rebuild forcado (apos mudar deps)
docker compose up --build

# Limpar tudo (volumes inclusos)
docker compose down -v
```

---

## Troubleshooting

| Problema | Solucao |
|----------|---------|
| Backend nao encontra `fastapi` | Rode `docker compose up --build` para reinstalar deps |
| DB connection failed | Verifique se o healthcheck passou: `docker compose ps` |
| Porta ja em uso | Pare o servico local ou altere a porta no `docker-compose.yml` |
| Hot-reload nao funciona | Reinicie: `docker compose down && docker compose up --build` |
| Mudou dependencias (pyproject.toml / package.json) | Rode `docker compose up --build` |

---

## Seguranca

As credenciais neste arquivo sao **apenas para desenvolvimento local**. Para producao, use variaveis de ambiente secretas e senhas fortes.
