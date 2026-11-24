# Security Audit

- **Date:** 2026-11-23, independently reviewed 2026-11-24
- **Scope:** all tracked files and the full git history of this repository
- **Method:** manual code review, ShellCheck, targeted regression tests, a pattern scan of history, and gitleaks 8.30.1 with redaction over history and the working tree

## Findings

| ID | Severity | Finding | Status |
| --- | --- | --- | --- |
| A1 | High (latent) | Guesses reached Bash arithmetic unvalidated, which permits command execution. In the original file this path was unreachable only because of A2. | Fixed |
| A2 | High (integrity) | A header comment disabled the assignment of the answer, so the game reported a win without reading input. | Fixed |
| A3 | Medium | End of input caused an endless loop once A2 was repaired. | Fixed |
| A4 | Low | Counting with `ls` and `wc` miscounted filenames that contain newlines. | Fixed |
| A5 | Low | The default make target appended to the tracked README on every run. | Fixed |
| A6 | Medium | A symlinked launcher sourced modules from the link's directory, so files planted beside the link ran as code. | Fixed |
| A7 | Low | An inherited `SHELLOPTS=noglob` disabled globbing, so every directory counted as one entry and the game accepted a wrong answer. | Fixed |
| A8 | Low | The loader crashed with a traceback on oversized values and accepted non-canonical integers, targets above the bound, and non-sequential trials. | Fixed |

## Controls added

- Strict decimal validation with explicit ranges for every numeric input
- No `eval`, and no dynamic command construction
- Rejected input is never echoed back to the terminal
- Directory counting resets inherited glob settings, so the environment cannot change the target
- Bound SQL parameters and transactional loading in the optional loader
- CI with read-only token permissions, no persisted credentials, and the checkout action pinned to a full commit SHA (`actions/checkout` v6.1.0)

## Dependencies

The runtime uses Bash and coreutils. The tests use only the Python standard library. There are no package manifests or vendored dependencies, so no ecosystem audit tool applies.

## Not applicable

The project has no web interface, network service, accounts, or stored credentials, so XSS, CSRF, authentication, and two-factor authentication do not apply.

## Secrets

gitleaks and the history scan matched no private keys, access tokens, or credential assignments. File contents contain no email addresses. The 2019 commits recorded the author's email address in their metadata, as git does by default; those commits were removed from every branch and tag by the 2026-11-24 history rewrite.

## Residual risk

- The generator is predictable by design and must not be used for security purposes.
- Earlier commits, which contained the defects above and the author email in their metadata but no secrets, were removed from every branch and tag by the 2026-11-24 history rewrite. They may stay reachable by direct SHA on GitHub until unreferenced objects are purged, so anything that was ever published should still be treated as exposed.
- The loader trusts the `attempts` column, so a hand-edited CSV can record a false probe count.
