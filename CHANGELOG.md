# Changelog

This project follows [Semantic Versioning](https://semver.org/).

## [1.0.1] - 2026-11-24

### Changed

- Documentation corrections: the release notes and security audit now reflect the published 1.0.0 release and the 2026-11-24 history rewrite. No code behaviour change.

## [1.0.0] - 2026-11-24

First versioned release. The earlier 2019 code carried no version number.

### Added

- `simulate` command with linear, bisection, and galloping strategies
- Seeded xorshift32 generator with unbiased bounded draws
- `--dir`, `--random`, `--seed`, `--max`, `--max-attempts`, `--help`, and `--version`
- Optional SQLite schema and CSV loader
- Unit, integration, property, statistical, and security tests with a committed report
- CI workflow, architecture documentation, security policy, and security audit

### Changed

- **Breaking:** the code is now organized under `src/guessinggame/`
- **Breaking:** ending input before a correct guess exits with code 4
- **Breaking:** `make` now prints help, and `make set_file` writes `build/project-info.md` instead of appending to `README.md`
- Corrected the wording of all game messages

### Fixed

- The game now computes its target and actually plays
- Guesses can no longer execute commands through shell arithmetic
- End of input no longer causes an endless loop
- Filenames containing newlines are counted correctly
- An inherited `noglob` shell option can no longer change the directory count
- A symlinked launcher loads modules from its real location instead of the link's directory
- The loader reports malformed input as an error and rejects non-canonical integers, targets above the bound, and non-sequential trials
