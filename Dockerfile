FROM python:3-slim as poetry

ENV POETRY_HOME=/opt/poetry
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV PATH="$POETRY_HOME/bin:$PATH"
WORKDIR /app

# Install Poetry
RUN python -c 'from urllib.request import urlopen; print(urlopen("https://install.python-poetry.org").read().decode())' | python -

# Copy pyproject.toml
COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock

# Install packages
RUN pip3 install --upgrade pip
RUN poetry install --only main --no-interaction --no-ansi --no-root -vvv

# Install sigma-cli
COPY ./ ./
RUN rm -r .github/ .git/
RUN poetry install --only main --no-interaction --no-ansi -vvv

# Copy Artifacts to clean image
FROM python:3.11-alpine as runtime

WORKDIR /app
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH "${PYTHONPATH}:/app:/app/.venv/lib/python3.11/site-packages/"

# Copy sigma-cli over
COPY --from=poetry /app /app

ENTRYPOINT ["sigma"]
CMD ["--help"]