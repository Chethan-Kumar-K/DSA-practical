import sys
import time
import random
import math
import csv

from bst import BST
from avl import AVL
from workload import generate_all_workloads

# Handle deep recursion in the plain BST
sys.setrecursionlimit(20000)


def run_experiment(n, dataset_name, ids):

    results = []

    # Same search and deletion samples for both trees
    rng = random.Random(42 + n)

    search_ids = rng.sample(ids, 1000)
    delete_ids = rng.sample(ids, int(n * 0.20))

    for tree_name, TreeClass in [
        ("BST", BST),
        ("AVL", AVL)
    ]:

        tree = TreeClass()

        # Measure insertion time
        start = time.perf_counter()

        for patient_id in ids:
            tree.insert(patient_id, f"Patient-{patient_id}")

        insertion_time = time.perf_counter() - start

        # Calculate height after insertion
        if tree_name == "BST":
            final_height = tree.height(tree.root)
            rotations = "N/A"
        else:
            final_height = tree.get_height(tree.root)
            rotations = tree.rotations

        # Measure average successful search comparisons
        total_search_comparisons = 0

        for patient_id in search_ids:
            before = tree.comparisons

            result = tree.search(patient_id)

            after = tree.comparisons

            assert result is not None

            total_search_comparisons += after - before

        average_comparisons = (
            total_search_comparisons / len(search_ids)
        )

        # Delete 20% of the patient IDs
        for patient_id in delete_ids:
            tree.delete(patient_id)

        # Calculate height after deletion
        if tree_name == "BST":
            deletion_height = tree.height(tree.root)
        else:
            deletion_height = tree.get_height(tree.root)

        results.append({
            "Tree": tree_name,
            "Dataset": dataset_name,
            "N": n,
            "Height": final_height,
            "Minimum Height": math.floor(math.log2(n)),
            "Insertion Time": round(insertion_time, 6),
            "Rotations": rotations,
            "Avg Search Comparisons": round(average_comparisons, 2),
            "Height After Deletion": deletion_height
        })

    return results


def main():

    sizes = [1000, 5000, 10000]

    all_results = []

    for n in sizes:

        datasets = generate_all_workloads(n)

        for dataset_name, ids in datasets.items():

            print(f"\nRunning {dataset_name}, N={n}")

            results = run_experiment(
                n, dataset_name, ids
            )

            all_results.extend(results)

    # Print comparison table
    print("\n========== EXPERIMENT RESULTS ==========\n")

    headers = [
        "Tree", "Dataset", "N", "Height",
        "Min Height", "Insert Time",
        "Rotations", "Avg Comparisons",
        "Height After Delete"
    ]

    print("{:<8} {:<15} {:<7} {:<8} {:<11} {:<13} {:<11} {:<17} {:<12}".format(
        *headers
    ))

    for row in all_results:

        print("{:<8} {:<15} {:<7} {:<8} {:<11} {:<13} {:<11} {:<17} {:<12}".format(
            row["Tree"],
            row["Dataset"],
            row["N"],
            row["Height"],
            row["Minimum Height"],
            row["Insertion Time"],
            row["Rotations"],
            row["Avg Search Comparisons"],
            row["Height After Deletion"]
        ))

    # Export results to CSV
    with open("results.csv", "w", newline="") as file:

        writer = csv.DictWriter(
            file, fieldnames=all_results[0].keys()
        )

        writer.writeheader()
        writer.writerows(all_results)

    print("\nResults saved to results.csv")


if __name__ == "__main__":
    main()
