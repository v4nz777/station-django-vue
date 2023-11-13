FROM python:3.10

ENV PYTHONUNBUFFERED 1


WORKDIR /backend

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt


COPY . .

CMD [ "daphne", "-e", "ssl:8443:privateKey=server.key:certKey=server.crt", "backend.asgi:application" ]
