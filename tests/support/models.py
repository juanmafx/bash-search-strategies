# Independent Python reference models used to cross-check the shell implementation.
WORD_MASK = 0xFFFFFFFF
SEED_SALT = 2463534242
WARMUP_ROUNDS = 16


def xorshift32(state):
    state ^= (state << 13) & WORD_MASK
    state ^= state >> 17
    state ^= (state << 5) & WORD_MASK
    return state


def seeded_state(seed):
    state = (seed ^ SEED_SALT) & WORD_MASK or SEED_SALT
    for _ in range(WARMUP_ROUNDS):
        state = xorshift32(state)
    return state


def bounded_stream(seed, value_range, count):
    state = seeded_state(seed)
    limit = WORD_MASK - WORD_MASK % value_range
    values = []
    while len(values) < count:
        state = xorshift32(state)
        candidate = state - 1
        if candidate < limit:
            values.append(candidate % value_range)
    return values


def bisection_attempts(target, low, high):
    attempts = 0
    while True:
        middle = low + (high - low) // 2
        attempts += 1
        if middle == target:
            return attempts
        if middle < target:
            low = middle + 1
        else:
            high = middle - 1


def galloping_attempts(target):
    if target == 0:
        return 1
    probe, attempts = 0, 1
    while True:
        following = probe * 2 + 1
        attempts += 1
        if following == target:
            return attempts
        if following > target:
            return attempts + bisection_attempts(target, probe + 1, following - 1)
        probe = following


def chi_square(observed, expected):
    return sum((count - expected) ** 2 / expected for count in observed)
