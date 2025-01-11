FROM --platform=linux/amd64 python:3.12.3-slim-bullseye as python3

FROM python3 as python-build-stage

ARG APP_HOME=/app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR ${APP_HOME}

RUN pip install --upgrade pip
RUN pip install poetry
COPY poetry.toml pyproject.toml README.md ./
RUN poetry install --without dev

COPY main.py alembic.ini pytest.ini ./
COPY alembic ./alembic
COPY src ./src

FROM python3 as python-run-stage

ARG APP_HOME=/app
ARG USER=fastapi

WORKDIR ${APP_HOME}

# For Mac Specific Error
# RUN echo "Acquire::http::Pipeline-Depth 0;" > /etc/apt/apt.conf.d/99custom && \
#     echo "Acquire::http::No-Cache true;" >> /etc/apt/apt.conf.d/99custom && \
#     echo "Acquire::BrokenProxy    true;" >> /etc/apt/apt.conf.d/99custom

RUN apt-get update && apt-get install --no-install-recommends -y \
    libpq-dev \
    gettext && \
    apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false && \
    rm -rf /var/lib/apt/lists/*

RUN addgroup --system ${USER} && \
    adduser --system --ingroup ${USER} ${USER}

COPY --chown=${USER}:${USER} ./deploy/scripts/start /start
COPY --chown=${USER}:${USER} ./deploy/scripts/unittest/ /unittest
COPY --chown=${USER}:${USER} ./deploy/scripts/celery/ /celery

RUN sed -i 's/\r$//g' /start /celery /unittest && \
    chmod +x /start /celery /unittest && \
    chown ${USER}:${USER} ${APP_HOME}

USER ${USER}

COPY --from=python-build-stage /usr/local/lib/python3.12 /usr/local/lib/python3.12
COPY --from=python-build-stage --chown=${USER}:${USER} ${APP_HOME} ${APP_HOME}

ENV PATH="/${APP_HOME}/.venv/bin:$PATH"

ENTRYPOINT ["/bin/bash"]
