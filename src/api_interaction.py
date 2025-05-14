import requests
from src.abstract_api import APIInteraction


class HeadHunterAPI(APIInteraction):
    """
    Represents an API interaction with the HeadHunter platform.
    """

    def __init__(self, base_url="https://api.hh.ru/vacancies"):
        self.__base_url = base_url
        super().__init__(self.__base_url)

    def get_base_url(self) -> str:
        """
        Returns the base URL for the API.

        Returns:
            str: The base URL.
        """
        return self.__base_url

    def get_vacancies(self, search_query: str) -> list[dict]:
        """
        Fetches vacancies from the HeadHunter API.
        """
        params = {
            "text": search_query,
            "page": 0,
            "per_page": 100,
            "only_with_salary": True
            }
        response = requests.get(self.__base_url, params=params)
        if response.status_code == 200:
            return response.json()["items"]
        else:
            print(
                f"Error fetching vacancies: Status code {response.status_code}"
            )
            return []
