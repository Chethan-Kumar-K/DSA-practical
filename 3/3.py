import random
import time
# Algorithms:
# 1. Naive (Brute-Force) String Matching
# 2. Knuth-Morris-Pratt (KMP) String Matching

def validate_dna(text):
    """
    Checks whether the input contains only A, C, G and T.
    Returns True if valid, otherwise False.
    """

    valid_characters = {'A', 'C', 'G', 'T'}

    for ch in text:
        if ch not in valid_characters:
            return False

    return True


def naive_search(text, pattern):
    """
    Naive / Brute-Force String Matching.

    Returns:
        positions     -> list of starting indices
        comparisons   -> total number of character comparisons
    """

    positions = []
    comparisons = 0

    n = len(text)
    m = len(pattern)

    # If pattern is longer than text, no match is possible
    if m > n:
        return positions, comparisons

    # Check every possible starting position
    for i in range(n - m + 1):

        j = 0

        # Compare pattern with text character by character
        while j < m:

            comparisons += 1

            if text[i + j] != pattern[j]:
                break

            j += 1

        # Pattern completely matched
        if j == m:
            positions.append(i)

    return positions, comparisons


def compute_lps(pattern):
    """
    Computes the LPS (Longest Proper Prefix which is also Suffix)
    array for the KMP algorithm.
    """

    m = len(pattern)

    lps = [0] * m

    length = 0
    i = 1

    while i < m:

        if pattern[i] == pattern[length]:

            length += 1
            lps[i] = length
            i += 1

        else:

            if length != 0:
                length = lps[length - 1]

            else:
                lps[i] = 0
                i += 1

    return lps


def kmp_search(text, pattern):
    """
    Knuth-Morris-Pratt string matching algorithm.

    Returns:
        positions     -> list of starting indices
        comparisons   -> total number of character comparisons
    """

    positions = []
    comparisons = 0

    n = len(text)
    m = len(pattern)

    if m > n:
        return positions, comparisons

    # Build LPS array
    lps = compute_lps(pattern)

    i = 0   # Index for text
    j = 0   # Index for pattern

    while i < n:

        comparisons += 1

        if text[i] == pattern[j]:

            i += 1
            j += 1

            # Complete pattern found
            if j == m:

                positions.append(i - j)

                # Continue searching for overlapping matches
                j = lps[j - 1]

        else:

            if j != 0:

                # Do not move i backward
                j = lps[j - 1]

            else:

                i += 1

    return positions, comparisons

def dna_value(ch):
    """
    Converts a DNA character into a base-4 value.
    """

    if ch == 'A':
        return 0
    elif ch == 'C':
        return 1
    elif ch == 'G':
        return 2
    else:
        return 3


def rabin_karp_search(text, pattern):
    """
    Rabin-Karp string matching using:
    - Base 4
    - Large prime modulus

    Returns:
        positions      -> actual match positions
        comparisons    -> character comparisons during verification
        spurious_hits  -> hash matches that are not actual matches
    """

    positions = []
    comparisons = 0
    spurious_hits = 0

    n = len(text)
    m = len(pattern)

    if m > n:
        return positions, comparisons, spurious_hits

    base = 4
    prime = 1000000007

    # h = base^(m-1) % prime
    h = 1

    for _ in range(m - 1):
        h = (h * base) % prime

    # Calculate initial pattern hash
    pattern_hash = 0

    # Calculate initial text-window hash
    text_hash = 0

    for i in range(m):
        pattern_hash = (
            base * pattern_hash + dna_value(pattern[i])
        ) % prime

        text_hash = (
            base * text_hash + dna_value(text[i])
        ) % prime

    # Slide pattern over text
    for i in range(n - m + 1):

        # Hashes match
        if pattern_hash == text_hash:

            match = True

            # Verify actual characters
            for j in range(m):

                comparisons += 1

                if text[i + j] != pattern[j]:
                    match = False
                    break

            if match:
                positions.append(i)
            else:
                spurious_hits += 1

        # Calculate next rolling hash
        if i < n - m:

            text_hash = (
                base * (text_hash - dna_value(text[i]) * h)
                + dna_value(text[i + m])
            ) % prime

            if text_hash < 0:
                text_hash += prime

    return positions, comparisons, spurious_hits

def performance_comparison():
    print("\n========== PERFORMANCE COMPARISON ==========")

    # Random DNA test case
    random_text = ''.join(random.choice("ACGT") for _ in range(100000))
    random_pattern = ''.join(random.choice("ACGT") for _ in range(10))

    # Repetitive DNA test case
    repetitive_text = "A" * 100000
    repetitive_pattern = "A" * 10

    test_cases = [
        ("Random DNA", random_text, random_pattern),
        ("Repetitive DNA", repetitive_text, repetitive_pattern)
    ]

    for name, text, pattern in test_cases:
        print(f"\n{name}")
        print(f"Text length = {len(text)}")
        print(f"Pattern length = {len(pattern)}")

        # Naive
        start = time.perf_counter()
        _, naive_comparisons = naive_search(text, pattern)
        naive_time = time.perf_counter() - start

        # KMP
        start = time.perf_counter()
        _, kmp_comparisons = kmp_search(text, pattern)
        kmp_time = time.perf_counter() - start

        # Rabin-Karp
        start = time.perf_counter()
        _, rk_comparisons, _ = rabin_karp_search(text, pattern)
        rk_time = time.perf_counter() - start

        print("\nAlgorithm       Comparisons       Time (seconds)")
        print(f"Naive           {naive_comparisons:<17} {naive_time:.6f}")
        print(f"KMP             {kmp_comparisons:<17} {kmp_time:.6f}")
        print(f"Rabin-Karp      {rk_comparisons:<17} {rk_time:.6f}")


def print_result(label, positions, comparisons):
    """
    Prints the result in the required format.
    """

    if positions:
        position_text = " ".join(map(str, positions))
    else:
        position_text = "NONE"

    print(
        f"{label} : Positions = {position_text} "
        f"| Count = {len(positions)} "
        f"| Comparisons = {comparisons}"
    )


def main():

    # Read input
    text = input("enter text: ").strip()
    pattern = input("enter pattern: ").strip()

    # Validate DNA input
    if not validate_dna(text) or not validate_dna(pattern):
        print("Invalid input")
        return

    # Compute LPS
    lps = compute_lps(pattern)

    print("LPS Array :", *lps)

    # Naive search
    naive_positions, naive_comparisons = naive_search(
        text, pattern
    )

    print_result(
        "Naive",
        naive_positions,
        naive_comparisons
    )

    # KMP search
    kmp_positions, kmp_comparisons = kmp_search(
        text, pattern
    )

    print_result(
        "KMP",
        kmp_positions,
        kmp_comparisons
    )

    # Rabin-Karp search
    rk_positions, rk_comparisons, rk_spurious = rabin_karp_search(
        text, pattern
    )

    print_result(
        "Rabin-Karp",
        rk_positions,
        rk_comparisons
    )

    print(f"Rabin-Karp : Spurious Hits = {rk_spurious}")
    performance_comparison()

# Program starts here
if __name__ == "__main__":
    main()