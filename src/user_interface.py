from src.hh_api import HeadHunterApi
from src.hh_json import JSONVacancy
from src.hh_vacancy import Vacancy


def user_interaction():
    platform = HeadHunterApi()
    storage = JSONVacancy("C:/Users/alvis/work/tmp/hh_project/data/vacancies.json")
    """
    Класс, реализующий пользовательский интерфейс.
    Предоставляет методы для взаимодействия с пользователем,
    отображения меню и обработки пользовательского ввода.
    """

    if not platform.get_api():
        print("Не удалось подключиться к API hh.ru")
        return

    while True:
        print("\n1. Ввести поисковый запрос")
        print("2. Получить топ N вакансий по зарплате")
        print("3. Найти вакансии по ключевому слову в описании")
        print("4. Выход")

        choice = input("Выберите действие: ")

        if choice == "1":
            query = input("Введите поисковый запрос: ")
            vacancies = platform.get_vacancies(query)
            vacancies_list = Vacancy.from_platform(vacancies)
            storage.add_vacancies(vacancies_list)
            print(f"Добавлено {len(vacancies_list)} вакансий.")

        elif choice == "2":
            n = int(input("Сколько вакансий вывести?: "))
            data = storage._load_data()
            vacancies_list = [
                Vacancy(**vacancy) for vacancy in data
            ]
            sorted_vacancies = sorted(
                vacancies_list,
                key=lambda x: (x.salary_from + x.salary_to) / 2,
                reverse=True,
            )
            for vacancy in sorted_vacancies[:n]:
                print(vacancy.__str__())

        elif choice == "3":
            keyword = input("Введите ключевое слово: ")
            data = storage._load_data()
            filtered = [v for v in data if keyword.lower() in v["description"].lower()]
            for vacancy in filtered:
                print(vacancy)

        elif choice == "4":
            break

        else:
            print("Неверный выбор, попробуйте снова.")
