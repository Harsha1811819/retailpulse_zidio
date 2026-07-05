# ============================================================
# STAGE 1 — BUILD DEPENDENCIES
# ============================================================

FROM python:3.11-slim AS builder

WORKDIR /build

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt

# ============================================================
# STAGE 2 — RUNTIME
# ============================================================

FROM python:3.11-slim

WORKDIR /app

# Install curl in the runtime stage for the healthcheck
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -u 1000 appuser

COPY --from=builder /wheels /wheels

COPY requirements.txt .

RUN pip install --no-cache-dir /wheels/* && rm -rf /wheels

# Copy application directories (matching our workspace structure)
COPY app/ ./app/
COPY Data/ ./Data/
COPY models/ ./models/

# ============================================================
# SECURITY
# ============================================================

USER appuser

# ============================================================
# PORT
# ============================================================

EXPOSE 8501

# ============================================================
# HEALTHCHECK
# ============================================================

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# ============================================================
# START APP
# ============================================================

CMD [ \
    "streamlit", \
    "run", \
    "app/main.py", \
    "--server.port=8501", \
    "--server.address=0.0.0.0" \
]