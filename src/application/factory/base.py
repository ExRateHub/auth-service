from abc import ABC, abstractmethod
from typing import Any


class BaseFactory[T](ABC):
    @abstractmethod
    def build(self, *args: Any, **kwargs: Any) -> T: ...
