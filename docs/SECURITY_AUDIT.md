# Security Audit

- **Date:** 2026-11-23
- **Scope:** all tracked files and the full git history of this repository
- **Method:** manual code review, ShellCheck, targeted regression tests, and a pattern scan of history for keys, tokens, credentials, and email addresses

## Findings

| ID | Severity | Finding | Status |
| --- | --- | --- | --- |
| A1 | High (latent) | Guesses reached Bash arithmetic unvalidated, which permits command execution. In the original file this path was unreachable only because of A2. | Fixed |
| A2 | High (integrity) | A header comment disabled the assignment of the answer, so the game reported a win without reading input. | Fixed |
| A3 | Medium | End of input caused an endless loop once A2 was repaired. | Fixed |
| A4 | Low | Counting with `ls` and `wc` miscounted filenames that contain newlines. | Fixed |
| A5 | Low | The default make target appended to the tracked README on every run. | Fixed |

## Controls added

- Strict decimal validation with explicit ranges for every numeric input
- No `eval`, and no dynamic command construction
- Rejected input is never echoed back to the terminal
- Directory counting resets inherited glob settings, so the environment cannot change the target
- Bound SQL parameters and transactional loading in the optional loader
- CI with read-only token permissions, no persisted credentials, and the checkout action pinned to a full commit SHA (`actions/checkout` v6.1.0)

## Dependencies

The runtime uses Bash and coreutils. The tests use only the Python standard library. There are no package manifests or vendored dependencies.

## Secrets

The history scan matched no private keys, access tokens, or credential assignments.

## Residual risk

- The generator is predictable by design and must not be used for security purposes.
- Earlier commits remain in git history unchanged. They contain the defects above but no secrets.
