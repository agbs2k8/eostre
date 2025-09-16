# Next.js dev Dockerfile
FROM node:20-alpine

WORKDIR /app

# Install dependencies first (better caching)
COPY package.json package-lock.json* pnpm-lock.yaml* yarn.lock* ./
RUN if [ -f package-lock.json ]; then npm ci; \
    elif [ -f pnpm-lock.yaml ]; then npm install -g pnpm && pnpm install; \
    elif [ -f yarn.lock ]; then yarn install --frozen-lockfile; \
    else npm install; fi

# Copy rest of the source
COPY . .

EXPOSE 3000

ENV PORT=3000 \
    HOST=0.0.0.0 \
    NODE_ENV=development

# Prefer npm dev; adjust if using pnpm/yarn
CMD ["npm", "run", "dev"]