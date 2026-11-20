import re

# 1. Build the LCS Dynamic Programming Table
def build_lcs_table(X, Y):
    m = len(X)
    n = len(Y)

    dp = [[0 for _ in range(n + 1)] for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if X[i - 1] == Y[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    return dp

# 2. Print the DP Table
def print_dp_table(dp):
    print("\nDP Table:")
    for row in dp:
        print(row)

# 3. Reconstruct the Actual LCS
def reconstruct_lcs(X, Y, dp):
    i = len(X)
    j = len(Y)
    lcs = []

    while i > 0 and j > 0:
        if X[i - 1] == Y[j - 1]:
            lcs.append(X[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1

    lcs.reverse()
    return lcs

# 4. Calculate Word-Level ROUGE-L
def calculate_rouge(reference, candidate):
    reference_words = re.findall(r"\b\w+\b", reference.lower())
    candidate_words = re.findall(r"\b\w+\b", candidate.lower())

    dp = build_lcs_table(reference_words, candidate_words)

    lcs_length = dp[len(reference_words)][len(candidate_words)]
    lcs_words = reconstruct_lcs(reference_words, candidate_words, dp)

    precision = (
        lcs_length / len(candidate_words)
        if candidate_words else 0.0
    )

    recall = (
        lcs_length / len(reference_words)
        if reference_words else 0.0
    )

    if precision + recall == 0:
        f1 = 0.0
    else:
        f1 = 2 * precision * recall / (precision + recall)

    return dp, lcs_length, lcs_words, precision, recall, f1

# 5. Space-Optimised LCS Using Two Rows
def lcs_two_rows(X, Y):
    # Keep the second sequence shorter to reduce memory usage
    if len(X) < len(Y):
        X, Y = Y, X

    m = len(X)
    n = len(Y)

    previous = [0] * (n + 1)

    for i in range(1, m + 1):
        current = [0] * (n + 1)

        for j in range(1, n + 1):
            if X[i - 1] == Y[j - 1]:
                current[j] = previous[j - 1] + 1
            else:
                current[j] = max(previous[j], current[j - 1])

        previous = current

    return previous[n]

# 6. Test Edge Cases
def test_edge_cases():
    test_cases = [
        ("hello world", "hello world"),
        ("", "hello world"),
        ("hello world", ""),
        ("apple banana", "cat dog"),
        ("a b a b", "b a b a")
    ]

    print("\n========== EDGE CASE TESTING ==========")

    for index, (reference, candidate) in enumerate(test_cases, start=1):
        result = calculate_rouge(reference, candidate)

        print(f"\nTest Case {index}")
        print("Reference:", reference)
        print("Candidate:", candidate)
        print("LCS Length:", result[1])
        print("LCS Words:", result[2])
        print("Precision:", round(result[3], 3))
        print("Recall:", round(result[4], 3))
        print("F1 Score:", round(result[5], 3))

# 7. Verify Space-Optimised LCS
def verify_two_rows():
    test_cases = [
        ("ABCBDAB", "BDCABA"),
        ("hello world", "hello world"),
        ("apple banana", "cat dog"),
        ("a b a b", "b a b a"),
        ("machine learning", "deep learning")
    ]

    print("\n========== TWO-ROW VERIFICATION ==========")

    for X, Y in test_cases:
        dp = build_lcs_table(X, Y)

        standard_length = dp[len(X)][len(Y)]
        optimised_length = lcs_two_rows(X, Y)

        print(f"\nX: {X}")
        print(f"Y: {Y}")
        print("Standard LCS Length:", standard_length)
        print("Two-Row LCS Length:", optimised_length)
        print("Match:", standard_length == optimised_length)

# 8. Main Batch Evaluation
def main():
    print("========== LCS AND ROUGE-L EVALUATION ==========")

    K = int(input("\nEnter number of summary pairs: "))

    results = []

    for i in range(K):
        print(f"\n========== SUMMARY PAIR {i + 1} ==========")

        reference = input("Enter reference summary: ")
        candidate = input("Enter candidate summary: ")

        dp, length, words, precision, recall, f1 = calculate_rouge(
            reference, candidate
        )

        print_dp_table(dp)

        print("\nLCS Length:", length)
        print("LCS Words:", " ".join(words))
        print("Precision:", round(precision, 3))
        print("Recall:", round(recall, 3))
        print("F1 Score:", round(f1, 3))

        results.append(f1)

    if results:
        print("\n========== BATCH RESULTS ==========")

        for i, score in enumerate(results, start=1):
            print(f"Pair {i} F1 Score: {score:.3f}")

        best_pair = results.index(max(results)) + 1

        print("\nBest Matching Pair:", best_pair)
        print("Highest F1 Score:", round(max(results), 3))

    test_edge_cases()
    verify_two_rows()

if __name__ == "__main__":
    main()
