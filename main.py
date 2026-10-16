# BuildTrack: A Python project management application.
# Display the main menu.
print("=== BuildTrack ===")
print("1. View Projects")
print("2. Add Project")
print("3. Exit")

# Read the menu selection as text.
choice = input("Select an option: ")

# Respond to the selected option; catch unsupported choices with else.
if choice == "1":
    print("No projects yet.")
elif choice == "2":
    print("Let's add a project!")
elif choice == "3":
    print("Goodbye!")
else:
    print("Invalid option.")
