# 🍕 RistoApp

> Gestão inteligente de estoque, CMV preditivo e automação operacional para restaurantes e cozinhas de alta demanda.

O **RistoApp** nasce como uma plataforma de retaguarda projetada para o ritmo acelerado de cozinhas industriais e restaurantes. O foco da primeira versão é estancar o aumento silencioso do CMV (Custo da Mercadoria Vendida), eliminar planilhas manuais, automatizar conversões de insumos e acelerar a rotulagem sanitária de fracionamentos, servindo como base sólida para a evolução em direção a um ERP gastronômico completo.

---

## 🎯 Problemas que Resolvemos

- **Aumento Silencioso do CMV:** Rastreamento pontual de perdas e sobras diárias com impacto financeiro em tempo real.
- **Sobrecarga e Erros Manuais:** Automação de cálculos manuais e substituição de planilhas paralelas propensas a falhas.
- **Conversão Automática de Unidades:** Conversão dinâmica nos bastidores entre entradas em grande volume (caixas, fardos) e saídas operacionais (gramas, ml).
- **Etiquetas Sanitárias Inteligentes:** Consolidação de rotulagem de insumos fracionados, economizando papel térmico e tempo da equipe em conformidade com a Anvisa.

---

## 🛠️ Stack Tecnológica

O projeto adota uma arquitetura desacoplada e fortemente tipada ponta a ponta:

| Camada | Tecnologia | Hospedagem / Infra |
| :--- | :--- | :--- |
| **Frontend** | Vue 3 (Composition API) + TypeScript + Vite | [Vercel](https://vercel.com/) |
| **Backend** | Python 3.14 + FastAPI + Pydantic | [Render](https://render.com/) |
| **Banco de Dados** | PostgreSQL 16 + SQLAlchemy 2.0 + Alembic | [Neon Serverless](https://neon.com/) |
| **Driver DB** | psycopg3 (`psycopg[binary,pool]`) | — |
| **DevOps & Containers** | Docker & Docker Compose, GitHub Actions | CI/CD automatizado |

---

## 🏗️ Arquitetura do Sistema

A infraestrutura segue o modelo descentralizado PaaS (*Platform as a Service*):

1. **SPA (Vercel):** Distribuição global de arquivos estáticos em milissegundos.
2. **API RESTful (Render):** Servidor assíncrono processando regras de negócio e validações rigorosas de estoque via Pydantic.
3. **Database Serverless (Neon):** Persistência relacional ACID com conexões via `psycopg3`.

---

## 🚀 Como Executar o Projeto Localmente

### Pré-requisitos

- [Git](https://git-scm.com/)
- [Docker](https://www.docker.com/) e Docker Compose (recomendado)
- Ou localmente: **Node.js 22+**, **Python 3.14+**, **uv** (gerenciador de pacotes) e instância **PostgreSQL 16**

---

### Opção 1: Via Docker Compose (Recomendado)

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/ristoapp.git
cd ristoapp
```

2. Configure as variáveis de ambiente:
```bash
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

3. Suba os containers:
```bash
docker compose up --build
```

- Frontend: `http://localhost:5173`
- Backend API: `http://localhost:8000`
- Documentação interativa Swagger: `http://localhost:8000/docs`

---

### Opção 2: Configuração Manual

#### Backend

```bash
cd backend
uv sync
alembic upgrade head
fastapi dev ./src/main.py
```

#### Frontend

```bash
cd frontend
npm install
npm run dev
```

---

## 📁 Estrutura do Repositório

```text
ristoapp/
├── backend/                # API FastAPI, modelos e migrações
│   ├── alembic/            # Versionamento de schema de banco
│   ├── src/
│   │   ├── main.py         # Entrypoint FastAPI
│   │   ├── core/           # Configurações, logs e database
│   │   └── modules/        # Módulos de domínio
│   │       └── auth/       # Autenticação (router, service, model, schema)
│   ├── tests/              # Testes pytest
│   ├── Dockerfile
│   └── pyproject.toml      # Dependências (gerenciadas via uv)
├── frontend/               # SPA Vue 3 + TypeScript
│   ├── src/
│   │   ├── main.ts         # Entrypoint e plugins
│   │   ├── router.ts       # Vue Router
│   │   ├── features/       # Feature-Sliced Design (módulos de domínio)
│   │   │   └── auth/       # Feature de autenticação
│   │   └── shared/         # API client, utils e assets compartilhados
│   ├── Dockerfile
│   └── package.json
├── docker-compose.yml      # Orquestração local de desenvolvimento
├── DOCKER_SETUP.md         # Documentação detalhada do setup Docker
└── README.md
```

---

## 🔒 Variáveis de Ambiente

### Backend (`backend/.env`)
```ini
ENVIRONMENT=development
DATABASE_URL=postgresql+psycopg://ristoapp:ristoapp_dev_password@localhost:5432/ristoapp
SECRET_KEY=sua-chave-secreta-aqui
```

### Frontend (`frontend/.env`)
```ini
VITE_API_BASE_URL=http://localhost:8000
```

---

## 📄 Licença

Este projeto é proprietário e desenvolvido sob medida para a equipe **RistoApp**.
