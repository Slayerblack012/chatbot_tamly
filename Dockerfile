FROM python:3.12-slim

WORKDIR /app

# Tạo non-root user nhằm tăng cường an ninh container
RUN groupadd -r appuser && useradd -r -g appuser appuser

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Phân quyền cho appuser
RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

# Healthcheck định kỳ kiểm tra backend
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/api/health')" || exit 1

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000", "--no-server-header"]
