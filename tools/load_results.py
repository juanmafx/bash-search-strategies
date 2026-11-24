#!/usr/bin/env python3
# Loads one simulation CSV into the optional SQLite schema using bound parameters.
import argparse
import csv
import re
import sqlite3
import sys
from pathlib import Path

SCHEMA_PATH = Path(__file__).resolve().parent.parent / "db" / "schema.sql"
EXPECTED_HEADER = ["trial", "seed", "strategy", "upper_bound", "target", "attempts"]
INTEGER_FIELDS = ("trial", "seed", "upper_bound", "target", "attempts")
CANONICAL_INTEGER = re.compile(r"0|[1-9][0-9]{0,9}")
MAX_TRIALS = 1_000_000


def parse_row(record):
    row = dict(zip(EXPECTED_HEADER, record, strict=True))
    for field in INTEGER_FIELDS:
        if not CANONICAL_INTEGER.fullmatch(row[field]):
            raise ValueError(f"{field} must be a canonical decimal integer")
        row[field] = int(row[field])
    if row["target"] > row["upper_bound"]:
        raise ValueError("target exceeds upper_bound")
    return row


def read_rows(csv_path):
    rows = []
    with open(csv_path, newline="", encoding="utf-8") as handle:
        reader = csv.reader(handle)
        if next(reader, None) != EXPECTED_HEADER:
            raise ValueError("unexpected CSV header")
        for record in reader:
            if len(rows) == MAX_TRIALS:
                raise ValueError("CSV has too many trials")
            row = parse_row(record)
            if row["trial"] != len(rows) + 1:
                raise ValueError("trial numbers must be sequential from 1")
            rows.append(row)
    if not rows:
        raise ValueError("CSV has no trials")
    if len({(row["seed"], row["strategy"], row["upper_bound"]) for row in rows}) != 1:
        raise ValueError("CSV mixes more than one run")
    return rows


def load(database_path, csv_path):
    rows = read_rows(csv_path)
    first = rows[0]
    connection = sqlite3.connect(database_path)
    try:
        connection.execute("PRAGMA foreign_keys = ON")
        connection.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
        connection.execute("PRAGMA foreign_keys = ON")
        with connection:
            cursor = connection.execute(
                "INSERT INTO simulation_runs (seed, strategy, upper_bound, trial_count) VALUES (?, ?, ?, ?)",
                (first["seed"], first["strategy"], first["upper_bound"], len(rows)),
            )
            run_id = cursor.lastrowid
            connection.executemany(
                "INSERT INTO trial_results (run_id, trial, target, attempts) VALUES (?, ?, ?, ?)",
                [(run_id, row["trial"], row["target"], row["attempts"]) for row in rows],
            )
        return run_id
    finally:
        connection.close()


def main(argv=None):
    parser = argparse.ArgumentParser(description="Load a simulation CSV into SQLite.")
    parser.add_argument("--db", required=True, type=Path)
    parser.add_argument("--csv", required=True, type=Path)
    arguments = parser.parse_args(argv)
    try:
        run_id = load(arguments.db, arguments.csv)
    except (ValueError, OSError, sqlite3.Error, csv.Error) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    print(f"loaded run {run_id}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
