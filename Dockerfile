FROM python:3.11-slim
WORKDIR /app

RUN apt-get update && apt-get install -y git

RUN git clone https://github.com/gery28/atlasProject .



RUN pip install --upgrade pip \
    && pip install -r requirements.txt

EXPOSE 5000
CMD ["waitress-serve", "--threads=8", "--host=127.0.0.1", "--port=8000", "main:app"]