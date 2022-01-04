FROM python:3.9.7

WORKDIR /usr/src/frontend/

COPY requirements.txt .

EXPOSE 8000

RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "8000"]

