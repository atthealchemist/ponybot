FROM ponybot-alpha_server:latest
RUN poetry export -f requirements.txt -o requirements.txt
RUN pip -q install -r requirements.txt
ENTRYPOINT [ "./entrypoint.sh" ]