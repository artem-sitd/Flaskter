FROM python:3.12

WORKDIR /flaskter

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="/root/.local/bin:$PATH"

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-dev

COPY . .

CMD ["poetry", "run", "gunicorn", "--bind", "0.0.0.0:5000", "run:app"]
