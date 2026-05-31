FROM python:3.11-slim

# this is for no wait to fill the buffer before to print the message
ENV PYTHONUNBUFFERED=1 

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

ENV HOST=0.0.0.0
ENV PORT=5000

CMD ["python", "-m", "app.webapp"]
