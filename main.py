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
        # enumerate gives each entry a number beginning at 1.
        for index, project in enumerate(project_list, start=1):
            print(f"{index}. {project}")


# Keep project data outside the menu loop so it survives menu selections.
projects = []

# Repeat the main menu until the user selects Exit.
while True:
    show_menu()
    choice = input("Select an option: ")

    if choice == "1":
        # Pass the projects list as an argument to our display function.
        show_projects(projects)
    elif choice == "2":
        while True:
            name = input("Project name (type 'quit' to cancel): ").strip()
            if name == "quit":
                break
            elif not name:
                print("Project name cannot be empty.")
            else:
                if name in projects:
                    print("Project already exists.")
                    continue

                projects.append(name)
                print(f"Project added: {name}")
                # Ask whether the user wants to add another project.
                add_another = input("Would you like to enter another project? (yes/no): ").strip().lower()
                if add_another != "yes":
                    break
    elif choice == "3":
        if not projects:
            print("No projects to remove.")
        else:
            print("Projects:")
            for index, project in enumerate(projects, start=1):
                print(f"{index}. {project}")

            selection = input("Enter the number of the project to remove: ").strip()
            if not selection.isdigit():
                print("Please enter a valid project number.")
            else:
                project_index = int(selection) - 1
                if not 0 <= project_index < len(projects):
                    print("Please enter a valid project number.")
                else:
                    project = projects[project_index]
                    confirmation = input(
                        f"Are you sure you want to remove '{project}'? (yes/no): "
                    ).strip().lower()
                    if confirmation == "yes":
                        projects.pop(project_index)
                        print(f"Project removed: {project}")
                    else:
                        print("Project was not removed.")
    elif choice == "4":
        print("Goodbye!")
        break
    else:
        print("Invalid option.")
