# proof-pilot inference venv installer

Installs the full OPD-32B inference runtime (patched SGLang + everything it
needs) into a writable scratch dir on a node whose filesystem is immutable
except `/tmp`. This is **host-side tooling for running outside the container** —
it is not used by, or shipped in, the Docker image (see `.dockerignore`). If you
can run the image, use that instead; this exists for bare nodes.

## Quick start

```bash
# 1. the code (SGLang patches are read from this checkout)
git clone https://github.com/hav4ik/imo-inference /tmp/chankhavu/imo-inference
cd /tmp/chankhavu/imo-inference

# 2. the runtime  (chankhavu/proof-pilot-env is PUBLIC -> no token needed)
./install/install_infervenv.sh

# 3. use it -- in EVERY shell
source /tmp/chankhavu/venvs/infervenv/.runtime/activate-env.sh
python -c "import sglang; print(sglang.__version__)"
```

Takes ~10 min: 4.6 GiB download, ~11 GiB extract, a short PyPI step. Needs
~17 GiB free under `/tmp/chankhavu` while installing (~11 GiB after) — check
`df -h /tmp` first if `/tmp` is a small tmpfs.

Defaults assume `PP_BASE=/tmp/chankhavu`; override with `--venv` / `--repo` /
`PP_BASE` for any other layout.

## What it installs

The runtime is **not** built from a requirements file — it's a prebuilt,
relocatable venv published by Yi-Chia Chen (ycchen) as the Kaggle dataset
`threerabbits/proof-pilot-env`, mirrored to `chankhavu/proof-pilot-env` on HF.
This archive is byte-identical to the Kaggle original.

| | |
|---|---|
| sglang | `0.5.14.dev20260618+g343aeeef39` (nightly, patched in place) |
| torch | `2.11.0+cu130` |
| flashinfer | `0.6.12` |
| sglang_kernel | `0.4.4+cu130` |
| humming_kernels | `0.1.5` |
| python | `3.12.13` (bundled standalone CPython) |

Plus, from `evaluation/requirements.txt` via PyPI: `flash-attn-4[cu13]==4.0.0b15`
(pins *down* from the b18 in the archive), `nvidia-cutlass-dsl`, `quack-kernels`,
`httpx`, `pyyaml`.

Import names differ from the package names — `flash-attn-4` imports as
`flash_attn`, `quack-kernels` as `quack`, `nvidia-cutlass-dsl` as
`nvidia_cutlass_dsl`.

`humming` is **not** importable directly: `HUMMING_PATH` is an env var that the
W4A8 glue feeds to `sys.path.insert()` at load time. To poke at it manually:

```python
import sys, os
sys.path.insert(0, os.environ["HUMMING_PATH"])
import humming
```

**No CUDA toolkit is installed.** torch ships its own CUDA 13 libs inside
site-packages (`nvidia/cu13/`), and that is what the harness points at — your
node's system CUDA/nvcc is not used or touched.

## Layout

Everything lives under one path. `rm -rf` on it is a complete uninstall.

```
/tmp/chankhavu/venvs/infervenv/       <- THE VENV
├── bin/python                        <- the interpreter you run
├── lib/python3.12/site-packages/     <- sglang (patched), torch, ...
├── pyvenv.cfg                        home -> .runtime/pybase/bin
└── .runtime/
    ├── pybase/                       standalone CPython — supplies the STDLIB
    ├── humming/                      W4A8 kernels (HUMMING_PATH=.runtime)
    ├── proof-pilot/                  ycchen repo subset (w4a8 helper)
    ├── flashinfer_cache/             warm JIT cache (seed)
    ├── humming_cache/                warm JIT cache (seed)
    ├── uv                            bundled uv 0.11.19
    ├── activate-env.sh               <- GENERATED; source this
    └── caches/                       live writable caches + fake $HOME
```

## Three things that will bite you if you skip them

**1. Always `source activate-env.sh`.** This node's `$HOME` is read-only, and
several libraries default to writing under `~`:

| library | default | redirected to |
|---|---|---|
| triton | `~/.triton` | `.runtime/caches/triton` |
| sglang | `~/.cache/sglang` | `.runtime/caches/sglang` |
| flashinfer | `~/.cache/flashinfer` | `.runtime/caches/flashinfer_base` |
| torch inductor | `~/.cache/torch` | `.runtime/caches/torchinductor` |
| HF hub | `~/.cache/huggingface` | `.runtime/caches/hf` |

Without it you get opaque `Read-only file system` / `Permission denied` errors
deep inside a JIT compile. The script also repoints `$HOME` itself as a safety
net for anything not enumerated above.

**2. `LD_LIBRARY_PATH` includes `.runtime/pybase/lib`** — `activate-env.sh` does
this for you. The bundled CPython is a relocated standalone build, so its
`libpython3.12.so.1.0` isn't on the loader path and `import flashinfer.comm`
raises `ImportError` from inside `cuda.tile`'s C extension.

Scope, measured rather than assumed: sglang **guards** that import, so the only
symptom is a warning and a fallback —

```
flashinfer.comm allreduce_fusion API is not available
(libpython3.12.so.1.0: cannot open shared object file)
... falling back to standard implementation
```

`enable_flashinfer_allreduce_fusion` is **off by default** and this config never
turns it on, and the olmo2/Olmo3Sink target never references comm fusion. So this
is **cosmetic today** — not a throughput loss. Setting the path clears the warning
and keeps `--enable-flashinfer-allreduce-fusion` usable if you ever want it.
Anything that imports `flashinfer.comm` *directly* does hard-fail without it.

**3. The venv must stay writable at runtime.** `launch_server.py` writes a
symlink into site-packages (`nvidia/cu13/include/cccl`) and to `/tmp/pp_link`
on every launch. Don't try to make the install read-only.

## Iterating on patches

The SGLang patches are read from **your checkout**, so the loop is:

```bash
cd /tmp/chankhavu/imo-inference && git pull
./install/install_infervenv.sh --repatch     # seconds, no download
```

`--repatch` re-copies the five patched SGLang files and re-runs the marker-based
Python patchers. Everything is idempotent; originals are kept as `*.orig`.

The upstream `sglang_patches/apply_patches.sh` hardcodes
`/workspace/pp/proof-pilot/deploy/w4a8/humming_w4a8.py` for its two humming
patches. The installer rewrites that path to the relocated helper before running
it, so upstream needs no edit.

## Options

```
--repo PATH     checkout to take patches from   (default /tmp/chankhavu/imo-inference)
--venv PATH     install target                  (default /tmp/chankhavu/venvs/infervenv)
--repatch       reapply patches only, then exit
--skip-pip      skip the PyPI step
```

| env | meaning |
|---|---|
| `PP_ENV_ARCHIVE` | local `proof-pilot-env.bin`; skips the HF download entirely |
| `HF_TOKEN` | optional; the mirror is public (only needed for a private fork) |
| `PP_BASE` | root for scratch + defaults (default `/tmp/chankhavu`) |
| `KEEP_ARCHIVE=1` | keep the 4.6 GiB download after extracting |

## Why the relocation step exists

The shipped venv contains **only** `site-packages` — it is not self-contained.
Its `pyvenv.cfg` `home` points at the build host's
`/.uv/python_install/cpython-3.12.13-linux-x86_64-gnu/bin`, which exists
nowhere else. Until that line is rewritten to the bundled `pybase`, the
interpreter cannot find its stdlib and even `import os` dies:

```
Could not find platform independent libraries <prefix>
```

The installer rewrites it and then asserts `sys.base_prefix` resolves correctly
and that `import sglang, torch` both succeed, so a bad relocation fails loudly
at install time instead of at server start.

It also rewrites the console-script shebangs in `bin/`, which ship pointing at a
stale build path (`/workspace/sglang-nightly-py312-venv/bin/python3`). The
harness never uses them (it always calls `$VENV/bin/python -m ...`), but they'd
be broken if you invoked `sglang`/`flashinfer`/`hf` directly.

## Requirements

- ~17 GiB free under `/tmp/chankhavu` during install (~11 GiB after)
- `curl`, `tar`, `sed`, `awk`, `od`, `df`
- network to HF + PyPI
- H200s for an actual server run (the archive's kernels target sm90a)

## Known issues found while building this

Three fixes live on branch `fix/runtime-libpython-and-docker-nits` (not merged
here). This installer works with or without them — it detects whether
`apply_patches.sh` supports `$W4A8_HELPER` and rewrites a copy of the dir if not.

1. **`sglang_patches/apply_patches.sh` hardcodes**
   `/workspace/pp/proof-pilot/deploy/w4a8/humming_w4a8.py`, so it cannot patch a
   relocated runtime without being rewritten. The fix takes the helper as `$2` /
   `$W4A8_HELPER`, same default.
2. **`launch_server.py` never puts the bundled CPython's lib dir on
   `LD_LIBRARY_PATH`** (only the `model.quantized` branch set that variable at
   all, so bf16 runs got none). Cosmetic — see section 2 above.
3. **`Dockerfile`**: `image.source` points at the upstream repo, and
   `HEALTHCHECK` re-hardcodes `/workspace/pp/venv` + `/opt/aimo-...` despite
   `ENV VENV`/`REPO` being defined directly above it.

Still unverified: **no server has ever been launched from this install.** The
venv, patches, imports and the repo's 51 unit tests all pass, but the kernels
target sm90a, so first H200 bring-up is the real test. Most likely trip points
are the hardcoded `/usr/lib/x86_64-linux-gnu/libcuda.so.1` in `launch_server.py`
(Singularity `--nv` may inject it under `/.singularity.d/libs/` instead — the
installer warns at preflight) and the `/tmp/pp_link` symlink write.

## Runtime provenance

Not built from a requirements file. The venv is ycchen's prebuilt bundle, from
the public Kaggle dataset `threerabbits/proof-pilot-env` (built by
`kaggle/bundle/build_bundle.sh` in `github.com/ycchen-tw/proof-pilot-codes`),
which `docker/entrypoint.sh` downloads at container start. The HF copy is
byte-identical (4,644,784,760 bytes). Consequence: **the image is not
reproducible from the Dockerfile alone** — it depends on that external archive,
with no checksum or version pin.
