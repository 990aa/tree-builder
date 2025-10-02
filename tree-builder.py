import os
import re
from pathlib import Path

def create_project_structure(tree_string: str, base_path: str):
    """
    Creates a directory and file structure from a multi-line string representation.

    Args:
        tree_string: A string formatted like a directory tree. 
                     Directories should end with a '/'.
        base_path: The root directory where the structure will be created.
    """
    lines = tree_string.strip().split('\n')
    
    if not lines or not lines[0].strip():
        print("Error: The tree string is empty or invalid.")
        return

    project_root_name = lines[0].strip().replace('/', '')
    project_root_path = Path(base_path) / project_root_name
    
    path_levels = [project_root_path]
    
    print(f"Creating project structure in: {project_root_path.resolve()}")
    project_root_path.mkdir(parents=True, exist_ok=True)

    for line in lines[1:]:
        if not line.strip():
            continue

        name = re.sub(r'^[│├──└─ ]+', '', line).strip()
        is_dir = name.endswith('/')
        name = name.replace('/', '')


        indentation = len(line) - len(line.lstrip(' │'))
        level = indentation // 4 + 1

        path_levels = path_levels[:level]
        parent_path = path_levels[-1]

        current_path = parent_path / name
        
        try:
            if is_dir:
                current_path.mkdir(exist_ok=True)
               
                path_levels.append(current_path)
                print(f"  Created directory: {current_path}")
            else:
                current_path.touch()
                print(f"  Created file:      {current_path}")
        except OSError as e:
            print(f"Error creating {current_path}: {e}")


if __name__ == '__main__':
    tree_file_path = 'tree-structure.txt'
    
    try:
        with open(tree_file_path, 'r') as f:
            tree_structure_from_file = f.read()
    except FileNotFoundError:
        print(f"Error: The file '{tree_file_path}' was not found.")
        print("Please create this file in the same directory as the script and define your project structure in it.")
        exit()

    destination_directory = input("Enter the full path where you want to create the project structure (e.g., /Users/YourUser/Desktop): ")

    if destination_directory and os.path.isdir(destination_directory):
        create_project_structure(tree_structure_from_file, destination_directory)
        print("\nProject structure created successfully!")
    else:
        print("\nInvalid directory provided. Please run the script again with a valid path.")