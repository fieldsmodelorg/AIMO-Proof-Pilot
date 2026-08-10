# The SGLang runtime (`/opt/pp`)

The container build needs a prebuilt SGLang runtime at `/opt/pp` (patched SGLang +
PyTorch/CUDA + FlashAttention + kernels + a bundled CPython). It is **not** built
from a requirements file at image-build time — it's a frozen environment layer.

The Dockerfile pulls it from a base image named by the `RUNTIME_BASE_IMAGE` arg:

```dockerfile
ARG RUNTIME_BASE_IMAGE=ghcr.io/fieldsmodelorg/aimo-proof-pilot:sha-463682b
FROM ${RUNTIME_BASE_IMAGE} AS runtime
# ... final image ...
COPY --from=runtime /opt/pp /opt/pp
```

## Default: reuse the existing release image (nothing to build or publish)

`RUNTIME_BASE_IMAGE` defaults to the last published release image, which already
bakes `/opt/pp`. `COPY --from=runtime /opt/pp` lifts **only** that directory into
the fresh final image (whose own base is `nvidia/cuda:13.0.3-devel-ubuntu24.04`),
so no external dataset is fetched and nothing new is built or pushed.

The only requirement: the base image must stay **published and readable** at build
time — keep its GHCR package **public** (Package settings → visibility), or CI must
be logged in to GHCR (it already is).

## Pin by digest (recommended for a frozen artifact)

Tags can move; digests can't. Once logged in to GHCR, resolve the digest and pin it:

```bash
docker manifest inspect ghcr.io/fieldsmodelorg/aimo-proof-pilot:sha-463682b \
  | jq -r '.config.digest // .manifests[0].digest'      # or read it off the GHCR package page
```

Then set the arg to `ghcr.io/fieldsmodelorg/aimo-proof-pilot@sha256:<digest>`.
(`sha-463682b` is already a per-commit tag, so it is effectively immutable even as
a tag.)

## Building on top / modifying

The base only supplies `/opt/pp`. Everything else comes from **this repo**, copied
fresh into the final image at build. To modify:

- **harness / configs / prompts** — edit the repo, `docker build`. Your changes are
  `COPY .`-ed in; nothing else needed.
- **SGLang behavior** — edit `sglang_patches/` (the attention-sink + DFlash patches
  are applied on top at container **boot**), or `uv pip install` extra packages into
  `/opt/pp/venv` in a downstream layer.
- **the runtime wholesale** — rebuild `/opt/pp` from your own pinned SGLang tree and
  point `RUNTIME_BASE_IMAGE` at an image carrying it (see below).

## Optional: a dedicated runtime base image

If you'd rather not have the main image build `FROM` a prior release of itself, bake
a slim, purpose-named base once (a `COPY`-only build — no compilation, no GPU) and
point `RUNTIME_BASE_IMAGE` at it:

```bash
SRC=ghcr.io/fieldsmodelorg/aimo-proof-pilot:sha-463682b
DST=ghcr.io/fieldsmodelorg/proof-pilot-runtime:v1

docker build -t "$DST" -f - . <<EOF
FROM ${SRC} AS src
FROM nvidia/cuda:13.0.3-devel-ubuntu24.04
COPY --from=src /opt/pp /opt/pp
LABEL org.opencontainers.image.description="Prebuilt SGLang runtime (/opt/pp) for AIMO Proof Pilot"
EOF
docker push "$DST"
```

Keep the base OS identical to the final image's (`nvidia/cuda:13.0.3-devel-ubuntu24.04`).

## Bare-metal installs

`install/install_infervenv.sh` needs the runtime as a local archive: extract `/opt/pp`
from the base image and tar it, then pass it via `PP_ENV_ARCHIVE` (or set `HF_REPO` to
your own host of `proof-pilot-env.bin`). No default download source is configured.
