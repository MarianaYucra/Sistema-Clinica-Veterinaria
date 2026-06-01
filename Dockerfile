# BUILDER (Compilación a Bytecode)
FROM python:3.13.12-slim AS builder
WORKDIR /build

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/
RUN rm -f ./app/webapp.py
RUN python -m compileall -b ./app/
RUN find ./app/ -name "*.py" -type f -delete

# RUNNER (Imagen Final)
FROM python:3.13.12-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /sistema

COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /build/app ./app

RUN mkdir -p data
CMD ["python", "-m", "app.main"]
