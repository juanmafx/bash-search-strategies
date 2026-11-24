import tempfile
import unittest
from pathlib import Path

from tests.support.harness import run_shell


def count(directory):
    return run_shell('count_directory_entries "$1"', str(directory))


class CountDirectoryEntriesTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.directory = Path(self.temporary.name)

    def test_empty_directory_is_zero(self):
        self.assertEqual(count(self.directory).stdout.strip(), "0")

    def test_counts_files_and_directories(self):
        (self.directory / "file").touch()
        (self.directory / "folder").mkdir()
        self.assertEqual(count(self.directory).stdout.strip(), "2")

    def test_hidden_entries_are_excluded(self):
        (self.directory / ".hidden").touch()
        (self.directory / "visible").touch()
        self.assertEqual(count(self.directory).stdout.strip(), "1")

    def test_filename_with_newline_counts_once(self):
        (self.directory / "two\nlines").touch()
        self.assertEqual(count(self.directory).stdout.strip(), "1")

    def test_directory_name_with_glob_characters(self):
        nested = self.directory / "a*[b] c"
        nested.mkdir()
        (nested / "file").touch()
        (self.directory / "other").touch()
        self.assertEqual(count(nested).stdout.strip(), "1")

    def test_missing_directory_fails(self):
        self.assertNotEqual(count(self.directory / "missing").returncode, 0)
