from primehunter.analysis.euclid import DEFAULT_LIMIT, DEFAULT_SEED, run_named_mode
from primehunter.data.euclid_exports import write_experiment_report


def main():
    results = run_named_mode("full", DEFAULT_SEED, DEFAULT_LIMIT)
    write_experiment_report("primes_output.txt", results)


if __name__ == "__main__":
    main()
