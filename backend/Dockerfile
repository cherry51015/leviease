# Use official Python image
FROM python:3.12-slim

WORKDIR /app

# Copy backend code
COPY backend/ ./backend

# Install dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Expose port for Cloud Run / Docker
ENV PORT 8080

# Run FastAPI
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8080"]
