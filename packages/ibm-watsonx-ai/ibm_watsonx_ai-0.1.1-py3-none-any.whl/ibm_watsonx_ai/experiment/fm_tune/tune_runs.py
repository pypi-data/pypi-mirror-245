#  -----------------------------------------------------------------------------------------
#  (C) Copyright IBM Corp. 2023.
#  https://opensource.org/licenses/BSD-3-Clause
#  -----------------------------------------------------------------------------------------

__all__ = [
    "TuneRuns"
]

from ibm_watson_machine_learning.experiment.fm_tune.tune_runs import TuneRuns
from ibm_watsonx_ai.utils.change_methods_docstring import change_docstrings
from ibm_watsonx_ai import APIClient


@change_docstrings
class TuneRuns(TuneRuns):
    """TuneRuns class is used to work with historical PromptTuner runs.

    :param wml_client: APIClient to handle WML operations
    :type wml_client: APIClient

    :param filter: filter, user can choose which runs to fetch specifying tuning name
    :type filter: str, optional

    :param limit: int number of records to be returned
    :type limit: int
    """
    pass
