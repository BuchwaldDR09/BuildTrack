# BuildTrack: A Python project management application.

import json
from pathlib import Path


def show_menu():
    """Display the main menu options."""
    print("\n=== BuildTrack ===")
    print("1. View Projects")
    print("2. Add Project")
    print("3. Remove Project")
    print("4. Exit")
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
            if name in project_list:
                print("Project already exists.")
                continue

            project_list.append(name)
            save_projects(project_list)  # Save immediately after a change.
            print(f"Project added: {name}")
            add_another = input("Would you like to enter another project? (yes/no): ").strip().lower()
            if add_another != "yes":
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


# Projects are only in memory for now; Lesson 8C will load the JSON file.
projects = []

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
        save_projects(projects)
        print("Goodbye!")
        break
    else:
        print("Invalid option.")
