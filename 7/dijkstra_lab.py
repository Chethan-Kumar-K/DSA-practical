def read_graph():
    print("\n1. Use Sample Input")
    print("2. Enter Custom Input")

    choice = input("Enter your choice: ")

    # ---------------- SAMPLE INPUT ----------------
    if choice == "1":
        n = 6

        graph = [[] for _ in range(n)]

        roads = [
            (0, 1, 4),
            (0, 2, 8),
            (1, 2, 2),
            (1, 3, 5),
            (2, 4, 10),
            (3, 4, 2),
            (3, 5, 6),
            (4, 5, 3)
        ]

        for u, v, w in roads:
            graph[u].append([v, w])
            graph[v].append([u, w])

        source = 0

        print("\nSample graph loaded successfully!")
        return graph, source

    # ---------------- CUSTOM INPUT ----------------
    elif choice == "2":
        n, m = map(
            int,
            input("Enter number of localities and roads (n m): ").split()
        )

        graph = [[] for _ in range(n)]

        print("Enter each road as: u v w")

        for _ in range(m):
            u, v, w = map(int, input().split())

            # Negative weights are not allowed
            if w < 0:
                print("Error: Negative edge weights are not allowed.")
                return None, None

            # Validate locality numbers
            if u < 0 or u >= n or v < 0 or v >= n:
                print("Error: Invalid locality number.")
                return None, None

            # Two-way road
            graph[u].append([v, w])
            graph[v].append([u, w])

        source = int(input("Enter source node: "))

        if source < 0 or source >= n:
            print("Error: Invalid source node.")
            return None, None

        return graph, source

    else:
        print("Invalid choice.")
        return None, None

def find_min_distance(dist, visited):
    min_distance = float("inf")
    min_node = -1

    for i in range(len(dist)):
        if not visited[i] and dist[i] < min_distance:
            min_distance = dist[i]
            min_node = i

    return min_node

def dijkstra(graph, source):
    n = len(graph)

    # Distance from source to every node
    dist = [float("inf")] * n

    # Parent array for reconstructing routes
    parent = [-1] * n

    # Keeps track of processed nodes
    visited = [False] * n

    # Distance from source to itself is 0
    dist[source] = 0

    for _ in range(n):

        # Find unvisited node with minimum distance
        u = find_min_distance(dist, visited)

        # No more reachable nodes
        if u == -1:
            break

        # Mark node as visited
        visited[u] = True

        # Check all neighbours of u
        for neighbour, weight in graph[u]:

            if not visited[neighbour]:

                new_distance = dist[u] + weight

                # Relaxation step
                if new_distance < dist[neighbour]:
                    dist[neighbour] = new_distance
                    parent[neighbour] = u

    return dist, parent

def get_path(parent, source, destination):
    path = []

    current = destination

    # Move backwards from destination to source
    while current != -1:
        path.append(current)

        if current == source:
            break

        current = parent[current]

    # If source was not reached, destination is unreachable
    if path[-1] != source:
        return None

    # Reverse the path manually
    left = 0
    right = len(path) - 1

    while left < right:
        path[left], path[right] = path[right], path[left]
        left += 1
        right -= 1

    return path

def print_results(dist, parent, source):
    locality_names = [
        "Hebbal Hub",
        "Indiranagar",
        "Koramangala",
        "MG Road",
        "Jayanagar",
        "Electronic City"
    ]

    print("\nShortest Travel Times and Routes")
    print("-" * 70)
    print(f"{'Locality':<25}{'Time (min)':<15}{'Route'}")
    print("-" * 70)

    for i in range(len(dist)):

        locality = str(i)

        # Add locality name if available
        if i < len(locality_names):
            locality += " " + locality_names[i]

        # Handle unreachable locality
        if dist[i] == float("inf"):
            print(f"{locality:<25}{'INF':<15}Not reachable")

        else:
            path = get_path(parent, source, i)

            # Convert path into route format
            route = ""

            for j in range(len(path)):
                route += str(path[j])

                if j != len(path) - 1:
                    route += " -> "

            print(f"{locality:<25}{dist[i]:<15}{route}")

def block_road(graph, u, v):
    road_found = False

    # Find and remove u -> v
    for i in range(len(graph[u])):
        if graph[u][i][0] == v:
            graph[u].pop(i)
            road_found = True
            break

    # Find and remove v -> u
    for i in range(len(graph[v])):
        if graph[v][i][0] == u:
            graph[v].pop(i)
            break

    return road_found

graph, source = read_graph()

if graph is not None:

    # Run Dijkstra before blocking a road
    dist, parent = dijkstra(graph, source)

    print_results(dist, parent, source)

    # Ask whether a road should be blocked
    choice = input("\nDo you want to block a road? (yes/no): ")

    if choice.lower() == "yes":
        u, v = map(
            int,
            input("Enter the road to block (u v): ").split()
        )

        # Validate node numbers
        if u < 0 or u >= len(graph) or v < 0 or v >= len(graph):
            print("Error: Invalid locality number.")

        else:
            # Store old distances before blocking
            old_dist = dist[:]

            # Block the road
road_found = block_road(graph, u, v)

if not road_found:
    print(f"\nError: Road {u} <-> {v} does not exist.")

else:
    print(f"\nRoad {u} <-> {v} has been blocked.")

    # Run Dijkstra again
    new_dist, new_parent = dijkstra(graph, source)

    print("\nUpdated Results:")
    print_results(new_dist, new_parent, source)

    # Show changed delivery times
    print("\nLocalities with changed delivery times:")

    changed = False

    for i in range(len(old_dist)):
        if old_dist[i] != new_dist[i]:
            print(
                f"Locality {i}: "
                f"{old_dist[i]} -> {new_dist[i]}"
            )
            changed = True

    if not changed:
        print("No delivery times changed.")