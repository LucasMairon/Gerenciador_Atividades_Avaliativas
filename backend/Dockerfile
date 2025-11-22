FROM python:3.12-slim
# LABEL mantainer = "lucasmairon2@gmail.com"

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1 
WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    netcat-openbsd \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libjpeg-dev \
    libopenjp2-7-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

RUN adduser --disabled-password --no-create-home --uid=1000 duser && \
    mkdir -p /data/web/static && \
    mkdir -p /data/web/media && \
    chown -R duser:duser /data && \
    chmod -R 755 /data && \
    chown -R duser:duser /app && \
    chown -R duser:duser /data


RUN python -m venv /venv && \
    /venv/bin/pip install --upgrade pip && \
    chown -R duser:duser /venv 

COPY ./requirements.txt /app/requirements.txt
RUN /venv/bin/pip install -r /app/requirements.txt

COPY ./scripts /scripts
RUN chmod -R +x /scripts


COPY --chown=duser:duser . /app

RUN chown -R duser:duser /venv

EXPOSE 8000

ENV PATH="/scripts:/venv/bin:$PATH"

USER duser

CMD ["entrypoint.sh"]
