# COS226_hashtables

## Reflection: Hash Function Performance Analysis

**Attempt 1 - Poor Hash + High Load**: poor_hash produced 14,798 collisions with linked list and 110M+ with linear probing. High load factor (0.9080) and weak hash function caused severe clustering.

**Attempt 2 - Polynomial Hash + High Load**: polynomial_hash improved to 6,814 collisions (linked list) and 77-108k (linear probing). Better distribution but still affected by high load factor.

**Attempt 3 - FNV-1a + High Load**: FNV-1a similar to polynomial_hash (~6,880 linked list, ~70-110k probing). Shows that hash function quality alone cannot overcome high load factor problems.

**Attempt 4 - FNV-1a + Lower Load**: Lowering load factor to 0.3333 reduced collisions to 5,017 (linked list) and 3,885-10,553 (probing). Load factor has more impact than hash function choice.

**Attempt 5 - FNV-1a + Lower Load + Double Hashing**: Best results with 4,715 (linked list) and 2,431-7,252 (probing) collisions. Double hashing further reduces clustering.

**Key Findings**:
- Load factor matters more than hash function quality
- Linked list chaining consistently better than linear probing
- Better hash functions reduce collisions but cannot fix clustering at high load
- Combining better hash + lower load + double hashing minimizes collisions most effectively


Intresting reading done along side assignment:
https://mojoauth.com/compare-hashing-algorithms/fnv-1a-vs-dhash#what-is-fnv-1a
https://codeforces.com/blog/entry/100027

Attempt 1 - Poor hash + high load factor
Strategy       | Key         | Table Size | Records | Load   | Wasted | Collisions | Time (s)
---------------+-------------+------------+---------+--------+--------+------------+---------
linked list    | movie title | 16519      | 15000   | 0.9080 | 16317  | 14798      | 0.007097
linked list    | movie quote | 16519      | 15000   | 0.9080 | 16447  | 14928      | 0.006053
linear probing | movie title | 16519      | 15000   | 0.9080 | 1519   | 110637689  | 2.950748
linear probing | movie quote | 16519      | 15000   | 0.9080 | 1519   | 111951273  | 2.986412


Attempt 2 - Polynomial hash + high load factor
Strategy       | Key         | Table Size | Records | Load   | Wasted | Collisions | Time (s)
---------------+-------------+------------+---------+--------+--------+------------+---------
linked list    | movie title | 16519      | 15000   | 0.9080 | 8333   | 6814       | 0.016264
linked list    | movie quote | 16519      | 15000   | 0.9080 | 6686   | 5167       | 0.019632
linear probing | movie title | 16519      | 15000   | 0.9080 | 1519   | 108849     | 0.016600
linear probing | movie quote | 16519      | 15000   | 0.9080 | 1519   | 77016      | 0.021159


Attempt 3 - FNV-1a hash + high load factor
Strategy       | Key         | Table Size | Records | Load   | Wasted | Collisions | Time (s)
---------------+-------------+------------+---------+--------+--------+------------+---------
linked list    | movie title | 16519      | 15000   | 0.9080 | 8399   | 6880       | 0.031567
linked list    | movie quote | 16519      | 15000   | 0.9080 | 6693   | 5174       | 0.052919
linear probing | movie title | 16519      | 15000   | 0.9080 | 1519   | 110047     | 0.033703
linear probing | movie quote | 16519      | 15000   | 0.9080 | 1519   | 70447      | 0.050449

Attempt 4 - FNV-1a hash + lower load factor
Strategy       | Key         | Table Size | Records | Load   | Wasted | Collisions | Time (s)
---------------+-------------+------------+---------+--------+--------+------------+---------
linked list    | movie title | 45007      | 15000   | 0.3333 | 35024  | 5017       | 0.032986
linked list    | movie quote | 45007      | 15000   | 0.3333 | 32366  | 2359       | 0.062701
linear probing | movie title | 45007      | 15000   | 0.3333 | 30007  | 10553      | 0.031673
linear probing | movie quote | 45007      | 15000   | 0.3333 | 30007  | 3885       | 0.047124


Attempt 5 - FNV-1a + lower load + double hashing
Strategy       | Key         | Table Size | Records | Load   | Wasted | Collisions | Time (s)
---------------+-------------+------------+---------+--------+--------+------------+---------
linked list    | movie title | 60013      | 15000   | 0.2499 | 49728  | 4715       | 0.032956
linked list    | movie quote | 60013      | 15000   | 0.2499 | 46870  | 1857       | 0.049757
linear probing | movie title | 60013      | 15000   | 0.2499 | 45013  | 7252       | 0.037849
linear probing | movie quote | 60013      | 15000   | 0.2499 | 45013  | 2431       | 0.061851
