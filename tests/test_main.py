import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))



import pytest
from unittest.mock import Mock, patch, MagicMock, ANY
from src.abstract_api import APIInteraction
from src.file_interaction import JSONSaver
from src.api_interaction import HeadHunterAPI
from src.vacancy_interaction import Vacancy, get_top_vacancies, sort_vacancies, filter_vacancies, get_vacancies_by_salary
from main import _get_vacancies, _save_data, _get_user_parameters, _process_vacancies, user_interaction


MOCK_RESPONSE = [
    {"name": "Vacancy 1", "alternate_url": "url1", "salary": {"from": 100}, "snippet": {"requirement": "req1"}},
    {"name": "Vacancy 2", "alternate_url": "url2", "salary": {"from": 200}, "snippet": {"requirement": "req2"}},
]


def mock_hh_api():
    mock_api = Mock(spec=HeadHunterAPI)

    mock_api.get_vacancies.return_value = MOCK_RESPONSE

    return mock_api


def mock_json_saver():
    mock_saver = Mock(spec=JSONSaver)
    mock_saver.read_from_file.return_value = []


@patch("src.api_interaction.HeadHunterAPI.get_vacancies")
def test_get_vacancies(mock_get_vacancies):
    mock_get_vacancies.return_value = MOCK_RESPONSE
    vacancies = _get_vacancies(HeadHunterAPI(), "test")
    assert len(vacancies) == 2
    assert isinstance(vacancies[0], Vacancy)
    mock_get_vacancies.assert_called_once_with("test")



@patch("tests.test_main.mock_json_saver")
def test_save_data(mock_json_saver):
    vacancies = [
        Vacancy("Vacancy 1", "url1", 100, "req1"),
        Vacancy("Vacancy 2", "url2", 200, "req2"),
    ]
    _save_data(mock_json_saver, vacancies)
    mock_json_saver.write_to_file.assert_called_once()



@patch("builtins.input", side_effect=["3", "filter1 filter2", "100-200"])
def test_get_user_parameters(mock_input):
    parameters = _get_user_parameters()
    assert parameters["top_n"] == 3
    assert parameters["filter_words"] == ["filter1", "filter2"]
    assert parameters["salary_range"] == "100-200"



def test_process_vacancies():
    vacancies = [
        Vacancy("Vacancy 1 filter1", "url1", 150, "req1"),
        Vacancy("Vacancy 2", "url2", 250, "req2"),
        Vacancy("Vacancy 3 filter2", "url3", 100, "req3"),
        Vacancy("Vacancy 4 filter1", "url4", 200, "req4"),
    ]
    parameters = {"top_n": 2, "filter_words": ["filter1"], "salary_range": "100-200"}
    processed_vacancies = _process_vacancies(vacancies, parameters)
    assert len(processed_vacancies) == 2
    assert processed_vacancies[0].title == "Vacancy 1 filter1"
    assert processed_vacancies[1].title == "Vacancy 4 filter1"

    

@patch("main.print_vacancies")
@patch("builtins.input", side_effect=["test", "3", "filter1 filter2", "100-200"])
@patch("tests.test_main.mock_hh_api")
@patch("tests.test_main.mock_json_saver")
def test_user_interaction(mock_json_saver, mock_hh_api, mock_input, mock_print_vacancies):
    with patch("main._get_vacancies", return_value=[Vacancy("Vacancy 1", "url1", 100, "req1")]):
        user_interaction()
    mock_print_vacancies.assert_called_once()
