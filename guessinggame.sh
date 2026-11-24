#!/usr/bin/env bash
# Entry point for the directory guessing game and search-strategy simulator.
set -euo pipefail
export LC_ALL=C

PROJECT_ROOT="$(cd -P -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
readonly PROJECT_ROOT

source "$PROJECT_ROOT/src/guessinggame/core/validation.sh"
source "$PROJECT_ROOT/src/guessinggame/core/random.sh"
source "$PROJECT_ROOT/src/guessinggame/core/target.sh"
source "$PROJECT_ROOT/src/guessinggame/strategies/search.sh"
source "$PROJECT_ROOT/src/guessinggame/simulation/simulate.sh"
source "$PROJECT_ROOT/src/guessinggame/cli/play.sh"
source "$PROJECT_ROOT/src/guessinggame/cli/main.sh"

main "$@"
