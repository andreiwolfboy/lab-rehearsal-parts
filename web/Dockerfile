# The smallest application the platform will run for a developer: the standard library's
# HTTP server, as an unprivileged user. Replace app/ with yours; keep USER and the port.
FROM python:3.13-slim
WORKDIR /app
COPY app/ /app/
# Not root: the platform drops every capability anyway, and a process that needs root to
# start will not start (records/second-developer.md). /data is where its state lives.
USER 1000:1000
EXPOSE 8000
CMD ["python3", "-u", "server.py"]
