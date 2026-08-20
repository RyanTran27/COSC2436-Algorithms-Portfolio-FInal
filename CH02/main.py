"""
Lab Exercise: Selection Sort
Course: Introduction to Algorithms
Reference: Grokking Algorithms, Chapter 2 -- Selection Sort

Complete the TODOs below to implement:
  1. find_smallest(arr)
  2. selection_sort(arr)
  3. rank_artists(plays)
"""


def find_smallest(arr):
    """
    Return the INDEX of the smallest element in arr.

    Steps (from the text):
      - Assume the first element is the smallest to start.
      - Track both the smallest value seen so far and its index.
      - Loop over the remaining elements, updating both variables
        whenever a smaller value is found.
      - Return the index (not the value).
    """
    # TODO: set smallest_value = arr[0] and smallest_index = 0
    smallest_value = arr[0]
    smallest_index = 0
    # TODO: loop over the rest of the list (from index 1 to end)
    #       if arr[i] is smaller than smallest_value, update
    #       smallest_value and smallest_index
    for i in range(1,len(arr)):
        if arr[i] < smallest_value:
            smallest_value = arr[i]
            smallest_index = i 
    # TODO: return smallest_index
    return smallest_index  # placeholder so the file runs

def selection_sort(arr):
    """
    Return a NEW list containing the elements of arr sorted from
    smallest to largest. The original list must NOT be modified.

    Steps (from the text):
      1. Make a copy of the input list so the original is not mutated.
      2. Create an empty result list.
      3. Loop once for each element: call find_smallest on the copy,
         pop that element out of the copy, and append it to the result.
      4. Return the result list.
    """
    # TODO: make a copy of arr (do not sort arr itself)
    arr_copy = arr.copy()

    # TODO: create an empty list to hold the sorted result
    sorted_arr = []
    # TODO: loop while the copy still has elements:
    #       - find the index of the smallest value in the copy
    #       - pop that value out of the copy
    #       - append it to the result list
    while arr_copy: 
        smallest_index = find_smallest(arr_copy)
        smallest_value = arr_copy.pop(smallest_index)
        sorted_arr.append(smallest_value)
  
    # TODO: return the result list
    return sorted_arr  # placeholder so the file runs


def rank_artists(plays):
    """
    plays: a dict mapping artist name -> play count

    Return a list of artist names ordered from MOST played to
    LEAST played. Reuse your selection sort logic (either find the
    largest remaining play count each pass, or sort ascending and
    reverse the result).
    """
    # TODO: build a list of (artist, play_count) pairs, or a list of
    #       artist names that you can sort by looking up play counts
    remaining_artists = list(plays.keys())
    ranked_artists = []

    # TODO: use selection-sort-style logic to order the artists by
    #       play count, from most played to least played
    while remaining_artists:
       largest_index = 0

       for i in range(1, len(remaining_artists)):
           current_artist = remaining_artists[i]
           largest_artist = remaining_artists[largest_index]

           if plays[current_artist] > plays[largest_artist]: 
               largest_index = i 

       ranked_artists.append(remaining_artists.pop(largest_index))
    # TODO: return the list of artist names in that order
    return ranked_artists  # placeholder so the file runs


if __name__ == "__main__":
    # ---- Part 1 tests: find_smallest ----
    print(find_smallest([5, 3, 6, 2, 10]))   # expected: 3
    print(find_smallest([1, 2, 3]))          # expected: 0
    print(find_smallest([7]))                # expected: 0

    # ---- Part 2 tests: selection_sort ----
    print(selection_sort([5, 3, 6, 2, 10]))  # expected: [2, 3, 5, 6, 10]
    print(selection_sort([]))                # expected: []
    print(selection_sort([4, 4, 1]))         # expected: [1, 4, 4]

    original = [9, 1, 5]
    selection_sort(original)
    print(original)                          # expected: [9, 1, 5] (unchanged!)

    # ---- Part 3 test: rank_artists ----
    plays = {
        "Radiohead": 156,
        "Kishore Kumar": 141,
        "The Black Keys": 35,
        "Neutral Milk Hotel": 94,
        "Beck": 88,
        "The Strokes": 61,
        "Wilco": 111,
    }
    print(rank_artists(plays))
  
    # expected: ['Radiohead', 'Kishore Kumar', 'Wilco', 'Neutral Milk Hotel',
    #            'Beck', 'The Strokes', 'The Black Keys']

# ---- Part 4: Analysis Questions ----
# 1. find_smallest takes O(n) time, and selection sort calls it n times.
#    What is the overall running time?
#    TODO: The overall running time is O(n^2).
#    This is because the algorithm searches through the list about n
#    times, and each search can take up to n comparisons.

# 2. On each pass, the copy shrinks: you check n elements, then n - 1,
#    then n - 2, and so on. On average you check about 1/2 * n elements
#    per pass. Why is the running time still written as O(n^2) rather
#    than O(1/2 * n^2)?
#    TODO: Big O notation ignores constant numbers such as 1/2 because they
#    do not change how quickly the running time grows as n gets larger.
#    Therefore, O(1/2 * n^2) is simplified to O(n^2).

# 3. Your implementation uses pop, which removes an element from the
#    middle of a list. Based on the array operation costs from Chapter 2,
#    what is the cost of that removal, and does it change the big O
#    running time of the sort?
#    TODO: Removing an element from the middle of a list costs O(n) because
#    the elements after it must shift to fill the empty space. Since this
#    removal happens repeatedly, it adds work, but the total running time
#    still grows at O(n^2), so the overall Big O does not change.

# ---- Challenge (Optional): in-place selection sort ----
def selection_sort_in_place(arr):
    for current_index in range(len(arr)):
        smallest_index = current_index

        for i in range(current_index + 1, len(arr)):
            if arr[i] < arr[smallest_index]:
                smallest_index = i

        arr[current_index], arr[smallest_index] = (
            arr[smallest_index],
            arr[current_index],
        )

    return arr
# TODO: implement an in-place version of selection sort here if
#       attempting the challenge, and note one advantage of it in a
#       comment.
# Advantage: This version uses less extra memory because it sorts
# the original list instead of creating a new list.
