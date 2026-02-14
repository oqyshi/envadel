FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Внутри контейнера он тоже может работать на 8000 порту, 
# мы разведем порты наружу через docker-compose
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]