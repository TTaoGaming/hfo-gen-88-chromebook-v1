# Multi-stage build for Shodh-Memory (patched for repos without Cargo.lock)
FROM rust:1.88-slim-bookworm AS builder

RUN apt-get update && apt-get install -y \
    pkg-config \
    libssl-dev \
    clang \
    llvm-dev \
    libclang-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY Cargo.toml ./
COPY benches ./benches
COPY src ./src

RUN cargo build --release

FROM debian:bookworm-slim

RUN apt-get update && apt-get install -y \
    ca-certificates \
    libssl3 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Shodh uses the `ort` crate which dynamically loads ONNX Runtime.
# Without this library present, the server can panic at startup.
ARG ORT_VERSION=1.23.0
RUN curl -fsSL -o /tmp/onnxruntime.tgz \
    "https://github.com/microsoft/onnxruntime/releases/download/v${ORT_VERSION}/onnxruntime-linux-x64-${ORT_VERSION}.tgz" \
    && tar -xzf /tmp/onnxruntime.tgz -C /tmp \
    && cp -a "/tmp/onnxruntime-linux-x64-${ORT_VERSION}/lib/libonnxruntime.so"* /usr/local/lib/ \
    && ldconfig \
    && rm -rf /tmp/onnxruntime.tgz "/tmp/onnxruntime-linux-x64-${ORT_VERSION}"

RUN useradd -m -u 1000 shodh && \
    mkdir -p /data && \
    chown -R shodh:shodh /data

COPY --from=builder /app/target/release/shodh-memory-server /usr/local/bin/shodh-memory-server

USER shodh
WORKDIR /data

EXPOSE 3030

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:3030/health || exit 1

ENV RUST_LOG=info \
    SHODH_HOST=0.0.0.0 \
    SHODH_PORT=3030 \
    SHODH_MEMORY_PATH=/data

CMD ["shodh-memory-server"]
