FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY --chown=1000:1000 . ./

USER 1000:1000
CMD ["python", "02_mongo_hardcoded.py"]
