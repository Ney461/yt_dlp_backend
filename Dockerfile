FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg && rm -rf /var/lib/apt/lists/*

RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

WORKDIR /home/user/app

RUN pip install --no-cache-dir --user uv

COPY --chown=user pyproject.toml uv.lock README.md ./
RUN uv sync --frozen --no-dev --no-install-project

COPY --chown=user src ./src
RUN uv sync --frozen --no-dev

EXPOSE 7860

CMD ["sh", "-c", "uv run uvicorn --app-dir src ytdlp_api.main:app --host 0.0.0.0 --port ${PORT:-7860}"]