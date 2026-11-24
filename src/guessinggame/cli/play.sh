# Interactive game loop with validated input and explicit termination states.
readonly EXIT_OUT_OF_ATTEMPTS=3
readonly EXIT_END_OF_INPUT=4
readonly MAX_GUESS=9999999999

play_game() {
  local target=$1 max_attempts=$2 attempts=0 raw guess
  while true; do
    printf 'Enter your guess:\n'
    raw=''
    if ! IFS=$' \t\r' read -r raw && [[ -z $raw ]]; then
      printf 'error: input ended before the correct guess.\n' >&2
      return "$EXIT_END_OF_INPUT"
    fi
    if ! parse_bounded_integer "$raw" 0 "$MAX_GUESS"; then
      printf 'Invalid guess: enter a whole number from 0 to %d.\n' "$MAX_GUESS" >&2
      continue
    fi
    guess=$PARSED_INTEGER
    attempts=$((attempts + 1))
    if ((guess == target)); then
      printf 'Congratulations, your guess was correct.\n'
      printf 'Solved in %d attempt(s).\n' "$attempts"
      return 0
    fi
    if ((guess > target)); then
      printf 'Your guess was too high.\n'
    else
      printf 'Your guess was too low.\n'
    fi
    if ((max_attempts > 0 && attempts >= max_attempts)); then
      printf 'Out of attempts.\n' >&2
      return "$EXIT_OUT_OF_ATTEMPTS"
    fi
  done
}
