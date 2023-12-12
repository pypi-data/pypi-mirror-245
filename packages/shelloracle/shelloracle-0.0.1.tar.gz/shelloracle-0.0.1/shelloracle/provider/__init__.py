from abc import abstractmethod
from collections.abc import AsyncGenerator
from typing import Protocol


class Provider(Protocol):
    """
    LLM Provider Protocol

    All providers must implement this interface.
    """

    @abstractmethod
    def generate(self, prompt: str) -> AsyncGenerator[str, None, None]:
        """
        This is an asynchronous generator method which defines the protocol that a provider implementation
        should adhere to. The method takes a prompt as an argument and produces an asynchronous stream
        of string results.

        :param prompt: A string value which serves as input to the provider's process of generating results.
        :return: An asynchronous generator yielding string results.
        """


def get_provider(name: str) -> type[Provider]:
    from .ollama import Ollama
    providers = {
        "ollama": Ollama
    }
    return providers[name]
