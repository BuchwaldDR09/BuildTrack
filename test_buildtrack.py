"""Regression tests for BuildTrack's project-management functions.

Run with: python -m unittest -v test_buildtrack
Mocks keep interactive inputs deterministic; temporary directories isolate real JSON I/O.
"""

import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import mock_open, patch

# main.py is the actual Python module. The alias provides a descriptive name.
import main as BuildTrack


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

    # Patch where the function is defined (main), not the local import alias.
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

    def test_temp_directory_round_trip_saves_and_loads_projects(self):
        """Exercise real JSON I/O without writing to the user's projects.json."""
        # Saving preserves the input order; loading returns a sorted project list.
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

        # The temporary directory is automatically removed after the test.
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_project_dir = Path(temp_dir)
            # Point BuildTrack's __file__ into the temporary folder.
            with patch.object(BuildTrack, "__file__", str(temp_project_dir / "main.py")):
                BuildTrack.save_projects(saved_projects, filename="projects.json")
                reloaded_projects = BuildTrack.load_projects(filename="projects.json")

            self.assertEqual(reloaded_projects, expected_projects)
            self.assertEqual(len(reloaded_projects), 5)
            self.assertTrue((temp_project_dir / "projects.json").exists())

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


if __name__ == "__main__":
    unittest.main()
