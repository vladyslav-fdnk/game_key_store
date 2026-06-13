FROM python:3.12-alpine
WORKDIR /app
RUN apk add --no-cache gcc musl-dev postgresql-dev libffi-dev
RUN pip install --no-cache-dir uv
COPY pyproject.toml ./
RUN uv pip install --system --no-cache -r pyproject.toml
COPY . .
EXPOSE 8000
