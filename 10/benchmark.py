import time
import random
from itertools import permutations


def brute_force(cost, n):

    min_cost = float('inf')

    for path in permutations(range(1, n)):

        current_cost = 0
        current = 0

        for next_location in path:
            current_cost += cost[current][next_location]
            current = next_location

        current_cost += cost[current][0]

        min_cost = min(min_cost, current_cost)

    return min_cost


def held_karp(cost, n):

    total_masks = 1 << n
    INF = float('inf')

    dp = [[INF] * n for _ in range(total_masks)]

    dp[1][0] = 0

    for mask in range(total_masks):

        if not (mask & 1):
            continue

        for i in range(n):

            if not (mask & (1 << i)):
                continue

            if dp[mask][i] == INF:
                continue

            for j in range(1, n):

                if not (mask & (1 << j)):

                    new_mask = mask | (1 << j)

                    dp[new_mask][j] = min(
                        dp[new_mask][j],
                        dp[mask][i] + cost[i][j]
                    )

    full_mask = total_masks - 1

    return min(
        dp[full_mask][i] + cost[i][0]
        for i in range(1, n)
    )

# Benchmark
print("TSP PERFORMANCE COMPARISON")
print("-" * 65)
print(f"{'Locations':<15}{'Brute Force (s)':<23}{'DP (s)':<15}")
print("-" * 65)

for n in [6, 8, 10, 12]:

    random.seed(42)

    cost = [[0 if i == j else random.randint(1, 100)
             for j in range(n)] for i in range(n)]

    start = time.perf_counter()
    brute_force(cost, n)
    brute_time = time.perf_counter() - start

    start = time.perf_counter()
    held_karp(cost, n)
    dp_time = time.perf_counter() - start

    print(f"{n:<15}{brute_time:<23.6f}{dp_time:<15.6f}")

print("-" * 65)
