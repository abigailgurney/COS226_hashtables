# COS226_hashtables

Reflection: 

A written reflection that discusses how well each of your 5 hash function methods
worked
• Analyze the statistics you collected for each approach
• Compare the performance of your different hash function approaches
• Discuss which methods were most effective and why



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