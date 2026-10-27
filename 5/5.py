from collections import deque

# Read input
V, E = map(int, input("Enter number of zones and roads (V E): ").split())

# Create vertices A, B, C, ...
vertices = [chr(ord('A') + i) for i in range(V)]
graph = {vertex: [] for vertex in vertices}

# Read roads
print("\nEnter the roads (example: A B):")
for i in range(E):
    u, v = input(f"Enter road {i + 1}: ").split()
    graph[u].append(v)
    graph[v].append(u)

# Read source and target
S, T = input("\nEnter source zone and target zone (S T): ").split()

# Sort neighbours alphabetically
for vertex in graph:
    graph[vertex].sort()

# 1. Print adjacency list
print("\n1. Adjacency List")
for vertex in graph:
    print(f"{vertex}: {graph[vertex]}")

# 2. BFS: visiting order, levels and waves
def bfs(graph, source):
    visited = {source}
    distance = {source: 0}
    parent = {source: None}
    queue = deque([source])
    order = []

    while queue:
        current = queue.popleft()
        order.append(current)

        for neighbour in graph[current]:
            if neighbour not in visited:
                visited.add(neighbour)
                distance[neighbour] = distance[current] + 1
                parent[neighbour] = current
                queue.append(neighbour)

    return order, distance, parent

bfs_order, distance, parent = bfs(graph, S)

print("\n2. BFS Visiting Order")
print(" -> ".join(bfs_order))

print("\nDistances from", S)
for vertex in vertices:
    if vertex in distance:
        print(f"{vertex}: {distance[vertex]} road(s)")
    else:
        print(f"{vertex}: Unreachable")

print("\nDispatch Waves")
for level in range(max(distance.values()) + 1):
    wave = [v for v in bfs_order if distance[v] == level]
    print(f"Wave {level}: {wave}")

# 3. Reconstruct shortest route using BFS parents
print(f"\n3. Fewest-Roads Route: {S} to {T}")

if T not in distance:
    print("Target is unreachable from the source.")
else:
    route = []
    current = T

    while current is not None:
        route.append(current)
        current = parent[current]

    route.reverse()
    print("Route:", " -> ".join(route))
    print("Route length:", distance[T], "road(s)")

# 4. DFS from source
def dfs(graph, source):
    visited = set()
    order = []

    def explore(vertex):
        visited.add(vertex)
        order.append(vertex)

        for neighbour in graph[vertex]:
            if neighbour not in visited:
                explore(neighbour)

    explore(source)
    return order

print("\n4. DFS Visiting Order")
print(" -> ".join(dfs(graph, S)))

# 5. Find connected components
def connected_components(graph, vertices):
    visited = set()
    components = []

    for vertex in vertices:
        if vertex not in visited:
            component = []
            stack = [vertex]
            visited.add(vertex)

            while stack:
                current = stack.pop()
                component.append(current)

                for neighbour in reversed(graph[current]):
                    if neighbour not in visited:
                        visited.add(neighbour)
                        stack.append(neighbour)

            components.append(sorted(component))

    return components

components = connected_components(graph, vertices)

print("\n5. Connected Components")
print("Number of components:", len(components))

for i, component in enumerate(components, start=1):
    print(f"Component {i}: {component}")

unreachable = [v for v in vertices if v not in distance]
print("Zones unreachable from", S, ":", unreachable)

# 6. Detect a cycle and return one example
def find_cycle(graph, vertices):
    visited = set()
    parent = {}

    def explore(vertex, previous):
        visited.add(vertex)
        parent[vertex] = previous

        for neighbour in graph[vertex]:
            if neighbour not in visited:
                cycle = explore(neighbour, vertex)
                if cycle:
                    return cycle
            elif neighbour != previous:
                # Reconstruct the cycle from the DFS tree
                path = [vertex]
                current = vertex

                while current != neighbour and current is not None:
                    current = parent[current]
                    if current is not None:
                        path.append(current)

                if current == neighbour:
                    path.reverse()
                    path.append(neighbour)
                    return path

        return None

    for vertex in vertices:
        if vertex not in visited:
            cycle = explore(vertex, None)
            if cycle:
                return cycle

    return None

print("\n6. Cycle Detection")
cycle = find_cycle(graph, vertices)

if cycle:
    print("Cycle detected: YES")
    print("Example cycle:", " -> ".join(cycle))
else:
    print("Cycle detected: NO")
