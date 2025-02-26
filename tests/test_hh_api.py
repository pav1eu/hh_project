from unittest.mock import Mock, patch

import pytest

from src.hh_api import HeadHunterApi


@pytest.fixture
def head_hunter_example():
    """Фикстура для создания экземпляра HeadHunterApi с конфигурацией из примера."""
    return HeadHunterApi("https://api.hh.ru/vacancies")


@pytest.fixture
def mock_hh_api():
    """Фикстура для создания мок-объекта HeadHunterApi с моковым API."""
    return HeadHunterApi("https://api.hh.ru/vacancies")


@pytest.fixture
def hh_platform():
    """Фикстура для создания экземпляра HeadHunterApi."""
    return HeadHunterApi("https://api.hh.ru/vacancies")


@pytest.fixture
def mock_get():
    """Фикстура для создания мока запроса GET."""
    return Mock()


def test_hh_api_init(head_hunter_example):
    assert head_hunter_example.url == "https://api.hh.ru/vacancies"


def test_connect_success(mock_hh_api):
    """Тест на успешное подключение к API."""
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200

        assert mock_hh_api.get_api() is True


def test_get_vacancies_success(mock_hh_api):
    """Тест на успешное получение вакансий."""
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "items": [{"id": 1, "name": "Developer"}]
        }

        vacancies = mock_hh_api.get_vacancies("developer")
        assert len(vacancies) == 1
        assert vacancies[0]["name"] == "Developer"


@patch("requests.get")
def test_get_vacancies_failure(mock_get, hh_platform):
    """Тестирование метода get_vacancies класса HeadHunterApi при неудачном запросе."""
    mock_response = Mock()
    mock_response.status_code = 404
    mock_response.json.return_value = {"items": []}
    mock_get.return_value = mock_response

    vacancies = hh_platform.get_vacancies("Python")

    assert vacancies == []
    mock_get.assert_called_once_with(
        hh_platform.url, params={"text": "Python", "per_page": 10}
    )
