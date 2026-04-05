import csv
import math
import time


# main.py
# Purpose: Build hash tables for movie titles and quotes, then compare several
# collision strategies and hash functions using the assignment statistics.
# Author: Abigail Gurney
# Recieved Help From: N/A
# Date: 10/11/2024


#Attempt 1: Benchmark poor hash with high load factor
# What was tried:
# - Used poor_hash function (based on key length + first/last character)
# - High load factor strategy (load_factor = (record_count / table_size))
# - Compared linked list vs collision 
# Why this approach:
# - Poor hash = baseline for collision behavior
# - High load factor tests performance under constrained space
# - worst-case scenario for optimization comparisons
# Results (15,000 movie records, table size 16,519):
# - Linked list (title): 14,798 collisions, 0.007s construction
# - Linked list (quote): 14,928 collisions, 0.006s construction
# - Linear probing (title): 110.6M collisions, 2.96s construction
# Key findings:
# - Linked list hash tables handled collisions reasonably well
# - Linear probing suffering
# - high load factor, taking 400x longer than linked list
# - Poor hash function creates highly uneven bucket distribution
# - Established baseline for comparing optimization techniques



def load_movie_data(file_path):
    records = []
    with open(file_path, newline="", encoding="utf-8") as file_handle:
        reader = csv.DictReader(file_handle)
        for row in reader:
            record = parse_movie_record(row)
            if record is not None:
                records.append(record)
    return records


def parse_movie_record(raw_line):
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
    if isinstance(movie_title, dict):
        movie_title = movie_title.get("movie_title", "")
    return " ".join((movie_title or "").strip().lower().split())


def normalize_movie_quote(movie_quote):
    if isinstance(movie_quote, dict):
        movie_quote = movie_quote.get("quote", "")
    return " ".join((movie_quote or "").strip().lower().split())


def poor_hash(key, table_size):
    # Weak hash: length + first/last char. High collisions for baseline comparison.
    if not key:
        return 0
    return (len(key) + ord(key[0]) + ord(key[-1])) % table_size


def polynomial_hash(key, table_size, base=31):
    value = 0
    for character in key:
        value = (value * base + ord(character)) % table_size
    return value


def fnv1a_hash(key, table_size):
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
    candidate = max(2, int(math.ceil(number)))
    while not is_prime(candidate):
        candidate += 1
    return candidate


def build_linked_list_hash_table(records, key_function, hash_function, table_size):
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
    if "buckets" in hash_table:
        return sum(1 for bucket in hash_table["buckets"] if not bucket)
    if "slots" in hash_table:
        return sum(1 for slot in hash_table["slots"] if slot is None)
    return 0


def count_collisions(hash_table):
    return hash_table.get("collisions", 0)


def measure_construction_time(builder_function, records, key_function, *builder_args, **builder_kwargs):
    start_time = time.perf_counter()
    hash_table = builder_function(records, key_function, *builder_args, **builder_kwargs)
    elapsed_time = time.perf_counter() - start_time
    return hash_table, elapsed_time


def print_hash_table_statistics(table_name, hash_table, construction_time):
    wasted_space = count_wasted_space(hash_table)
    collisions = count_collisions(hash_table)
    table_size = hash_table.get("table_size", 0)
    record_count = hash_table.get("record_count", 0)
    load_factor = (record_count / table_size) if table_size else 0

    print(table_name)
    print(f"  table size: {table_size}")
    print(f"  records stored: {record_count}")
    print(f"  load factor: {load_factor:.4f}")
    print(f"  wasted space: {wasted_space}")
    print(f"  collisions: {collisions}")
    print(f"  construction time: {construction_time:.6f} seconds")


def run_single_attempt(movie_records, attempt_settings):
    key_functions = [
        ("movie title", normalize_movie_title),
        ("movie quote", normalize_movie_quote),
    ]

    table_builders = [
        ("linked list", build_linked_list_hash_table),
        ("linear probing", build_linear_probing_hash_table),
    ]

    print(attempt_settings["label"])
    for table_label, builder in table_builders:
        for key_label, key_function in key_functions:
            table_name = f"{attempt_settings['label']} - {table_label} - {key_label}"
            builder_args = [attempt_settings["hash_function"], attempt_settings["table_size"]]
            if builder is build_linear_probing_hash_table:
                builder_args.append(attempt_settings["use_double_hashing"])

            hash_table, construction_time = measure_construction_time(
                builder,
                movie_records,
                key_function,
                *builder_args,
            )
            print_hash_table_statistics(table_name, hash_table, construction_time)
    print()


def run_hash_table_attempts(file_path):
    movie_records = load_movie_data(file_path)
    if not movie_records:
        print("No movie records were loaded.")
        return

    record_count = len(movie_records)

    active_attempt = {
        "label": "Attempt 1 - Poor hash + high load factor",
        "hash_function": poor_hash,
        "table_size": next_prime(record_count * 1.1),
        "use_double_hashing": False,
    }

    run_single_attempt(movie_records, active_attempt)


def main():
    file_path = "MOCK_DATA.csv"
    run_hash_table_attempts(file_path)


if __name__ == "__main__":
    main()
