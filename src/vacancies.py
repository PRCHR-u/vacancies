import uuid
import json
from abc import ABC, abstractmethod
from typing import List
import requests


class DataSaver(ABC):

    """
    Абстрактный класс для сохранения информации о вакансиях в файл.
    """

    @abstractmethod
    def add_vacancy(self, vacancy):
        pass

    @abstractmethod
    def get_vacancies(self, criteria: dict):
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy):
        pass


class Vacancy:

    """
    Класс для представления вакансии.



    """

    def __init__(self, title: str, url: str, salary: str, description: str):
        self._title = title
        self._url = url
        self._salary = (
            self.validate_salary(salary)
            if salary is not None
            else "Зарплата не указана"
        )
        self._description = description
        self._id = str(uuid.uuid4())

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, title: str):
        if not isinstance(title, str) or not title:
            raise ValueError("Title must be a non-empty string.")
        self._title = title

    @property
    def url(self) -> str:
        return self._url

    @url.setter
    def url(self, url: str):
        if not isinstance(url, str) or not url:
            raise ValueError("URL must be a non-empty string.")
        self._url = url

    @property
    def salary(self) -> str:
        return self._salary

    @salary.setter
    def salary(self, salary: str):
        self._salary = self.validate_salary(salary)

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, description: str):
        if not isinstance(description, str) or not description:
            raise ValueError("Description must be a non-empty string.")
        self._description = description

    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, id: str):
        if not isinstance(id, str) or not id:
            raise ValueError("Id must be a non-empty string.")
        self._id = id
    def __repr__(self):
        return (
            f"{self.__class__.__name__}(title={self.title}, url={self.url}, salary={self.salary}, "
            f"description={self.description}, id={self.id})"
        )
        self.title = title
        self.url = url
        self.salary = self.validate_salary(salary) if salary is not None else "Зарплата не указана"


        self.description = description
        self.id = str(uuid.uuid4())

    def __str__(self) -> str:
        """
        Возвращает название вакансии.

        Returns:
            str: Название вакансии.
        """


    def __lt__(self, other):
        """
        Сравнивает вакансии по зарплате.

        Args:
            other (Vacancy): Другая вакансия для сравнения.


        Returns:
            bool: True, если зарплата текущей вакансии меньше, чем у другой, иначе False.
        """
        if not isinstance(other, Vacancy):
            raise TypeError("Can compare Vacancy with only Vacancy")
        
        self_salary = self.get_salary_value(self.salary)
        other_salary = self.get_salary_value(other.salary)
        return self_salary < other_salary

    
    def get_salary_value(self, salary: str) -> int:
        """
        Извлекает числовое значение зарплаты из строки.

        Args:
            salary (str): Строка с зарплатой.

        Returns:
            int: Числовое значение зарплаты.
        """
        if salary == "Зарплата не указана":
            return 0
        # Предполагаем формат "100 000-150 000 руб."
        salary_range = salary.split(" ")[0].split("-")
        try:
            if len(salary_range) == 2:
                # Используем среднее значение
                return (int(salary_range[0].replace(" ", "")) + int(salary_range[1].replace(" ", ""))) // 2
            elif len(salary_range) == 1:
                return int(salary_range[0].replace(" ", ""))
        except ValueError:
            return 0

    def cast_to_object_list(json_data: list) -> list:
        """
        Преобразует набор данных из JSON в список объектов Vacancy.

        Args:
            json_data (list): Список словарей с данными о вакансиях.

        Returns:
            list: Список объектов Vacancy.
        """
        vacancies = []
        for item in json_data:
        
            # Проверка наличия необходимых ключей
            if 'name' in item and 'alternate_url' in item and 'salary' in item and 'snippet' in item:
                salary = item['salary']
                if salary is None:
                    salary_str = "Зарплата не указана"
                else:
                    salary_str = ""
                    if salary.get('from') is not None:
                        salary_str += str(salary['from'])
                    if salary.get('to') is not None:
                        salary_str += "-" + str(salary['to'])  
                    if salary['currency']:
                        salary_str += " " + salary['currency']

                
                vacancies.append(
                    Vacancy(
                        title=item['name'],
                        url=item['alternate_url'],
                        salary=salary_str,
                        description=item['snippet'].get('requirement') if item['snippet'].get('requirement') else "Описание не указано",
                    )   

                )
        return vacancies
    
    def validate_salary(self, salary: str) -> str:
        """
        Проверяет указана ли зарплата.

        Args:
            salary (str): Зарплата.

        Returns:
            str: Зарплата или "Зарплата не указана", если зарплата не указана.
        """
        if salary == '':
            return "Зарплата не указана"
        return salary
    
class VacancyDataSaver(Vacancy, DataSaver):
    """
    Класс для реализации DataSaver в Vacancy
    """
    def add_vacancy(self, vacancy):
        pass
    
    def get_vacancies(self, criteria: dict):
        pass
    
    def delete_vacancy(self, vacancy):
        pass

    


class APIService(ABC):
    """
    Абстрактный класс для работы с API сервиса с вакансиями.
    """

    @abstractmethod
    def get_vacancies(self, query: str):
        pass


class HeadHunterAPI(APIService):
    """
    Класс для работы с API hh.ru.
    """

    def __init__(self, base_url: str = "https://api.hh.ru/"):
        self.base_url = base_url

    def get_vacancies(self, query: str) -> list:
        """
        Получает вакансии с hh.ru по поисковому запросу.

        Args:
            query (str): Поисковый запрос.

        Returns:
            list: Список словарей с данными о вакансиях.
        """
        url = f"{self.base_url}vacancies"
        params = {"text": query, "per_page": 100}
        headers = {
            "User-Agent": "VacancySearchApp/1.0 (max.makarov@yandex.ru)"
        }
        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()  # Вызывает исключение, если статус ответа не 200
            data = response.json()

            # Проверяем наличие ключа 'items' в ответе
            if "items" not in data:
                print("Ошибка: Ключ 'items' не найден в ответе API.")
                return []
            return data['items']
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except requests.exceptions.ConnectionError as conn_err:
            print(f"Connection error occurred: {conn_err}")
        except requests.exceptions.Timeout as timeout_err:
            print(f"Timeout error occurred: {timeout_err}")
        except Exception as err:
            print(f"An error occurred: {err}")
        return []



class MockedHeadHunterAPI(APIService):

    """
    Класс для мокирования API hh.ru.
    """
    def get_vacancies(self, query: str):
        """
        Мокированный метод для получения вакансий с hh.ru.


        Args:
            query (str): Поисковый запрос.

        Returns:
            list: Список словарей с данными о вакансиях.
        """
        mocked_data = [
            {"name": "Python Developer", "alternate_url": "https://hh.ru/vacancy/1", "salary": {"from": 100000, "to": 150000, "currency": "руб."}, "snippet": {"requirement": "Требования: опыт работы от 3 лет..."}},
            {"name": "Java Developer", "alternate_url": "https://hh.ru/vacancy/2", "salary": {"from": 120000, "to": 180000, "currency": "руб."}, "snippet": {"requirement": "Требования: опыт работы от 2 лет..."}},
            {"name": "C++ Developer", "alternate_url": "https://hh.ru/vacancy/3", "salary": {"from": 110000, "to": 160000, "currency": "руб."}, "snippet": {"requirement": "Требования: опыт работы от 5 лет..."}},
            {"name": "Python Junior Developer", "alternate_url": "https://hh.ru/vacancy/4", "salary": {"from": 50000, "to": 80000, "currency": "руб."}, "snippet": {"requirement": "Требования: опыт работы от 1 года..."}},
        ]
        return mocked_data



class JSONSaver(DataSaver):
    """
    Класс для сохранения информации о вакансиях в JSON-файл.
    """

    def __init__(self, filename: str = "data/vacancies.json"):
        self.filename = filename  
        self.data = self.load_data()

    def load_data(self):
        """
        Загружает данные из JSON-файла.
        
        Returns:
            list: Список словарей с данными о вакансиях.
        """

        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def save_data(self):
        """
        Сохраняет данные в JSON-файл.

        """
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump(self.data, file, ensure_ascii=False, indent=4)

    def add_vacancy(self, vacancy: Vacancy):
        """Добавляет вакансию в JSON-файл.

        Args:
            vacancy (Vacancy): Вакансия для добавления.
        """

        # Проверка наличия вакансии с таким же ID
        for item in self.data:
            if item['id'] == vacancy.id:
                print("Вакансия с таким ID уже существует.")
                return

        vacancy_data = {
            "id": vacancy.id,  # Включаем ID в данные
            "title": vacancy.title,
            "url": vacancy.url,
            "salary": vacancy.salary,
            "description": vacancy.description,
        }
        self.data.append(vacancy_data)

        self.save_data()

    def get_vacancies(self, criteria: dict) -> list:
        """
        Получает вакансии из JSON-файла по указанным критериям.

        Args:
            criteria (dict): Критерии поиска.

        Returns:
            list: Список вакансий, удовлетворяющих критериям.
        """
        filtered_vacancies = []
        for vacancy_data in self.data:
            match = True
            for key, value in criteria.items():
                if vacancy_data.get(key) != value:
                    match = False
                    break
            if match:
                filtered_vacancies.append(vacancy_data)

        return filtered_vacancies
    def get_vacancy_by_id(self, vacancy_id: str):
        """
        Получает вакансию по её идентификатору.

        Args:
            vacancy_id (str): Идентификатор вакансии.

        Returns:
            dict: Данные вакансии, если найдена, иначе None.
        """
        for vacancy_data in self.data:
            if vacancy_data['id'] == vacancy_id:
                return vacancy_data
        return None

    def delete_vacancy(self, vacancy: Vacancy):
        """
        Удаляет информацию о вакансии по идентификатору.
        """
        vacancy_data = {
            "title": vacancy.title,
            "url": vacancy.url,
            "salary": vacancy.salary,
            "description": vacancy.description,
        } 

        if vacancy_data in self.data:
            self.data.remove(vacancy_data)
            self.save_data()
    
    def __len__(self):
        """
        Возвращает количество вакансий в файле.    
        Returns:
            int: Количество вакансий.
        """
        return len(self.data)


def filter_vacancies(vacancies: List["Vacancy"], filter_words: List[str]) -> List["Vacancy"]:



    """
    Фильтрует вакансии по ключевым словам в описании.

    Args:
        vacancies (list): Список вакансий.
        filter_words (list): Список ключевых слов.

    Returns:
        list: Отфильтрованный список вакансий.
    """
    filtered_vacancies = []
    for vacancy in vacancies:

        if any(word.lower() in vacancy.description.lower() for word in filter_words):
            filtered_vacancies.append(vacancy)
    return filtered_vacancies


def sort_vacancies(vacancies: List["Vacancy"]) -> List["Vacancy"]:
    """    
    Сортирует вакансии по зарплате в порядке убывания.

    Args:
        vacancies (list): Список вакансий.

    Returns:
        list: Отсортированный список вакансий.
    """
    return sorted(vacancies, reverse=True)


def get_top_vacancies(vacancies: List["Vacancy"], top_n: int) -> List["Vacancy"]:
    """
    Возвращает топ N вакансий.

    Args:
        vacancies (list): Список вакансий.
        top_n (int): Количество вакансий для вывода в топ.

    Returns:

        list: Список топ N вакансий.
    """
    return vacancies[:top_n]


def get_vacancies_by_salary(vacancies: List["Vacancy"], salary_range: str) -> List["Vacancy"]:
    """    
    Возвращает вакансии по диапазону зарплат.

    Args:
        vacancies (list): Список вакансий.
        salary_range (str): Диапазон зарплат.

    Returns:
        list: Список вакансий, удовлетворяющих диапазону зарплат.
    """
    ranged_vacancies = []
    if "-" not in salary_range:
        return ranged_vacancies
    
    min_salary, max_salary = map(int, salary_range.split("-"))


    for vacancy in vacancies:
        salary_value = vacancy.get_salary_value(vacancy.salary)
        if min_salary <= salary_value <= max_salary:
            ranged_vacancies.append(vacancy)
    return ranged_vacancies

def print_vacancies(vacancies: List["Vacancy"]):
    """
    Выводит информацию о вакансиях в консоль.

    Args:
        vacancies (list): Список вакансий.
    """
    if not vacancies:

        print("Нет вакансий, удовлетворяющих запросу.")
        return

    for vacancy in vacancies:
        print(f"Название: {vacancy.title}")
        print(f"Ссылка: {vacancy.url}")
        print(f"Зарплата: {vacancy.salary}")
        print(f"Описание: {vacancy.description}")
        print("-" * 20)

    
def user_interaction():
    """
    Функция для взаимодействия с пользователем.
    """
    hh_api = HeadHunterAPI()
    json_saver = JSONSaver()
    while True:
        print("Выберите действие:")
        print("1 - Поиск вакансий")
        print("2 - Фильтрация вакансий")
        print("3 - Вывод топ вакансий")
        print("4 - Поиск вакансий по зарплате")
        print("5 - Вывод вакансий")
        print("6 - Выход")

        choice = input("Введите номер действия: ")

        if choice == '1':
            search_query = input("Введите поисковый запрос: ")
            hh_vacancies = hh_api.get_vacancies(search_query)
            vacancies_list = Vacancy.cast_to_object_list(hh_vacancies)

            for vacancy in vacancies_list[:20]:
                json_saver.add_vacancy(vacancy)
            print(f'Всего вакансий загружено: {len(json_saver)}')
            print("Загруженные вакансии:")
            for vacancy in vacancies_list[:20]:
                print(f"  {vacancy.title}")
        elif choice == '2':
            filter_words = input("Введите ключевые слова для фильтрации вакансий (через пробел): ").split()
            vacancies_list = [
                Vacancy(**data) for data in json_saver.get_vacancies({})
            ]
            filtered_vacancies = filter_vacancies(vacancies_list, filter_words)
            print_vacancies(filtered_vacancies)
            print(f"Всего найдено вакансий: {len(filtered_vacancies)}")


        elif choice == '3':
            try:
                top_n = int(input("Введите количество вакансий для вывода в топ N: "))
            except ValueError:
                print("Некорректный ввод. Пожалуйста, введите целое число.")
                continue

            vacancies_list = [
                Vacancy(**data) for data in json_saver.get_vacancies({})
            ]

            sorted_vacancies = sort_vacancies(vacancies_list)
            top_vacancies = get_top_vacancies(sorted_vacancies, top_n)
            print_vacancies(top_vacancies)
            print(f"Всего найдено вакансий: {len(top_vacancies)}")

        elif choice == '4':
            salary_range = input("Введите диапазон зарплат (Пример: 100000-150000): ")
            vacancies_list = [
                Vacancy(**data) for data in json_saver.get_vacancies({})
            ]
            ranged_vacancies = get_vacancies_by_salary(vacancies_list, salary_range)
            print_vacancies(ranged_vacancies)
            print(f"Всего найдено вакансий: {len(ranged_vacancies)}")

        elif choice == '5':
            vacancies_list = [
                Vacancy(**data) for data in json_saver.get_vacancies({})
            ]

            print_vacancies(vacancies_list)

        elif choice == '6':
            print(f'Всего вакансий в хранилище: {len(json_saver)}')
            break
        else:
            print("Некорректный выбор. Пожалуйста, выберите действие из списка.")
            
    
    



