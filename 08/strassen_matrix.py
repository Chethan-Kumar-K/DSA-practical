import random
import time
import matplotlib.pyplot as plt

# --------------------------------------------------
# Operation Counters
# --------------------------------------------------

strassen_multiplications = 0
strassen_additions = 0

# --------------------------------------------------
# Matrix Helper Functions
# --------------------------------------------------

def add_matrices(A, B):
    """Add two matrices and count scalar additions."""

    global strassen_additions

    n = len(A)

    result = [
        [0 for _ in range(n)]
        for _ in range(n)
    ]

    for i in range(n):
        for j in range(n):
            result[i][j] = A[i][j] + B[i][j]
            strassen_additions += 1

    return result


def subtract_matrices(A, B):
    """Subtract two matrices and count operations."""

    global strassen_additions

    n = len(A)

    result = [
        [0 for _ in range(n)]
        for _ in range(n)
    ]

    for i in range(n):
        for j in range(n):
            result[i][j] = A[i][j] - B[i][j]
            strassen_additions += 1

    return result


def split_matrix(A):
    """Split a matrix into four equal-sized submatrices."""
    n = len(A)
    mid = n // 2

    A11 = [row[:mid] for row in A[:mid]]
    A12 = [row[mid:] for row in A[:mid]]
    A21 = [row[:mid] for row in A[mid:]]
    A22 = [row[mid:] for row in A[mid:]]

    return A11, A12, A21, A22


def combine_matrices(C11, C12, C21, C22):
    """Combine four submatrices into one matrix."""

    top = [
        C11[i] + C12[i]
        for i in range(len(C11))
    ]

    bottom = [
        C21[i] + C22[i]
        for i in range(len(C21))
    ]

    return top + bottom


# --------------------------------------------------
# Classical Matrix Multiplication
# --------------------------------------------------

def classical_multiply(A, B):
    n = len(A)

    C = [[0 for _ in range(n)] for _ in range(n)]

    multiplications = 0
    additions = 0

    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]

                multiplications += 1
                additions += 1

    return C, multiplications, additions

# --------------------------------------------------
# Padding Functions
# --------------------------------------------------

def next_power_of_two(n):
    """Return the next power of two greater than or equal to n."""
    power = 1

    while power < n:
        power *= 2

    return power


def pad_matrix(A, size):
    """Pad a matrix with zeros up to the given size."""
    rows = len(A)
    cols = len(A[0])

    padded = [[0 for _ in range(size)] for _ in range(size)]

    for i in range(rows):
        for j in range(cols):
            padded[i][j] = A[i][j]

    return padded


def trim_matrix(A, rows, cols):
    """Trim a padded matrix back to the required size."""
    return [
        row[:cols]
        for row in A[:rows]
    ]

# --------------------------------------------------
# Strassen's Matrix Multiplication with Cutoff
# --------------------------------------------------

def strassen_multiply(A, B, threshold=2):
    n = len(A)

    # Switch to classical multiplication for small matrices
    if n <= threshold:
        result, multiplications, additions = classical_multiply(A, B)

        global strassen_multiplications
        global strassen_additions

        strassen_multiplications += multiplications
        strassen_additions += additions

        return result

    # Split matrices into four parts
    A11, A12, A21, A22 = split_matrix(A)
    B11, B12, B21, B22 = split_matrix(B)

    # --------------------------------------------------
    # Strassen's seven products
    # --------------------------------------------------

    # M1 = (A11 + A22)(B11 + B22)
    M1 = strassen_multiply(
        add_matrices(A11, A22),
        add_matrices(B11, B22),
        threshold
    )

    # M2 = (A21 + A22)B11
    M2 = strassen_multiply(
        add_matrices(A21, A22),
        B11,
        threshold
    )

    # M3 = A11(B12 - B22)
    M3 = strassen_multiply(
        A11,
        subtract_matrices(B12, B22),
        threshold
    )

    # M4 = A22(B21 - B11)
    M4 = strassen_multiply(
        A22,
        subtract_matrices(B21, B11),
        threshold
    )

    # M5 = (A11 + A12)B22
    M5 = strassen_multiply(
        add_matrices(A11, A12),
        B22,
        threshold
    )

    # M6 = (A21 - A11)(B11 + B12)
    M6 = strassen_multiply(
        subtract_matrices(A21, A11),
        add_matrices(B11, B12),
        threshold
    )

    # M7 = (A12 - A22)(B21 + B22)
    M7 = strassen_multiply(
        subtract_matrices(A12, A22),
        add_matrices(B21, B22),
        threshold
    )

    # --------------------------------------------------
    # Calculate result blocks
    # --------------------------------------------------

    # C11 = M1 + M4 - M5 + M7
    C11 = add_matrices(
        subtract_matrices(
            add_matrices(M1, M4),
            M5
        ),
        M7
    )

    # C12 = M3 + M5
    C12 = add_matrices(M3, M5)

    # C21 = M2 + M4
    C21 = add_matrices(M2, M4)

    # C22 = M1 - M2 + M3 + M6
    C22 = add_matrices(
        add_matrices(
            subtract_matrices(M1, M2),
            M3
        ),
        M6
    )

    return combine_matrices(C11, C12, C21, C22)

def strassen(A, B, threshold=2):
    """Multiply matrices using Strassen with automatic padding."""

    n = len(A)
    m = len(A[0])
    p = len(B[0])

    # Find the largest required dimension
    max_size = max(n, m, len(B), p)

    # Find the next power of two
    size = next_power_of_two(max_size)

    # Pad both matrices
    A_padded = pad_matrix(A, size)
    B_padded = pad_matrix(B, size)

    # Perform Strassen multiplication
    result_padded = strassen_multiply(
        A_padded,
        B_padded,
        threshold
    )

    # Trim the result to the original result size
    return trim_matrix(result_padded, n, p)


# --------------------------------------------------
# Display Function
# --------------------------------------------------

def print_matrix(matrix):
    for row in matrix:
        print(row)


# --------------------------------------------------
# Random Matrix Generator
# --------------------------------------------------

def generate_random_matrix(n):
    """Generate an n × n matrix with random integers."""

    return [
        [random.randint(1, 10) for _ in range(n)]
        for _ in range(n)
    ]

# --------------------------------------------------
# Benchmark Function
# --------------------------------------------------

def run_benchmark(threshold=32):

    sizes = [2, 4, 8, 16, 32, 64, 128, 256, 512]

    classical_times = []
    strassen_times = []

    print("\n" + "=" * 80)
    print("BENCHMARK RESULTS")
    print("=" * 80)

    print(
        f"{'Size':<10}"
        f"{'Classical (s)':<20}"
        f"{'Strassen (s)':<20}"
        f"{'Validation':<15}"
    )

    print("-" * 80)

    for n in sizes:

        print(f"Testing {n} × {n}...", end=" ", flush=True)

        # Generate random matrices
        A = generate_random_matrix(n)
        B = generate_random_matrix(n)

        # -------------------------------
        # Classical multiplication timing
        # -------------------------------

        start = time.perf_counter()

        classical_result, _, _ = classical_multiply(A, B)

        classical_time = time.perf_counter() - start

        # -------------------------------
        # Strassen multiplication timing
        # -------------------------------

        start = time.perf_counter()

        strassen_result = strassen(A, B, threshold)

        strassen_time = time.perf_counter() - start

        # -------------------------------
        # Validation
        # -------------------------------

        if classical_result == strassen_result:
            validation = "PASS"
        else:
            validation = "FAIL"

        classical_times.append(classical_time)
        strassen_times.append(strassen_time)

        print("Done")

        print(
            f"{n:<10}"
            f"{classical_time:<20.6f}"
            f"{strassen_time:<20.6f}"
            f"{validation:<15}"
        )

    # --------------------------------
    # Plot the graph
    # --------------------------------

    plt.figure(figsize=(10, 6))

    plt.plot(
        sizes,
        classical_times,
        marker="o",
        label="Classical Multiplication"
    )

    plt.plot(
        sizes,
        strassen_times,
        marker="s",
        label="Strassen Multiplication"
    )

    plt.xlabel("Matrix Size (n)")
    plt.ylabel("Execution Time (seconds)")
    plt.title("Classical vs Strassen Matrix Multiplication")
    plt.legend()
    plt.grid(True)

    plt.savefig("matrix_multiplication_comparison.png")

    plt.show()


######


# --------------------------------------------------
# Self-Learning: Cutoff Threshold Experiment
# --------------------------------------------------

def find_best_threshold():

    # Matrix size used for the experiment
    matrix_size = 256

    # Different cutoff values to test
    thresholds = [1, 2, 4, 8, 16, 32, 64]

    print("\n" + "=" * 70)
    print("SELF-LEARNING: CUTOFF THRESHOLD EXPERIMENT")
    print("=" * 70)

    print(f"Matrix Size: {matrix_size} × {matrix_size}")
    print(f"{'Threshold':<15}{'Strassen Time (seconds)':<25}")
    print("-" * 70)

    # Generate the SAME matrices for every threshold
    A = generate_random_matrix(matrix_size)
    B = generate_random_matrix(matrix_size)

    results = []

    for threshold in thresholds:

        start = time.perf_counter()

        result = strassen(A, B, threshold)

        execution_time = time.perf_counter() - start

        results.append((threshold, execution_time))

        print(f"{threshold:<15}{execution_time:<25.6f}")

    # Find the best threshold
    best_threshold, best_time = min(results, key=lambda x: x[1])

    print("-" * 70)
    print(f"Best Threshold: {best_threshold}")
    print(f"Best Time: {best_time:.6f} seconds")

    return results, best_threshold


#######


# --------------------------------------------------
# Sample Test
# --------------------------------------------------

if __name__ == "__main__":

    A = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
    ]

    B = [
    [9, 8, 7],
    [6, 5, 4],
    [3, 2, 1]
    ]

    print("Matrix A:")
    print_matrix(A)

    print("\nMatrix B:")
    print_matrix(B)

    # Classical multiplication
    classical_result, multiplications, additions = classical_multiply(A, B)

    print("\nClassical Result:")
    print_matrix(classical_result)

    # Strassen multiplication
    strassen_multiplications = 0
    strassen_additions = 0

    threshold = 2
    print(f"\nCutoff Threshold: {threshold}")

    strassen_result = strassen(A, B, threshold)

    print("\nStrassen Result:")
    print_matrix(strassen_result)

    print(f"\nStrassen Scalar Multiplications: {strassen_multiplications}")
    print(f"Strassen Additions/Subtractions: {strassen_additions}")

    # Validation
    if classical_result == strassen_result:
        print("\nValidation: PASS")
    else:
        print("\nValidation: FAIL")

    print("\nStarting full benchmark...")

    benchmark_threshold = 32

    run_benchmark(benchmark_threshold)

print("\nStarting cutoff threshold experiment...")

threshold_results, best_threshold = find_best_threshold()