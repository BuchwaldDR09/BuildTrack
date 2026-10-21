"""Read-only Pandas reporting for saved BuildTrack projects."""

import importlib

import pandas as pd


def display_project_report():
    """Display saved project names in a DataFrame with a total count."""
    # Load the application module when the report is requested. This keeps
    # main.py's import of this module from becoming a circular import at startup.
    app_module = importlib.import_module("main")
    projects = app_module.load_projects()  # Reads JSON; does not save or edit it.

    if not projects:
        print("No projects saved.")
        # Explicit columns give the empty report the same structure as full ones.
        empty_df = pd.DataFrame(columns=["Project"])
        print(empty_df)
        print(f"Total projects: {len(projects)}")
        return

    # Each project name becomes one row under the "Project" column.
    project_df = pd.DataFrame({"Project": projects})
    print(project_df)
    print(f"Total projects: {len(project_df)}")


def main():
    """Run the project report on its own, outside BuildTrack's menu."""
    display_project_report()


if __name__ == "__main__":
    main()
