# CareerForge AI Frontend Dockerfile for Google Cloud Run
# Stage 1: Build
FROM node:22-alpine AS builder

WORKDIR /app
COPY frontend/package.json ./
RUN npm install

ARG VITE_API_BASE=""
ENV VITE_API_BASE=$VITE_API_BASE

COPY frontend ./
RUN npm run build

# Stage 2: Production Nginx Server
FROM nginx:alpine

COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD wget -q --spider http://localhost:8080/health || exit 1

CMD ["nginx", "-g", "daemon off;"]
