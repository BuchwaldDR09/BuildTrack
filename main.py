# BuildTrack: A Python project management application.

# Create the project list once, before the repeating menu begins.
projects = []

# Keep showing the main menu until option 3 uses break to exit.
while True:
    print("=== BuildTrack ===")
    print("1. View Projects")
    print("2. Add Project")
    print("3. Exit")

    choice = input("Select an option: ")

    # An empty list is False in a condition; a non-empty list is True.
    if choice == "1" and not projects:
        print("No projects to display.")
    elif choice == "1" and projects:
        print("Projects:")
        # Visit each project in the list and display its name.
        for project in projects:
            print(f"- {project}")
    elif choice == "2":
        # This inner loop allows multiple additions in one menu visit.
        while True:
            name = input("Project name (type 'quit' to cancel): ")
            if name == "quit":
                break  # Leave the inner loop and return to the main menu.
            projects.append(name)
            print(f"Project added: {name}")
    elif choice == "3":
        print("Goodbye!")
        break  # Leave the main menu loop and end the program.
    else:
        print("Invalid option.")
