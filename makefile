.DEFAULT_GOAL := help
PYTHON ?= python3
SHELLCHECK ?= shellcheck
SHELL_SOURCES := guessinggame.sh $(wildcard src/guessinggame/*/*.sh)

.PHONY: help lint test report simulate set_file

help:
	@printf '%s\n' 'Targets: lint test report simulate set_file'

lint:
	$(SHELLCHECK) --shell=bash $(SHELL_SOURCES)

test:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) -m unittest discover -s tests -t .

report:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) -m tests.run_report

simulate:
	./guessinggame.sh simulate --strategy bisection --seed 42 --max 1023 --trials 100

set_file:
	mkdir -p build
	{ printf '# guessinggame\n\nDate: '; date -u '+%Y-%m-%dT%H:%M:%SZ'; printf 'Lines in guessinggame.sh: '; wc -l < guessinggame.sh; } > build/project-info.md
