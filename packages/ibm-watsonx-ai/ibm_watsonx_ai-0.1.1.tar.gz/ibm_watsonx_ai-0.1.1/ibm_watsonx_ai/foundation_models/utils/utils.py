#  -----------------------------------------------------------------------------------------
#  (C) Copyright IBM Corp. 2023.
#  https://opensource.org/licenses/BSD-3-Clause
#  -----------------------------------------------------------------------------------------

from ibm_watson_machine_learning.foundation_models.utils.utils import (PromptTuningParams, _get_foundation_models_spec,
                                                                       get_model_specs, get_supported_tasks,
                                                                       get_all_supported_tasks_dict, load_request_json,
                                                                       is_training_prompt_tuning, TemplateFormatter)

from ibm_watsonx_ai.utils.change_methods_docstring import change_docstrings, copy_func


@change_docstrings
class PromptTuningParams(PromptTuningParams):
    pass


_get_foundation_models_spec = copy_func(_get_foundation_models_spec)

get_model_specs = copy_func(get_model_specs)

get_supported_tasks = copy_func(get_supported_tasks)

get_all_supported_tasks_dict = copy_func(get_all_supported_tasks_dict)

load_request_json = copy_func(load_request_json)

is_training_prompt_tuning = copy_func(is_training_prompt_tuning)


@change_docstrings
class TemplateFormatter(TemplateFormatter):
    pass
