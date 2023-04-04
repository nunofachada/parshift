# Copyright (c) 2022-2023 Bruno Saraiva and contributors
# Distributed under the MIT License (See accompanying file LICENSE or copy
# at http://opensource.org/licenses/MIT)

from __future__ import annotations
from pandas._typing import FilePath, ReadCsvBuffer
from typing import Any
import matplotlib.pyplot as plt
import pandas as pd

from .annotation import read_ccsv, annotate
from .statistics import cond_probs
from .plotting import frequency_treemap

# from parshift.annotation import read_ccsv, annotate
# from parshift.statistics import cond_probs
# from parshift.plotting import frequency_treemap


class Parshift:
    def __init__(self):
        """Parshift initialization"""

        self.annotation: pd.DataFrame
        self.stats: pd.DataFrame

    def load_and_process(
        self,
        filepath_or_buffer: FilePath | ReadCsvBuffer[bytes] | ReadCsvBuffer[str],
        **kwargs: Any,
    ):
        """Read a conversation file in CSV format, validate it,
        get Gibson's participation shift codes from turns in a conversation,
        determine the conditional probabilities for a sequence of participation shift codes
        and return a dict with parshift annotations and conditional probabilities.

        The conversation file should have the following columns:

        - `id`: ID of the message (int)
        - `user_id`: ID of the user sending the message (str)
        - `message_text`: The message itself (string)
        - `reply_to_id` or `target_id`: The reply ID or the target ID (int)

        Arguments:
            filepath_or_buffer: Any valid string path to CSV file, as accepted by
                Pandas [`read_csv()`][pandas.read_csv] function.
            **kwargs: Keyword parameters passed to Pandas
                [`read_csv()`][pandas.read_csv] function.

        - Parshift.annotation will be dataframe equal as returned by [`annotate()`][parshift.annotation.annotate].
        - Parshift.stats will be dataframe equal as returned by [`cond_probs()`][parshift.statistics.cond_probs].
        """

        df_annotate = annotate(read_ccsv(filepath_or_buffer, **kwargs))

        self.annotation = df_annotate
        self.stats = cond_probs(df_annotate)

    def get_plot(self, type: str = "pshift", save: bool = False):

        if self.stats is None:
            raise ValueError(
                "Parshift.stats is None. Please run Parshift.load_and_process() first."
            )

        if type == "pshift":
            ax = frequency_treemap(self.stats, column_name="pshift")
        elif type == "pshift_type":
            ax = frequency_treemap(self.stats, column_name="pshift_type")

        if save:
            ax.savefig(f"plot_{type}.png")
        else:
            # plt.show()
            return ax
