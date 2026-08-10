# Publishing the SGLang runtime base image

The container build inherits its frozen SGLang runtime (`/opt/pp`) from a base
image, `RUNTIME_BASE_IMAGE` in the `Dockerfile`:

```dockerfile
ARG RUNTIME_BASE_IMAGE=ghcr.io/fieldsmodelorg/proof-pilot-runtime:v1
FROM ${RUNTIME_BASE_IMAGE} AS runtime
```

This keeps the build's only heavy dependency a **container registry** (org-owned,
digest-pinnable) instead of an external dataset. You publish that base image
**once**. It is a repackage of bytes you already ship — **no rebuild, no GPU, no
HF token**.

## What `/opt/pp` is

A prebuilt, relocatable SGLang runtime: `venv/` (patched SGLang + PyTorch/CUDA +
FlashAttention + flashinfer + kernels, site-packages only), `pybase/` (bundled
standalone CPython 3.12), `humming/` + `proof-pilot/` (W4A8), warm JIT caches,
`uv/`. ~11 GiB extracted. It is **unpatched** — the attention-sink + DFlash
patches in `sglang_patches/` are applied on top at container boot, so the base
stays modifiable.

## One-time publish (from the existing release image)

The last published release image already contains a ready `/opt/pp`. Extract it
into a slim, purpose-named base and push. This is a trivial `COPY`-only build (no
compilation, no GPU):

```bash
SRC=ghcr.io/fieldsmodelorg/aimo-proof-pilot:sha-29c2ec5     # any release with a good /opt/pp
DST=ghcr.io/fieldsmodelorg/proof-pilot-runtime:v1

docker build -t "$DST" -f - . <<EOF
FROM ${SRC} AS src
FROM nvidia/cuda:13.0.3-devel-ubuntu24.04
COPY --from=src /opt/pp /opt/pp
LABEL org.opencontainers.image.description="Prebuilt SGLang runtime (/opt/pp) for AIMO Proof Pilot"
EOF

docker push "$DST"
```

> Base OS must match what the main image expects for `/opt/pp` — keep it
> `nvidia/cuda:13.0.3-devel-ubuntu24.04` (same as the final image).

### Alternative (no new image): point straight at the release image

If you'd rather not publish a dedicated base, set `RUNTIME_BASE_IMAGE` to the
release image itself — `/opt/pp` is already inside it:

```bash
docker build --build-arg RUNTIME_BASE_IMAGE=ghcr.io/fieldsmodelorg/aimo-proof-pilot@sha256:<digest> ...
```

Slim dedicated base is cleaner to present; the release-image route needs zero new
publishing. Either works.

## Pin it by digest (for reproducibility)

Tags move; digests don't. After pushing, resolve the digest and pin it:

```bash
docker inspect --format='{{index .RepoDigests 0}}' ghcr.io/fieldsmodelorg/proof-pilot-runtime:v1
# -> ghcr.io/fieldsmodelorg/proof-pilot-runtime@sha256:XXXX...
```

Then set that as the `Dockerfile` default:

```dockerfile
ARG RUNTIME_BASE_IMAGE=ghcr.io/fieldsmodelorg/proof-pilot-runtime@sha256:XXXX...
```

Make the GHCR package **public** (Package settings → Change visibility) so
`docker build` needs no login.

## Build the final image

```bash
docker build -t ghcr.io/fieldsmodelorg/aimo-proof-pilot:<tag> .
```

A plain `docker build` (no GPU) validates this stage end-to-end — the runtime
stage only pulls the base, re-asserts `evaluation/requirements.txt`, and runs an
`import sglang, torch, flash_attn` check.

## Rebuilding the runtime from scratch (optional)

The `/opt/pp` bytes are a frozen build of a nightly SGLang fork + the in-repo
patches + `evaluation/requirements.txt`. There is no tagged upstream release to
pin, which is why it ships prebuilt; the base image + its digest are the
reproducibility anchor. To modify the runtime itself, edit `sglang_patches/`
(applied at boot — the common case) or rebuild the base from your own pinned
SGLang tree and re-publish it here.
