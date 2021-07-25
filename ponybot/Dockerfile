# Defining variables
ARG PONYBOT_ROOT=/ponybot/app
ARG PONYBOT_ENVIRONMENT=dev

# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8-slim-buster

EXPOSE 8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

COPY .env-${PONYBOT_ENVIRONMENT} ./ponybot/app/.env
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
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN ls -la .
RUN adduser -u 5678 --disabled-password --gecos "" appuser
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
# File wsgi.py was not found in subfolder: 'workspace'. Please enter the Python path to wsgi file.
CMD ["gunicorn", "--workers=4", "-b", "0.0.0.0:8000", "-k", "uvicorn.workers.UvicornWorker", "ponybot.wsgi"]
