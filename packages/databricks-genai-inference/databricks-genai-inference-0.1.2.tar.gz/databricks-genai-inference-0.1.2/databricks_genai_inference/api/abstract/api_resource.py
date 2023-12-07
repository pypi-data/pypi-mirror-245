from abc import ABC, abstractmethod
from typing import Generator, Union

from pydantic import BaseModel

from databricks_genai_inference.api.abstract.foundation_model_object import FoundationModelObject


class APIResource(ABC):

    @classmethod
    @abstractmethod
    def create(cls, **kwargs) -> Union[FoundationModelObject, Generator[FoundationModelObject, None, None]]:
        pass

    @classmethod
    @abstractmethod
    def _parse_and_validate_request(cls, **kwargs) -> BaseModel:
        pass

    @classmethod
    @abstractmethod
    def _get_non_streaming_response(cls, url, headers, json, timeout) -> FoundationModelObject:
        pass

    @classmethod
    @abstractmethod
    def _get_streaming_response(cls, url, headers, json, timeout) -> Generator[FoundationModelObject, None, None]:
        pass
