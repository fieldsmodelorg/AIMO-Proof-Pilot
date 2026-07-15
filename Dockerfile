# syntax=docker/dockerfile:1.7

FROM ghcr.io/astral-sh/uv:0.11.19 AS uv

FROM nvidia/cuda:13.0.3-devel-ubuntu24.04

ARG DEBIAN_FRONTEND=noninteractive
ARG VCS_REF=unknown

LABEL org.opencontainers.image.source="https://github.com/bogoconic1/aimo-proof-pilot-inference"
LABEL org.opencontainers.image.revision="$VCS_REF"
LABEL org.opencontainers.image.title="AIMO Proof Pilot Inference"
LABEL org.opencontainers.image.description="OPD-32B generate-verify-refine inference for 8x H200"

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        bash \
        ca-certificates \
        curl \
        git \
        git-lfs \
        jq \
        libaio1t64 \
        libgl1 \
        libglib2.0-0 \
        libgomp1 \
        libibverbs1 \
        libnuma1 \
        numactl \
        pciutils \
        procps \
        python3 \
        python3-venv \
        rsync \
        tar \
        tini \
        unzip \
    && rm -rf /var/lib/apt/lists/*

COPY --from=uv /uv /uvx /usr/local/bin/

ENV UV_LINK_MODE=copy \
    UV_TOOL_BIN_DIR=/usr/local/bin \
    HF_HOME=/workspace/.hf_home \
    HF_XET_HIGH_PERFORMANCE=0 \
    NVIDIA_VISIBLE_DEVICES=all \
    NVIDIA_DRIVER_CAPABILITIES=compute,utility \
    CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7 \
    REPO=/opt/aimo-proof-pilot-inference \
    VENV=/workspace/pp/venv \
    IMAGE_REVISION=$VCS_REF

RUN uv tool install --python /usr/bin/python3 "kaggle==2.2.3" \
    && uv tool install --python /usr/bin/python3 "huggingface-hub==1.18.0"

WORKDIR /opt/aimo-proof-pilot-inference
COPY . /opt/aimo-proof-pilot-inference

RUN chmod 0755 docker/entrypoint.sh run_submission.sh

VOLUME ["/workspace"]
STOPSIGNAL SIGTERM

HEALTHCHECK --start-period=45m --interval=30s --timeout=10s --retries=5 \
    CMD test -n "$CONFIG" \
        && test -f /workspace/.proof-pilot/server-ready \
        && URL=$(/workspace/pp/venv/bin/python \
            /opt/aimo-proof-pilot-inference/docker/inspect_config.py "$CONFIG" \
            | jq -er .server_url) \
        && curl -fsS "$URL/health" >/dev/null \
        || exit 1

ENTRYPOINT ["/usr/bin/tini", "--", "/opt/aimo-proof-pilot-inference/docker/entrypoint.sh"]
CMD ["serve"]
