import csv
import math
import time


# main.py
# Purpose: Build hash tables for movie titles and quotes, then compare several
# collision strategies and hash functions using the assignment statistics.
# Author: Abigail Gurney
# Recieved Help From: N/A
# Date: 10/11/2024


#Attempt 5: FNV-1a + lower load + double hashing
# What was tried:
# - Used fnv1a_hash function for the movie title and quote keys
# - Increased table size to lower the load factor even more
# - Enabled double hashing for linear probing and compared to linked list chaining
# Why this approach:
# - FNV-1a gives a stronger distribution test than polynomial_hash
# - Lower load factor plus double hashing should reduce probing collisions
# - This shows how much probing improves when clustering pressure is reduced
# Results (15,000 movie records, table size 60,013):
# - Linked list (title): 4,715 collisions, ~0.030s construction
# - Linked list (quote): 1,857 collisions, ~0.050s construction
# - Linear probing (title): 7,252 collisions, ~0.038s construction
# - Linear probing (quote): 2,431 collisions, ~0.064s construction
# Key findings:
# - Lower load and double hashing reduced probing collisions compared to earlier runs
# - Linked list chaining still had fewer collisions than probing
# - The combined console table makes the final results easier to compare
# - FNV-1a performed best when the table had more open space
# - This attempt gives a clear contrast against higher-load configurations



def load_movie_data(file_path):
    # Load CSV file and parse all movie records.
    records = []
    with open(file_path, newline="", encoding="utf-8") as file_handle:
        reader = csv.DictReader(file_handle)
        for row in reader:
            record = parse_movie_record(row)
            if record is not None:
                records.append(record)
    return records


def parse_movie_record(raw_line):
    # Parse a single movie record from CSV row data.
    if raw_line is None:
        return None

    if isinstance(raw_line, dict):
        movie_title = (raw_line.get("movie_title") or "").strip()
        quote = (raw_line.get("quote") or "").strip()
        if not movie_title and not quote:
            return None
        return {
            "movie_title": movie_title,
            "quote": quote,
            "raw": raw_line,
        }

    if isinstance(raw_line, str):
        text = raw_line.strip()
        if not text:
            return None

        reader = csv.reader([text])
        values = next(reader, [])
        if not values:
            return None

        movie_title = values[0].strip() if len(values) > 0 else ""
        quote = values[-1].strip() if len(values) > 1 else ""
        if not movie_title and not quote:
            return None
        return {
            "movie_title": movie_title,
            "quote": quote,
            "raw": text,
        }

    return None


def normalize_movie_title(movie_title):
    # structure title for consistent hashing (lowercase, no extra spaces).
    if isinstance(movie_title, dict):
        movie_title = movie_title.get("movie_title", "")
    return " ".join((movie_title or "").strip().lower().split())


def normalize_movie_quote(movie_quote):
    # structure quote for consistent hashing (lowercase, no extra spaces).
    if isinstance(movie_quote, dict):
        movie_quote = movie_quote.get("quote", "")
    return " ".join((movie_quote or "").strip().lower().split())


def poor_hash(key, table_size):
    # Weak hash: length + first/last char. High collisions for baseline comparison.
    if not key:
        return 0
    return (len(key) + ord(key[0]) + ord(key[-1])) % table_size


def polynomial_hash(key, table_size, base=31):
    # Rolling polynomial hash for better key distribution.
    value = 0
    for character in key:
        value = (value * base + ord(character)) % table_size
    return value


def fnv1a_hash(key, table_size):
    # FNV-1a hash for strong bit mixing and collision resistance.
    value = 2166136261
    for character in key:
        value ^= ord(character)
        value = (value * 16777619) % (2**32)
    return value % table_size


def secondary_hash(key, table_size):
    # Double hashing step: ensures full table coverage and reduces clustering.
    if table_size <= 2:
        return 1
    step = 1 + (polynomial_hash(key, table_size - 1, base=37) % (table_size - 1))
    if step % table_size == 0:
        return 1
    return step


def is_prime(number):
    # Check if a number is prime (for table size selection).
    if number < 2:
        return False
    if number in (2, 3):
        return True
    if number % 2 == 0:
        return False
    limit = int(math.sqrt(number)) + 1
    for divisor in range(3, limit, 2):
        if number % divisor == 0:
            return False
    return True


def next_prime(number):
    # Find the next prime number (used for hash table sizing).
    candidate = max(2, int(math.ceil(number)))
    while not is_prime(candidate):
        candidate += 1
    return candidate


def build_linked_list_hash_table(records, key_function, hash_function, table_size):
    # Build hash table using linked list chaining for collision resolution.
    buckets = [[] for _ in range(table_size)]
    collisions = 0

    for record in records:
        key = key_function(record)
        index = hash_function(key, table_size)
        bucket = buckets[index]
        if bucket:
            collisions += 1
        bucket.append((key, record))

    return {
        "strategy": "linked_list",
        "buckets": buckets,
        "collisions": collisions,
        "record_count": len(records),
        "table_size": table_size,
    }


def build_linear_probing_hash_table(records, key_function, hash_function, table_size, use_double_hashing=False):
    # Build hash table using linear/double probing for collision fix.
    slots = [None] * table_size
    collisions = 0

    for record in records:
        key = key_function(record)
        index = hash_function(key, table_size)
        step = secondary_hash(key, table_size) if use_double_hashing else 1
        start_index = index

        while slots[index] is not None:
            collisions += 1
            index = (index + step) % table_size
            if index == start_index:
                raise RuntimeError("Hash table is full; increase the table size.")

        slots[index] = (key, record)

    return {"strategy": "linear_probing", "slots": slots, "collisions": collisions,"record_count": len(records), "table_size": table_size, "double_hashing": use_double_hashing,}


def count_wasted_space(hash_table):
    # Count empty slots/buckets to measure table utilization.
    if "buckets" in hash_table:
        return sum(1 for bucket in hash_table["buckets"] if not bucket)
    if "slots" in hash_table:
        return sum(1 for slot in hash_table["slots"] if slot is None)
    return 0


def count_collisions(hash_table):
    # get total collision count from hash table results.
    return hash_table.get("collisions", 0)


def measure_construction_time(builder_function, records, key_function, *builder_args, **builder_kwargs):
    # get how long it takes to build a hash table.
    start_time = time.perf_counter()
    hash_table = builder_function(records, key_function, *builder_args, **builder_kwargs)
    elapsed_time = time.perf_counter() - start_time
    return hash_table, elapsed_time


def summarize_hash_table(hash_table, construction_time):
    # get key statistics from a hash table for reporting.
    table_size = hash_table.get("table_size", 0)
    record_count = hash_table.get("record_count", 0)
    return {
        "table_size": table_size,
        "record_count": record_count,
        "load_factor": (record_count / table_size) if table_size else 0,
        "wasted_space": count_wasted_space(hash_table),
        "collisions": count_collisions(hash_table),
        "construction_time": construction_time,
    }


def print_combined_console_table(attempt_label, rows):
    # structure and print all results in a table.
    headers = ["Strategy", "Key", "Table Size", "Records", "Load", "Wasted", "Collisions", "Time (s)"]
    table_rows = []
    for row in rows:
        table_rows.append(
            [
                row["strategy"],
                row["key_label"],
                str(row["table_size"]),
                str(row["record_count"]),
                f"{row['load_factor']:.4f}",
                str(row["wasted_space"]),
                str(row["collisions"]),
                f"{row['construction_time']:.6f}",
            ]
        )

    column_widths = []
    for index, header in enumerate(headers):
        max_width = len(header)
        for row in table_rows:
            max_width = max(max_width, len(row[index]))
        column_widths.append(max_width)

    def format_row(values):
        return " | ".join(value.ljust(column_widths[index]) for index, value in enumerate(values))

    divider = "-+-".join("-" * width for width in column_widths)

    print(attempt_label)
    print(format_row(headers))
    print(divider)
    for row in table_rows:
        print(format_row(row))
    print()


def run_single_attempt(movie_records, attempt_settings):
    # Run one complete attempt with all strategy/key combinations.
    key_functions = [
        ("movie title", normalize_movie_title),
        ("movie quote", normalize_movie_quote),
    ]

    table_builders = [
        ("linked list", build_linked_list_hash_table),
        ("linear probing", build_linear_probing_hash_table),
    ]

    combined_rows = []
    for table_label, builder in table_builders:
        for key_label, key_function in key_functions:
            builder_args = [attempt_settings["hash_function"], attempt_settings["table_size"]]
            if builder is build_linear_probing_hash_table:
                builder_args.append(attempt_settings["use_double_hashing"])

            hash_table, construction_time = measure_construction_time(
                builder,
                movie_records,
                key_function,
                *builder_args,
            )
            summary = summarize_hash_table(hash_table, construction_time)
            summary.update(
                {
                    "strategy": table_label,
                    "key_label": key_label,
                }
            )
            combined_rows.append(summary)

    print_combined_console_table(attempt_settings["label"], combined_rows)


def run_hash_table_attempts(file_path):
    # Execute all hash table benchmark attempts and output results.
    movie_records = load_movie_data(file_path)
    if not movie_records:
        print("No movie records were loaded.")
        return

    record_count = len(movie_records)


    active_attempt = {
        "label": "Attempt 5 - FNV-1a + lower load + double hashing",
        "hash_function": fnv1a_hash,
        "table_size": next_prime(record_count * 4),
        "use_double_hashing": True,
    }


    run_single_attempt(movie_records, active_attempt)


def main():
    file_path = "MOCK_DATA.csv"
    run_hash_table_attempts(file_path)


if __name__ == "__main__":
    main()
