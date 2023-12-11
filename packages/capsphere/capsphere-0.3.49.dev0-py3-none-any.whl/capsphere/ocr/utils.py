from abc import ABC, abstractmethod
from typing import Any


class DocumentScanner(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def verify(self) -> None:
        pass

    @abstractmethod
    def convert(self) -> Any:
        pass


