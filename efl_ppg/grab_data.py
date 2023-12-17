"""grab_data
"""
import re

import pandas as pd
import requests


def _ensure_season_format(
    season: str, expected_pattern: str = r"^\d{4}-\d{2}$"
) -> None:
    """Ensures an inputted season str matches the expected pattern (which
    is defaulted to YYYY-YY).

    Args:
        season - str: String to check.
        expected_pattern - str: Pattern to check. Defaults to ^\d{4}-\d{2}.

    Raises
        ValueError - If inputted season pattern doesn't match the expected pattern.
    """
    # TODO: Have a generic helper regex check, which this function calls.
    # TODO: Add check that the second year follows on directly.

    if not re.search(expected_pattern, season):
        raise ValueError(
            f"""
Expected season pattern in the format {expected_pattern}. Found "{season}".
        """
        )
    return


def _ensure_site_exists(url: str) -> bool:
    """Ensures a specified URL is found.

    Args
        url: str - URL to check the existence of.

    Returns
        True if the URL is found. Else, False.
    """
    response = requests.get(url)
    return True if response.status_code == 200 else False


def grab_data(
    level: int,
    season: str,
) -> pd.DataFrame | None:
    """Reads the data from github.com/football csv into a Pandas dataframe.

    Args
        level: int - Integer representation of the football pyramid level to
            get the data of, eg. 1 = Premiership.
        season: str - The season from which to get the data from. Expected to be
            in the format YYYY-YY, eg. 2023-24.

    """
    _ensure_season_format(season)

    country: str = "england"
    decade = season.split("-")[0][:3] + "0s"
    url_base: str = "https://github.com/footballcsv/{country}/blob/master/{decade}/{season}/{country_code}.{level}.csv?raw=true"

    url = url_base.format(
        country=country,
        decade=decade,
        season=season,
        country_code=country[:3],
        level=level,
    )

    if _ensure_site_exists(url):
        try:
            df = pd.read_csv(url, sep=",", dtype=object)
            print(f"Sucessfully loaded {season}, level {level} dataframe...")
            return df
        except Exception as e:
            print("Error when loading dataframe:\n", e)

    else:
        print(
            f"""
Website not found. Searched for "{url}".
Dataframe for Level {level}, Season {season} excluded. 
        """
        )
        return


if __name__ == "__main__":
    df = grab_data(1, "2020-21")
    print(df.head())
    df.to_csv("efl_ppg/test_output/test_set.csv", index=False)

__all__ = ["grab_data"]
