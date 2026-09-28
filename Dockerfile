FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY project-2-api-monitor/ project-2-api-monitor/
COPY synthetic_reporter.py .
COPY .env .
ENV PORT=10000
EXPOSE 10000
CMD ["python3", "synthetic_reporter.py"]
