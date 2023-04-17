FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get install -y build-essential
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]

