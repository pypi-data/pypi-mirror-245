#  -----------------------------------------------------------------------------------------
#  (C) Copyright IBM Corp. 2023.
#  https://opensource.org/licenses/BSD-3-Clause
#  -----------------------------------------------------------------------------------------

from __future__ import print_function, annotations

from ibm_watson_machine_learning.foundation_models.prompts.prompt_template import (PromptTemplateLock, PromptTemplate,
                                                                                   PromptTemplateManager)
from ibm_watsonx_ai.utils.change_methods_docstring import change_docstrings


@change_docstrings
class PromptTemplateLock(PromptTemplateLock):
    """Storage for lock object.
    """
    pass


@change_docstrings
class PromptTemplate(PromptTemplate):
    """Storage for prompt template parameters.

    :param prompt_id: Id of prompt template, defaults to None.
    :type prompt_id: Optional[str], attribute setting not allowed

    :param created_at: Time the prompt was created (UTC), defaults to None.
    :type created_at: Optional[str], attribute setting not allowed

    :param lock: Locked state of asset, defaults to None.
    :type lock: Optional[PromptTemplateLock], attribute setting not allowed

    :param is_template: True if prompt is a template, False otherwise; defaults to None.
    :type is_template: Optional[bool], attribute setting not allowed

    :param name: Prompt template name, defaults to None.
    :type name: Optional[str], optional

    :param model_id: Foundation model id, defaults to None.
    :type model_id: Optional[ModelTypes], optional

    :param model_params: Model parameters, defaults to None.
    :type model_params: Optional[Dict], optional

    :param model_version: Semvar version for tracking in IBM AI Factsheets, defaults to None.
    :type model_version: Optional[str], optional

    :param task_ids: List of task ids, defaults to None.
    :type task_ids: Optional[List[str]], optional

    :param description: Prompt template asset description, defaults to None.
    :type description: Optional[str], optional

    :param input_text: Input text for prompt, defaults to None.
    :type input_text: Optional[str], optional

    :param input_variables: Input variables can be present in fields: `instruction`,
                            `input_prefix`, `output_prefix`, `input_text`, `examples`
                            and are indentified by braces ('{' and '}'), defaults to None.
    :type temaplate_parameters: (List | Dict[str, Dict[str, str]] | None), optional

    :param instruction: Instruction for model, defaults to None.
    :type instruction: Optional[str], optional

    :param input_prefix: Prefix string placed before input text, defaults to None.
    :type input_prefix: Optional[str], optional

    :param output_prefix: Prefix before model response, defaults to None.
    :type output_prefix: Optional[str], optional

    :param exmaples: Examples may help the model to adjust the response; [[input1, output1], ...], defaults to None.
    :type exmaples: Optional[List[List[str]]], optional
    """
    pass


@change_docstrings
class PromptTemplateManager(PromptTemplateManager):
    """Instantiate the prompt template manager.

    :param credentials: Credentials to watsonx.ai instance.
    :type credentials: dict

    :param project_id: ID of project
    :type project_id: str

    :param space_id: ID of project
    :type space_id: str

    :param verify: user can pass as verify one of following:
        - the path to a CA_BUNDLE file
        - the path of directory with certificates of trusted CAs
        - `True` - default path to truststore will be taken
        - `False` - no verification will be made
    :type verify: bool or str, optional

    .. note::
        One of these parameters is required: ['project_id ', 'space_id']

    **Example**

    .. code-block:: python

        from ibm_watsonx_ai.foundation_models.prompts import PromptTemplate, PromptTemplateManager
        from ibm_watsonx_ai.foundation_models import Model
        from ibm_watsonx_ai.foundation_models.utils.enums import ModelTypes
        prompt_mgr = PromptTemplateManager(
                        model_id=ModelTypes.FLAN_UL2,
                        params=generate_params,
                        credentials={
                            "apikey": "***",
                            "url": "https://us-south.ml.cloud.ibm.com"
                        },
                        project_id="*****"
                        )

        prompt_template = PromptTemplate(name="My prompt",
                                         model_id=ModelTypes.FLAN_UL2,
                                         input_prefix="Human",
                                         output_prefix="Assistant",
                                         input_text="What is a mortgage and how does it work?")

        stored_prompt_template = prompt_mgr.store_prompt(prompt_template)
        print(stored_prompt_template.prompt_id)   # id of prompt template asset
    """
    pass
