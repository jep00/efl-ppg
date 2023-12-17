"""Testing for generate_table module.

To do this, we will - assuming the grab_data class works as expected - generate
a table and compare against a known correct league table.
"""
import unittest

import pandas as pd

from efl_ppg.grab_data import grab_data
from efl_ppg.generate_table import GenerateTable


def prepare_test_dataset(level: int, season: str) -> pd.DataFrame:
    """ """
    results_set = grab_data(level, season)
    table_generator = GenerateTable(results=results_set)
    return table_generator.process_results()


class TestGenerateTable(unittest.TestCase):
    pass


def main():
    prepare_test_dataset(1, "2010-11")
    return


if __name__ == "__main__":
    main()
