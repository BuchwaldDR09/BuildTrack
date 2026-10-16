# BuildTrack: A Python project management application.

def show_menu():
    """Display the main menu options."""
    print("=== BuildTrack ===")
    print("1. View Projects")
    print("2. Add Project")
    print("3. Remove Project")
    print("4. Exit")

# Create the list once, so projects remain while the app runs.
projects = []

# The main loop repeats until option 4 triggers break.
while True:
    # Call the function each time the menu needs to appear.
    show_menu()

    # input() returns text, even if the user types a number.
    choice = input("Select an option: ")

    # Choice 1: Report when there are no projects to show.
    if choice == "1" and not projects:
        print("No projects to display.")
    # Choice 1: Otherwise, display each saved project.
    elif choice == "1" and projects:
        print("Projects:")
        for project in projects:
            print(f"- {project}")
    # Choice 2: Ask for project names and add each unique, non-empty name.
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
    # Choice 3: List projects by number and remove one only after confirmation.
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
    # Choice 4: End the program.
    elif choice == "4":
        print("Goodbye!")
        break
    # Any other input: Report that the menu choice is invalid.
    else:
        print("Invalid option.")
