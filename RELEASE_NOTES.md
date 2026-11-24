# Release Notes: v1.0.0

This is the first versioned release of `unix3`, a modernization of a 2019 shell assignment. It has not been tagged or published yet.

## Highlights

- The game works: the 2019 script declared a win without reading any input.
- All input is validated before use, closing a command-execution path in the original logic.
- A reproducible simulator compares linear, bisection, and galloping search.
- Automated tests cover behavior, algorithm bounds, generator statistics, and hostile input.

## Upgrade notes

- `make` no longer modifies `README.md`. Use `make set_file` to generate `build/project-info.md`.
- Scripts that call the game should handle exit codes `2`, `3`, and `4`.

## Verification

```bash
make lint
make test
```

The latest recorded run is in `reports/tests/test-report.md`.
