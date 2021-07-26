# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8-slim-buster

EXPOSE 8000

# Defining variables
ENV PONYBOT_BOT_SERVICE_NAME=bot
ENV PONYBOT_BOT_SERVICE_ENVIRONMENT=dev
ENV PONYBOT_BOT_SERVICE_ROOT=/ponybot/${PONYBOT_BOT_SERVICE_NAME}/${PONYBOT_BOT_SERVICE_ENVIRONMENT}/

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Switching to service root directory
WORKDIR ${PONYBOT_BOT_SERVICE_ROOT}

## Install poetry
RUN pip install --upgrade pip && pip --no-cache-dir install poetry

# Copying env file
COPY .env-${PONYBOT_BOT_SERVICE_ENVIRONMENT} ${PONYBOT_BOT_SERVICE_ROOT}/.env
# Copying service sources
COPY . ${PONYBOT_BOT_SERVICE_ROOT}

# Setting rights to execute scripts in scripts folder
RUN chmod +x -R ${PONYBOT_BOT_SERVICE_ROOT}/scripts/

# Install server requirements
RUN poetry install



# Creates a non-root user with an explicit UID and adds permission to access the /app folder
RUN adduser -u 5678 --disabled-password --gecos "" bot_user
USER bot_user

# Switching to poetry venv
# RUN ./scripts/docker-poetry-activate.sh

ENTRYPOINT "./scripts/docker-entrypoint.sh"