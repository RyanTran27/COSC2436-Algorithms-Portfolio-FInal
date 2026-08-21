"""
Lab: Six Degrees -- Graph Modeling & Breadth-First Search
Chapter 6 concepts: representing a network as a graph (dict of lists),
and using a queue-based BFS to answer "is there a path?" and
"what's the shortest path?", plus a topological sort mini-exercise.

Fill in the TODO sections. Do not change the shape of the data
structures or the function signatures.
"""

import collections


# ---------------------------------------------------------------------------
# PART 1 DATA: a small professional/social network
# graph["you"] = ["alice", "bob", "claire"]  <-- book's exact pattern
# NOTE: this graph deliberately contains a CYCLE (peggy -> you) so that
# your search() function MUST use a `searched` set or it will hang forever!
# ---------------------------------------------------------------------------
network = {
    "you": ["alice", "bob", "claire"],
    "alice": ["peggy"],
    "bob": ["anuj", "peggy"],
    "claire": ["thom", "jonny"],
    "peggy": ["you", "maria"],   # cycle back to "you"!
    "anuj": [],
    "thom": ["diego"],
    "jonny": ["sam"],
    "maria": ["lee"],
    "diego": [],
    "sam": [],
    "lee": [],
}

# Which skill(s) each person has. Used by person_has_skill().
skills = {
    "you": ["project_management"],
    "alice": ["design"],
    "bob": ["sales"],
    "claire": ["marketing"],
    "peggy": ["finance"],
    "anuj": ["manufacturing"],
    "thom": ["design"],
    "jonny": ["sales"],
    "maria": ["manufacturing"],
    "diego": ["python"],
    "sam": ["python"],
    "lee": ["manufacturing"],
}


def person_has_skill(name, skill_to_find):
    """
    Return True if `name` has `skill_to_find` in the skills dict, else False.
    This is the book's `person_is_seller` analog.
    """
    # TODO: Step 1 - look up `name` in the `skills` dictionary (use .get()
    #                so a missing name returns an empty list, not an error)
    person_skills = skills.get(name, [])

    # TODO: Step 2 - return True if skill_to_find is in that person's list
    #                of skills, otherwise return False
    return skill_to_find in person_skills


def search(start_name, skill_to_find):
    """
    Breadth-first search over `network` starting at start_name.
    Return True if some person reachable from start_name has skill_to_find,
    otherwise return False.

    Follow the book's exact algorithm:
1. Create a queue (collections.deque) and add start_name's neighbors.
2. Create a `searched` set to avoid re-checking/re-queueing people
   (THIS IS CRITICAL -- the network has a cycle, so without this
   set your loop will run forever).
3. While the queue is not empty: pop the first person, and if not
   already searched, check their skill. If found, return True.
   Otherwise mark them searched and add their neighbors to the queue.
4. If the queue empties out with no match, return False.
    """
    # TODO: Step 1 - create search_queue = collections.deque()
    search_queue = collections.deque()

    # TODO: Step 2 - extend search_queue with network[start_name]
    search_queue.extend(network[start_name])

    # TODO: Step 3 - create an empty set called `searched`
    searched = set()

    # TODO: Step 4 - loop while search_queue is not empty:
    #                 a) pop the leftmost person off the queue
    #                 b) if person not in searched:
    #                      - if person_has_skill(person, skill_to_find): return True
    #                      - else add person's neighbors to the queue
    #                      - add person to `searched`
    while search_queue:
        person = search_queue.popleft()

        if person not in searched:
            if person_has_skill(person, skill_to_find):
                return True

            search_queue.extend(network.get(person, []))
            searched.add(person)

    # TODO: Step 5 - after the loop, return False (no one found)
    return False


# ---------------------------------------------------------------------------
# PART 2: shortest path (degree of separation), not just True/False
# ---------------------------------------------------------------------------
def search_shortest_path(start_name, skill_to_find):
    """
    Same idea as search(), but return the SHORTEST number of hops (int)
    from start_name to the first person with skill_to_find.
    Return -1 if no one in the network has the skill.

    Hint: track each person's distance from start_name as you discover them
    (e.g., store (person, distance) tuples in the queue, or a separate
    distances dict), since BFS visits people in order of increasing distance.
    """
    # TODO: Step 1 - create search_queue with (neighbor, 1) tuples for each
    #                neighbor of start_name (distance 1 = direct contact)
    search_queue = collections.deque()

    for neighbor in network[start_name]:
        search_queue.append((neighbor, 1))

    # TODO: Step 2 - create an empty `searched` set
    searched = set()

    # TODO: Step 3 - loop while search_queue is not empty:
    #                 a) pop (person, distance) off the queue
    #                 b) if person not in searched:
    #                      - if they have the skill, return distance
    #                      - else enqueue each neighbor with (neighbor, distance + 1)
    #                      - add person to searched
    while search_queue:
        person, distance = search_queue.popleft()

        if person not in searched:
            if person_has_skill(person, skill_to_find):
                return distance

            for neighbor in network.get(person, []):
                search_queue.append((neighbor, distance + 1))

            searched.add(person)

    # TODO: Step 4 - return -1 if nobody found
    return -1


def search_with_path(start_name, skill_to_find):
    """
    BONUS/stretch: same as search_shortest_path, but also reconstruct and
    return the actual path as a list of names, e.g. ["you", "bob", "anuj"].
    Return an empty list [] if no one is found.

    Hint: while doing BFS, store a `came_from` dict mapping
    neighbor -> person (the predecessor that discovered it). Once you find
    the target, walk backwards through came_from to rebuild the path, then
    reverse it.
    """
    # TODO: Step 1 - create search_queue with start_name's direct neighbors
    search_queue = collections.deque(network[start_name])

    # TODO: Step 2 - create an empty `searched` set
    searched = set()

    # TODO: Step 3 - create a `came_from` dict; for each of start_name's
    #                direct neighbors, came_from[neighbor] = start_name
    came_from = {}

    for neighbor in network[start_name]:
        came_from[neighbor] = start_name

    # TODO: Step 4 - loop while search_queue is not empty:
    #                 a) pop a person off the queue
    #                 b) if person not in searched:
    #                      - if they have the skill: reconstruct the path
    #                        by walking came_from backwards from person to
    #                        start_name, then reverse it and return it
    #                      - else, for each neighbor not yet in came_from,
    #                        set came_from[neighbor] = person and enqueue it
    #                      - add person to searched
    while search_queue:
        person = search_queue.popleft()

        if person not in searched:
            if person_has_skill(person, skill_to_find):
                path = [person]

                while person != start_name:
                    person = came_from[person]
                    path.append(person)

                path.reverse()
                return path

            for neighbor in network.get(person, []):
                if neighbor not in came_from:
                    came_from[neighbor] = person
                    search_queue.append(neighbor)

            searched.add(person)

    # TODO: Step 5 - return [] if nobody found
    return []


# ---------------------------------------------------------------------------
# PART 3: topological sort mini-exercise
# A small DAG modeling steps to set up a GitHub Classroom assignment.
# ---------------------------------------------------------------------------
# dependency_graph[step] = [steps that must happen BEFORE `step`]
dependency_graph = {
    "create_repo_template": [],
    "write_starter_code": ["create_repo_template"],
    "write_tests": ["write_starter_code"],
    "create_classroom_assignment": ["write_starter_code", "write_tests"],
    "invite_students": ["create_classroom_assignment"],
    "grade_submissions": ["invite_students"],
}

# A proposed ordering to check for validity (Exercise 6.3 style)
proposed_order = [
    "create_repo_template",
    "write_starter_code",
    "write_tests",
    "create_classroom_assignment",
    "invite_students",
    "grade_submissions",
]


def is_valid_order(order, dep_graph):
    """
    Return True if `order` is a valid topological ordering of dep_graph,
    i.e. every step appears only after all of its dependencies.
    """
    # TODO: Step 1 - build a dict mapping each step name to its position
    #                (index) in `order`
    # TODO: Step 2 - for every step in dep_graph, for every dependency of
    #                that step, check that the dependency's position is
    #                BEFORE the step's position in `order`
    # TODO: Step 3 - return False as soon as you find a violation,
    #                otherwise return True after checking everything
    return False  # placeholder


def topological_sort(dep_graph):
    """
    Return a valid topological ordering (list of step names) of dep_graph.
    A simple, non-optimal approach is fine: repeatedly find a step whose
    dependencies have all already been placed in the result list, add it,
    and repeat until every step has been placed.
    """
    # TODO: Step 1 - create an empty list called `order`
    # TODO: Step 2 - loop until len(order) == len(dep_graph):
    #                 a) look through dep_graph for a step not yet in order
    #                    whose dependencies are ALL already in order
    #                 b) append that step to order
    # TODO: Step 3 - return order
    return []  # placeholder


if __name__ == "__main__":
    # Part 1: is there a path to someone in manufacturing?
    found_manufacturing = search("you", "manufacturing")
    print(found_manufacturing)

    # Part 1: is there a path to someone who knows python?
    found_python = search("you", "python")
    print(found_python)

    # Part 2: shortest path (degree of separation) to someone in manufacturing
    distance_manufacturing = search_shortest_path("you", "manufacturing")
    print(distance_manufacturing)

    # Part 2 bonus: actual path to someone who knows python
    path_to_python = search_with_path("you", "python")
    print(path_to_python)

    # Part 3: check whether the proposed ordering is valid
    order_is_valid = is_valid_order(proposed_order, dependency_graph)
    print(order_is_valid)

    # Part 3: compute a topological ordering ourselves
    computed_order = topological_sort(dependency_graph)
    print(computed_order)
