FROM python:3.13

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root --no-cache

COPY . .

EXPOSE 8084

CMD ["poetry", "run", "python", "src/user_service/main.py"]
