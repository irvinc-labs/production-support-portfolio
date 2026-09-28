FROM python:3.14-slim

WORKDIR /app

# Compliance: create a non-root service user
RUN useradd --create-home --uid 10001 appuser

# Install application dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY app/ app/

# Render runtime port
ENV PORT=10000

# Run as non-root user
USER appuser

EXPOSE 10000

CMD ["python3", "app/src/main.py"]
