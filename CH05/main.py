import time

# ============================================================
# PART 1: Three Classic Hash Table (dict) Use Cases
# ============================================================

# ---- Use Case 1: Lookup Tool (Contact Book) ----

def add_contact(contact_book, name, number):
    """
    Add a name/number pair to the contact_book dictionary.
    contact_book: dict mapping name -> phone number
    """
    # TODO: Store the name as the key and number as the value in contact_book
    # Step 1: Use contact_book[name] = number to add the entry
    contact_book[name] = number


def lookup_contact(contact_book, name):
    """
    Look up a name in the contact_book.
    Return the phone number if found, or the string "Not found" if missing.
    """
    # TODO: Check if name exists in contact_book
    # Step 1: Use an if/else or .get() to safely look up the key
    # Step 2: Return the number if found, otherwise return "Not found"
    return contact_book.get(name, "Not found")


# ---- Use Case 2: Duplicate-Catcher (Voter Check) ----

def check_voter(voted_dict, name):
    """
    Check whether 'name' has already voted.
    voted_dict: dict mapping name -> True (if they voted)
    Returns a string message: "Allowed to vote" or "Already voted!"
    Also should mark the name as voted the first time.
    """
    # TODO: Step 1: Check if name is already a key in voted_dict
    # Step 2: If yes, this is a duplicate vote attempt -> return "Already voted!"
    # Step 3: If no, add name to voted_dict (mark as voted) -> return "Allowed to vote"
    if name in voted_dict:
        return "Already voted!"

    voted_dict[name] = True
    return "Allowed to vote"


# ---- Use Case 3: Cache Simulator (Web Page Cache) ----

def simulate_server_call(url):
    """
    Pretend this is an expensive network/server call.
    This helper is already implemented for you - do not modify.
    """
    time.sleep(0.01)  # short sleep so the demo runs quickly
    return "Contents of " + url


def get_page(cache, url):
    """
    Return the page contents for 'url', using 'cache' (a dict) to avoid
    repeating expensive simulate_server_call() calls.
    Should print whether this request was a "HIT" or "MISS" before returning.
    """
    # TODO: Step 1: Check if url is already a key in cache
    # Step 2: If it is, print "HIT" and return the cached value
    # Step 3: If not, print "MISS", call simulate_server_call(url),
    #         store the result in cache, then return it
    if url in cache:
        print("HIT")
        return cache[url]

    print("MISS")
    page_contents = simulate_server_call(url)
    cache[url] = page_contents
    return page_contents


# ============================================================
# PART 2: Build Your Own Mini Hash Table
# ============================================================

def simple_hash(key, num_slots):
    """
    A simple hash function: sum the character codes of key,
    then mod by num_slots to fit it into the array.
    """
    # TODO: Step 1: Loop over each character in key
    # Step 2: Add up ord(char) for every character into a running total
    # Step 3: Return total % num_slots
    total = 0

    for char in key:
        total += ord(char)

    return total % num_slots


class MiniHashTable:
    """
    A simplified hash table built on a plain Python list.
    Collisions are handled via chaining: each slot holds a list of
    (key, value) pairs.
    """

    def __init__(self, num_slots):
        self.num_slots = num_slots
        # Each slot starts as an empty list (chain) for collision resolution
        self.slots = [[] for _ in range(num_slots)]
        self.num_items = 0

    def insert(self, key, value):
        """
        Insert key/value into the table using simple_hash to find the slot.
        If key already exists in that slot's chain, update its value.
        Otherwise, append (key, value) to the chain and increase num_items.
        """
        # TODO: Step 1: Find the slot index using simple_hash(key, self.num_slots)
        # Step 2: Loop through self.slots[index] looking for an existing pair with this key
        # Step 3: If found, update its value; if not found, append (key, value)
        # Step 4: If this was a brand new key, increment self.num_items
        index = simple_hash(key, self.num_slots)

        for pair_index in range(len(self.slots[index])):
            current_key, current_value = self.slots[index][pair_index]

            if current_key == key:
                self.slots[index][pair_index] = (key, value)
                return

        self.slots[index].append((key, value))
        self.num_items += 1

    def get(self, key):
        """
        Retrieve the value associated with key, or None if not found.
        """
        # TODO: Step 1: Find the slot index using simple_hash(key, self.num_slots)
        # Step 2: Search self.slots[index] for a pair matching key
        # Step 3: Return the value if found, otherwise return None
        index = simple_hash(key, self.num_slots)

        for current_key, current_value in self.slots[index]:
            if current_key == key:
                return current_value

        return None

    def load_factor(self):
        """
        Return the current load factor: num_items / num_slots.
        """
        # TODO: Step 1: Divide self.num_items by self.num_slots
        # Step 2: Return the result
        return self.num_items / self.num_slots


# ============================================================
# PART 3: Load Factor & Hash Quality Investigation
# ============================================================

def bad_hash(key, num_slots):
    """
    A deliberately weak hash function: uses only the length of the key.
    This is already implemented for you - it is meant to perform poorly!
    """
    return len(key) % num_slots


def investigate_hash_quality(hash_func, keys, num_slots):
    """
    Build a small array of chains using hash_func on each key in keys.
    Return a tuple: (total_collisions, longest_chain_length)

    A "collision" happens each time a key lands in a slot that already
    has at least one key in it before this key is added.
    """
    # TODO: Step 1: Create a list of num_slots empty lists (the chains)
    # Step 2: Loop through each key in keys
    #   - Compute the slot index using hash_func(key, num_slots)
    #   - If that slot already has 1+ items in it, count that as a collision
    #   - Append the key to that slot's chain
    # Step 3: After the loop, find the longest chain length across all slots
    # Step 4: Return (total_collisions, longest_chain_length)
    chains = [[] for _ in range(num_slots)]
    total_collisions = 0

    for key in keys:
        index = hash_func(key, num_slots)

        if len(chains[index]) > 0:
            total_collisions += 1

        chains[index].append(key)

    longest_chain_length = 0

    for chain in chains:
        if len(chain) > longest_chain_length:
            longest_chain_length = len(chain)

    return total_collisions, longest_chain_length


# ============================================================
# MAIN PROGRAM - Deterministic demo data (no files, no randomness)
# ============================================================

if __name__ == "__main__":
    # ---- Part 1 Demo: Contact Book ----
    contact_book = {}
    add_contact(contact_book, "Maggie", "555-1234")
    add_contact(contact_book, "Sam", "555-5678")
    print(lookup_contact(contact_book, "Maggie"))
    print(lookup_contact(contact_book, "NotInBook"))

    # ---- Part 1 Demo: Voter Check ----
    voted_dict = {}
    voter_list = ["Tom", "Lisa", "Tom", "Sam", "Lisa"]
    duplicate_attempts = 0

    for name in voter_list:
        result = check_voter(voted_dict, name)
        print(result)

        if result == "Already voted!":
            duplicate_attempts += 1

    print("Duplicate attempts:", duplicate_attempts)

    # ---- Part 1 Demo: Cache Simulator ----
    page_cache = {}
    urls_to_fetch = [
        "http://site.test/home",
        "http://site.test/home",
        "http://site.test/about",
        "http://site.test/contact",
        "http://site.test/home",
    ]

    for url in urls_to_fetch:
        page = get_page(page_cache, url)
        print(page)

    # ---- Part 2 Demo: Mini Hash Table ----
    mini_table = MiniHashTable(5)
    mini_table.insert("apple", 10)
    mini_table.insert("avocado", 20)
    mini_table.insert("banana", 30)

    print(mini_table.get("apple"))
    print(mini_table.get("avocado"))
    print(mini_table.get("missing_key"))
    print(mini_table.load_factor())

    # ---- Part 3 Demo: Hash Quality Investigation ----
    sample_keys = [
        "Maggie", "Tom", "Lisa", "Sam", "Ella",
        "Noah", "Ava", "Liam", "Mia", "Ethan",
        "Grace", "Oliver",
    ]
    num_slots = 8

    good_collisions, good_longest = investigate_hash_quality(
        simple_hash, sample_keys, num_slots
    )
    print(good_collisions)
    print(good_longest)

    bad_collisions, bad_longest = investigate_hash_quality(
        bad_hash, sample_keys, num_slots
    )
    print(bad_collisions)
    print(bad_longest)
