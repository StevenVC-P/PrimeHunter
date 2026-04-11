# Euclid-Style Prime Experiment Comparison

## Setup

All three experiments:

- start from the seed `[2]`
- look at values below `1000`
- build candidates from products of already known primes
- then examine `product + 1`

The experiments differ in two choices:

- whether repeated prime factors are allowed in the product
- whether composite `product + 1` results are factored to extract new prime factors

## The Three Modes

### 1. Repeated primes allowed; factor composite results

Script:
`python -m scripts.research.euclid_experiment`

Output:
`primes_output.txt`

Rules:

- repeated factors are allowed, so products like `2^2`, `2^8`, `3^2`, and `2^2 * 3^3` can appear
- if `product + 1` is composite, its prime factors are checked and any new primes are added

Result:

- found `168` of `168` known primes below `1000`
- missing `0`

Interpretation:

- this is the strongest version we tested
- allowing repeated prime factors gives the search much more reach
- factoring composite results fills in primes that are hidden inside values like `33 = 3 * 11` or `65 = 5 * 13`

### 2. Square-free only; factor composite results

Script:
`python -m scripts.research.euclid_square_free_experiment`

Output:
`primes_square_free_output.txt`

Rules:

- each prime can appear at most once in a product
- if `product + 1` is composite, its prime factors are checked and any new primes are added

Result:

- found `114` of `168` known primes below `1000`
- missing `54`

Missing primes:

`[271, 307, 337, 379, 401, 421, 461, 491, 509, 521, 523, 541, 557, 569, 577, 593, 601, 613, 617, 631, 641, 653, 661, 673, 677, 701, 709, 727, 733, 739, 751, 757, 761, 769, 773, 797, 809, 811, 821, 829, 853, 857, 877, 881, 883, 919, 929, 937, 941, 953, 977, 983, 991, 997]`

Interpretation:

- factorization helps a lot
- but removing repeated prime factors still cuts off a large part of the search space
- many of the missing primes seem to depend on constructions that use repeated factors like `2^k`, `3^2`, or more structured repeated products

### 3. Square-free only; prime results only

Script:
`python -m scripts.research.euclid_square_free_no_factor_experiment`

Output:
`primes_square_free_no_factor_output.txt`

Rules:

- each prime can appear at most once in a product
- if `product + 1` is composite, it is discarded

Result:

- found `4` of `168` known primes below `1000`
- missing `164`
- found primes: `[2, 3, 7, 43]`

Interpretation:

- this is by far the weakest version
- without repeated factors and without factorization, the search stalls almost immediately

## Direct Comparison

| Mode | Repeated factors? | Factor composites? | Found below 1000 | Missing below 1000 |
|---|---|---|---:|---:|
| Full Euclid-style exploration | Yes | Yes | 168 | 0 |
| Square-free with factorization | No | Yes | 114 | 54 |
| Square-free without factorization | No | No | 4 | 164 |

## Main Takeaways

1. Factoring composite `product + 1` values matters.

Examples:

- `2^5 + 1 = 33 = 3 * 11` reveals `11`
- `2^6 + 1 = 65 = 5 * 13` reveals `13`
- `2 * 7 + 1 = 15 = 3 * 5` reveals `5`

If composite results are ignored, many primes are lost immediately.

2. Repeated prime factors matter too.

Even after adding factorization, the square-free version still misses `54` primes below `1000`.

This means factorization alone is not enough. The ability to use products with repeated factors appears to be a major part of why the full experiment reaches all primes below `1000`.

3. The strongest version combines both ideas.

The best-performing experiment is the one that:

- allows repeated factors in the product
- factors composite `product + 1` values

That version recovers every prime below `1000` in this test.

## Suggested Next Questions

- How far does the full version continue to find all primes as the limit increases beyond `1000`?
- At what limit does the square-free with factorization version begin to miss a larger percentage?
- Which missing primes in the square-free version require repeated-factor constructions most directly?
- Can the outputs be grouped by discovery mechanism: direct prime hit vs. composite factor reveal?


