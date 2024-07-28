def generate_file_tree(files):
    """
    Generate a tree structure from a list of files
    
    :param files: List of dictionaries containing file information
    :return: Nested dictionary representing the file tree
    """
    tree = {}
    for file in files:
        parts = file['path'].split('/')
        current = tree
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]
        current[parts[-1]] = "file"
    return tree

def tree_to_string(tree, indent=""):
    """
    Convert a tree structure to a string representation
    
    :param tree: Nested dictionary representing the file tree
    :param indent: Current indentation level
    :return: String representation of the file tree
    """
    result = ""
    for key, value in sorted(tree.items()):
        if value == "file":
            result += f"{indent}├── {key}\n"
        else:
            result += f"{indent}├── {key}/\n"
            result += tree_to_string(value, indent + "│   ")
    return result