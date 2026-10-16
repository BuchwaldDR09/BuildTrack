# BuildTrack: A Python project management application.

# Create this list once so projects persist while the program runs.
projects = []

# The main menu repeats until option 4 executes break.
while True:
    print("=== BuildTrack ===")
    print("1. View Projects")
    print("2. Add Project")
    print("3. Remove Project")
    print("4. Exit")

    choice = input("Select an option: ")

    if choice == "1" and not projects:
        print("No projects to display.")
    elif choice == "1" and projects:
        print("Projects:")
        for project in projects:
            print(f"- {project}")
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
    elif choice == "3":
        if not projects:
            print("No projects to remove.")
        else:
            print("Projects:")
            # enumerate(..., start=1) numbers each project for the user.
            for index, project in enumerate(projects, start=1):
                print(f"{index}. {project}")

            selection = input("Enter the number of the project to remove: ").strip()
            # isdigit() rejects letters and blank input before int() is called.
            if not selection.isdigit():
                print("Please enter a valid project number.")
            else:
                # List indexes start at 0, but menu numbering starts at 1.
                project_index = int(selection) - 1
                if not 0 <= project_index < len(projects):
                    print("Please enter a valid project number.")
                else:
                    project = projects[project_index]
                    confirmation = input(
                        f"Are you sure you want to remove '{project}'? (yes/no): "
                    ).strip().lower()
                    if confirmation == "yes":
                        # pop(index) deletes the selected item from the list.
                        projects.pop(project_index)
                        print(f"Project removed: {project}")
                    else:
                        print("Project was not removed.")
    elif choice == "4":
        print("Goodbye!")
        break
    else:
        print("Invalid option.")
