FROM python:3.11-slim

# this is for no wait to fill the buffer before to print the message
ENV PYTHONUNBUFFERED=1 

WORKDIR /app

COPY . /app

CMD ["python", "-m", "app.main"]