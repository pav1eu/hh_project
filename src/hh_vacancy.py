class Vacancy:
    __slots__ = ["name", "description", "salary_from", "salary_to", "url"]
    """
    Класс для представления вакансии.
    Содержит информацию о вакансии, такую как название,
    зарплата, описание и т.д.
    """

    def __init__(self, name, url, description=None, salary_from=None, salary_to=None):
        self.name = name
        self.description = description or "Описание не указано"
        self.salary_from = salary_from if salary_from is not None else 0
        self.salary_to = salary_to if salary_to is not None else 0
        self.url = url

        self._validate()

    def _validate(self):
        if not self.name or not self.url:
            raise ValueError("Эти аттрибуты обязательны")
        if self.salary_from < 0 or self.salary_to < 0:
            raise ValueError("Зарплата должна быть положительной")
        if self.salary_from > self.salary_to > 1:
            raise ValueError("Минимальная зарплата должна быть больше максимальной")
        if self.salary_from == 0:
            self.salary_from = 'Обговаривается на собеседовании'
        if self.salary_to == 0:
            self.salary_to = 'Обговаривается на собеседовании'

    def __str__(self):
        return f"Вакансия: {self.name},\nОписание: {self.description},\nЗарплата: {self.salary_from} - {self.salary_to},\nURL: {self.url}"

    def __lt__(self, other):
        return (self.salary_from + self.salary_to) // 2 < (
                other.salary_from + other.salary_to
        ) // 2

    def __gt__(self, other):
        return (self.salary_from + self.salary_to) // 2 > (
                other.salary_from + other.salary_to
        ) // 2

    @staticmethod
    def from_platform(platform_data):
        """Метод для формирования списка вакансий из данных платформы"""
        vacancies = []
        for job_data in platform_data:
            name = job_data.get("name", "Название не указано")
            url = job_data.get(
                "apply_alternate_url", ""
            )

            salary_from = (
                job_data.get("salary", {}).get("from", 0)
                if job_data.get("salary")
                else 0
            )

            salary_to = (
                job_data.get("salary", {}).get("to", 0) if job_data.get("salary") else 0
            )

            department = job_data.get("department")
            description = (
                department.get("name", "Описание не указано")
                if department
                else "Описание не указано"
            )

            vacancy = Vacancy(
                name=name,
                url=url,
                salary_from=salary_from,
                salary_to=salary_to,
                description=description,
            )
            vacancies.append(vacancy)
        return vacancies

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "salary_from": self.salary_from,
            "salary_to": self.salary_to,
            "url": self.url,
        }
