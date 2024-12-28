FROM python:3.12-slim

WORKDIR /app

RUN mkdir -p /app/fonts

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

VOLUME /app/fonts

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"] 