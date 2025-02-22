import pytest

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
def vacancy_without_name():
    """Фикстура для создания вакансии без названия."""
    return {
        "name": "",
        "url": "https://hh.ru/applicant/vacancy_response?vacancyId=117286365",
        "salary_from": 100000,
        "salary_to": 120000,
        "description": "Разработка и поддержка, back end части веб-приложений.",
    }


@pytest.fixture
def vacancy_without_url():
    """Фикстура для создания вакансии без url."""
    return {
        "name": "",
        "url": "",
        "salary_from": 100000,
        "salary_to": 120000,
        "description": "Разработка и поддержка, back end части веб-приложений.",
    }


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


@pytest.fixture
def vacancy_with_salary_to_less_salary_from():
    return {
        "name": "Python_developer",
        "url": "https://hh.ru/applicant/vacancy_response?vacancyId=117286365",
        "salary_from": 120000,
        "salary_to": 110000,
        "description": "Разработка и поддержка, back end части веб-приложений.",
    }


# Тестирование создания объекта Vacancy
def test_vacancy_init(vacancy_python_developer):
    """Тест инициализации экземпляра объекта Vacancy"""
    assert vacancy_python_developer.name == "Python_developer"
    assert (
            vacancy_python_developer.url
            == "https://hh.ru/applicant/vacancy_response?vacancyId=117286365"
    )
    assert vacancy_python_developer.salary_from == 100000
    assert vacancy_python_developer.salary_to == 120000
    assert (
            vacancy_python_developer.description
            == "Разработка и поддержка, back end части веб-приложений."
    )


def test_create_vacancy_without_name(vacancy_without_name):
    """Тест на создание вакансии с отсутствием названия."""
    with pytest.raises(ValueError, match="Эти аттрибуты обязательны"):
        Vacancy(**vacancy_without_name)


def test_create_vacancy_without_url(vacancy_without_url):
    """Тест на создание вакансии с отсутствием url."""
    with pytest.raises(ValueError, match="Эти аттрибуты обязательны"):
        Vacancy(**vacancy_without_url)


def test_create_vacancy_negative_salary(vacancy_with_negative_salary):
    """Тест на создание вакансии с отрицательной зарплатой."""
    with pytest.raises(ValueError, match="Зарплата должна быть положительной"):
        Vacancy(**vacancy_with_negative_salary)


def test_create_vacancy_where_salary_to_more_salary_from(
        vacancy_with_salary_to_less_salary_from,
):
    """Тест на создание вакансии с зарплатой от больше чем зарплата до."""
    with pytest.raises(
            ValueError, match="Минимальная зарплата должна быть больше максимальной"
    ):
        Vacancy(**vacancy_with_salary_to_less_salary_from)


def test_str_method(vacancy_python_developer):
    """Тест на метод __str__."""

    assert (
            str(vacancy_python_developer)
            == "Вакансия: Python_developer,\nОписание: Разработка и поддержка, back end части веб-приложений.,"
               "\nЗарплата: 100000 - 120000,\nURL: https://hh.ru/applicant/vacancy_response?vacancyId=117286365"
    )


def test_vacancy_comparison_lt(vacancy_python_developer, vacancy_system_administrator):
    """Тест на сравнение вакансий по средней зарплате (меньше)."""

    assert vacancy_python_developer > vacancy_system_administrator


def test_vacancy_comparison_gt(vacancy_system_administrator, vacancy_python_developer):
    """Тест на сравнение вакансий по средней зарплате (больше)."""

    assert vacancy_system_administrator < vacancy_python_developer


# Тестирование метода __lt__ (меньше)
def test_vacancy_comparison_lt_again(vacancy_python_developer, vacancy_system_administrator):
    """Тест оператора < (__lt__) для сравнения вакансий по средней зарплате."""
    assert vacancy_system_administrator < vacancy_python_developer
    assert not vacancy_python_developer < vacancy_system_administrator


# Тестирование метода validate (с отрицательной зарплатой)
def test_validate_invalid_salary():
    """Тестирование валидации зарплаты в классе Vacancy."""
    with pytest.raises(ValueError, match="Зарплата должна быть положительной"):
        vacancy = Vacancy(
            name="Программист Python", url="https://example.com", salary_from=-100000
        )
