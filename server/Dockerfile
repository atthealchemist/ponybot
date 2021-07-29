FROM python:3.8-slim-buster

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PONYBOT_SERVER_VERSION alpha
ENV PONYBOT_SERVER_CONFIGURATION dev
ENV PONYBOT_SERVER_ROOT /ponybot/${PONYBOT_SERVER_VERSION}/server/${PONYBOT_SERVER_CONFIGURATION}

WORKDIR ${PONYBOT_SERVER_ROOT}

COPY ./env-dev ${PONYBOT_SERVER_ROOT}/.env
COPY . ${PONYBOT_SERVER_ROOT}

RUN pip -q install poetry
RUN poetry export -f requirements.txt -o requirements.txt
RUN pip -q install -r requirements.txt

RUN chmod +x ${PONYBOT_SERVER_ROOT}/entrypoint.sh
ENTRYPOINT [ "./entrypoint.sh" ]