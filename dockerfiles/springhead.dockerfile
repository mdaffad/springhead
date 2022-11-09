FROM python:3.9-slim AS base

# Env variables
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    PATH="/opt/venv/bin:$PATH"

FROM base as builder

WORKDIR /app/

# Install gcc and make virtualenv
RUN python -m venv /opt/venv

COPY ./requirements ./requirements/

# Allow installing dev dependencies to run tests
ARG INSTALL_DEV=false
RUN bash -c "if [ $INSTALL_DEV == 'true' ] ;\
    then pip install -r requirements/requirements.dev.txt ;\
    else pip install -r requirements/requirements.txt ;\
    fi"

FROM base AS runner

RUN apt-get update && apt-get -y --no-install-recommends install dumb-init

COPY --from=builder /opt/venv /opt/venv

WORKDIR /app/

COPY app ./app
COPY springhead ./springhead
COPY scripts ./scripts

ENV PYTHONPATH=/app

RUN python -m nltk.downloader stopwords && \
    python -m nltk.downloader punkt && \
    python -m nltk.downloader wordnet && \
    python -m nltk.downloader omw-1.4

CMD [ "--", "sh", "./scripts/start.sh" ]
ENTRYPOINT ["dumb-init"]

