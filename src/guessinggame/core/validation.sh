# Strict integer parsing that never lets untrusted text reach shell arithmetic.
PARSED_INTEGER=0

parse_bounded_integer() {
  local raw=$1 minimum=$2 maximum=$3 value
  [[ $raw =~ ^[0-9]{1,10}$ ]] || return 1
  value=$((10#$raw))
  if ((value < minimum || value > maximum)); then
    return 1
  fi
  PARSED_INTEGER=$value
}
