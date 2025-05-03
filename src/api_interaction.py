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
        Creates a mock response for the get_vacancies method.
        """
        mock_response = [
            {
                "name": "Vacancy 1",
                "alternate_url": "https://example.com/vacancy1",
                "salary": {
                    "from": 1000
                },
                "snippet": {
                    "requirement": "Requirement 1"
                }
            },
            {
                "name": "Vacancy 2",
                "alternate_url": "https://example.com/vacancy2",
                "salary": {
                    "from": 2000
                },
                "snippet": {
                    "requirement": "Requirement 2"
                }
            }
        ]

        return mock_response

