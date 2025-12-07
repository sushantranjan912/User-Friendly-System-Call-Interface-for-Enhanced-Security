FROM python:3.11-slim

# Prevent Python from writing .pyc files and buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8000
# Default APP_MODULE (module:callable). Update if your backend entrypoint differs.
ARG APP_MODULE=backend.app:app
ENV APP_MODULE=${APP_MODULE}

WORKDIR /app

# Install dependencies (requirements.txt is at repo root)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code into the container
COPY backend/ ./backend
WORKDIR /app/backend

EXPOSE ${PORT}

# Start with gunicorn. Ensure APP_MODULE matches your callable (e.g. backend.app:app)
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT} --workers 3 ${APP_MODULE}"]
