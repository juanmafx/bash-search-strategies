-- Optional SQLite 3.37+ schema for persisting simulation results.
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS simulation_runs (
  id INTEGER PRIMARY KEY,
  seed INTEGER NOT NULL CHECK (seed BETWEEN 0 AND 4294967295),
  strategy TEXT NOT NULL CHECK (strategy IN ('linear', 'bisection', 'galloping')),
  upper_bound INTEGER NOT NULL CHECK (upper_bound BETWEEN 0 AND 2147483647),
  trial_count INTEGER NOT NULL CHECK (trial_count BETWEEN 1 AND 1000000),
  created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now'))
) STRICT;

CREATE TABLE IF NOT EXISTS trial_results (
  run_id INTEGER NOT NULL REFERENCES simulation_runs (id) ON DELETE CASCADE,
  trial INTEGER NOT NULL CHECK (trial >= 1),
  target INTEGER NOT NULL CHECK (target >= 0),
  attempts INTEGER NOT NULL CHECK (attempts >= 1),
  PRIMARY KEY (run_id, trial)
) STRICT, WITHOUT ROWID;

CREATE INDEX IF NOT EXISTS idx_simulation_runs_strategy_bound
  ON simulation_runs (strategy, upper_bound);

CREATE VIEW IF NOT EXISTS run_summary AS
SELECT
  r.id AS run_id,
  r.seed,
  r.strategy,
  r.upper_bound,
  COUNT(t.trial) AS trials,
  AVG(t.attempts) AS mean_attempts,
  MAX(t.attempts) AS worst_attempts
FROM simulation_runs AS r
JOIN trial_results AS t ON t.run_id = r.id
GROUP BY r.id;
