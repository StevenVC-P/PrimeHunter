"""Pure prime-number helpers for PrimeHunter."""


def is_prime(n):
    """Return True when n is prime."""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def all_primes_below(limit):
    """Return the canonical reference list of primes less than limit."""
    return [n for n in range(2, limit) if is_prime(n)]


def prime_factors(n):
    """Return the prime factors of n with multiplicity."""
    factors = []

    while n % 2 == 0:
        factors.append(2)
        n //= 2

    while n % 3 == 0:
        factors.append(3)
        n //= 3

    i = 5
    while i * i <= n:
        while n % i == 0:
            factors.append(i)
            n //= i
        while n % (i + 2) == 0:
            factors.append(i + 2)
            n //= i + 2
        i += 6

    if n > 1:
        factors.append(n)

    return factors


def parse_seed_primes(seed_text):
    """Parse a comma-separated seed string into validated prime integers."""
    if seed_text is None:
        return []

    values = []
    for part in seed_text.split(","):
        text = part.strip()
        if not text:
            continue
        value = int(text)
        if not is_prime(value):
            raise ValueError(f"Seed value {value} is not prime.")
        values.append(value)

    if not values:
        raise ValueError("Seed list must contain at least one prime.")

    return sorted(set(values))
