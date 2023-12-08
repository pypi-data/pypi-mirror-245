#  -----------------------------------------------------------------------------------------
#  (C) Copyright IBM Corp. 2023.
#  https://opensource.org/licenses/BSD-3-Clause
#  -----------------------------------------------------------------------------------------

from ibm_watson_machine_learning.foundation_models.inference.deployment_model_inference import DeploymentModelInference
from ibm_watsonx_ai.utils.change_methods_docstring import change_docstrings


__all__ = [
    "DeploymentModelInference"
]


@change_docstrings
class DeploymentModelInference(DeploymentModelInference):
    """Base abstract class for the model interface."""
    pass
