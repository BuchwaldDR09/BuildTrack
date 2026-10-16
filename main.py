# BuildTrack: A Python project management application.

def show_menu():
    """Display the main menu options."""
    print("=== BuildTrack ===")
    print("1. View Projects")
    print("2. Add Project")
    print("3. Remove Project")
    print("4. Exit")
    print("")


def show_projects(project_list):
    """Display projects as a numbered list, or a message if there are none."""
    if not project_list:
        print("No projects to display.")
    else:
        print("Projects:")
        for index, project in enumerate(project_list, start=1):
            print(f"{index}. {project}")


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

            # Mutate the list passed to the function (no return needed).
            project_list.append(name)
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
                    # pop(index) removes the selected item from the same list.
                    project_list.pop(project_index)
                    print(f"Project removed: {project}")
                else:
                    print("Project was not removed.")


# Create this list once so all functions share the same project data.
projects = []

# The menu repeats until the user chooses Exit.
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
        print("Goodbye!")
        break
    else:
        print("Invalid option.")
