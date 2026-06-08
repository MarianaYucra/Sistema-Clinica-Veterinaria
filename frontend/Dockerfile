FROM node:24-alpine AS build

WORKDIR /app
ENV CI=true
ENV HOST=0.0.0.0
ENV PORT=4173

COPY package.json pnpm-lock.yaml ./
RUN corepack enable && pnpm install --frozen-lockfile

COPY . .
RUN pnpm build

EXPOSE 4173

CMD ["node", "build"]
