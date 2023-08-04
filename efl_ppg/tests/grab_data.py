"""Testing for grab_data module.
"""
import unittest

from efl_ppg.grab_data import _ensure_season_format, _ensure_site_exists


class TestGrabData(unittest.TestCase):
    def test_ensure_season_format_with_default_pattern(self):
        self.assertIsNone(_ensure_season_format("2023-24"))

    def test_ensure_season_format_with_pattern_override(self):
        self.assertIsNone(
            _ensure_season_format("2-2", expected_pattern=r"^\d{1}-\d{1}$")
        )
        self.assertIsNone(_ensure_season_format("Anything", expected_pattern=r"^.*$"))

    def test_ensure_season_format_failures_with_default_pattern(self):
        with self.assertRaises(ValueError):
            _ensure_season_format("20AA-23")

        with self.assertRaises(ValueError):
            _ensure_season_format("2022/23")

        with self.assertRaises(ValueError):
            _ensure_season_format("202324")

    def test_ensure_season_format_failures_with_pattern_override(self):
        with self.assertRaises(ValueError):
            _ensure_season_format("2022-23", expected_pattern=r"^\d{6}$")

        with self.assertRaises(ValueError):
            _ensure_season_format("2022/23", expected_pattern=r"^\d{4}/{2}$")

    def test_ensure_site_exists_for_non_existing_url(self):
        self.assertIs(
            _ensure_site_exists("https://jep00.github.io/a-page-that-doesnt-exist"),
            False,
        )

    def test_ensure_site_exists_for_existing_url(self):
        self.assertIs(_ensure_site_exists("https://jep00.github.io"), True)


if __name__ == "__main__":
    unittest.main()
