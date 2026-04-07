# GNOSIS application image — Python 3.11, non-root, import healthcheck.
# Long-running HTTP API is not wired yet; CMD keeps the container alive for compose + exec workflows.

FROM python:3.11-slim-bookworm AS runtime

RUN useradd --create-home --uid 1000 gnosis

WORKDIR /app

COPY pyproject.toml README.md ./
COPY src ./src

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir .

USER gnosis

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD python -c "import gnosis; raise SystemExit(0)"

# Placeholder until an ASGI server is added; keeps the service up for `docker compose` parity.
CMD ["sh", "-c", "exec tail -f /dev/null"]
