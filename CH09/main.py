"""
Lab: "Cheapest Route" -- Weighted Graphs and Dijkstra's Algorithm

Part 1: Implement Dijkstra's algorithm (dict-of-dicts weighted graph).
Part 2: Compare BFS "fewest hops" vs Dijkstra "lowest cost" on a small
San Francisco style map (Twin Peaks -> Golden Gate Bridge).
Part 3: Break Dijkstra's algorithm on purpose with a negative-weight edge.

All graphs below are hardcoded literals -- no randomness, no file I/O --
so the autograder can check exact costs, parents, and paths.
"""

from collections import deque

INFINITY = float("inf")

# ---------------------------------------------------------------------------

# PART 1: Weighted graphs and Dijkstra's algorithm

# ---------------------------------------------------------------------------

def find_lowest_cost_node(costs, processed):
    """
    Greedy selection step: among all nodes NOT already in `processed`,
    return the node with the smallest current cost. Return None if there
    are no more unprocessed nodes with a finite cost.

    This is the step that makes Dijkstra's algorithm a GREEDY algorithm:
    at every round we commit to whichever unprocessed node currently looks
    cheapest, and we never revisit that decision.
    """

    # TODO Step 1: set lowest_cost = INFINITY and lowest_cost_node = None
    lowest_cost = INFINITY
    lowest_cost_node = None

    # TODO Step 2: loop over costs.items() as (node, cost)
    for node, cost in costs.items():

        # TODO Step 3: if node is not in processed AND cost < lowest_cost:
        #              update lowest_cost = cost and lowest_cost_node = node
        if node not in processed and cost < lowest_cost:
            lowest_cost = cost
            lowest_cost_node = node

    # TODO Step 4: return lowest_cost_node
    return lowest_cost_node


def dijkstra(graph, start, finish):
    """
    Run Dijkstra's algorithm on a weighted graph represented as a
    dict-of-dicts, e.g. graph["start"] = {"a": 6, "b": 2}.

    Returns a tuple (costs, parents):
      costs   -- dict mapping node -> cheapest known cost from `start`
      parents -- dict mapping node -> the node we reached it cheapest from
    """
    costs = {}
    parents = {}

    # TODO Step 1: initialize costs[node] = INFINITY and parents[node] = None
    #              for every node in graph
    for node in graph:
        costs[node] = INFINITY
        parents[node] = None

    costs[start] = 0

    # TODO Step 2: overwrite the entries for start's direct neighbors using
    #              graph[start]: costs[neighbor] = weight, parents[neighbor] = start
    for neighbor, weight in graph[start].items():
        costs[neighbor] = weight
        parents[neighbor] = start

    # TODO Step 3: create an empty `processed` list to track finalized nodes
    processed = []

    # TODO Step 4: node = find_lowest_cost_node(costs, processed)
    node = find_lowest_cost_node(costs, processed)

    # TODO Step 5: while node is not None:
    #                cost = costs[node]
    #                neighbors = graph[node]
    #                for each neighbor, weight in neighbors.items():
    #                    new_cost = cost + weight
    #                    if new_cost < costs[neighbor]:
    #                        costs[neighbor] = new_cost
    #                        parents[neighbor] = node
    #                processed.append(node)
    #                node = find_lowest_cost_node(costs, processed)
    while node is not None:
        cost = costs[node]
        neighbors = graph[node]

        for neighbor, weight in neighbors.items():
            new_cost = cost + weight

            if new_cost < costs[neighbor]:
                costs[neighbor] = new_cost
                parents[neighbor] = node

        processed.append(node)
        node = find_lowest_cost_node(costs, processed)

    # TODO: Add a comment here explaining, in your own words, why the
    #       `processed` list is required -- what would go wrong (and how
    #       much extra work would happen) if a node could be reprocessed?
    # The processed list prevents Dijkstra from repeatedly checking nodes
    # whose shortest cost has already been finalized. Without it, the same
    # nodes could be processed again and cause unnecessary repeated work.

    return costs, parents


def build_path(parents, start, finish):
    """
    Walk the parents table backwards from `finish` to `start`, then
    reverse the result so it reads start -> ... -> finish.
    """
    path = []

    # TODO Step 1: set node = finish
    node = finish

    # TODO Step 2: while node is not None:
    #                append node to path
    #                node = parents.get(node)
    while node is not None:
        path.append(node)
        node = parents.get(node)

    # TODO Step 3: reverse path so it goes from start to finish
    path.reverse()

    # TODO Step 4: return path
    return path


# Book's warm-up graph: Start / A / B / Finish (dict-of-dicts)

book_graph = {}
book_graph["start"] = {"a": 6, "b": 2}
book_graph["a"] = {"finish": 1}
book_graph["b"] = {"a": 3, "finish": 5}
book_graph["finish"] = {}

# ---------------------------------------------------------------------------

# PART 2: Fewest hops vs. lowest cost (Twin Peaks -> Golden Gate Bridge)

# ---------------------------------------------------------------------------

def bfs_shortest_path(graph, start, finish):
    """
    Provided from Chapter 6: breadth-first search finds the path with the
    FEWEST EDGES (hops) on an unweighted graph (dict-of-lists). This
    function is already implemented for you -- study it, don't edit it.
    """
    queue = deque([start])
    visited = set([start])
    parents = {start: None}

    while queue:
        node = queue.popleft()
        if node == finish:
            break
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                parents[neighbor] = node
                queue.append(neighbor)

    path = []
    node = finish
    while node is not None:
        path.append(node)
        node = parents.get(node)
    path.reverse()
    return path


# Unweighted version (dict-of-lists) -- same map, ignoring travel time.

sf_unweighted = {
    "twin_peaks": ["a", "c"],
    "a": ["b"],
    "b": ["golden_gate"],
    "c": ["d"],
    "d": ["e"],
    "e": ["golden_gate"],
    "golden_gate": [],
}

# Weighted version (dict-of-dicts) -- edge weights are travel time.

# The 3-segment route (twin_peaks -> a -> b -> golden_gate) is SLOWER

# than the 4-segment route (twin_peaks -> c -> d -> e -> golden_gate).

sf_weighted = {
    "twin_peaks": {"a": 10, "c": 3},
    "a": {"b": 10},
    "b": {"golden_gate": 10},
    "c": {"d": 3},
    "d": {"e": 3},
    "e": {"golden_gate": 3},
    "golden_gate": {},
}

# ---------------------------------------------------------------------------

# PART 3: Break Dijkstra's algorithm on purpose (negative-weight edge)

# ---------------------------------------------------------------------------

# Trade graph with a negative-weight edge (a -> b costs -10).

# The TRUE cheapest route start -> a -> b -> finish costs 2 + (-10) + 5 = -3,

# but Dijkstra's algorithm will mark "b" as processed too early (via the

# direct start -> b edge, cost 1) and never reconsider it once the cheaper

# path through "a" is discovered.

negative_graph = {
    "start": {"b": 1, "a": 2},
    "a": {"b": -10, "finish": 100},
    "b": {"finish": 5},
    "finish": {},
}


def main():
    print("=== Part 1: Book's Start/A/B/Finish graph ===")
    costs, parents = dijkstra(book_graph, "start", "finish")
    print(costs)
    print(parents)
    path = build_path(parents, "start", "finish")
    print(path)

    print("=== Part 2: Twin Peaks -> Golden Gate Bridge ===")
    bfs_path = bfs_shortest_path(sf_unweighted, "twin_peaks", "golden_gate")
    print("BFS path (fewest hops):")
    print(bfs_path)

    sf_costs, sf_parents = dijkstra(sf_weighted, "twin_peaks", "golden_gate")
    dijkstra_path = build_path(sf_parents, "twin_peaks", "golden_gate")
    print("Dijkstra path (lowest cost):")
    print(dijkstra_path)
    print("Dijkstra total cost:")
    print(sf_costs.get("golden_gate"))

    # TODO: In a comment (or a print statement), explain in your own words
    #       what BFS thinks "shortest" means versus what Dijkstra thinks
    #       "shortest" means, based on the two results printed above.
    # BFS considers the shortest path to be the route with the fewest edges
    # or hops. Dijkstra considers the shortest path to be the route with the
    # lowest total weight or cost, even if that route has more hops.

    print("=== Part 3: Negative-weight edge breaks Dijkstra ===")
    neg_costs, neg_parents = dijkstra(negative_graph, "start", "finish")
    print(neg_costs)
    print(neg_parents)
    neg_path = build_path(neg_parents, "start", "finish")
    print(neg_path)

    # TODO: Hand-trace the algorithm on `negative_graph`. Identify which
    #       node got marked "processed" too early, and write 2-3 sentences
    #       (as a comment here) explaining the assumption that broke:
    #       once Dijkstra finalizes a node it never reconsiders it, and a
    #       negative edge means a cheaper route can still appear later.
    #       Also name the algorithm (Bellman-Ford) that handles this case.
    # Node "b" is processed too early because its initial cost of 1 looks
    # cheaper than node "a" with cost 2. Later, the negative edge from
    # "a" to "b" creates a cheaper cost of -8, but Dijkstra does not
    # properly reconsider already finalized nodes. Bellman-Ford can handle
    # graphs that contain negative edge weights.

    # TODO: Reflection -- in a comment, answer: where does the "cost" on
    #       an edge come from in real routing software (travel time,
    #       tolls, elevation, data-transfer latency, etc.), and how does
    #       changing what you measure change the answer without changing
    #       a single line of the algorithm?
    # In real routing software, edge cost can represent travel time,
    # distance, toll price, elevation, fuel use, or network latency.
    # Changing the meaning of the cost can produce a different best route
    # without changing Dijkstra's algorithm itself.


if __name__ == "__main__":
    main()
