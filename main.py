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
        # The inner loop accepts multiple project names until 'quit'.
        while True:
            # Remove leading and trailing spaces before validating.
            name = input("Project name (type 'quit' to cancel): ").strip()
            if name == "quit":
                break  # Return to the outer menu loop.
            elif not name:
                print("Project name cannot be empty.")
            else:
                # Reject exact duplicates before appending.
                if name in projects:
                    print("Project already exists.")
                    continue  # Ask for another name without adding this one.

                projects.append(name)
                print(f"Project added: {name}")
    elif choice == "3":
        print("Goodbye!")
        break
    else:
        print("Invalid option.")
