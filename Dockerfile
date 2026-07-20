# syntax=docker/dockerfile:1.7

FROM ghcr.io/astral-sh/uv:0.11.19 AS uv

# ---------------------------------------------------------------------------
# Stage: bake the pinned SGLang runtime venv into an image layer.
# The runtime (patched-SGLang venv + kernels) is downloaded, sha256-verified,
# extracted, relocated, and topped with the pinned PyPI deps ONCE, at build
# time -- so the final image is self-contained: no runtime download, no
# HF_TOKEN for the runtime, no per-boot pip install. Only the (public) model
# weights are fetched at boot.
#
# Source is the revision-pinned HF mirror; pass an HF token as a build secret
# (`--secret id=hf_token,env=HF_TOKEN`) if the mirror is private, or make the
# mirror public and no secret is needed. The sha256 pin freezes the content.
# ---------------------------------------------------------------------------
FROM nvidia/cuda:13.0.3-devel-ubuntu24.04 AS runtime
ARG DEBIAN_FRONTEND=noninteractive
ARG RUNTIME_HF_REPO=chankhavu/proof-pilot-env
ARG RUNTIME_HF_REVISION=5c0bf00bcc38c91b336f99d68aaab6b66aa93c1d
ARG RUNTIME_ARCHIVE_SHA256=71190f4f2554c29ec6b99ae6bda7af64f1348876b85cfbdfa1d102f9dfa8c831

RUN apt-get update \
    && apt-get install -y --no-install-recommends bash ca-certificates curl tar \
    && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
COPY --from=uv /uv /usr/local/bin/uv
COPY evaluation/requirements.txt /tmp/requirements.txt

RUN --mount=type=secret,id=hf_token \
    set -Eeuo pipefail; \
    token="$(cat /run/secrets/hf_token 2>/dev/null || true)"; \
    url="https://huggingface.co/datasets/${RUNTIME_HF_REPO}/resolve/${RUNTIME_HF_REVISION}/proof-pilot-env.bin"; \
    echo "downloading pinned runtime ${RUNTIME_HF_REPO}@${RUNTIME_HF_REVISION}"; \
    curl -fL ${token:+-H "Authorization: Bearer ${token}"} "$url" -o /tmp/pp.bin; \
    echo "${RUNTIME_ARCHIVE_SHA256}  /tmp/pp.bin" | sha256sum -c -; \
    mkdir -p /opt/pp; \
    tar -xzf /tmp/pp.bin -C /opt/pp --strip-components=1; \
    rm -f /tmp/pp.bin; \
    test -x /opt/pp/venv/bin/python; \
    test -x /opt/pp/pybase/bin/python3; \
    sed -i 's|^home = .*|home = /opt/pp/pybase/bin|' /opt/pp/venv/pyvenv.cfg; \
    UV_LINK_MODE=copy /usr/local/bin/uv pip install \
        --python /opt/pp/venv/bin/python -r /tmp/requirements.txt; \
    touch "/opt/pp/.proof-pilot-deps-$(sha256sum /tmp/requirements.txt | awk '{print $1}')"; \
    LD_LIBRARY_PATH=/opt/pp/pybase/lib /opt/pp/venv/bin/python -c \
        "import sglang, torch, flash_attn; print('baked runtime:', sglang.__version__, torch.__version__)"

# ---------------------------------------------------------------------------
# Final image
# ---------------------------------------------------------------------------
FROM nvidia/cuda:13.0.3-devel-ubuntu24.04

ARG DEBIAN_FRONTEND=noninteractive
ARG VCS_REF=unknown

LABEL org.opencontainers.image.source="https://github.com/hav4ik/imo-inference"
LABEL org.opencontainers.image.revision="$VCS_REF"
LABEL org.opencontainers.image.title="AIMO Proof Pilot Inference"
LABEL org.opencontainers.image.description="OPD-32B generate-verify-refine inference; SGLang runtime baked in"

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
    REPO=/opt/aimo-proof-pilot-inference \
    RUNTIME_ROOT=/opt/pp \
    VENV=/opt/pp/venv \
    IMAGE_REVISION=$VCS_REF

RUN uv tool install --python /usr/bin/python3 "huggingface-hub==1.18.0"

# The pinned, relocated, deps-complete SGLang runtime (a non-/workspace path so
# a runtime -v mount over /workspace never hides it).
COPY --from=runtime /opt/pp /opt/pp

WORKDIR /opt/aimo-proof-pilot-inference
COPY . /opt/aimo-proof-pilot-inference

RUN chmod 0755 docker/entrypoint.sh run_submission.sh

VOLUME ["/workspace"]
STOPSIGNAL SIGTERM

HEALTHCHECK --start-period=45m --interval=30s --timeout=10s --retries=5 \
    CMD test -n "$CONFIG" \
        && test -f /workspace/.proof-pilot/server-ready \
        && URL=$("$VENV/bin/python" \
            "$REPO/docker/inspect_config.py" "$CONFIG" \
            | jq -er .server_url) \
        && curl -fsS "$URL/health" >/dev/null \
        || exit 1

ENTRYPOINT ["/usr/bin/tini", "--", "/opt/aimo-proof-pilot-inference/docker/entrypoint.sh"]
CMD ["serve"]
