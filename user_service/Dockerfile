FROM python:3.11-slim

WORKDIR /user

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8081

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8081"]