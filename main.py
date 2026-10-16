# BuildTrack: A Python project management application.

# True is always true, so this loop repeats until break is reached.
while True:
    # Display the menu each time through the loop.
    print("=== BuildTrack ===")
    print("1. View Projects")
    print("2. Add Project")
    print("3. Exit")

    # input() returns text, even when the user types a number.
    choice = input("Select an option: ")

    if choice == "1":
        print("No projects yet.")
    elif choice == "2":
        print("Let's add a project!")
    elif choice == "3":
        print("Goodbye!")
        break  # Exit the loop and end the program.
    else:
        print("Invalid option.")
