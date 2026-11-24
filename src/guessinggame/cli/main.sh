# Command-line parsing and dispatch for the play and simulate commands.
readonly EXIT_USAGE=2
readonly MAX_SEED=4294967295
readonly MAX_UPPER_BOUND=2147483647
readonly MAX_TRIALS=1000000
readonly MAX_ATTEMPT_LIMIT=1000000

print_usage() {
  cat <<'USAGE'
Usage:
  guessinggame.sh [play] [--dir PATH] [--max-attempts N]
  guessinggame.sh [play] --random [--seed S] [--max N] [--max-attempts N]
  guessinggame.sh simulate [--strategy NAME] [--seed S] [--max N] [--trials T]
  guessinggame.sh --help | --version

Commands:
  play       Guess the number of visible entries in a directory (default),
             or a random integer in [0, N] with --random.
  simulate   Run a search strategy against seeded targets and print CSV.

Options:
  --dir PATH         Directory to count (default: current directory).
  --random           Use a random target instead of a directory count.
  --seed S           Generator seed, 0 to 4294967295.
  --max N            Inclusive upper bound, 0 to 2147483647 (default: 1023).
  --max-attempts N   Stop after N counted guesses, 1 to 1000000.
  --strategy NAME    linear, bisection, or galloping (default: bisection).
  --trials T         Number of simulated trials, 1 to 1000000 (default: 100).

Exit codes:
  0 solved or completed, 2 usage error, 3 out of attempts, 4 input ended.
USAGE
}

usage_error() {
  printf 'error: %s\n' "$1" >&2
  printf "Run 'guessinggame.sh --help' for usage.\n" >&2
  exit "$EXIT_USAGE"
}

read_integer_option() {
  local name=$1 value=$2 minimum=$3 maximum=$4
  parse_bounded_integer "$value" "$minimum" "$maximum" ||
    usage_error "$name must be an integer from $minimum to $maximum."
}

command_play() {
  local directory=. directory_given=0 use_random=0 seed='' upper_bound='' max_attempts=0 target
  while (($# > 0)); do
    case $1 in
      --random)
        use_random=1
        shift
        continue
        ;;
      --dir | --seed | --max | --max-attempts)
        (($# >= 2)) || usage_error "$1 requires a value."
        ;;
      *) usage_error "unknown play option." ;;
    esac
    case $1 in
      --dir)
        directory=$2
        directory_given=1
        ;;
      --seed)
        read_integer_option --seed "$2" 0 "$MAX_SEED"
        seed=$PARSED_INTEGER
        use_random=1
        ;;
      --max)
        read_integer_option --max "$2" 0 "$MAX_UPPER_BOUND"
        upper_bound=$PARSED_INTEGER
        use_random=1
        ;;
      --max-attempts)
        read_integer_option --max-attempts "$2" 1 "$MAX_ATTEMPT_LIMIT"
        max_attempts=$PARSED_INTEGER
        ;;
    esac
    shift 2
  done
  if ((use_random)); then
    ((directory_given == 0)) || usage_error "--dir cannot be combined with a random target."
    [[ -n $seed ]] || seed=$(rng_entropy_seed)
    [[ -n $upper_bound ]] || upper_bound=1023
    rng_seed "$seed"
    rng_bounded "$((upper_bound + 1))"
    target=$RNG_VALUE
  else
    target=$(count_directory_entries "$directory") ||
      usage_error "--dir must be a readable directory."
  fi
  play_game "$target" "$max_attempts"
}

command_simulate() {
  local strategy=bisection seed=42 upper_bound=1023 trials=100
  while (($# > 0)); do
    case $1 in
      --strategy | --seed | --max | --trials)
        (($# >= 2)) || usage_error "$1 requires a value."
        ;;
      *) usage_error "unknown simulate option." ;;
    esac
    case $1 in
      --strategy)
        case $2 in
          linear | bisection | galloping) strategy=$2 ;;
          *) usage_error "--strategy must be linear, bisection, or galloping." ;;
        esac
        ;;
      --seed)
        read_integer_option --seed "$2" 0 "$MAX_SEED"
        seed=$PARSED_INTEGER
        ;;
      --max)
        read_integer_option --max "$2" 0 "$MAX_UPPER_BOUND"
        upper_bound=$PARSED_INTEGER
        ;;
      --trials)
        read_integer_option --trials "$2" 1 "$MAX_TRIALS"
        trials=$PARSED_INTEGER
        ;;
    esac
    shift 2
  done
  run_simulation "$seed" "$strategy" "$upper_bound" "$trials"
}

main() {
  case ${1:-play} in
    --help | -h) print_usage ;;
    --version)
      printf 'guessinggame %s\n' "$(<"$PROJECT_ROOT/VERSION")"
      ;;
    simulate)
      shift
      command_simulate "$@"
      ;;
    play)
      (($# == 0)) || shift
      command_play "$@"
      ;;
    *) command_play "$@" ;;
  esac
}
