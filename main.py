from src.api_interaction import HeadHunterAPI
from src.file_interaction import JSONSaver
from src.vacancy_interaction import Vacancy, filter_vacancies, get_vacancies_by_salary, sort_vacancies, get_top_vacancies, print_vacancies
import os


def user_interaction():
    """Функция для взаимодействия с пользователем."""
    hh_api = HeadHunterAPI()
    json_saver = JSONSaver()
    
    existing_data = json_saver.read_from_file("vacancies.json")

    search_query = input("Введите поисковый запрос: ")
    hh_vacancies = hh_api.get_vacancies(search_query)
    vacancies = Vacancy.cast_to_object_list(hh_vacancies)

    new_data = []
    for vacancy in vacancies:
        new_data.append({
            'title': vacancy.title,
            'url': vacancy.url,
            'salary': vacancy.salary,
            'requirements': vacancy.requirements
        })
    

    top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()
    salary_range = input("Введите диапазон зарплат: ")

    filtered_vacancies = filter_vacancies(vacancies_list, filter_words)
    ranged_vacancies = get_vacancies_by_salary(filtered_vacancies, salary_range)
    
    sorted_vacancies = sort_vacancies(ranged_vacancies)
    top_vacancies = get_top_vacancies(sorted_vacancies, top_n)
    print_vacancies(top_vacancies)


if __name__ == "__main__":
    user_interaction()
