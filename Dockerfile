FROM python:3.9

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8000

WORKDIR /app/src

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "80"]