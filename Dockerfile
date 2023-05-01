FROM python:3.11
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir poetry
RUN poetry config virtualenvs.create false && poetry install --only main --no-interaction --no-ansi
CMD ["python", "scraper.py"]