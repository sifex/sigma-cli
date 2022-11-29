FROM python:3-slim as python
ENV PYTHONUNBUFFERED=true
WORKDIR /app


FROM python as poetry
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV PATH="$POETRY_HOME/bin:$PATH"
RUN python -c 'from urllib.request import urlopen; print(urlopen("https://install.python-poetry.org").read().decode())' | python -

# Copy pyproject.toml
COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock

# Install packages
RUN pip3 install --upgrade pip
RUN poetry install --only main --no-interaction --no-ansi --no-root -vvv

COPY ./ ./

RUN poetry install --only main --no-interaction --no-ansi -vvv


FROM python:alpine as runtime
WORKDIR /app
ENV PATH="/app/.venv/bin:$PATH"
COPY --from=poetry /app /app
ENTRYPOINT ["sigma"]
CMD ["--help"]