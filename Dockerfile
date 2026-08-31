FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg curl unzip git && rm -rf /var/lib/apt/lists/*

ENV DENO_INSTALL=/usr/local
RUN curl -fsSL https://deno.land/install.sh | sh
ENV PATH="/usr/local/bin:$PATH"

RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:/usr/local/bin:$PATH"

WORKDIR /home/user

RUN git clone --single-branch --branch 1.3.2 https://github.com/Brainicism/bgutil-ytdlp-pot-provider.git \
    && cd bgutil-ytdlp-pot-provider/server \
    && deno install --allow-scripts=npm:canvas --frozen

WORKDIR /home/user/app

RUN pip install --no-cache-dir --user uv

COPY --chown=user pyproject.toml uv.lock README.md ./
RUN uv sync --frozen --no-dev --no-install-project

COPY --chown=user src ./src
RUN uv sync --frozen --no-dev

EXPOSE 7860

CMD ["sh", "-c", "uv run uvicorn --app-dir src ytdlp_api.main:app --host 0.0.0.0 --port ${PORT:-7860}"]