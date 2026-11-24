# Seeded xorshift32 generator with rejection sampling for unbiased bounded draws.
RNG_WORD_MASK=4294967295
RNG_SEED_SALT=2463534242
RNG_WARMUP_ROUNDS=16
RNG_STATE=$RNG_SEED_SALT
RNG_VALUE=0

rng_next() {
  local state=$RNG_STATE
  state=$((state ^ ((state << 13) & RNG_WORD_MASK)))
  state=$((state ^ (state >> 17)))
  state=$((state ^ ((state << 5) & RNG_WORD_MASK)))
  RNG_STATE=$state
}

rng_seed() {
  local seed=$1 round
  RNG_STATE=$(((seed ^ RNG_SEED_SALT) & RNG_WORD_MASK))
  if ((RNG_STATE == 0)); then
    RNG_STATE=$RNG_SEED_SALT
  fi
  for ((round = 0; round < RNG_WARMUP_ROUNDS; round++)); do
    rng_next
  done
}

rng_bounded() {
  local range=$1 limit candidate
  limit=$((RNG_WORD_MASK - RNG_WORD_MASK % range))
  while true; do
    rng_next
    candidate=$((RNG_STATE - 1))
    if ((candidate < limit)); then
      RNG_VALUE=$((candidate % range))
      return 0
    fi
  done
}

rng_entropy_seed() {
  od -An -N4 -tu4 /dev/urandom | tr -d '[:space:]'
}
