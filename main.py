# BuildTrack: A Python project management application.

import json
from pathlib import Path


def show_menu():
    """Display the main menu options."""
    print("\n=== BuildTrack ===")
    print("1. View Projects")
    print("2. Add Project")
    print("3. Remove Project")
    print("4. Search Projects")
    print("5. Rename Project")
    print("6. Exit")
    print("")


def count_projects(project_list):
    """Return the number of projects in the list."""
    return len(project_list)


def show_projects(project_list):
    """Display projects as a numbered list, or a message if there are none."""
    if not project_list:
        print("No projects to display.")
    else:
        print(f"Projects: ({count_projects(project_list)} total)")
        for index, project in enumerate(project_list, start=1):
            print(f"{index}. {project}")


def save_projects(project_list, filename="projects.json"):
    """Save the project list as JSON beside this Python file."""
    # __file__ points to main.py, independently of the working directory.
    file_path = Path(__file__).resolve().parent / filename

    # 'w' creates or replaces the file; indent=4 makes JSON readable.
    with open(file_path, "w", encoding="utf-8") as project_file:
        json.dump(project_list, project_file, indent=4)


def add_projects(project_list):
    """Ask for project names and add each unique, non-empty name."""
    while True:
        name = input("Project name (type 'quit' to cancel): ").strip()
        if name == 'quit':
            break
        elif not name:
            print("Project name cannot be empty.")
        else:
            # Compare folded text so capitalization alone cannot create a duplicate.
            if any(existing.casefold() == name.casefold() for existing in project_list):
                print("Project already exists.")
                continue

            project_list.append(name)
            # Keep the source list alphabetized (case-insensitive), not just the display.
            project_list.sort(key=str.casefold)
            save_projects(project_list)  # Save immediately after a change.
            print(f"Project added: {name}")
            add_another = input("Would you like to enter another project? (yes/no): ").strip().lower()
            if add_another != "yes":
                break


def rename_project(project_list):
    """Rename a numbered project, retrying invalid names or allowing cancellation."""
    if not project_list:
        print("No projects to rename.")
    else:
        print("Projects:")
        for index, project in enumerate(project_list, start=1):
            print(f"{index}. {project}")

        selection = input("Enter the number of the project to rename: ").strip()
        if not selection.isdigit():
            print("Please enter a valid project number.")
        else:
            # Translate the displayed number (starting at 1) to a list index (starting at 0).
            project_index = int(selection) - 1
            if not 0 <= project_index < len(project_list):
                print("Please enter a valid project number.")
            else:
                old_name = project_list[project_index]
                while True:
                    new_name = input(
                        f"Enter the new name for '{old_name}' (type 'quit' to cancel): "
                    ).strip()
                    if new_name.lower() == "quit":
                        print("Project was not renamed.")
                        break
                    if not new_name:
                        print("Project name cannot be empty.")
                        continue
                    # Skip the selected project; changing only capitalization is allowed.
                    if any(
                        index != project_index and existing.casefold() == new_name.casefold()
                        for index, existing in enumerate(project_list)
                    ):
                        print("Project already exists.")
                        continue

                    confirmation = input(
                        f"Are you sure you want to rename '{old_name}' to '{new_name}'? (yes/no): "
                    ).strip().lower()
                    if confirmation == "yes":
                        # Assignment updates the name without changing the list's length.
                        project_list[project_index] = new_name
                        project_list.sort(key=str.casefold)
                        save_projects(project_list)  # Save the new name and alphabetical order.
                        print(f"Project renamed: {old_name} -> {new_name}")
                    else:
                        print("Project was not renamed.")
                    break


def remove_projects(project_list):
    """Remove a numbered project after the user confirms the selection."""
    if not project_list:
        print("No projects to remove.")
    else:
        print("Projects:")
        for index, project in enumerate(project_list, start=1):
            print(f"{index}. {project}")

        selection = input("Enter the number of the project to remove: ").strip()
        if not selection.isdigit():
            print("Please enter a valid project number.")
        else:
            project_index = int(selection) - 1
            if not 0 <= project_index < len(project_list):
                print("Please enter a valid project number.")
            else:
                project = project_list[project_index]
                confirmation = input(
                    f"Are you sure you want to remove '{project}'? (yes/no): "
                ).strip().lower()
                if confirmation == "yes":
                    project_list.pop(project_index)
                    save_projects(project_list)  # Persist the deletion.
                    print(f"Project removed: {project}")
                else:
                    print("Project was not removed.")


def load_projects(filename="projects.json"):
    """Load projects alphabetically, or start empty if no JSON file exists."""
    # Use the same folder and filename convention as save_projects().
    file_path = Path(__file__).resolve().parent / filename

    # First run: there is no JSON file to load yet.
    if file_path.exists():
        # Read mode ('r') does not overwrite the saved data.
        with open(file_path, "r", encoding="utf-8") as project_file:
            # Normalize existing saved lists to alphabetical order at startup.
            return sorted(json.load(project_file), key=str.casefold)
    else:
        return []


def search_projects(project_list, search_term):
    """Return project names containing a case-insensitive partial match."""
    # Ignore surrounding spaces and compare using a common case.
    search_term = search_term.strip().lower()
    if not search_term:
        return []

    # A list comprehension creates a new list; original projects are unchanged.
    return [project for project in project_list if search_term in project.lower()]


# Restore saved projects on startup instead of always creating an empty list.
projects = load_projects()

# True is always true, so this loop repeats until break is reached.
while True:
    show_menu()
    choice = input("Select an option: ")

    if choice == "1":
        show_projects(projects)
    elif choice == "2":
        add_projects(projects)
    elif choice == "3":
        remove_projects(projects)
    elif choice == "4":
        # Only display matches; searching must not modify saved projects.
        search_term = input("Enter a project name or part of one to search: ").strip()
        matching_projects = search_projects(projects, search_term)
        if matching_projects:
            show_projects(matching_projects)
        else:
            print("No matching projects found.")
    elif choice == "5":
        rename_project(projects)
    elif choice == "6":
        save_projects(projects)
        print("Goodbye!")
        break
    else:
        print("Invalid option.")
