FROM node:22-alpine

WORKDIR /app

# Copia package.json e lock
COPY package.json package-lock.json ./

# Instala dependências
RUN npm ci

# Copia código
COPY . .

EXPOSE 5173

# Executa Vite dev server
CMD ["npm", "run", "dev", "--", "--host"]
