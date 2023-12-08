#  -----------------------------------------------------------------------------------------
#  (C) Copyright IBM Corp. 2023.
#  https://opensource.org/licenses/BSD-3-Clause
#  -----------------------------------------------------------------------------------------
from ibm_watson_machine_learning.foundation_models.inference.fm_model_inference import FMModelInference
from ibm_watsonx_ai.utils.change_methods_docstring import change_docstrings


__all__ = [
    "FMModelInference"
]


@change_docstrings
class FMModelInference(FMModelInference):
    """Base abstract class for the model interface."""
    pass
