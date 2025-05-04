import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from src.vacancy_interaction import (
    Vacancy,
    filter_vacancies,
    get_vacancies_by_salary,
    sort_vacancies,
    get_top_vacancies,

)


def test_vacancy_initialization():
    vacancy = Vacancy(
        "Test Title", "https://test.com", "1000", "Test Requirements"
    )
    assert vacancy.title == "Test Title"
    assert vacancy.url == "https://test.com"
    assert vacancy.salary == 1000
    assert vacancy.requirements == "Test Requirements"


def test_vacancy_initialization_na_salary():
    vacancy = Vacancy(
        "Test Title", "https://test.com", "N/A", "Test Requirements"
    )
    assert vacancy.salary == "N/A"


def test_vacancy_invalid_title():
    with pytest.raises(ValueError):
        Vacancy("", "https://test.com", "1000", "Test Requirements")


def test_vacancy_invalid_url():
    with pytest.raises(ValueError):
        Vacancy("Test Title", "   ", "1000", "Test Requirements")


def test_vacancy_invalid_salary():
    with pytest.raises(ValueError):
        Vacancy("Test Title", "https://test.com", "abc", "Test Requirements")


def test_vacancy_validate_string():
    vacancy = Vacancy(
        "Test Title", "https://test.com", "1000", "Test Requirements"
    )
    assert vacancy._validate_string("valid", "Field") == "valid"
    with pytest.raises(ValueError):
        vacancy._validate_string("", "Field")

    with pytest.raises(ValueError):
        vacancy._validate_string(123, "Field")

    with pytest.raises(ValueError):
        vacancy._validate_string("   ", "Field")


def test_vacancy_comparison():
    vacancy1 = Vacancy(
        "Test Title1", "https://test1.com", "1000", "Test1"
    )
    vacancy2 = Vacancy(
        "Test Title2", "https://test2.com", "2000", "Test2"
    )
    vacancy3 = Vacancy("Test Title3", "https://test3.com", "1000", "Test3")
    vacancy4 = Vacancy("Test Title4", "https://test4.com", "N/A", "Test4")
    assert vacancy1 < vacancy2
    assert vacancy2 > vacancy1
    assert vacancy1 <= vacancy2
    assert vacancy2 >= vacancy1
    assert vacancy1 == vacancy3
    assert vacancy4 < vacancy2
    assert vacancy2 > vacancy4
    assert vacancy4 <= vacancy1
    assert vacancy1 >= vacancy4
    assert vacancy4 <= vacancy4
    with pytest.raises(TypeError):
        vacancy1 < "abc"


def test_cast_to_object_list():
    data = [
        {
            "name": "Title1",
            "alternate_url": "url1",
            "salary": {"from": "1000"},
            "snippet": {"requirement": "req1"},
        },
        {
            "name": "Title2",
            "alternate_url": "url2",
            "salary": {"from": "2000"},
            "snippet": {"requirement": "req2"},
        },
        {
            "name": "Title3",
            "alternate_url": "url3",
            "salary": {"from": "N/A"},
            "snippet": {"requirement": "req3"},
        },
    ]

    vacancies = Vacancy.cast_to_object_list(data)

    assert len(vacancies) == 3
    assert vacancies[0].title == "Title1"
    assert vacancies[0].url == "url1"
    assert vacancies[0].salary == 1000
    assert vacancies[0].requirements == "req1"
    assert vacancies[2].salary == "N/A"


def test_filter_vacancies():
    vacancies = [
        Vacancy("Python Developer", "url1", "1000", "req1"),
        Vacancy("Java Developer", "url2", "2000", "req2"),
        Vacancy("python Engineer", "url3", "3000", "req3"),
    ]

    filtered = filter_vacancies(vacancies, ["python"])
    assert len(filtered) == 2
    assert filtered[0].title == "Python Developer"

    filtered = filter_vacancies(vacancies, ["engineer"])
    assert len(filtered) == 1
    assert filtered[0].title == "python Engineer"


def test_get_vacancies_by_salary():
    vacancies = [
        Vacancy("Title1", "url1", "1000", "req1"),
        Vacancy("Title2", "url2", "2000", "req2"),
        Vacancy("Title3", "url3", "3000", "req3"),
        Vacancy("Title4", "url4", "N/A", "req4"),
    ]

    ranged = get_vacancies_by_salary(vacancies, "1000-2000")
    assert len(ranged) == 2
    assert ranged[0].title == "Title1"
    assert ranged[1].title == "Title2"

    ranged = get_vacancies_by_salary(vacancies, "3000-4000")
    assert len(ranged) == 1
    assert ranged[0].title == "Title3"
    ranged = get_vacancies_by_salary(vacancies, "abc")
    assert len(ranged) == 0


def test_sort_vacancies():
    vacancies = [
        Vacancy("Title1", "url1", "2000", "req1"),
        Vacancy("Title2", "url2", "1000", "req2"),
        Vacancy("Title3", "url3", "3000", "req3"),
        Vacancy("Title4", "url4", "N/A", "req4"),
    ]
    sorted_vacancies = sort_vacancies(vacancies)
    assert sorted_vacancies[0].title == "Title3"
    assert sorted_vacancies[1].title == "Title1"
    assert sorted_vacancies[2].title == "Title2"
    assert sorted_vacancies[3].title == "Title4"


def test_get_top_vacancies():
    vacancies = [
        Vacancy("Title1", "url1", "1000", "req1"),
        Vacancy("Title2", "url2", "2000", "req2"),
        Vacancy("Title3", "url3", "3000", "req3"),
    ]
    top2 = get_top_vacancies(vacancies, 2)
    assert len(top2) == 2
    assert top2[0].title == "Title1"
    assert top2[1].title == "Title2"

    top5 = get_top_vacancies(vacancies, 5)
    assert len(top5) == 3
