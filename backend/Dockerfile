FROM python:3.10

ENV PYTHONUNBUFFERED 1
# RUN apt-get update && apt-get install -y python-dev-is-python3 libffi-dev gcc libc-dev

WORKDIR /backend

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]