from src.api_interaction import HeadHunterAPI
from src.file_interaction import JSONSaver
from src.vacancy_interaction import Vacancy, filter_vacancies, get_vacancies_by_salary, sort_vacancies, get_top_vacancies
from typing import Dict


def _get_vacancies(api: HeadHunterAPI, search_query: str) -> list[Vacancy]:
    """
    Fetches vacancies from the API based on the search query.

    Args:
        api: An instance of HeadHunterAPI.
        search_query: The search query string.

    Returns:
        A list of Vacancy objects.
    """
    """
    
    Fetches vacancies from the API based on the search query.

    Args:
        api: An instance of HeadHunterAPI.
        search_query: The search query string.

    Returns:
        A list of Vacancy objects.
    """
    hh_vacancies = api.get_vacancies(search_query)
    vacancies = Vacancy.cast_to_object_list(hh_vacancies) if hh_vacancies else []
    return vacancies


def print_vacancies(vacancies) -> list:
    """
    Prints information about each vacancy in the provided list.

    Args:
        vacancies: A list of Vacancy objects.
    """

    for vacancy in vacancies:
        print(f"{vacancy.title}, url: {vacancy.url}, salary: {vacancy.salary}, requirements: {vacancy.requirements}")
    return vacancies


def _save_data(saver: JSONSaver, data: list):
    """
    Saves data to file using provided saver object.

    Args:
        saver: file saver object
        data: data to save

    """

    existing_data = saver.read_from_file()
    new_data = []
    for vacancy in data:
        new_data.append({
            'title': vacancy.title,
            'url': vacancy.url,
            'salary': vacancy.salary,
            'requirements': vacancy.requirements
        })
    existing_urls = {item['url'] for item in existing_data}
    unique_data = [item for item in new_data if item['url'] not in existing_urls]
    existing_data.extend(unique_data)
    saver.write_to_file(existing_data)


def _get_user_parameters() -> Dict:
    """
    Gets user input for filtering and sorting vacancies.

    Returns:
        A dictionary containing user parameters (top_n, filter_words, salary_range).
    """
    top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()
    salary_range = input("Введите диапазон зарплат: ")
    return {"top_n": top_n, "filter_words": filter_words, "salary_range": salary_range}


def _process_vacancies(vacancies: list[Vacancy], parameters: Dict) -> list[Vacancy]:
    """
    Filters, sorts, and gets the top N vacancies based on user parameters.

    Args:
        vacancies: A list of Vacancy objects.
        parameters: A dictionary of user parameters.

    Returns:
        A list of processed Vacancy objects.
    """
    filtered_vacancies = filter_vacancies(vacancies, parameters["filter_words"])
    ranged_vacancies = get_vacancies_by_salary(filtered_vacancies, parameters["salary_range"])
    top_vacancies = get_top_vacancies(ranged_vacancies, len(ranged_vacancies) if len(ranged_vacancies) < parameters["top_n"] else parameters["top_n"] )
    return top_vacancies


def user_interaction():
    """

    Main function for user interaction.
    Fetches vacancies, saves them to file,
    gets user parameters for filtering,
    filters and sorts vacancies,
    and prints the top vacancies.

    """

    api = HeadHunterAPI()

    search_query = input("Введите поисковый запрос: ")
    vacancies = _get_vacancies(api, search_query)
    _save_data(JSONSaver(), vacancies)

    parameters = _get_user_parameters()    

    top_vacancies = _process_vacancies(vacancies, parameters)
    print_vacancies(top_vacancies)


if __name__ == "__main__":
    user_interaction()
