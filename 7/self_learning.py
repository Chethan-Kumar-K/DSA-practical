import heapq
import random
import time

def generate_graph(n, edges):
    graph = [[] for _ in range(n)]

    added = 0

    while added < edges:
        u = random.randint(0, n - 1)
        v = random.randint(0, n - 1)

        # Avoid self-loops
        if u == v:
            continue

        weight = random.randint(1, 20)

        # Undirected graph
        graph[u].append((v, weight))
        graph[v].append((u, weight))

        added += 1

    return graph

def dijkstra_array(graph, source):
    n = len(graph)

    # Distance array
    dist = [float("inf")] * n
    dist[source] = 0

    # Visited array
    visited = [False] * n

    for _ in range(n):
        min_distance = float("inf")
        u = -1

        # Find the unvisited node with minimum distance
        for i in range(n):
            if not visited[i] and dist[i] < min_distance:
                min_distance = dist[i]
                u = i

        # No more reachable nodes
        if u == -1:
            break

        visited[u] = True

        # Relax all neighbours
        for neighbour, weight in graph[u]:
            if not visited[neighbour]:
                new_distance = dist[u] + weight

                if new_distance < dist[neighbour]:
                    dist[neighbour] = new_distance

    return dist

def dijkstra_heap(graph, source):
    n = len(graph)

    # Distance array
    dist = [float("inf")] * n
    dist[source] = 0

    # Min-heap starts with the source
    heap = [(0, source)]

    while heap:
        current_distance, u = heapq.heappop(heap)

        # Ignore outdated heap entries
        if current_distance > dist[u]:
            continue

        # Relax all neighbours
        for neighbour, weight in graph[u]:
            new_distance = current_distance + weight

            if new_distance < dist[neighbour]:
                dist[neighbour] = new_distance

                # Add updated distance to heap
                heapq.heappush(heap, (new_distance, neighbour))

    return dist

# Number of nodes and roads
n = 1000
edges = 3000
source = 0

print("Generating random graph...")
graph = generate_graph(n, edges)

print(f"Graph generated with {n} nodes and {edges} roads.\n")


# ---------------- ARRAY-BASED DIJKSTRA ----------------

start_time = time.perf_counter()

dist_array = dijkstra_array(graph, source)

end_time = time.perf_counter()

array_time = end_time - start_time


# ---------------- MIN-HEAP DIJKSTRA ----------------

start_time = time.perf_counter()

dist_heap = dijkstra_heap(graph, source)

end_time = time.perf_counter()

heap_time = end_time - start_time


# ---------------- RESULTS ----------------

print("Performance Comparison")
print("-" * 40)

print(f"Array-Based Dijkstra: {array_time:.6f} seconds")
print(f"Min-Heap Dijkstra   : {heap_time:.6f} seconds")

# Verify that both algorithms produce the same result
if dist_array == dist_heap:
    print("\nVerification: Both algorithms produced the same distances.")
else:
    print("\nVerification: Results are different.")