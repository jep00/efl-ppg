"""generate_table

From the raw data frame found in (which is all the results from a given season),
we use the generate_table class to format it to be a league table.
"""
import pandas as pd

WIN_POINTS = 3
DRAW_POINTS = 1
LOSS_POINTS = 0


class GenerateTable:
    """ """

    def __init__(self, results: pd.DataFrame) -> None:
        self.results = results
        self.table = None

        if not self._ensure_column_headers():
            print("- Found unexpected column headers! -")

    # Validation Helpers
    def _ensure_column_headers(self) -> bool:
        expected_columns = ["Round", "Date", "Team 1", "FT", "Team 2"]
        if list(self.results.columns) != expected_columns:
            return False
        return True

    def process_results(self) -> pd.DataFrame:
        # Preparation steps of the results dataframe.
        self._map_columns()
        self._find_outcome()

        # Final season table generation
        self._create_table()
        self._populate_table()
        return self.table

    # Preparation steps helpers
    def _map_columns(self):
        """Column renaming."""
        self.results = self.results.rename(
            columns={
                "Round": "matchday",
                "Date": "date",
                "Team 1": "home_team",
                "FT": "full_time_result",
                "Team 2": "away_team",
            }
        )

    def _find_outcome(self):
        """Populates an outcome column, eg. Home Win if home goals > away goals."""
        self.results["home_goals"] = [
            x.split("–")[0] for x in self.results.full_time_result
        ]
        self.results["away_goals"] = [
            x.split("–")[1] for x in self.results.full_time_result
        ]
        self.results["outcome"] = None
        self.results.loc[
            self.results.home_goals > self.results.away_goals, "outcome"
        ] = "home_win"
        self.results.loc[
            self.results.home_goals < self.results.away_goals, "outcome"
        ] = "away_win"
        self.results.loc[
            self.results.home_goals == self.results.away_goals, "outcome"
        ] = "draw"

    # Table generation helpers
    def _create_table(self):
        """"""
        teams = list(self.results.home_team.unique())
        self.table = pd.DataFrame(data={"team": teams})
        columns_to_add = [
            "played",
            # Matches
            "win",
            "draw",
            "loss",
            # Goals
            "scored",
            "conceded",
            # Points
            "points",
        ]
        for c in columns_to_add:
            self.table[c] = 0

    def _populate_table(self):
        """Iterates through all the teams and finds the number of points and the
        goal difference based on their seasons results.
        """
        # TODO: Refactor this so it's not a for loop iterating through all teams.
        # TODO: Add differentiation between home/away results.

        for t in list(self.table.team.unique()):
            # RESULTS
            temp_df = self.results.loc[
                # Filter for any games involving the team
                (self.results.home_team == t)
                | (self.results.away_team == t)
            ]
            # Wins:
            wins = temp_df.loc[
                (
                    ((temp_df.outcome == "home_win") & (temp_df.home_team == t))
                    | ((temp_df.outcome == "away_win") & (temp_df.away_team == t))
                )
            ].shape[0]

            losses = temp_df.loc[
                (
                    ((temp_df.outcome == "home_win") & (temp_df.home_team != t))
                    | ((temp_df.outcome == "away_win") & (temp_df.away_team != t))
                )
            ].shape[0]

            draws = temp_df.loc[(temp_df.outcome == "draw")].shape[0]

            self.table.loc[self.table.team == t, "win"] = wins
            self.table.loc[self.table.team == t, "loss"] = losses
            self.table.loc[self.table.team == t, "draw"] = draws

            # GOALS
            home_goals = (
                self.results.loc[self.results.home_team == t]["home_goals"]
                .astype(int)
                .sum()
            )
            away_goals = (
                self.results.loc[self.results.away_team == t]["away_goals"]
                .astype(int)
                .sum()
            )

            home_conceded = (
                self.results.loc[self.results.home_team == t]["away_goals"]
                .astype(int)
                .sum()
            )
            away_conceded = (
                self.results.loc[self.results.away_team == t]["home_goals"]
                .astype(int)
                .sum()
            )

            self.table.loc[self.table.team == t, "scored"] = home_goals + away_goals
            self.table.loc[self.table.team == t, "conceded"] = (
                home_conceded + away_conceded
            )

        # Totals
        self.table["goal_difference"] = self.table["scored"] - self.table["conceded"]
        self.table["played"] = (
            self.table["win"] + self.table["draw"] + self.table["loss"]
        )
        self.table["points"] = (
            (WIN_POINTS * self.table["win"])
            + (DRAW_POINTS * self.table["draw"])
            + (LOSS_POINTS * self.table["loss"])
        )

        self.table = self.table.sort_values(
            by=["points", "goal_difference", "scored", "team"], ascending=False
        ).reset_index(drop=True)


if __name__ == "__main__":
    df = pd.read_csv("efl_ppg/test_output/test_set.csv")
    table_generator = GenerateTable(results=df)
    table = table_generator.process_results()
    table.to_csv("efl_ppg/test_output/test_table.csv", index=False)
