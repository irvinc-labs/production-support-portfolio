FROM python:3.14-slim

WORKDIR /app

# Compliance: Create a non-root service user for enterprise security
RUN useradd --create-home --uid 10001 appuser

# Copy our application source code into the container folder
COPY app/src/main.py .

# Switch to the secure user
USER appuser

# Tell the cloud network that our app listens on port 8080
EXPOSE 8080

# Turn on the app when the container boots
CMD ["python3", "main.py"]
