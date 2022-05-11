FROM python:3.7 AS build

WORKDIR /app/

# Install Poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.in-project true

# Copy poetry.lock* in case it doesn't exist in the repo
COPY ./pyproject.toml ./poetry.lock* /app/

# Allow installing dev dependencies to run tests
ARG INSTALL_DEV=false
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install --no-root ; else poetry install --no-root --no-dev ; fi"

COPY ./app /app
WORKDIR /app

ENV PYTHONPATH=/app

# Copy all necessary files from the first stage image
FROM python:3.7-slim
WORKDIR /app
COPY --from=build /app/.venv /opt/venv
COPY --from=build /app /app
ENV PATH="/opt/venv/bin:$PATH"
