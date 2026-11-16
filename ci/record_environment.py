"""Record reproducibility metadata without collecting secret environment values."""

import argparse
import importlib.metadata
import json
import os
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=["before-install", "after-checks"], required=True)
    args = parser.parse_args()
    revision = subprocess.run(
        ["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=True
    ).stdout.strip()
    record = {
        "recorded_at": datetime.now(timezone.utc).isoformat(),
        "phase": args.phase,
        "checked_out_sha": revision,
        "python": sys.version,
        "python_executable": sys.executable,
        "platform": platform.platform(),
        "runner_image": {
            key: os.environ.get(key) for key in ("ImageOS", "ImageVersion", "RUNNER_OS")
        },
        "github": {
            key: os.environ.get(key)
            for key in ("GITHUB_RUN_ID", "GITHUB_RUN_ATTEMPT", "GITHUB_JOB", "GITHUB_SHA", "GITHUB_EVENT_NAME")
        },
        "environment_presence": {"INVOICE_CURRENCY": bool(os.environ.get("INVOICE_CURRENCY"))},
        "packages": dict(
            sorted((package.metadata["Name"], package.version) for package in importlib.metadata.distributions())
        ),
    }
    destination = Path("artifacts") / f"environment-{args.phase}.json"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(f"Recorded {args.phase} environment for {revision}")


if __name__ == "__main__":
    main()
