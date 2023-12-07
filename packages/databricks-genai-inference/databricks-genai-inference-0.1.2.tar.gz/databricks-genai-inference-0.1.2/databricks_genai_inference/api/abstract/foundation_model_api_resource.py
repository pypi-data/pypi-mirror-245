"""Foundation Model API Resource.
"""
import json as json_lib
from typing import Optional

import requests
from databricks_cli.configure import provider
from pydantic import BaseModel, ConfigDict, ValidationError

from databricks_genai_inference.api.abstract.api_resource import APIResource
from databricks_genai_inference.api.abstract.foundation_model_object import FoundationModelObject
from databricks_genai_inference.api.exception import FoundationModelAPIException


class FoundationModelAPIInput(BaseModel):
    """
    A class representing the input schema for a Foundation Model API request.

    Attributes:
        model (str): The name of the model to use.
        timeout (Optional[int]): The timeout for the API request.
    """
    model_config = ConfigDict(extra='forbid')

    model: str
    timeout: Optional[int] = None


class FoundationModelAPIResource(APIResource):
    """
    A class representing a foundation model API resource.

    Attributes:
        SUPPORTED_MODEL_LIST (list): A list of supported models.
        DEFAULT_TIMEOUT (int): The default timeout for API requests.
        model_input (FoundationModelAPIInput): The input schema for the API.
        model_output (FoundationModelObject): The output schema for the API.
        model_streaming_output (FoundationModelObject): The streaming output schema for the API.
        config (Config): The configuration object for the API.
    """

    SUPPORTED_MODEL_LIST = []
    DEFAULT_TIMEOUT = 60
    model_input = FoundationModelAPIInput
    model_output = FoundationModelObject
    model_streaming_output = FoundationModelObject

    @classmethod
    def create(cls, **kwargs):
        """
        Creates a new API response.

        Args:
        **kwargs: The keyword arguments for the API.

        Returns:
        The result of the API query.
        """
        api_input = cls._parse_and_validate_request(**kwargs)
        return cls._make_query(api_input)

    @classmethod
    def _parse_and_validate_request(cls, **kwargs) -> FoundationModelAPIInput:
        """
        Parses and validates the request parameters.

        Args:
            **kwargs: The request parameters.

        Returns:
            A FoundationModelAPIInput object.

        Raises:
            FoundationModelAPIException: If the request parameters are invalid.
        """
        try:
            api_input = cls.model_input(**kwargs)
            if api_input.model not in cls.SUPPORTED_MODEL_LIST:
                raise FoundationModelAPIException(
                    message=f"Invalid model name: {api_input.model}. Supported model list: {cls.SUPPORTED_MODEL_LIST}")
            return api_input
        except ValidationError as e:
            raise FoundationModelAPIException(message=str(e)) from e

    @classmethod
    def _make_query(cls, model_input: FoundationModelAPIInput):
        """
        Makes a query to the API.

        Args:
        model_input (FoundationModelAPIInput): The input for the API.

        Returns:
        The response of the API query.

        Raises:
        FoundationModelAPIException: If the API query fails.
        """
        url = f'{provider.get_config().host}/serving-endpoints/databricks-{model_input.model}/invocations'
        headers = {'authorization': f'Bearer {provider.get_config().token}', 'Content-Type': 'application/json'}
        json = model_input.model_dump(exclude_unset=True)
        timeout = json.pop("timeout", cls.DEFAULT_TIMEOUT)
        try:
            if model_input.model_dump().get("stream", False):
                return cls._get_streaming_response(url=url, headers=headers, json=json, timeout=timeout)
            else:
                return cls._get_non_streaming_response(url=url, headers=headers, json=json, timeout=timeout)
        except requests.exceptions.ReadTimeout as e:
            raise FoundationModelAPIException(message=f'API request timed out after {timeout} seconds') from e
        except requests.exceptions.ConnectionError as e:
            raise FoundationModelAPIException(message="API request failed with connection error") from e
        except FoundationModelAPIException as e:
            raise e

    @classmethod
    def _get_non_streaming_response(cls, url, headers, json, timeout):
        """
        Sends a request to the API and returns the non-streaming response.

        Args:
        url (str): The URL for the API.
        headers (dict): The headers for the API request.
        json (dict): The JSON data for the API request.
        timeout (int): The timeout for the API request.

        Raises:
        NotImplementedError: If the method is not implemented.
        """
        response = requests.post(url=url, headers=headers, json=json, timeout=timeout)
        if response.ok:
            try:
                return cls.model_output(response.json())
            except requests.JSONDecodeError as e:
                raise FoundationModelAPIException(response=response, url=url) from e
        else:
            raise FoundationModelAPIException(response=response, url=url)

    @classmethod
    def _get_streaming_response(cls, url, headers, json, timeout):
        """
        Sends a request to the API and returns the streaming response.

        Args:
        url (str): The URL for the API.
        headers (dict): The headers for the API request.
        json (dict): The JSON data for the API request.
        timeout (int): The timeout for the API request.

        Raises:
        NotImplementedError: If the method is not implemented.
        """
        with requests.post(url=url, headers=headers, json=json, timeout=timeout, stream=True) as response:
            if response.ok:
                try:
                    for line in response.iter_lines():
                        if line:
                            line = line.decode('utf-8')
                            if line.startswith("data: "):
                                line = line[len("data: "):]
                            if line == '[DONE]':
                                break
                            loaded_json = json_lib.loads(line)
                            if loaded_json:
                                yield cls.model_streaming_output(loaded_json)
                except json_lib.decoder.JSONDecodeError as e:
                    raise FoundationModelAPIException(response=response, message="JSONDecodeError", url=url) from e
            else:
                raise FoundationModelAPIException(response=response, url=url)
