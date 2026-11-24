# Architecture

## Overview

The project is a single-process command-line tool with no client/server split, network access, or required storage. Dependencies point one way:

```text
guessinggame.sh
      |
      v
 cli/main.sh ---> cli/play.sh ---> core/validation.sh
      |
      +---------> core/validation.sh, core/random.sh, core/target.sh
      |
      v
 simulation/simulate.sh ---> core/random.sh, strategies/search.sh
```

| Module | Responsibility |
| --- | --- |
| `core/validation.sh` | Converts untrusted text to a bounded integer |
| `core/random.sh` | Seeded generator and unbiased bounded draws |
| `core/target.sh` | Counts visible directory entries |
| `strategies/search.sh` | Linear, bisection, and galloping probe counts |
| `simulation/simulate.sh` | Runs trials and writes CSV and a summary |
| `cli/play.sh` | Interactive loop and termination states |
| `cli/main.sh` | Option parsing and dispatch |

## Design decisions

- **Validate before arithmetic.** Bash evaluates `-eq` and `-gt` operands inside `[[ ]]`, and everything inside `$(( ))`, as arithmetic expressions, so only text that passed the decimal pattern reaches them.
- **Resolve the launcher first.** The entry point canonicalizes its own path before sourcing modules, so a symlink cannot load files planted beside the link.
- **Globals for return values.** Generator and solver results use named globals because a `$(...)` call would fork per draw and discard generator state.
- **Data on stdout, diagnostics on stderr.** Simulation output can be piped straight to a file.
- **Explicit exit codes.** Scripts can distinguish a win, bad usage, exhausted attempts, and ended input.

## Algorithms and complexity

For a hidden integer among `N` candidates, with `t` the target:

| Strategy | Requires a bound | Worst-case probes | Time | Space |
| --- | --- | --- | --- | --- |
| Linear | No | `t + 1` | O(t) | O(1) |
| Bisection | Yes | `floor(log2 N) + 1` | O(log N) | O(1) |
| Galloping | No | `max(1, 2 * ceil(log2(t + 1)))` | O(log t) | O(1) |

`linear` returns its probe count in closed form, so simulating it is O(1) per trial.

**Bisection** is optimal in the worst case. Each three-way answer leaves at most half of the remaining candidates, and `k` probes can distinguish at most `2^k - 1` values, so `ceil(log2(N + 1))` probes are necessary. That equals `floor(log2 N) + 1`.

**Galloping** probes `0, 1, 3, 7, ...` until it reaches or passes `t`, then bisects the open interval. It suits the directory game, where no upper bound is known.

## Random number generation

The generator is Marsaglia's xorshift32 (shifts 13, 17, 5), chosen because every operation stays inside 64-bit shell integers with no signed overflow.

- **Period:** `2^32 - 1`. The state is never zero.
- **Seeding:** the seed is XORed with a fixed salt, then 16 rounds are discarded. Exactly one pair of seeds shares a stream: `0` and the salt value `2463534242`.
- **Bounded draws:** rejection sampling discards values above the largest multiple of the range, which removes modulo bias over the full period. Expected draws per value are below 2.
- **Limits:** xorshift32 is known to fail stronger statistical batteries and is predictable. It is suitable for these simulations and not for security use.

## Persistence

`db/schema.sql` defines `simulation_runs`, `trial_results`, and the `run_summary` view, with `STRICT` typing, range checks, and cascading deletes. `tools/load_results.py` checks the header, canonical integers, sequential trials, a single run per file, and that each target is within the bound, then inserts the rows in one transaction using bound parameters. It does not recompute `attempts`, so it cannot detect a forged probe count.

## Testing strategy

| Suite | Focus |
| --- | --- |
| `tests/unit` | Parser, generator vectors, strategies, directory counting |
| `tests/integration` | CLI behavior, exit codes, makefile, schema, loader |
| `tests/properties` | Exhaustive and seeded-random bounds, model agreement, chi-square checks |
| `tests/security` | Injection payloads, hostile filenames and environment |

Statistical tests use fixed seeds, so they are deterministic rather than flaky. Critical values correspond to a significance level of 0.001.
