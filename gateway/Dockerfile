FROM python:3.11

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root --no-cache

COPY . .

EXPOSE 8083

CMD ["poetry", "run", "python", "src/gateway/main.py"]
