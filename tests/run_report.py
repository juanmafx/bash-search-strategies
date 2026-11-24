# Runs the suite and writes JSON and Markdown reports from the observed results.
import hashlib
import json
import platform
import subprocess
import sys
import time
import unittest
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
REPORT_DIRECTORY = PROJECT_ROOT / "reports" / "tests"
DIGEST_ROOTS = ("src", "tests", "tools", "db")
DIGEST_FILES = ("guessinggame.sh", "makefile", "VERSION")


class RecordingResult(unittest.TextTestResult):
    def __init__(self, *arguments, **keywords):
        super().__init__(*arguments, **keywords)
        self.records = []
        self.started = 0.0

    def startTest(self, test):
        self.started = time.perf_counter()
        super().startTest(test)

    def record(self, test, outcome):
        elapsed = round(time.perf_counter() - self.started, 4)
        self.records.append({"test": test.id(), "outcome": outcome, "seconds": elapsed})

    def addSuccess(self, test):
        super().addSuccess(test)
        self.record(test, "passed")

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.record(test, "failed")

    def addError(self, test, err):
        super().addError(test, err)
        self.record(test, "error")

    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        self.record(test, "skipped")

    def addSubTest(self, test, subtest, err):
        super().addSubTest(test, subtest, err)
        if err is not None:
            failed = issubclass(err[0], test.failureException)
            self.record(subtest, "failed" if failed else "error")


def source_digest():
    paths = [PROJECT_ROOT / name for name in DIGEST_FILES]
    for root in DIGEST_ROOTS:
        paths.extend(path for path in (PROJECT_ROOT / root).rglob("*") if path.is_file())
    digest = hashlib.sha256()
    for path in sorted(p for p in paths if "__pycache__" not in p.parts):
        digest.update(path.relative_to(PROJECT_ROOT).as_posix().encode())
        digest.update(path.read_bytes())
    return digest.hexdigest()


def tool_version(command):
    completed = subprocess.run(command, capture_output=True, text=True, check=False)
    lines = completed.stdout.splitlines()
    return lines[0] if lines else "unavailable"


def write_reports(result, duration):
    counts = {name: 0 for name in ("passed", "failed", "error", "skipped")}
    for record in result.records:
        counts[record["outcome"]] += 1
    report = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "command": "make report",
        "source_sha256": source_digest(),
        "environment": {
            "python": platform.python_version(),
            "bash": tool_version(["bash", "--version"]),
            "platform": platform.system(),
        },
        "tests_run": result.testsRun,
        "counts": counts,
        "duration_seconds": round(duration, 2),
        "successful": result.wasSuccessful(),
        "results": sorted(result.records, key=lambda record: record["test"]),
    }
    REPORT_DIRECTORY.mkdir(parents=True, exist_ok=True)
    (REPORT_DIRECTORY / "test-report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# Test Report",
        "",
        f"- Generated: {report['generated_at']}",
        f"- Command: `{report['command']}`",
        f"- Source SHA-256: `{report['source_sha256']}`",
        f"- Python: {report['environment']['python']}",
        f"- Bash: {report['environment']['bash']}",
        f"- Platform: {report['environment']['platform']}",
        f"- Tests run: {report['tests_run']}",
        f"- Passed: {counts['passed']}, failed: {counts['failed']}, errors: {counts['error']}, skipped: {counts['skipped']}",
        f"- Duration: {report['duration_seconds']} s",
        "",
        "| Test | Outcome | Seconds |",
        "| --- | --- | ---: |",
    ]
    lines.extend(f"| `{r['test']}` | {r['outcome']} | {r['seconds']} |" for r in report["results"])
    (REPORT_DIRECTORY / "test-report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    suite = unittest.defaultTestLoader.discover(
        str(PROJECT_ROOT / "tests"), top_level_dir=str(PROJECT_ROOT)
    )
    runner = unittest.TextTestRunner(resultclass=RecordingResult, verbosity=1)
    started = time.perf_counter()
    result = runner.run(suite)
    write_reports(result, time.perf_counter() - started)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
