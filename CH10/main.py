"""
Lab: "Good Enough" -- Greedy Algorithms and Approximation

Three parts:
  Part 1: Greedy gets it exactly right -- classroom scheduling
  Part 2: Greedy gets it wrong -- 0/1 knapsack counterexample
  Part 3: When exact isn't an option -- set covering + subset counting

All data below is hardcoded (no randomness, no file I/O) so results are
reproducible and gradeable.
"""

import itertools


# ---------------------------------------------------------------------------
# Part 1: Greedy gets it exactly right -- classroom scheduling
# ---------------------------------------------------------------------------

def schedule_classes(classes):
    """Given a list of (name, start, end) tuples, greedily pick classes so
    that no two scheduled classes overlap, and as many classes as possible
    get scheduled.

    TODO: State the greedy rule this function uses in ONE sentence as a
    comment right here (e.g. "pick the one that ends soonest").

    TODO: Implement the greedy algorithm:
      1. Sort the classes by end time.
      2. Walk through them in that order.
      3. Keep a class if its start time is not before the end time of the
         last class you kept.
      4. Return the list of kept (name, start, end) tuples, in the order
         they were scheduled.
    """
    # Greedy rule: always pick the class that ends soonest.
    scheduled = []
    last_end_time = float("-inf")

    sorted_classes = sorted(classes, key=lambda class_info: class_info[2])

    for class_info in sorted_classes:
        name, start, end = class_info

        if start >= last_end_time:
            scheduled.append(class_info)
            last_end_time = end

    return scheduled


# ---------------------------------------------------------------------------
# Part 2: Greedy gets it wrong -- the knapsack counterexample
# ---------------------------------------------------------------------------

def greedy_knapsack(items, capacity):
    """items: list of (name, value, weight) tuples.
    Greedily grab the most valuable item that still fits in the remaining
    capacity, repeat until nothing else fits.

    TODO: Implement the greedy strategy:
      1. Sort items by value, highest first.
      2. Walk through them in that order.
      3. If an item's weight fits in the remaining capacity, take it and
         subtract its weight from the remaining capacity.
      4. Return (chosen_items, total_value) where chosen_items is a list
         of the item tuples taken.
    """
    chosen_items = []
    total_value = 0
    remaining_capacity = capacity

    sorted_items = sorted(items, key=lambda item: item[1], reverse=True)

    for item in sorted_items:
        name, value, weight = item

        if weight <= remaining_capacity:
            chosen_items.append(item)
            total_value += value
            remaining_capacity -= weight

    return chosen_items, total_value


def brute_force_knapsack(items, capacity):
    """items: list of (name, value, weight) tuples.
    Check every possible subset (use itertools.combinations) and return the
    subset with the highest total value that still fits under capacity.

    Keep this to at most 15 items in practice (2^15 subsets is fast).

    TODO: Implement the brute-force search:
      1. For every subset size from 0 to len(items):
         - For every combination of that size (itertools.combinations):
           - Sum the weights; if the subset fits under capacity, sum the
             values too.
           - Track the best (highest-value) subset seen so far.
      2. Return (best_items, best_value).
    """
    best_items = []
    best_value = 0

    for subset_size in range(len(items) + 1):
        for combination in itertools.combinations(items, subset_size):
            total_weight = sum(item[2] for item in combination)

            if total_weight <= capacity:
                total_value = sum(item[1] for item in combination)

                if total_value > best_value:
                    best_value = total_value
                    best_items = list(combination)

    return best_items, best_value


# ---------------------------------------------------------------------------
# Part 3: When exact isn't an option -- set covering
# ---------------------------------------------------------------------------

def greedy_set_cover(states_needed, stations):
    """states_needed: a set of states that must be covered.
    stations: a dict mapping station name -> set of states it covers.

    Repeatedly pick the station that covers the most still-uncovered
    states, until every needed state is covered.

    TODO: Implement the greedy set-cover algorithm:
      1. Make a copy of states_needed to track what's left to cover.
      2. While there are still states left to cover:
         a. Find the station whose set of states, intersected with what's
            left, is the largest (use set intersection).
         b. Add that station's name to the result list, in order chosen.
         c. Remove the states that station covers from what's left
            (use set difference).
      3. Return the list of chosen station names, in the order picked.
    """
    final_stations = []
    states_left = states_needed.copy()

    while states_left:
        best_station = None
        states_covered = set()

        for station, states in stations.items():
            covered = states_left & states

            if len(covered) > len(states_covered):
                best_station = station
                states_covered = covered

        if best_station is None:
            break

        final_stations.append(best_station)
        states_left = states_left - states_covered

    return final_stations


def count_subsets(n):
    """Return the number of possible subsets of n items (2**n).

    This is what an exact set-cover / knapsack solver would have to check
    in the worst case -- we print the count instead of ever computing it
    for large n, since 2**100 subsets can never actually be enumerated.

    TODO: Return 2 ** n.
    """
    return 2 ** n


# ---------------------------------------------------------------------------
# Entry point -- deterministic, hardcoded data from the book's examples
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # --- Part 1 data: the book's five-class scheduling table ---
    classes = [
        ("Art", 9.0, 10.0),
        ("English", 9.5, 10.5),
        ("Math", 10.0, 11.0),
        ("CS", 10.5, 11.5),
        ("Music", 11.0, 12.0),
    ]

    scheduled = schedule_classes(classes)
    print("Part 1: Scheduled classes")
    print(scheduled)

    # --- Part 2 data: the book's stereo / laptop / guitar knapsack ---
    items = [
        ("stereo", 3000, 4),
        ("laptop", 2000, 3),
        ("guitar", 1500, 1),
    ]
    capacity = 4

    greedy_items, greedy_value = greedy_knapsack(items, capacity)
    print("Part 2: Greedy knapsack choice")
    print(greedy_items)
    print("Part 2: Greedy knapsack value")
    print(greedy_value)

    best_items, best_value = brute_force_knapsack(items, capacity)
    print("Part 2: Brute-force knapsack choice")
    print(best_items)
    print("Part 2: Brute-force knapsack value")
    print(best_value)

    gap = best_value - greedy_value
    print("Part 2: Gap between brute force and greedy")
    print(gap)

    # --- Part 3 data: the book's radio-station set-covering example ---
    states_needed = {"mt", "wa", "or", "id", "nv", "ut", "ca", "az"}
    stations = {
        "kone": {"id", "nv", "ut"},
        "ktwo": {"wa", "id", "mt"},
        "kthree": {"or", "nv", "ca"},
        "kfour": {"nv", "ut"},
        "kfive": {"ca", "az"},
    }

    final_stations = greedy_set_cover(states_needed, stations)
    print("Part 3: Stations chosen, in order")
    print(final_stations)

    small_count = count_subsets(5)
    medium_count = count_subsets(20)
    large_count = count_subsets(100)

    print("Part 3: Exact solver combinations to check for 5 stations")
    print(small_count)
    print("Part 3: Exact solver combinations to check for 20 stations")
    print(medium_count)
    print("Part 3: Exact solver combinations to check for 100 stations")
    print(large_count)

    # --- Reflection prompt ---
    # TODO: Replace the string below with your answer. Name the greedy
    # algorithm you already wrote in an earlier lab (Huffman tree
    # construction repeatedly merges the two lowest-frequency nodes) and
    # say whether that one is exactly optimal or an approximation.
    reflection_answer = "The Huffman tree construction algorithm is greedy because it repeatedly merges the two lowest-frequency nodes, and it produces an exactly optimal prefix code rather than an approximation."
    print("Reflection")
    print(reflection_answer)
