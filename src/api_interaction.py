import requests
from src.abstract_api import APIInteraction


class HeadHunterAPI(APIInteraction):
    def __init__(self, base_url="https://api.hh.ru/vacancies"):
        self.__base_url = base_url
        super().__init__(self.__base_url)

    def get_base_url(self):
        return self.__base_url

    def get_vacancies(self, search_query):
        params = {
            "text": search_query,
            "area": 113,
            "per_page": 100,
            "page": 0,
            "only_with_salary": True
        }
        response = requests.get(self.__base_url, params=params)
        response.raise_for_status()
        return response.json()["items"]
