import random
import time



def recursive_sum(arr):
    """
    Recursively sum the elements of arr.

    Base case: an empty list sums to 0.
    Recursive case: add the first element to recursive_sum of the rest.
    """
    if not arr:
        return 0

    return arr[0] + recursive_sum(arr[1:])


def recursive_count(arr):
    """
    Recursively count the number of elements in arr.

    Base case: an empty list contains 0 elements.
    Recursive case: count 1 plus recursive_count of the rest.
    """
    if not arr:
        return 0

    return 1 + recursive_count(arr[1:])


def recursive_max(arr):
    """
    Recursively find the maximum value in arr.

    Error case: an empty list has no maximum -- raise ValueError.
    Base case: a single-element list returns that element.
    Recursive case: compare the first element to the maximum of the rest.
    """
    if not arr:
        raise ValueError("An empty list has no maximum")

    if len(arr) == 1:
        return arr[0]

    max_of_rest = recursive_max(arr[1:])

    if arr[0] > max_of_rest:
        return arr[0]

    return max_of_rest


def binary_search_recursive(arr, target):
    """
    Recursively search for target in a SORTED list arr.
    Return the index of target if found, else -1.

    Base case: the search range is empty, or the target is found.
    Recursive case: search either the left half or right half.
    """
    def helper(low, high):
        if low > high:
            return -1

        mid = (low + high) // 2

        if arr[mid] == target:
            return mid
        elif target < arr[mid]:
            return helper(low, mid - 1)
        else:
            return helper(mid + 1, high)

    return helper(0, len(arr) - 1)


# ---------------------------------------------------------------------------
# PART 2: Quicksort
# ---------------------------------------------------------------------------

def quicksort(array, pivot_strategy="first"):
    """
    Sort array using the quicksort divide-and-conquer algorithm.
    Return a NEW list. Do not modify the caller's list.

    pivot_strategy: one of "first", "random", "middle"
        "first"  -- standard tier: pivot index 0
        "random" -- stretch tier: random.randrange(len(array))
        "middle" -- stretch tier: len(array) // 2
    Any other value must raise ValueError.

    Base case: an array with fewer than 2 elements is already sorted.
    Recursive case: pick a pivot, partition the remaining values, recursively
    sort both partitions, and combine them.
    """
    if len(array) < 2:
        return list(array)

    if pivot_strategy == "first":
        pivot_index = 0
    elif pivot_strategy == "random":
        pivot_index = random.randrange(len(array))
    elif pivot_strategy == "middle":
        pivot_index = len(array) // 2
    else:
        raise ValueError("Unknown pivot strategy")

    pivot = array[pivot_index]

    rest = array[:pivot_index] + array[pivot_index + 1:]

    less = [value for value in rest if value < pivot]
    greater_or_equal = [value for value in rest if value >= pivot]

    return (
        quicksort(less, pivot_strategy)
        + [pivot]
        + quicksort(greater_or_equal, pivot_strategy)
    )


# ---------------------------------------------------------------------------
# PART 3: Empirical worst-case vs average-case investigation
# ---------------------------------------------------------------------------

def measure_time(arr, pivot_strategy):
    """
    Time how long quicksort takes to sort a COPY of arr using the given
    pivot_strategy.

    Return:
      - the elapsed time in seconds (a nonnegative float), or
      - None if the sort reached Python's recursion limit.

    A poor pivot on already-ordered data produces one-sided partitions and a
    recursion depth of about n, which can exceed Python's limit. That is a real
    experimental result for this lab, not a bug -- report it, do not hide it by
    raising the global recursion limit.
    """
    start = time.perf_counter()

    try:
        result = quicksort(list(arr), pivot_strategy)
    except RecursionError:
        return None

    elapsed = time.perf_counter() - start

    if result != sorted(arr):
        raise RuntimeError("Quicksort produced an incorrect result")

    return elapsed


def run_benchmark(unsorted_list, sorted_list, reverse_sorted_list):
    """
    For each input shape (unsorted, sorted, reverse-sorted) and each pivot
    strategy ("first", "random"), measure the quicksort run time and print one
    tabulated row per combination.

    All six rows must print. When measure_time returns None, print
    "RecursionError" for that row and CONTINUE with the remaining cases.

    Students should observe:
      - "first" pivot on sorted/reverse-sorted data is much slower (O(n^2))
        and may not finish at all before hitting the recursion limit
      - "random" pivot removes that worst-case behavior on average
    """
    input_shapes = {
        "unsorted": unsorted_list,
        "sorted": sorted_list,
        "reverse sorted": reverse_sorted_list,
    }
    pivot_strategies = ["first", "random"]

    print(f"{'Shape':<18} {'Strategy':<12} {'Result'}")

    for shape_name, data in input_shapes.items():
        for strategy in pivot_strategies:
            elapsed = measure_time(data, strategy)

            if elapsed is None:
                result_text = "RecursionError"
            else:
                result_text = f"{elapsed:.6f} s"

            print(f"{shape_name:<18} {strategy:<12} {result_text}")


# ---------------------------------------------------------------------------
# Entry point -- this scaffolding is already written for you. Do not change the
# function name, the data it builds, or the guard below.
# ---------------------------------------------------------------------------

def main():
    # Seeded so the random pivot and the shuffled list are reproducible for
    # everyone in the class.
    random.seed(42)

    sample_numbers = [4, 7, 1, 9, 3, 8, 2, 6, 5, 10, 0, -3]

    print("Part 1: Divide & Conquer warm-ups")
    print("recursive_sum:", recursive_sum(sample_numbers))
    print("recursive_count:", recursive_count(sample_numbers))
    print("recursive_max:", recursive_max(sample_numbers))

    sorted_sample = sorted(sample_numbers)

    print(
        "binary_search_recursive (target=8):",
        binary_search_recursive(sorted_sample, 8),
    )
    print(
        "binary_search_recursive (target=99):",
        binary_search_recursive(sorted_sample, 99),
    )

    print("\nPart 2: Quicksort")
    print("first pivot:", quicksort(sample_numbers, "first"))
    print("random pivot:", quicksort(sample_numbers, "random"))
    print("middle pivot:", quicksort(sample_numbers, "middle"))

    print("\nPart 3: Benchmark")

    # All three shapes hold the SAME values in different orders, so any timing
    # difference comes from the ordering and the pivot rule -- nothing else.
    n = 1000

    sorted_list = list(range(n))
    reverse_sorted_list = list(reversed(sorted_list))
    unsorted_list = sorted_list.copy()
    random.shuffle(unsorted_list)

    run_benchmark(
        unsorted_list,
        sorted_list,
        reverse_sorted_list,
    )


if __name__ == "__main__":
    main()
