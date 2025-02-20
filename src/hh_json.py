import json
from abc import ABC
from pathlib import Path
from src.hh_vacancy import Vacancy


class VacancyFile(ABC):

    @staticmethod
    def add_vacancies(self, vacancies):
        pass

    @staticmethod
    def get_vacancies(self, criteria):
        pass

    @staticmethod
    def delete_vacancies(self, criteria):
        pass

class JSONVacancy(VacancyFile):
    def __init__(self, file_path="vacancies.json"):
        self.__file_path = Path(file_path)
        if not self.__file_path.exists():
            self._save_data([])

    def _load_data(self):
        try:
            with open(self.__file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                return json.loads(content) if content else []
        except FileNotFoundError:
            return []
        except Exception as e:
            print(f"Ошибка при чтении файла {e}")
            return []

    def _save_data(self, data):
        try:
            with open(self.__file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Ошибка при записи файла {e}")

    def add_vacancies(self, vacancies):
        data = self._load_data()
        result = []
        for vacancy in vacancies:
            vacancy_dict = vacancy.to_dict()
            if vacancy_dict not in data:
                data.append(vacancy_dict)
                result.append(vacancy)
        self._save_data(data)

    def get_vacancies(self, criteria):
        data = self._load_data()
        result = []
        for item in data:
            if all(item.get(key) == value for key, value in criteria.items()):
                result.append(item)
        return result

    def delete_vacancies(self, criteria):
        data = self._load_data()
        data = [item for item in data if not all(item.get(key) == value for key, value in criteria.tem())]
        self._save_data(data)