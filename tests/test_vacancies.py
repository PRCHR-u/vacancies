import pytest
import json
from src.vacancies import (Vacancy, JSONSaver, filter_vacancies,
                           sort_vacancies, get_top_vacancies,
                           get_vacancies_by_salary)

def test_vacancy_init():
    vacancy = Vacancy("Test Title", "http://test.url", "100000-150000 руб.", "Test Description")
    assert vacancy._title == "Test Title"
    assert vacancy._url == "http://test.url"
    assert vacancy._salary == "100000-150000 руб."
    assert vacancy._description == "Test Description"
    assert vacancy._id is not None

def test_vacancy_init_no_salary():
    vacancy = Vacancy("Test Title", "http://test.url", None, "Test Description")
    assert vacancy._salary == "Зарплата не указана"

def test_vacancy_str():
    vacancy = Vacancy("Test Title", "http://test.url", "100000-150000 руб.", "Test Description")
    assert str(vacancy) == "Test Title"

def test_vacancy_lt():
    vacancy1 = Vacancy("Test Title1", "http://test.url", "100000-150000 руб.", "Test Description")
    vacancy2 = Vacancy("Test Title2", "http://test.url", "160000-200000 руб.", "Test Description")
    assert vacancy1 < vacancy2

def test_vacancy_get_salary_value():
    vacancy1 = Vacancy("Test Title1", "http://test1.url", "100000-150000 руб.", "Test Description1")
    assert vacancy1.get_salary_value(vacancy1._salary) == 125000
    vacancy2 = Vacancy("Test Title2", "http://test2.url", "150000 руб.", "Test Description2")
    assert vacancy2.get_salary_value(vacancy2._salary) == 150000
    vacancy3 = Vacancy("Test Title3", "http://test3.url", "Зарплата не указана", "Test Description3")
    assert vacancy3.get_salary_value(vacancy3._salary) == 0
    vacancy4 = Vacancy("Test Title4", "http://test4.url", "qwerty руб.", "Test Description4")
    assert vacancy4.get_salary_value(vacancy4.salary) == 0

def test_vacancy_cast_to_object_list():
    json_data = [
        {"name": "Test1", "alternate_url": "http://test1.url", "salary": {"from": 100000, "to": 150000, "currency": "руб."}, "snippet": {"requirement": "Test1 Description"}},
        {"name": "Test2", "alternate_url": "http://test2.url", "salary": {"from": 160000, "to": 200000, "currency": "руб."}, "snippet": {"requirement": "Test2 Description"}},
        {"name": "Test3", "alternate_url": "http://test3.url", "salary": None, "snippet": {"requirement": "Test3 Description"}},
        {"name": "Test4", "alternate_url": "http://test4.url", "salary": {"from": 100000, "currency": "руб."}, "snippet": {"requirement": "Test4 Description"}},
        {"name": "Test5", "alternate_url": "http://test5.url", "salary": {"to": 100000, "currency": "руб."}, "snippet": {"requirement": "Test5 Description"}},
        {"name": "Test6", "alternate_url": "http://test6.url", "salary": {"currency": "руб."}, "snippet": {"requirement": "Test6 Description"}},
    ]
    vacancies = Vacancy.cast_to_object_list(json_data)
    assert len(vacancies) == 6
    assert vacancies[0]._title == "Test1"
    assert vacancies[1]._salary == "160000-200000 руб."
    assert vacancies[2]._salary == "Зарплата не указана"
    assert vacancies[3]._salary == "100000 руб."
    assert vacancies[4]._salary == "-100000 руб."
    assert vacancies[5]._salary == " руб."

def test_vacancy_validate_salary():
    vacancy1 = Vacancy("Test Title", "http://test1.url", "100000 руб.", "Test Description1")
    assert vacancy1.validate_salary(vacancy1._salary) == "100000 руб."
    vacancy2 = Vacancy("Test Title2", "http://test2.url", "", "Test Description2")
    assert vacancy2.validate_salary(vacancy2._salary) == "Зарплата не указана"



def test_json_saver_add_and_get_vacancy(tmp_path):
    saver = JSONSaver(filename=tmp_path / "test_vacancies.json")
    vacancy = Vacancy("Test Title", "http://test.url", "100000-150000 руб.", "Test Description")
    saver.add_vacancy(vacancy)
    loaded_vacancies = saver.get_vacancies({"title": "Test Title"})
    assert len(loaded_vacancies) == 1
    assert loaded_vacancies[0]["title"] == "Test Title"

def test_json_saver_get_vacancies_by_criteria(tmp_path):
    saver = JSONSaver(filename=tmp_path / "test_vacancies.json")
    vacancy1 = Vacancy("Test Title1", "http://test1.url", "100000-150000 руб.", "Test Description1")
    vacancy2 = Vacancy("Test Title2", "http://test2.url", "160000-200000 руб.", "Test Description2")
    saver.add_vacancy(vacancy1)
    saver.add_vacancy(vacancy2)

    loaded_vacancies = saver.get_vacancies({"title": "Test Title1"})
    assert len(loaded_vacancies) == 1
    assert loaded_vacancies[0]["title"] == "Test Title1"

    loaded_vacancies = saver.get_vacancies({"salary": "160000-200000 руб."})
    assert len(loaded_vacancies) == 1
    assert loaded_vacancies[0]["salary"] == "160000-200000 руб."

    loaded_vacancies = saver.get_vacancies({"title": "Nonexistent"})
    assert len(loaded_vacancies) == 0

def test_json_saver_get_vacancy_by_id(tmp_path):
    saver = JSONSaver(filename=tmp_path / "test_vacancies.json")
    vacancy = Vacancy("Test Title", "http://test.url", "100000-150000 руб.", "Test Description")
    saver.add_vacancy(vacancy)
    loaded_vacancy = saver.get_vacancy_by_id(vacancy.id)
    assert loaded_vacancy["title"] == "Test Title"

def test_json_saver_delete_vacancy(tmp_path):
    saver = JSONSaver(filename=tmp_path / "test_vacancies.json")
    vacancy = Vacancy("Test Title", "http://test.url", "100000-150000 руб.", "Test Description")
    saver.add_vacancy(vacancy)
    saver.delete_vacancy(vacancy)
    assert len(saver) == 0

def test_json_saver_len(tmp_path):
    saver = JSONSaver(filename=tmp_path / "test_vacancies.json")
    vacancy = Vacancy("Test Title", "http://test.url", "100000-150000 руб.", "Test Description")
    saver.add_vacancy(vacancy)
    assert len(saver) == 1

def test_filter_vacancies():
    vacancy1 = Vacancy("Test Title1", "http://test1.url", "100000-150000 руб.", "Test Description1")
    vacancy2 = Vacancy("Test Title2", "http://test2.url", "160000-200000 руб.", "Test Description2")
    vacancy3 = Vacancy("Test Title3", "http://test3.url", "210000-250000 руб.", "Test Description3")
    vacancy4 = Vacancy("Test Title4", "http://test4.url", "210000-250000 руб.", "Test Description3 with key word")
    vacancies = [vacancy1, vacancy2, vacancy3, vacancy4]
    filter_words = ["key"]
    filtered_vacancies = filter_vacancies(vacancies, filter_words)
    assert len(filtered_vacancies) == 1
    assert filtered_vacancies[0].title == "Test Title4"
    
def test_sort_vacancies():
    vacancy1 = Vacancy("Test Title1", "http://test1.url", "100000-150000 руб.", "Test Description1")
    vacancy2 = Vacancy("Test Title2", "http://test2.url", "160000-200000 руб.", "Test Description2")
    vacancy3 = Vacancy("Test Title3", "http://test3.url", "210000-250000 руб.", "Test Description3")
    vacancies = [vacancy1, vacancy2, vacancy3]
    sorted_vacancies = sort_vacancies(vacancies)
    assert sorted_vacancies == [vacancy3, vacancy2, vacancy1]
    
def test_get_top_vacancies():
    vacancy1 = Vacancy("Test Title1", "http://test1.url", "100000-150000 руб.", "Test Description1")
    vacancy2 = Vacancy("Test Title2", "http://test2.url", "160000-200000 руб.", "Test Description2")
    vacancy3 = Vacancy("Test Title3", "http://test3.url", "210000-250000 руб.", "Test Description3")
    vacancies = [vacancy1, vacancy2, vacancy3]
    top_vacancies = get_top_vacancies(vacancies, 2)
    assert top_vacancies == [vacancy1, vacancy2]

def test_get_vacancies_by_salary():
    vacancy1 = Vacancy("Test Title1", "http://test1.url", "100000-150000 руб.", "Test Description1")
    vacancy2 = Vacancy("Test Title2", "http://test2.url", "160000-200000 руб.", "Test Description2")
    vacancy3 = Vacancy("Test Title3", "http://test3.url", "210000-250000 руб.", "Test Description3")
    vacancies = [vacancy1, vacancy2, vacancy3]
    salary_range = "120000-220000"
    ranged_vacancies = get_vacancies_by_salary(vacancies, salary_range)
    assert ranged_vacancies == [vacancy1, vacancy2]