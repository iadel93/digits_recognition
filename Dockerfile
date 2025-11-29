FROM python:3.13

WORKDIR /usr/local/app

COPY src ./src

COPY models ./models

COPY pyproject.toml .
COPY poetry.lock .
COPY README.md .

RUN pip install poetry
RUN poetry lock
RUN poetry install

EXPOSE 8000 8501