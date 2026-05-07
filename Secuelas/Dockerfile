# ── Stage 1: Build React frontend ─────────────────────────────────────────────
FROM node:18-alpine AS frontend-builder
WORKDIR /frontend

# Install dependencies first (better layer caching)
COPY frontend/package.json frontend/package-lock.json* ./
RUN npm install

# Copy source and build
COPY frontend/ .
RUN npm run build

# ── Stage 2: Python + Flask (serves API + React build) ────────────────────────
FROM python:3.11-slim
WORKDIR /app

# Install Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source
COPY backend/ .

# Copy the React production build from stage 1
COPY --from=frontend-builder /frontend/build ./build

# Flask needs to know which app module to use
ENV FLASK_APP=app.py

# Railway injects $PORT at runtime; default to 8080 for local testing
EXPOSE 8080

# Initialize the DB, then start gunicorn
CMD sh -c "flask init-db && gunicorn --bind 0.0.0.0:${PORT:-8080} --workers 2 --timeout 120 app:app"
