from abc import ABC, abstractmethod

import requests


class BaseApi(ABC):
    """Абстрактный класс для получния API запроса"""

    @abstractmethod
    def get_api(self):
        pass

    @abstractmethod
    def get_vacancies(self, query, page=1):
        pass


class HeadHunterApi(BaseApi):
    """Класс получения API запроса и проверка на положительный ответ"""

    def __init__(self, url="https://api.hh.ru/vacancies"):
        self.url = url

    def get_api(self):
        try:
            response = requests.get(self.url)
            if response.status_code == 200:
                return True
        except requests.exceptions.RequestException as e:
            print(f"Ошибка подключения {e}")
            return False

    def get_vacancies(self, query, page=10):
        params = {"text": query, "per_page": page}
        try:
            response = requests.get(self.url, params=params)
            response.raise_for_status()
            return response.json().get("items", [])
        except Exception as e:
            print(f"Неизвестная ошибка {e}")
            return []
