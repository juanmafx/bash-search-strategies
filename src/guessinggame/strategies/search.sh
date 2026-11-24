# Search strategies that count the probes needed to locate a hidden integer.
SOLVER_ATTEMPTS=0

solve_linear() {
  SOLVER_ATTEMPTS=$(($1 + 1))
}

solve_bisection() {
  local target=$1 low=$2 high=$3 middle attempts=0
  while true; do
    middle=$((low + (high - low) / 2))
    attempts=$((attempts + 1))
    if ((middle == target)); then
      break
    elif ((middle < target)); then
      low=$((middle + 1))
    else
      high=$((middle - 1))
    fi
  done
  SOLVER_ATTEMPTS=$attempts
}

solve_galloping() {
  local target=$1 probe=0 next attempts=1
  if ((target == 0)); then
    SOLVER_ATTEMPTS=1
    return 0
  fi
  while true; do
    next=$((probe * 2 + 1))
    attempts=$((attempts + 1))
    if ((next == target)); then
      SOLVER_ATTEMPTS=$attempts
      return 0
    fi
    if ((next > target)); then
      solve_bisection "$target" "$((probe + 1))" "$((next - 1))"
      SOLVER_ATTEMPTS=$((SOLVER_ATTEMPTS + attempts))
      return 0
    fi
    probe=$next
  done
}

bit_length() {
  local value=$1 bits=0
  while ((value > 0)); do
    value=$((value >> 1))
    bits=$((bits + 1))
  done
  printf '%d\n' "$bits"
}
