FROM python:3.11

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root --no-cache

COPY . .

EXPOSE 8085

CMD ["poetry", "run", "python", "src/video_service/main.py"]
