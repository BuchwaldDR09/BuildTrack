# BuildTrack: A Python project management application.

# Create the project list once so names survive menu repetitions.
projects = []

# Repeat the main menu until the user chooses Exit.
while True:
    print("=== BuildTrack ===")
    print("1. View Projects")
    print("2. Add Project")
    print("3. Exit")

    choice = input("Select an option: ")

    if choice == "1" and not projects:
        print("No projects to display.")
    elif choice == "1" and projects:
        print("Projects:")
        for project in projects:
            print(f"- {project}")
    elif choice == "2":
        # Keep accepting projects until the user types 'quit'.
        while True:
            # strip() removes whitespace around the entered name.
            name = input("Project name (type 'quit' to cancel): ").strip()
            if name == "quit":
                break  # Return to the main menu.
            elif not name:
                # An empty string is false, so it must not be saved.
                print("Project name cannot be empty.")
            else:
                projects.append(name)
                print(f"Project added: {name}")
    elif choice == "3":
        print("Goodbye!")
        break
    else:
        print("Invalid option.")
