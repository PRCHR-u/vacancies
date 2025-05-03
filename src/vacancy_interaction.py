class Vacancy:
    __slots__ = ['title', 'url', 'salary', 'requirements']
    def __init__(self, title, url, salary, requirements):
        self.title = self.validate_string(title, "Title")
        self.url = self._validate_string(url, "URL")
        if salary != "N/A":
            try:
                self.salary = int(salary)
            except ValueError:
                raise ValueError("Salary must be an integer or 'N/A'.")
        else:
            self.salary = salary
        self.requirements = requirements
    
    def validate_string(self, value, field_name):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field_name} must be a non-empty string.")
        return value
        
    def __le__(self, other):
        if not isinstance(other, Vacancy):
            raise TypeError("Can only compare Vacancy objects.")
        
        if self.salary == "N/A":
            return True
        if other.salary == "N/A":
            return False
        return int(self.salary) <= int(other.salary)

    def __lt__(self, other):
        if not isinstance(other, Vacancy):
            raise TypeError("Can only compare Vacancy objects.")
        
        if self.salary == "N/A":
            return True
        if other.salary == "N/A":
            return False
        return int(self.salary) < int(other.salary)

    def __gt__(self, other):
        if not isinstance(other, Vacancy):
            raise TypeError("Can only compare Vacancy objects.")
        if self.salary == "N/A":
            return False
        if other.salary == "N/A":
            return True
        return int(self.salary) > int(other.salary)
    
    def __eq__(self, other):
        if not isinstance(other, Vacancy):
            raise TypeError("Can only compare Vacancy objects.")
        return self.salary == other.salary
    
    def _validate_string(self, value, field_name):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field_name} must be a non-empty string.")
        return value
    

    @staticmethod
    def cast_to_object_list(vacancies_json):
        vacancies_list = []
        for item in vacancies_json:
            vacancy = Vacancy(
                title=item.get("name", "N/A"),
                url=item.get("alternate_url", "N/A"),
                salary=item.get("salary", {}).get("from", "N/A"),
                requirements=item.get("snippet", {}).get("requirement", "N/A"),
            )
            vacancies_list.append(vacancy)
        return vacancies_list


def filter_vacancies(vacancies, filter_words):
    filtered_vacancies = []
    for vacancy in vacancies:
        if any(word.lower() in vacancy.title.lower() for word in filter_words):
            filtered_vacancies.append(vacancy)
    return filtered_vacancies


def get_vacancies_by_salary(vacancies, salary_range):
    ranged_vacancies = []
    try:
        salary_from, salary_to = map(int, salary_range.split('-'))
        for vacancy in vacancies:
            if vacancy.salary != "N/A" and salary_from <= int(vacancy.salary) <= salary_to:
                ranged_vacancies.append(vacancy)
    except ValueError:
        print("Invalid salary range format.")
    return ranged_vacancies


def sort_vacancies(vacancies):
    return sorted(vacancies, key=lambda x: x.salary if x.salary != "N/A" else 0, reverse=True)


def get_top_vacancies(vacancies, top_n):
    return vacancies[:top_n]


def print_vacancies(vacancies):
    for vacancy in vacancies:
        print(f"Title: {vacancy.title}")
        print(f"URL: {vacancy.url}")
        print(f"Salary: {vacancy.salary}")
        print(f"Requirements: {vacancy.requirements}")
        print("-" * 20)