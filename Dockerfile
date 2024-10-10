FROM python:3.12-alpine AS build
WORKDIR /app

RUN python3 -mvenv ./.venv
COPY requirements.txt .ruff.toml ./

FROM build AS dev
WORKDIR /app

RUN ./.venv/bin/pip install -r requirements.txt

COPY . .

EXPOSE 5000

# werkzeug dev server
CMD ["./.venv/bin/python3", "./run.py"]

# gunicorn prod server for use behind nginx
# CMD ["./.venv/bin/gunicorn", "--config", "gunicorn.conf.py"]
