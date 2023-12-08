#  -----------------------------------------------------------------------------------------
#  (C) Copyright IBM Corp. 2023.
#  https://opensource.org/licenses/BSD-3-Clause
#  -----------------------------------------------------------------------------------------

from ibm_watson_machine_learning.foundation_models.inference.base_model_inference import BaseModelInference
from ibm_watsonx_ai.utils.change_methods_docstring import change_docstrings
from abc import ABC


__all__ = [
    "BaseModelInference"
]


@change_docstrings
class BaseModelInference(BaseModelInference, ABC):
    """Base interface class for the model interface."""
    pass
