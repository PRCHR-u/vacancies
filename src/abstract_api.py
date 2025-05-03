from abc import ABC, abstractmethod

class APIInteraction(ABC):
    def __init__(self, base_url: str):
        self.__base_url = base_url

    @abstractmethod
    def get_vacancies(self, search_query):
        pass