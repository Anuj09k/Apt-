# Aptimizer API
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# shapely 2.x, numpy, pillow and reportlab all ship manylinux wheels, so no GEOS or
# image libraries need building from source. curl is here only for the healthcheck.
RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Never run as root in a container that faces the internet.
RUN useradd --create-home --uid 10001 apt && chown -R apt:apt /app
USER apt

# Host platforms assign the port (Render sets PORT=10000 and forwards traffic there);
# 8000 is the local and docker-compose default. WEB_CONCURRENCY is 2 here to keep the
# previous behaviour, and is set to 1 on Render's 512 MB free instance -- the imports
# alone (numpy, pandas, shapely, ifcopenshell, reportlab) do not leave room for two.
ENV PORT=8000 \
    WEB_CONCURRENCY=2

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=40s --retries=3 \
  CMD curl -fsS "http://localhost:${PORT}/api/" || exit 1

CMD ["sh", "-c", "exec uvicorn server:app --host 0.0.0.0 --port ${PORT} --workers ${WEB_CONCURRENCY}"]
