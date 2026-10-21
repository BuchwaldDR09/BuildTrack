import importlib
from pathlib import Path

import pandas as pd


# Build and display the report; optional arguments filter rows and export them to CSV.
def display_project_report(search_term=None, csv_path=None):
    """Display saved project names in a DataFrame with an optional case-insensitive filter."""
    app_module = importlib.import_module("main")

    # Refuse exports that would overwrite BuildTrack's source project data.
    if csv_path is not None:
        projects_path = (Path(app_module.__file__).resolve().parent / "projects.json").resolve()
        export_path = Path(csv_path).resolve()
        if export_path == projects_path:
            print("CSV export refused: destination is the BuildTrack projects.json file.")
            csv_path = None

    projects = app_module.load_projects()

    # Keep the report shape stable when there are no saved projects.
    if not projects:
        print("No projects saved.")
        empty_df = pd.DataFrame(columns=["Project"])
        print(empty_df)
        print(f"Total projects: {len(projects)}")
        if csv_path is not None:
            empty_df.to_csv(csv_path, index=False)
        return

    # Pandas supplies the table used for both printing and optional CSV export.
    project_df = pd.DataFrame({"Project": projects})

    # Search is case-insensitive and literal, so punctuation is not treated as regex.
    if search_term is not None and str(search_term).strip():
        normalized_term = str(search_term).strip()
        filtered_df = project_df[
            project_df["Project"].astype(str).str.casefold().str.contains(
                normalized_term.casefold(), regex=False, na=False
            )
        ]

        if filtered_df.empty:
            print(f"No projects match the search term: '{normalized_term}'")
            print(filtered_df)
            print(f"Matching projects: {len(filtered_df)}")
            if csv_path is not None:
                filtered_df.to_csv(csv_path, index=False)
            return

        # Display and export the same filtered rows, with a count of those matches.
        print(f"Projects matching '{normalized_term}':")
        print(filtered_df)
        print(f"Matching projects: {len(filtered_df)}")
        if csv_path is not None:
            filtered_df.to_csv(csv_path, index=False)
        return

    # A blank or omitted search term reports every project.
    print(project_df)
    print(f"Total projects: {len(project_df)}")
    if csv_path is not None:
        project_df.to_csv(csv_path, index=False)


# Allow this module to run as a standalone report script.
def main():
    """Run the project report."""
    display_project_report()


if __name__ == "__main__":
    main()
