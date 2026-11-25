import csv
from pathlib import Path
import matplotlib.pyplot as plt

# Locate results.csv in the same folder as this script
folder = Path(__file__).parent
csv_file = folder / "results.csv"

data = {}

# Read experiment results
with open(csv_file, "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        key = (row["Dataset"], row["Tree"])
        data.setdefault(key, {"N": [], "Height": []})

        data[key]["N"].append(int(row["N"]))
        data[key]["Height"].append(int(row["Height"]))

# Create three graphs
datasets = ["Sequential", "Random", "Nearly Sorted"]

fig, axes = plt.subplots(1, 3, figsize=(16, 5))

for ax, dataset in zip(axes, datasets):

    for tree in ["BST", "AVL"]:
        values = data[(dataset, tree)]

        ax.plot(
            values["N"],
            values["Height"],
            marker="o",
            label=tree
        )

    ax.set_title(dataset)
    ax.set_xlabel("Number of Patient IDs (N)")
    ax.set_ylabel("Tree Height")
    ax.legend()
    ax.grid(True)

fig.suptitle("BST vs AVL Tree Height Comparison")
plt.tight_layout()

output_file = folder / "tree_height_comparison.png"
plt.savefig(output_file, dpi=300)

print(f"Graph saved to: {output_file}")