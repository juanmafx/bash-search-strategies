# Reproducible simulation that emits one CSV row per trial and a stderr summary.
run_simulation() {
  local seed=$1 strategy=$2 upper_bound=$3 trials=$4
  local trial total=0 worst=0 mean_millis
  rng_seed "$seed"
  printf 'trial,seed,strategy,upper_bound,target,attempts\n'
  for ((trial = 1; trial <= trials; trial++)); do
    rng_bounded "$((upper_bound + 1))"
    case $strategy in
      linear) solve_linear "$RNG_VALUE" ;;
      bisection) solve_bisection "$RNG_VALUE" 0 "$upper_bound" ;;
      galloping) solve_galloping "$RNG_VALUE" ;;
    esac
    total=$((total + SOLVER_ATTEMPTS))
    if ((SOLVER_ATTEMPTS > worst)); then
      worst=$SOLVER_ATTEMPTS
    fi
    printf '%d,%d,%s,%d,%d,%d\n' "$trial" "$seed" "$strategy" "$upper_bound" "$RNG_VALUE" "$SOLVER_ATTEMPTS"
  done
  mean_millis=$((total * 1000 / trials))
  printf 'summary: trials=%d mean_attempts=%d.%03d worst_attempts=%d\n' \
    "$trials" "$((mean_millis / 1000))" "$((mean_millis % 1000))" "$worst" >&2
}
