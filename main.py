import json, requests
from typing import List

class HeadHunterAPI:
    """Класс для работы с API hh.ru."""
    def __init__(self) -> None:
        """Инициализация API hh.ru."""
        self.base_url = "https://api.hh.ru/vacancies"

    def get_vacancies(self, search_query: str) -> list[dict]:
        """Получение вакансий с hh.ru в формате JSON."""
        params = {
            "text": search_query,
            "per_page": 100,
            "page": 0
        }
        response = requests.get(self.base_url, params=params)
        response.raise_for_status()
        return response.json()["items"]

class Vacancy:
    """Класс для представления вакансии."""
    def __init__(self, title: str, url: str, salary: str, requirements: str) -> None:
        """Инициализация вакансии."""
        self.title = title
        self.url = url
        self.salary = salary
        self.requirements = requirements

    def __str__(self) -> str:
        """Строковое представление вакансии."""
        return f"{self.title} ({self.url}) - {self.salary}\nТребования: {self.requirements}"

    @staticmethod
    def cast_to_object_list(vacancies: list[dict]) -> list["Vacancy"]:
        """Преобразование списка вакансий из JSON в список объектов."""
        objects = []
        for vacancy in vacancies:
            title = vacancy["name"]
            url = vacancy["alternate_url"]
            salary = "Не указана"
            if vacancy["salary"]:
                salary = f"{vacancy['salary']['from'] or ''}-{vacancy['salary']['to'] or ''} {vacancy['salary']['currency'] or ''}"
            requirements = vacancy.get("snippet", {}).get("requirement", "Не указаны")
            objects.append(Vacancy(title, url, salary, requirements))
        return objects

class JSONSaver:
    """Класс для сохранения информации о вакансиях в файл."""
    def __init__(self, filename: str = "vacancies.json") -> None:
        """Инициализация сохранения вакансий."""
        self.filename = filename
        self.data: List[dict] = []

    def add_vacancy(self, vacancy: Vacancy) -> None:
        """Добавление вакансии в список."""
        self.data.append({
            "title": vacancy.title,
            "url": vacancy.url,
            "salary": vacancy.salary,
            "requirements": vacancy.requirements
        })
        self._save_to_file()

    def delete_vacancy(self, vacancy: Vacancy) -> None:
        """Удаление вакансии из списка."""
        self.data = [v for v in self.data if v["url"] != vacancy.url]
        self._save_to_file()
    
    def _save_to_file(self) -> None:
        with open(self.filename, "w", encoding='utf-8') as file:
            json.dump(self.data, file, ensure_ascii=False, indent=4)

    def __len__(self):
        return len(self.data)

def filter_vacancies(vacancies: List[Vacancy], filter_words: List[str]) -> List[Vacancy]:
    """Фильтрация вакансий по ключевым словам."""
    return [v for v in vacancies if any(word.lower() in v.title.lower() or word.lower() in v.requirements.lower() for word in filter_words)]

def sort_vacancies(vacancies: List[Vacancy]) -> List[Vacancy]:
    """Сортировка вакансий по зарплате."""
    return sorted(vacancies, key=lambda v: int(v.salary.split('-')[0]) if '-' in v.salary and v.salary.split('-')[0].isdigit() else 0, reverse=True)

def get_top_vacancies(vacancies: List[Vacancy], top_n: int) -> List[Vacancy]:
    """Получение топ N вакансий."""
    return vacancies[:top_n]

def get_vacancies_by_salary(vacancies: List[Vacancy], salary_range: str) -> List[Vacancy]:
    """Получение вакансий по диапазону зарплат."""
    try:
        min_salary, max_salary = map(int, salary_range.split('-'))
        return [v for v in vacancies if v.salary != "Не указана" and min_salary <= int(v.salary.split('-')[0]) <= max_salary]
    except ValueError:
        print("Некорректный диапазон зарплат.")
        return []

def print_vacancies(vacancies: List[Vacancy]) -> None:
    """Вывод списка вакансий на экран."""
    for vacancy in vacancies:
        print(vacancy)


def user_interaction():

    hh_api = HeadHunterAPI()
    json_saver = JSONSaver()
    search_query = input("Введите поисковый запрос: ")
    hh_vacancies = hh_api.get_vacancies(search_query)
    vacancies_list = Vacancy.cast_to_object_list(hh_vacancies)
    for vacancy in vacancies_list:
        json_saver.add_vacancy(vacancy)    
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

