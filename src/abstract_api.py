from abc import ABC, abstractmethod


class APIInteraction(ABC):
    """
    Abstract base class for interacting with APIs.
    Defines the basic structure for API interactions.
    """

    def __init__(self, base_url: str):
        self.__base_url = base_url

    @abstractmethod
    def get_vacancies(self, search_query: str) -> list[dict]:
        pass
