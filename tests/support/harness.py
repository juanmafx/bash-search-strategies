# Shared helpers that drive the CLI and shell modules through subprocess argv.
import os
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ENTRY_POINT = PROJECT_ROOT / "guessinggame.sh"
MODULES = (
    "core/validation.sh",
    "core/random.sh",
    "core/target.sh",
    "strategies/search.sh",
)
SOURCE_PREAMBLE = "".join(
    f'source "{PROJECT_ROOT}/src/guessinggame/{module}"\n' for module in MODULES
)


def clean_environment():
    environment = {key: value for key, value in os.environ.items() if key != "BASH_ENV"}
    environment["LC_ALL"] = "C"
    return environment


def run_cli(*arguments, stdin="", cwd=None, timeout=60, extra_environment=None):
    return subprocess.run(
        ["bash", str(ENTRY_POINT), *arguments],
        input=stdin,
        capture_output=True,
        text=True,
        cwd=cwd or PROJECT_ROOT,
        env={**clean_environment(), **(extra_environment or {})},
        timeout=timeout,
        check=False,
    )


def run_shell(script, *arguments, timeout=120):
    return subprocess.run(
        ["bash", "-c", "set -euo pipefail\n" + SOURCE_PREAMBLE + script, "harness", *arguments],
        capture_output=True,
        text=True,
        env=clean_environment(),
        timeout=timeout,
        check=False,
    )


def shell_integers(script, *arguments, timeout=120):
    completed = run_shell(script, *arguments, timeout=timeout)
    if completed.returncode != 0:
        raise AssertionError(completed.stderr)
    return [int(token) for token in completed.stdout.split()]


def parse_csv_rows(text):
    lines = text.strip().splitlines()
    header = lines[0].split(",")
    return [dict(zip(header, line.split(","), strict=True)) for line in lines[1:]]
