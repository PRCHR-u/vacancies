from typing import List


class Vacancy:
    """
    Represents a job vacancy with a title, URL, salary, and requirements.

    Attributes:
        title (str): The title of the vacancy.
        url (str): The URL to the vacancy's details.
        salary (int or str): The salary offered for the vacancy,
        or "N/A" if not specified.
        requirements (str): The requirements for the vacancy.
    """
    def __str__(self):
        return (
            f"Vacancy(title='{self.title}', url='{self.url}', "
            f"salary={self.salary}, requirements='{self.requirements}')"
        )

    __slots__ = ["title", "url", "salary", "requirements"]

    def __init__(self, title: str, url: str, salary: str, requirements: str):
        """Initializes a Vacancy object.
        Initializes a Vacancy object.

        Args:
            requirements (str): The requirements for the vacancy.
            salary (str): The salary offered for the vacancy, can be "N/A".

            title (str): The title of the vacancy.
            url (str): The URL to the vacancy's details.
            salary (str): The salary offered for the vacancy, can be "N/A".
            requirements (str): The requirements for the vacancy.

        Raises:
            ValueError: If title is empty,
            URL is empty, or salary is not an integer or "N/A".
        """
        self.title = self._validate_string(title, "Title")
        self.url = self._validate_string(url, "URL")
        if salary != "N/A":
            try:
                self.salary = int(salary)
            except ValueError as error:
                raise ValueError(
                    f"Salary must be an integer or 'N/A'. {error}"
                )
        else:
            self.salary = salary
        self.requirements = requirements

    def _validate_string(self, value: str, field_name: str) -> str:
        """
        Validates if the given value is a non-empty string.

        Args:
            value (str): The string value to validate.
            field_name (str): The name of the field being validated.

        Returns:
            str: The validated string.

        Raises:
            ValueError: If the value is not a string or is an empty string.
        """
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field_name} must be a non-empty string.")
        return value

    def __le__(self, other: "Vacancy") -> bool:
        """
        Checks if this Vacancy's salary is
        less than or equal to another Vacancy's salary.

        Args:
            other (Vacancy): The other Vacancy object to compare with.

        Returns:
            bool: True if this Vacancy's salary is
            less than or equal to the other's, False otherwise.
        Raises:
            TypeError: If the other object is not a Vacancy.
        """
        if not isinstance(other, Vacancy):
            raise TypeError("Can only compare Vacancy objects.")

        if self.salary == "N/A":
            return True
        if other.salary == "N/A":
            return False
        return int(self.salary) <= int(other.salary)

    def __lt__(self, other: "Vacancy") -> bool:
        """
        Checks if this Vacancy's salary is less than another Vacancy's salary.

        Args:
            other (Vacancy): The other Vacancy object to compare with.

        Returns:
            bool: True if this Vacancy's salary
            is less than the other's, False otherwise.
        Raises:
            TypeError: If the other object is not a Vacancy.
        """
        if not isinstance(other, Vacancy):
            raise TypeError("Can only compare Vacancy objects.")

        if self.salary == "N/A":
            return True
        if other.salary == "N/A":
            return False
        return int(self.salary) < int(other.salary)

    def __gt__(self, other: "Vacancy") -> bool:
        """
        Checks if this Vacancy's salary is
        greater than another Vacancy's salary.

        Args:
            other (Vacancy): The other Vacancy object to compare with.

        Returns:
            bool: True if this Vacancy's salary is
            greater than the other's, False otherwise.
        Raises:
            TypeError: If the other object is not a Vacancy.
        """
        if not isinstance(other, Vacancy):
            raise TypeError("Can only compare Vacancy objects.")

        if self.salary == "N/A":
            return False
        if other.salary == "N/A":
            return True
        return int(self.salary) > int(other.salary)

    def __eq__(self, other):
        """
        Checks if this Vacancy's salary is equal to another Vacancy's salary.

        Returns:
            bool: True if this Vacancy's salary is equal to the other's,
            False otherwise.

        Raises:
            TypeError: If the other object is not a Vacancy.
        """
        if not isinstance(other, Vacancy):
            raise TypeError("Can only compare Vacancy objects.")
        return self.salary == other.salary

    @staticmethod
    def cast_to_object_list(vacancies_json: List[dict]) -> List["Vacancy"]:
        """
        Casts a list of dictionaries (JSON data) to a list of Vacancy objects.

        Args:
            vacancies_json (list): A list of dictionaries, where each
            dictionary represents a vacancy.

        Returns:
            list: A list of Vacancy objects created from the input data.
        """
        vacancies_list = []
        for item in vacancies_json:
            vacancy = Vacancy(
                title=item.get("name", "N/A"),
                url=item.get("alternate_url", "N/A"),
                salary=item.get("salary", {}).get("from", "N/A"),

                requirements=item.get("snippet", {}).get("requirement", "N/A")
            )
            vacancies_list.append(vacancy)
        return vacancies_list


def filter_vacancies(
        vacancies: List["Vacancy"], filter_words: list
) -> List["Vacancy"]:
    """
    Filters a list of vacancies by the given filter words.

    Args:
        vacancies (list): A list of Vacancy objects.
        filter_words (list): A list of words to filter the vacancies by.

    Returns:
        list: A filtered list of Vacancy objects.
    """
    filtered_vacancies = []
    for vacancy in vacancies:
        if any(word.lower() in vacancy.title.lower() for word in filter_words):
            filtered_vacancies.append(vacancy)
    return filtered_vacancies


def get_vacancies_by_salary(vacancies: list, salary_range: str) -> list:
    """
    Filters a list of vacancies by the specified salary range.

    Args:
        vacancies: A list of Vacancy objects.
        salary_range: A string representing the salary range in the format
        "min-max".

    Returns:
        list: A filtered list of Vacancy objects within the specified
        salary range.
    """
    ranged_vacancies = []
    try:
        salary_from, salary_to = map(int, salary_range.split("-"))
        for vacancy in vacancies:
            if vacancy.salary != "N/A" and (
                salary_from <= int(vacancy.salary) <= salary_to
            ):
                ranged_vacancies.append(vacancy)
    except ValueError:
        print("Invalid salary range format.")
    return ranged_vacancies


def sort_vacancies(vacancies):
    """
    Sorts a list of vacancies by salary in descending order.
    Args:
        vacancies (list): A list of Vacancy objects.
    Returns: list: A sorted list of Vacancy objects.
    """
    return sorted(
        vacancies,
        key=lambda x: x.salary if x.salary != "N/A" else 0,
        reverse=True,

    )


def get_top_vacancies(vacancies: list, top_n: int) -> list:
    """
    Gets the top N vacancies from a list of vacancies.

    Args:
        vacancies (list): A list of Vacancy objects.
        top_n (int): The number of top vacancies to retrieve.

    Returns:
        list: A list of the top N Vacancy objects.
    """
    return vacancies[:top_n]


def print_vacancies(vacancies):
    """Prints the details of each vacancy in the list."""
    for vacancy in vacancies:
        print(
              f"Title: {vacancy.title}\n"
              f"URL: {vacancy.url}\n"
              f"Salary: {vacancy.salary}\n"
              f"Requirements: {vacancy.requirements}\n"
              f"{'-' * 20}\n"
            )
