import sqlite3
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tests.support.harness import PROJECT_ROOT, run_cli

SCHEMA = PROJECT_ROOT / "db" / "schema.sql"
LOADER = PROJECT_ROOT / "tools" / "load_results.py"


class SchemaTests(unittest.TestCase):
    def setUp(self):
        self.connection = sqlite3.connect(":memory:")
        self.addCleanup(self.connection.close)
        self.connection.executescript(SCHEMA.read_text(encoding="utf-8"))
        self.connection.execute("PRAGMA foreign_keys = ON")

    def test_schema_is_idempotent(self):
        self.connection.executescript(SCHEMA.read_text(encoding="utf-8"))

    def test_rejects_unknown_strategy(self):
        with self.assertRaises(sqlite3.IntegrityError):
            self.connection.execute(
                "INSERT INTO simulation_runs (seed, strategy, upper_bound, trial_count) VALUES (1, 'x', 1, 1)"
            )

    def test_rejects_orphan_trial(self):
        with self.assertRaises(sqlite3.IntegrityError):
            self.connection.execute(
                "INSERT INTO trial_results (run_id, trial, target, attempts) VALUES (99, 1, 0, 1)"
            )

    def test_delete_cascades(self):
        self.connection.execute(
            "INSERT INTO simulation_runs (id, seed, strategy, upper_bound, trial_count) VALUES (1, 1, 'linear', 1, 1)"
        )
        self.connection.execute("INSERT INTO trial_results VALUES (1, 1, 0, 1)")
        self.connection.execute("DELETE FROM simulation_runs WHERE id = 1")
        self.assertEqual(self.connection.execute("SELECT COUNT(*) FROM trial_results").fetchone()[0], 0)


class LoaderTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.workspace = Path(self.temporary.name)
        self.database = self.workspace / "results.sqlite3"
        self.csv_path = self.workspace / "run.csv"

    def load(self):
        return subprocess.run(
            [sys.executable, str(LOADER), "--db", str(self.database), "--csv", str(self.csv_path)],
            capture_output=True,
            text=True,
            check=False,
        )

    def test_loads_real_simulation_output(self):
        output = run_cli("simulate", "--seed", "42", "--max", "255", "--trials", "25").stdout
        self.csv_path.write_text(output, encoding="utf-8")
        self.assertEqual(self.load().returncode, 0)
        connection = sqlite3.connect(self.database)
        self.addCleanup(connection.close)
        trials, worst = connection.execute("SELECT trials, worst_attempts FROM run_summary").fetchone()
        self.assertEqual(trials, 25)
        self.assertLessEqual(worst, 8)

    def test_rejects_wrong_header(self):
        self.csv_path.write_text("a,b\n1,2\n", encoding="utf-8")
        self.assertEqual(self.load().returncode, 2)

    def test_rejects_invalid_row_atomically(self):
        header = "trial,seed,strategy,upper_bound,target,attempts\n"
        self.csv_path.write_text(header + "1,1,linear,5,0,1\n2,1,linear,5,1,0\n", encoding="utf-8")
        self.assertEqual(self.load().returncode, 2)
        connection = sqlite3.connect(self.database)
        self.addCleanup(connection.close)
        self.assertEqual(connection.execute("SELECT COUNT(*) FROM simulation_runs").fetchone()[0], 0)

    def test_strategy_text_is_bound_not_executed(self):
        header = "trial,seed,strategy,upper_bound,target,attempts\n"
        hostile = "linear'); DROP TABLE simulation_runs; --"
        self.csv_path.write_text(f"{header}1,1,{hostile},5,0,1\n", encoding="utf-8")
        self.assertEqual(self.load().returncode, 2)
        connection = sqlite3.connect(self.database)
        self.addCleanup(connection.close)
        self.assertEqual(connection.execute("SELECT COUNT(*) FROM simulation_runs").fetchone()[0], 0)
