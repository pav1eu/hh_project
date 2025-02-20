import json

import pytest

from src.hh_json import JSONVacancy
from src.hh_vacancy import Vacancy


@pytest.fixture
def vacancy_python_developer():
    """Фикстура для создания вакансии Python developer."""
    return Vacancy(
        name="Python_developer",
        url="https://hh.ru/applicant/vacancy_response?vacancyId=117286365",
        salary_from=100000,
        salary_to=120000,
        description="Разработка и поддержка, back end части веб-приложений.",
    )


@pytest.fixture
def vacancy_system_administrator():
    return Vacancy(
        name="system_administrator",
        url="https://hh.ru/applicant/vacancy_response?vacancyId=117286366",
        salary_from=99000,
        salary_to=110000,
        description="Администрирование, конфигурация, серверы.",
    )


@pytest.fixture
def temp_json_file():
    """Фикстура для создания временного JSON-файла."""
    return "test_vacancies.json"


@pytest.fixture
def vacancy_with_negative_salary():
    """Фикстура для создания вакансии с отрицательным зарплатным предложением."""
    return {
        "name": "Python_developer",
        "url": "https://hh.ru/applicant/vacancy_response?vacancyId=117286365",
        "salary_from": -100000,
        "salary_to": 120000,
        "description": "Разработка и поддержка, back end части веб-приложений.",
    }


def test_add_vacancies(
        temp_json_file, vacancy_python_developer, vacancy_system_administrator
):
    """Тестирование метода add_vacancies класса JSONVacancy.  Проверяет, что после добавления вакансий в
    JSON-файл, количество записей соответствует добавленным вакансиям и данные корректно сохраняются.
    """
    storage = JSONVacancy(temp_json_file)
    storage.add_vacancies([vacancy_python_developer, vacancy_system_administrator])

    with open(temp_json_file, "r", encoding="utf-8") as file:
        data = json.load(file)

    assert len(data) == 2
    assert data[1]["name"] == vacancy_python_developer.name
    assert data[0]["name"] == vacancy_system_administrator.name


def test_get_vacancies(
        temp_json_file, vacancy_python_developer, vacancy_system_administrator
):
    """Тестирование метода get_vacancies класса JSONVacancy. Проверяет, что метод возвращает корректную вакансию
    по заданным критериям."""
    storage = JSONVacancy(temp_json_file)
    storage.add_vacancies([vacancy_python_developer, vacancy_system_administrator])

    result = storage.get_vacancies({"name": "Python_developer"})
    assert len(result) == 1
    assert result[0]["name"] == "Python_developer"


def test_delete_vacancies(
        temp_json_file, vacancy_python_developer, vacancy_system_administrator
):
    """Тестирование метода delete_vacancies класса JSONVacancy. Проверяет, что после удаления вакансии по
    заданным критериям, в JSON-файле остаётся только одна вакансия, которая не соответствует критериям удаления.
    """
    storage = JSONVacancy(temp_json_file)
    storage.add_vacancies([vacancy_python_developer, vacancy_system_administrator])

    storage.delete_vacancies({"name": "Python_developer"})
    data = storage._load_data()

    assert len(data) == 1
    assert data[0]["name"] == "system_administrator"


def test_add_invalid_vacancy(temp_json_file, vacancy_with_negative_salary):
    """Тестирование валидации при добавлении некорректной вакансии в JSONVacancy. Проверяет, что при попытке
    добавить вакансию с отрицательной зарплатой выбрасывается исключение ValueError."""
    storage = JSONVacancy(temp_json_file)
    with pytest.raises(ValueError):
        storage.add_vacancies([Vacancy(**vacancy_with_negative_salary)])
