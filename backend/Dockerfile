FROM python:3.13.1-alpine3.21 AS requirements-stage

WORKDIR /tmp

# Install Poetry
RUN pip3 install poetry poetry-plugin-export

# Copy poetry files
COPY backend/pyproject.toml /tmp
COPY backend/poetry.lock /tmp

# Export poetry packages to requirements.txt, to be installed
RUN poetry export --without-hashes --with core -f requirements.txt --output requirements.txt

FROM python:3.13.1-alpine3.21

RUN apk update && apk add --no-cache \
    build-base \
    g++ \
    gcc \
    musl-dev \
    linux-headers \
    python3-dev \
    libffi-dev \
    openssl-dev \
    cargo \
    rust

RUN pip3 install --upgrade pip

# # set environment variables
# # Prevents Python from writing pyc files to disc (equivalent to python -B option)
ENV PYTHONDONTWRITEBYTECODE=1

# # Prevents Python from buffering stdout and stderr (equivalent to python -u option)
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copy requirements from previous stage to docker container in /app 
COPY --from=requirements-stage /tmp/requirements.txt /app/requirements.txt

# Install the dependencies
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# # Copy everything from ./api directory to /app in the container
COPY backend/src/ /app/src

# # Expose the port 5000 on which our application runs
EXPOSE 5000

CMD ["python", "-m", "uvicorn", \
    "src.api:app", \
    "--host", \
    "0.0.0.0", \
    "--port", \
    "5000"]
