from typing import TypeVar

from polyfactory.factories.pydantic_factory import ModelFactory
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class BasePydanticFactory(ModelFactory[T]):
    __is_base_factory__ = True
    __use_examples__ = True
    __use_defaults__ = True
