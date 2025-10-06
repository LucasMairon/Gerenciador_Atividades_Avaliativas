FROM python:3.12-alpine
# LABEL mantainer = "lucasmairon2@gmail.com"

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1 

COPY . /app
COPY ./scripts /scripts

WORKDIR /app

EXPOSE 8000

RUN python -m venv /venv && \
    /venv/bin/pip install --upgrade pip && \
    /venv/bin/pip install -r /app/requirements.txt && \
    adduser --disabled-password --no-create-home --uid=1000 duser && \
    mkdir -p /data/web/static && \
    mkdir -p /data/web/media && \
    chown -R duser:duser /venv && \
    chown -R duser:duser /app && \
    chown -R duser:duser /data && \
    chmod -R +x /scripts

ENV PATH="/scripts:/venv/bin:$PATH"

USER duser

CMD ["entrypoint.sh"]
