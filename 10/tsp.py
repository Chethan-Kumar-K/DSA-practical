# Travelling Salesman Problem using Dynamic Programming
# Held-Karp Algorithm

import math

# Recurrence:
# dp[mask][i] = minimum cost to start at 0,
# visit all locations in mask, and end at i.
#
# dp[mask][i] = min(dp[mask without i][j] + cost[j][i])
#
# Base Case:
# dp[1][0] = 0
# Starting at location 0 has zero cost.

def tsp(cost, n):

    total_masks = 1 << n
    INF = math.inf

    # DP table
    dp = [[INF] * n for _ in range(total_masks)]

    # Parent table for route reconstruction
    parent = [[-1] * n for _ in range(total_masks)]

    # Base case: Start at location 0
    dp[1][0] = 0

    # Iterate through all possible subsets
    for mask in range(total_masks):

        # Only consider subsets containing location 0
        if not (mask & 1):
            continue

        for i in range(n):

            # Check whether location i is visited
            if not (mask & (1 << i)):
                continue

            if dp[mask][i] == INF:
                continue

            # Try visiting every unvisited location
            for j in range(1, n):

                if not (mask & (1 << j)):

                    new_mask = mask | (1 << j)

                    new_cost = dp[mask][i] + cost[i][j]

                    if new_cost < dp[new_mask][j]:

                        dp[new_mask][j] = new_cost
                        parent[new_mask][j] = i

    # All locations visited
    full_mask = total_masks - 1

    # Find minimum cost to return to location 0
    min_cost = INF
    last_location = -1

    for i in range(1, n):

        total_cost = dp[full_mask][i] + cost[i][0]

        if total_cost < min_cost:
            min_cost = total_cost
            last_location = i

    # Reconstruct optimal route
    route = []
    mask = full_mask
    current = last_location

    while current != 0:

        route.append(current)

        previous = parent[mask][current]

        mask ^= (1 << current)
        current = previous

    route.append(0)

    route.reverse()
    route.append(0)

    return min_cost, route


# Main program 
n = int(input("Enter number of locations: "))

print("Enter the cost matrix:")

cost = []

for i in range(n):
    row = list(map(int, input().split()))
    cost.append(row)

# Calculate optimal tour
min_cost, route = tsp(cost, n)

print("\nMinimum tour cost:", min_cost)

print("Optimal route:", " -> ".join(map(str, route)))
