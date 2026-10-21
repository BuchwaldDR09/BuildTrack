import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import mock_open, patch

import main as BuildTrack
import pandas as pd
import project_report


# Tests cover project search, validation, persistence, and menu behavior.
class BuildTrackTests(unittest.TestCase):
    def test_search_projects_matches_partial_term_without_case(self):
        projects = ["Build Website", "Write report", "Website redesign"]

        matches = BuildTrack.search_projects(projects, "SITE")

        self.assertEqual(matches, ["Build Website", "Website redesign"])

    def test_search_projects_returns_no_matches_for_blank_term(self):
        self.assertEqual(BuildTrack.search_projects(["Alpha"], "   "), [])

    def test_project_name_exists_ignores_case_and_can_exclude_index(self):
        projects = ["Alpha", "Beta"]

        self.assertTrue(BuildTrack.project_name_exists(projects, "alpha"))
        self.assertFalse(BuildTrack.project_name_exists(projects, "ALPHA", 0))
        self.assertFalse(BuildTrack.project_name_exists(projects, "Gamma"))

    @patch("main.save_projects")
    @patch("builtins.input", side_effect=["beta", "yes", "Alpha", "no"])
    def test_add_projects_sorts_names_alphabetically(self, mock_input, mock_save):
        projects = []

        BuildTrack.add_projects(projects)

        self.assertEqual(projects, ["Alpha", "beta"])
        self.assertEqual(mock_save.call_count, 2)

    @patch("builtins.input", side_effect=["alpha", "quit"])
    def test_add_projects_rejects_duplicate_ignoring_case(self, mock_input):
        projects = ["Alpha"]
        output = io.StringIO()

        with patch("sys.stdout", output):
            BuildTrack.add_projects(projects)

        self.assertEqual(projects, ["Alpha"])
        self.assertIn("Project already exists.", output.getvalue())

    @patch("main.save_projects")
    @patch("builtins.input", side_effect=["1", "beta", "Gamma", "yes"])
    def test_rename_retries_duplicate_then_sorts(self, mock_input, mock_save):
        projects = ["Alpha", "Beta"]
        output = io.StringIO()

        with patch("sys.stdout", output):
            BuildTrack.rename_project(projects)

        self.assertEqual(projects, ["Beta", "Gamma"])
        self.assertIn("Project already exists.", output.getvalue())
        mock_save.assert_called_once_with(projects)

    @patch("main.save_projects")
    @patch("builtins.input", side_effect=["1", "yes"])
    def test_remove_project_after_confirmation(self, mock_input, mock_save):
        projects = ["Alpha", "Beta"]

        BuildTrack.remove_projects(projects)

        self.assertEqual(projects, ["Beta"])
        mock_save.assert_called_once_with(projects)

    def test_load_projects_sorts_case_insensitively(self):
        file_reader = mock_open(read_data=json.dumps(["zebra", "Apple", "banana"]))

        with patch("pathlib.Path.exists", return_value=True), patch(
            "builtins.open", file_reader
        ):
            projects = BuildTrack.load_projects()

        self.assertEqual(projects, ["Apple", "banana", "zebra"])
        file_reader.assert_called_once()

    def test_load_projects_creates_empty_json_file_when_missing(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            projects_path = Path(temp_dir) / "projects.json"
            with patch.object(BuildTrack, "__file__", str(Path(temp_dir) / "main.py")):
                projects = BuildTrack.load_projects()

            self.assertEqual(projects, [])
            self.assertTrue(projects_path.exists())
            self.assertEqual(json.loads(projects_path.read_text(encoding="utf-8")), [])

    def test_main_creates_projects_file_before_first_menu_input(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            projects_path = Path(temp_dir) / "projects.json"

            def exit_after_checking_startup_file(prompt):
                self.assertTrue(projects_path.exists())
                self.assertEqual(json.loads(projects_path.read_text(encoding="utf-8")), [])
                return "6"

            with patch.object(BuildTrack, "__file__", str(Path(temp_dir) / "main.py")), \
                 patch("builtins.input", side_effect=exit_after_checking_startup_file), \
                 patch("sys.stdout", io.StringIO()):
                BuildTrack.main()

            self.assertEqual(json.loads(projects_path.read_text(encoding="utf-8")), [])

    # Use a temporary directory to verify persistence without changing live data.
    def test_temp_directory_round_trip_saves_and_loads_projects(self):
        saved_projects = [
            "Alpha",
            "Beta",
            "Gamma",
            "Delta",
            "Epsilon",
        ]
        expected_projects = [
            "Alpha",
            "Beta",
            "Delta",
            "Epsilon",
            "Gamma",
        ]

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_project_dir = Path(temp_dir)
            with patch.object(BuildTrack, "__file__", str(temp_project_dir / "main.py")):
                BuildTrack.save_projects(saved_projects, filename="projects.json")
                reloaded_projects = BuildTrack.load_projects(filename="projects.json")

            self.assertEqual(reloaded_projects, expected_projects)
            self.assertEqual(len(reloaded_projects), 5)
            self.assertTrue((temp_project_dir / "projects.json").exists())

    def test_project_report_exports_filtered_projects_from_temporary_data(self):
        projects = ["Build Website", "Write report", "Website redesign"]
        expected_projects = ["Build Website", "Website redesign"]

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_project_dir = Path(temp_dir)
            projects_path = temp_project_dir / "projects.json"
            csv_path = temp_project_dir / "filtered-projects.csv"
            projects_path.write_text(json.dumps(projects), encoding="utf-8")
            original_projects_data = projects_path.read_bytes()

            with patch.object(BuildTrack, "__file__", str(temp_project_dir / "main.py")), \
                 patch("sys.stdout", io.StringIO()):
                project_report.display_project_report(search_term="site", csv_path=csv_path)

            exported_projects = pd.read_csv(csv_path)["Project"].tolist()
            self.assertEqual(projects_path.read_bytes(), original_projects_data)

        self.assertEqual(exported_projects, expected_projects)

    # Verify the app loads once and persists its list when the user exits.
    @patch("main.save_projects")
    @patch("main.load_projects", return_value=[])
    @patch("builtins.input", return_value="6")
    def test_main_saves_when_exiting(self, mock_input, mock_load, mock_save):
        output = io.StringIO()

        with patch("sys.stdout", output):
            BuildTrack.main()

        mock_load.assert_called_once_with()
        mock_save.assert_called_once_with([])
        self.assertIn("Goodbye!", output.getvalue())


# Support direct execution as well as unittest discovery.
if __name__ == "__main__":
    unittest.main()
