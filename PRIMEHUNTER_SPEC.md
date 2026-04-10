# PrimeHunter Specification
### Backend Engine for Prime and Twin Prime Structural Analysis

Last Updated: April 2026

---

# 1. Purpose

PrimeHunter is a **pure backend computation engine** designed to:

- analyze prime numbers and twin-prime candidates
- model modular “disruption” behavior of primes
- support large-scale numerical experimentation
- provide structured data outputs for frontend systems

PrimeHunter does **not** include:
- UI logic
- visualization concerns
- presentation formatting beyond structured output

It is intended to serve as the computational backbone for systems such as **Dual Prime Explorer**.

---

# 2. Core Philosophy

PrimeHunter is built around the idea that:

> Primes are the survivors of layered modular constraints.

Rather than only identifying primes, PrimeHunter focuses on:

- candidate generation (e.g., \(6n \pm 1\))
- disruption analysis (which primes eliminate candidates)
- structural modeling (residue classes, modular behavior)

---

# 3. System Architecture

PrimeHunter is divided into three logical layers:

## 3.1 Math Core (Pure Functions)

Stateless, deterministic functions.

Examples:
- `is_prime(n)`
- `factor(n)`
- `smallest_factor(n)`
- `generate_primes(limit)`

---

## 3.2 Analysis Layer

Builds higher-level structures using core functions.

Examples:
- analyze twin-prime centers
- compute disruptors
- evaluate candidate classes
- run modular elimination logic

---

## 3.3 Data / API Layer

Returns structured outputs for external systems.

- JSON responses
- experiment results
- range queries

---

# 4. Core Concepts

## 4.1 Twin Prime Candidates

All candidates are of the form:
