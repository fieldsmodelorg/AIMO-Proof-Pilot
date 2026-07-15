#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "evaluation" / "harness"))

from eval_config import active_model, load_config  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Inspect an authoritative runtime configuration without modifying it."
        )
    )
    parser.add_argument("config", type=Path)
    args = parser.parse_args()

    config = load_config(args.config)
    model = active_model(config)
    server = config["server"]
    client_host = server["host"]
    if client_host in {"0.0.0.0", "::", "[::]"}:
        client_host = "127.0.0.1"
    if ":" in client_host and not client_host.startswith("["):
        client_host = f"[{client_host}]"
    server_url = "http://{}:{}".format(client_host, server["port"])
    print(
        json.dumps(
            {
                "server_host": server["host"],
                "server_port": server["port"],
                "server_url": server_url,
                "expected_gpu_count": (
                    model.tensor_parallel_size * model.data_parallel_size
                ),
                "target_model": str(model.target),
                "draft_model": str(model.draft) if model.draft else None,
            }
        )
    )


if __name__ == "__main__":
    main()
