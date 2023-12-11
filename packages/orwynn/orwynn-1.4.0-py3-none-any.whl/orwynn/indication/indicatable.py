from typing import TypeVar, Union

from orwynn.model.model import Model

Indicatable = Union[Model, Exception]
IndicatableTypeVar = TypeVar("IndicatableTypeVar", bound=Indicatable)
