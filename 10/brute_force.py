# Travelling Salesman Problem using Brute Force

from itertools import permutations


def tsp_brute_force(cost, n):

    min_cost = float('inf')
    best_route = []

    # Generate all permutations of locations except 0
    for path in permutations(range(1, n)):

        current_cost = 0
        current_location = 0

        # Calculate the cost of the route
        for next_location in path:

            current_cost += cost[current_location][next_location]
            current_location = next_location

        # Return to starting location
        current_cost += cost[current_location][0]

        # Update minimum cost
        if current_cost < min_cost:
            min_cost = current_cost
            best_route = [0] + list(path) + [0]

    return min_cost, best_route


# Main program
n = int(input("Enter number of locations: "))

print("Enter the cost matrix:")

cost = []

for i in range(n):
    row = list(map(int, input().split()))
    cost.append(row)

min_cost, route = tsp_brute_force(cost, n)

print("\nMinimum tour cost:", min_cost)
print("Optimal route:", " -> ".join(map(str, route)))
