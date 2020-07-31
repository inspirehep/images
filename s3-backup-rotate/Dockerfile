FROM python:3.8-slim

WORKDIR /usr/src/app

RUN pip install --no-cache-dir poetry

COPY pyproject.toml .
COPY poetry.lock .
COPY s3-backup-rotate.py .

RUN poetry install

CMD [ "poetry", "run", "python", "s3-backup-rotate.py" ]
