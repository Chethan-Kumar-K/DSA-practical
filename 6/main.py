import subprocess
import sys
from pathlib import Path

folder = Path(__file__).parent

print("\nSTEP 1: RUNNING EXPERIMENTS \n")

subprocess.run(
    [sys.executable, str(folder / "experiment.py")],
    check=True
)

print("\nSTEP 2: GENERATING GRAPH \n")

subprocess.run(
    [sys.executable, str(folder / "plot_results.py")],
    check=True
)

print("\nEXERCISE 6 COMPLETED \n")