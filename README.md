# bash-search-strategies

A number-guessing game for the Unix command line, extended into a small, reproducible study of integer search strategies. It is written in Bash, with no runtime dependencies beyond Bash and coreutils.

> **Project history:** originally created in 2019 as an assignment, modernized in 2026.

## Purpose

The player guesses how many visible entries a directory contains, and the program answers "too high" or "too low" until the guess is right. That feedback loop is a search problem, so the project also measures how many probes different strategies need to find a hidden integer.

## Why this project exists

It began as a short shell exercise. The 2019 script never actually played: its header comment swallowed the line that computed the answer, so it declared a win without reading any input. The 2026 version fixes that, treats all input as untrusted, and uses the game as a compact, testable example of defensive shell programming and algorithm analysis.

## What it does

- **Play** against a directory count or a seeded random target.
- **Simulate** the `linear`, `bisection`, and `galloping` search strategies and emit one CSV row per trial.
- **Reproduce** a simulation byte for byte from its seed, strategy, bound, and trial count.
- **Persist** results to SQLite through an optional schema and loader.

## Architecture

```text
guessinggame.sh           Entry point
src/guessinggame/
  core/                   Validation, seeded generator, target resolution
  strategies/             Search algorithms
  simulation/             Trial runner and CSV output
  cli/                    Argument parsing and the game loop
db/schema.sql             Optional SQLite schema
tools/load_results.py     CSV-to-SQLite loader
tests/                    Unit, integration, property, and security suites
reports/tests/            Committed report from a real test run
```

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for module boundaries, algorithms, and complexity.

## Quick start

Requirements: Bash with 64-bit integers and coreutils. Python 3.11+ is needed only for the tests and the loader, GNU Make for the shortcuts, ShellCheck for linting, and the `sqlite3` command only for the query example below.

```bash
git clone https://github.com/juanmafx/bash-search-strategies.git
cd bash-search-strategies
./guessinggame.sh
```

## Usage guide

```bash
./guessinggame.sh --dir /path/to/directory
./guessinggame.sh --random --seed 42 --max 100 --max-attempts 7
./guessinggame.sh simulate --strategy bisection --seed 42 --max 1023 --trials 1000 > run.csv
python3 tools/load_results.py --db results.sqlite3 --csv run.csv
sqlite3 results.sqlite3 'SELECT * FROM run_summary;'
```

Measured output of `simulate` with seed 42, bound 1023, and 1000 trials:

| Strategy | Mean attempts | Worst attempts |
| --- | ---: | ---: |
| `linear` | 521.559 | 1024 |
| `bisection` | 9.119 | 11 |
| `galloping` | 17.316 | 20 |

`galloping` costs more here because it does not use the known upper bound. It needs far fewer probes than `linear` when no bound is known.

## Configuration

The program reads no configuration files or application-specific environment variables. Behavior is controlled by flags:

| Flag | Range | Default |
| --- | --- | --- |
| `--dir PATH` | readable directory | current directory |
| `--random` | switch | off |
| `--seed S` | 0 to 4294967295 | random in `play`, 42 in `simulate` |
| `--max N` | 0 to 2147483647 | 1023 |
| `--max-attempts N` | 1 to 1000000 | unlimited |
| `--strategy NAME` | `linear`, `bisection`, `galloping` | `bisection` |
| `--trials T` | 1 to 1000000 | 100 |

Exit codes: `0` solved or completed, `2` usage error, `3` out of attempts, `4` input ended.

## Database (optional)

The game needs no persistence. [db/schema.sql](db/schema.sql) is an **optional** SQLite 3.37+ schema for keeping simulation results, and nothing in the game depends on it.

## Testing

```bash
make test     # run every suite
make lint     # run ShellCheck
make report   # run the suite and rewrite reports/tests/
```

The suite uses only the Python standard library. It cross-checks the shell code against independent Python models, verifies strategy bounds exhaustively for small ranges and with seeded random cases for large ones, and applies chi-square tests to the generator. The latest real run is in [reports/tests/test-report.md](reports/tests/test-report.md).

## Security notes

- Input is matched against a strict decimal pattern before any arithmetic, because Bash arithmetic can execute embedded command substitutions.
- The code uses no `eval` and does not parse `ls` output.
- Modules load from the launcher's resolved location, so a symlink cannot redirect them to files beside the link.
- The loader rejects non-canonical integers, out-of-range targets, and non-sequential trials before writing.
- The generator is **not cryptographically secure**. It exists for reproducible experiments and must not be used for secrets.

See [SECURITY.md](SECURITY.md) and [docs/SECURITY_AUDIT.md](docs/SECURITY_AUDIT.md).

## Project history

- **2019:** created as an assignment with a guessing script and a makefile that generated the README.
- **2026:** modernized with a working game, a modular structure, search-strategy simulation, tests, CI, and a security audit. See [CHANGELOG.md](CHANGELOG.md).

## Attribution and license

The original script's header marks it as an assignment. Its requirements match the peer-graded Bash, Make, Git, and GitHub assignment from *The Unix Workbench* (Johns Hopkins University, Coursera). The 2019 repository does not name its source, so this match is inferred. Credit for the exercise concept belongs to its authors, and this project does not claim that concept as original. No license has been published for this repository, so default copyright applies.
