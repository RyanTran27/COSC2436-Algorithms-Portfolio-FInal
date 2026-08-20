 def trace_enter(label, depth):
    """Print a message showing we are ENTERING a recursive call."""
    indent = "  " * depth
    print(indent + "-> entering: " + str(label))


def trace_exit(label, depth):
    """Print a message showing we are EXITING a recursive call."""
    indent = "  " * depth
    print(indent + "<- exiting: " + str(label))


# ---------------------------------------------------------------------------
# Task 1: find_file(structure, target_name)
# ---------------------------------------------------------------------------

def find_file(structure, target_name, current_path="", depth=0):
    """
    Recursively search the nested file system 'structure' for a file
    whose 'name' matches target_name. Return the full path (string) to
    the file if found, or None if it is not found anywhere.
    """
    new_path = current_path + "/" + structure["name"]

    trace_enter(new_path, depth)

    # BASE CASE #1: current node is a file
    if structure["type"] == "file":
        if structure["name"] == target_name:
            trace_exit(new_path, depth)
            return new_path

        trace_exit(new_path, depth)
        return None

    # RECURSIVE CASE: current node is a folder
    for item in structure["contents"]:
        result = find_file(item, target_name, new_path, depth + 1)

        if result is not None:
            trace_exit(new_path, depth)
            return result

    # BASE CASE #2: searched the entire folder with no match
    trace_exit(new_path, depth)
    return None


# ---------------------------------------------------------------------------
# Task 2: count_files(structure)
# ---------------------------------------------------------------------------

def count_files(structure, depth=0):
    """
    Recursively count how many files exist anywhere inside structure.
    """

    # BASE CASE: a file contributes exactly 1
    if structure["type"] == "file":
        return 1

    # RECURSIVE CASE: add the counts from each item
    total = 0

    for item in structure["contents"]:
        total += count_files(item, depth + 1)

    return total


# ---------------------------------------------------------------------------
# Task 3: total_size(structure)
# ---------------------------------------------------------------------------

def total_size(structure, depth=0):
    """
    Recursively sum the sizes of every file.
    """

    # BASE CASE: a file contributes its own size
    if structure["type"] == "file":
        return structure["size"]

    # RECURSIVE CASE: add the sizes from each item
    total = 0

    for item in structure["contents"]:
        total += total_size(item, depth + 1)

    return total


# ---------------------------------------------------------------------------
# Task 4: print_tree_with_depth(structure, depth=0)
# ---------------------------------------------------------------------------

def print_tree_with_depth(structure, depth=0):
    """
    Recursively print the file system tree.
    """

    # Print the current node indented by depth
    print("  " * depth + structure["name"])

    # BASE CASE: a file has no contents
    if structure["type"] == "file":
        return

    # RECURSIVE CASE: print every item in the folder
    for item in structure["contents"]:
        print_tree_with_depth(item, depth + 1)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    file_system = {
        "name": "root",
        "type": "folder",
        "contents": [
            {
                "name": "readme.txt",
                "type": "file",
                "size": 5
            },
            {
                "name": "photo.jpg",
                "type": "file",
                "size": 200
            },
            {
                "name": "documents",
                "type": "folder",
                "contents": [
                    {
                        "name": "resume.docx",
                        "type": "file",
                        "size": 15
                    },
                    {
                        "name": "taxes",
                        "type": "folder",
                        "contents": [
                            {
                                "name": "2022.pdf",
                                "type": "file",
                                "size": 40
                            },
                            {
                                "name": "2023.pdf",
                                "type": "file",
                                "size": 42
                            }
                        ]
                    }
                ]
            },
            {
                "name": "music",
                "type": "folder",
                "contents": [
                    {
                        "name": "song1.mp3",
                        "type": "file",
                        "size": 30
                    }
                ]
            },
            {
                "name": "empty_folder",
                "type": "folder",
                "contents": []
            }
        ]
    }

    print("Finding 2023.pdf:")
    print("Result:", find_file(file_system, "2023.pdf"))

    print("\nFinding missing.txt:")
    print("Result:", find_file(file_system, "missing.txt"))

    print("\nNumber of files:")
    print(count_files(file_system))

    print("\nTotal file size:")
    print(total_size(file_system))

    print("\nFile system tree:")
    print_tree_with_depth(file_system)
