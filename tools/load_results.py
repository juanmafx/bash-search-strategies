#!/usr/bin/env python3
# Loads one simulation CSV into the optional SQLite schema using bound parameters.
import argparse
import csv
import sqlite3
import sys
from pathlib import Path

SCHEMA_PATH = Path(__file__).resolve().parent.parent / "db" / "schema.sql"
EXPECTED_HEADER = ["trial", "seed", "strategy", "upper_bound", "target", "attempts"]


def read_rows(csv_path):
    with open(csv_path, newline="", encoding="utf-8") as handle:
        reader = csv.reader(handle)
        if next(reader, None) != EXPECTED_HEADER:
            raise ValueError("unexpected CSV header")
        rows = [dict(zip(EXPECTED_HEADER, row, strict=True)) for row in reader]
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
                (int(first["seed"]), first["strategy"], int(first["upper_bound"]), len(rows)),
            )
            run_id = cursor.lastrowid
            connection.executemany(
                "INSERT INTO trial_results (run_id, trial, target, attempts) VALUES (?, ?, ?, ?)",
                [(run_id, int(row["trial"]), int(row["target"]), int(row["attempts"])) for row in rows],
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
    except (ValueError, OSError, sqlite3.Error) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    print(f"loaded run {run_id}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
