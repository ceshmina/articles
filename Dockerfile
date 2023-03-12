FROM python:3.11

RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH "/root/.local/bin:$PATH"

WORKDIR /articles
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.in-project true \
    && poetry install
