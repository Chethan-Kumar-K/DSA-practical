import random


def generate_sequential(n):
    return list(range(1, n + 1))


def generate_random(n, seed=42):
    ids = list(range(1, n + 1))

    rng = random.Random(seed)
    rng.shuffle(ids)

    return ids


def generate_nearly_sorted(n, seed=42):
    ids = list(range(1, n + 1))

    rng = random.Random(seed)

    # Select approximately 5% of positions
    count = int(n * 0.05)

    positions = rng.sample(range(n), count)

    # Swap selected positions in pairs
    for i in range(0, count - 1, 2):
        a = positions[i]
        b = positions[i + 1]

        ids[a], ids[b] = ids[b], ids[a]

    return ids


def generate_all_workloads(n, seed=42):
    return {
        "Sequential": generate_sequential(n),
        "Random": generate_random(n, seed),
        "Nearly Sorted": generate_nearly_sorted(n, seed)
    }


if __name__ == "__main__":

    sizes = [1000, 5000, 10000]

    for n in sizes:
        datasets = generate_all_workloads(n)

        print(f"\nDataset Size: {n}")

        for name, ids in datasets.items():
            print(f"\n{name}:")
            print("First 10 IDs:", ids[:10])
            print("Total IDs:", len(ids))
            print("Unique IDs:", len(set(ids)))
