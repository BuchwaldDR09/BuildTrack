"""Read-only Pandas reports for BuildTrack's saved projects."""

import importlib

import pandas as pd


def display_project_report(search_term=None):
    """Display saved project names in a DataFrame with an optional case-insensitive filter."""
    # Import on demand to avoid a circular import with main.py.
    app_module = importlib.import_module("main")
    projects = app_module.load_projects()  # Reading does not change projects.json.

    if not projects:
        print("No projects saved.")
        empty_df = pd.DataFrame(columns=["Project"])
        print(empty_df)
        print(f"Total projects: {len(projects)}")
        return

    project_df = pd.DataFrame({"Project": projects})

    if search_term is not None and str(search_term).strip():
        normalized_term = str(search_term).strip()
        filtered_df = project_df[
            project_df["Project"].astype(str).str.casefold().str.contains(
                # regex=False treats punctuation like '.' and '[' literally.
                normalized_term.casefold(), regex=False, na=False
            )
        ]

        if filtered_df.empty:
            print(f"No projects match the search term: '{normalized_term}'")
            print(filtered_df)
            print(f"Matching projects: {len(filtered_df)}")
            return

        print(f"Projects matching '{normalized_term}':")
        print(filtered_df)
        print(f"Matching projects: {len(filtered_df)}")
        return

    print(project_df)
    print(f"Total projects: {len(project_df)}")


def main():
    """Run the project report."""
    display_project_report()


if __name__ == "__main__":
    main()
