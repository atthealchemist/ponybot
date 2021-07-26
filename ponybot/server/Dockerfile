# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8-slim-buster

EXPOSE 8000

# Defining variables
ENV PONYBOT_ENVIRONMENT=dev
ENV PONYBOT_ROOT=/ponybot/${PONYBOT_ENVIRONMENT}/app
ENV PONYBOT_SERVER_WORKERS_COUNT=4

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

COPY .env-${PONYBOT_ENVIRONMENT} ${PONYBOT_ROOT}/.env
## Install pip requirements
COPY requirements ./requirements
# Install server requirements
RUN python -m pip install -r requirements/server.txt
# Install base application requirements
RUN python -m pip install -r requirements/base.txt
# Install testing requirements
RUN python -m pip install -r requirements/testing.txt

WORKDIR ${PONYBOT_ROOT}
COPY . ${PONYBOT_ROOT}

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
RUN adduser -u 5678 --disabled-password --gecos "" appuser
USER appuser

CMD ["./docker-entrypoint.sh"]