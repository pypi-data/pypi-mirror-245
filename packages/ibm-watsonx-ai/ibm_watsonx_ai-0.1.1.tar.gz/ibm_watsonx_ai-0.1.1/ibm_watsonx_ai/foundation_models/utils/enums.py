#  -----------------------------------------------------------------------------------------
#  (C) Copyright IBM Corp. 2023.
#  https://opensource.org/licenses/BSD-3-Clause
#  -----------------------------------------------------------------------------------------

from ibm_watson_machine_learning.foundation_models.utils.enums import (ModelTypes, DecodingMethods, PromptTuningTypes,
                                                                       PromptTuningInitMethods, TuneExperimentTasks,
                                                                       PromptTemplateFormats)

from ibm_watsonx_ai.utils.change_methods_docstring import copy_enum

__all__ = [
    "ModelTypes",
    "DecodingMethods",
    "PromptTuningTypes",
    "PromptTuningInitMethods",
    "TuneExperimentTasks",
    "PromptTemplateFormats",
]

ModelTypes = copy_enum(ModelTypes)

DecodingMethods = copy_enum(DecodingMethods)

PromptTuningTypes = copy_enum(PromptTuningTypes)

PromptTuningInitMethods = copy_enum(PromptTuningInitMethods)

TuneExperimentTasks = copy_enum(TuneExperimentTasks)

PromptTemplateFormats = copy_enum(PromptTemplateFormats)
