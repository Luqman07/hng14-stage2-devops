FROM node:18-alpine AS builder

WORKDIR /app

COPY package*.json .

RUN npm ci --omit=dev
COPY . .

FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app/node_modules ./node_modules
COPY . .
RUN adduser --disabled-password --no-create-home appuser \
    && chown -R appuser:appuser /app

USER appuser
EXPOSE 3000
HEALTHCHECK --interval=15s --timeout=5s --start-period=10s --retries=3 \
CMD node -e "require('http').get('http://localhost:3000/health', (r) => process.exit(r.statusCode === 200 ? 0 : 1)).on('error', () => process.exit(1))"

CMD ["npm", "start"]    