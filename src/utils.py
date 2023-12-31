import requests
import psycopg2


def get_employers_data(emp_ids: list) -> list:
    """ Принимает id компаний
     Возвращает информацию о работодателях """

    employer_list = []
    employer_data = []

    for id in emp_ids:
        url = f"https://api.hh.ru/employers/{id}"
        response = requests.get(url).json()
        employer_data.append(response)

    for item in employer_data:
        emp = {'employer_id': item['id'],
               'employer_name': item['name'],
               'url': item['alternate_url'],
               'vacancies': item['open_vacancies']
               }
        employer_list.append(emp)
    return employer_list


def get_salary(salary: dict) -> list:
    """ Преобразует параметр salary в нужный формат """

    new_salary = [0, 0, None]
    if salary and salary['from']:
        new_salary[0] = salary['from']
        new_salary[2] = salary['currency']
    if salary and salary['to']:
        new_salary[0] = salary['to']
    return new_salary


def get_vacancies_data(emp_ids: list) -> list:
    """ Принимает id компаний
        Возвращает информацию о вакансиях """

    vacancy_data = []
    vacancy_list = []

    url = "https://api.hh.ru/vacancies/"
    for i in range(20):
        params = {
            'page': i,
            'per_page': 100,
            'employer_id': emp_ids,
            'currency': 'RUR',
            'only_with_salary': True
        }
        response = requests.get(url, params=params).json()['items']
        vacancy_data.append(response)

    for item in vacancy_data:
        for vacancy in item:
            salary_from, salary_to, currency = get_salary(vacancy['salary'])
            vac = {'vacancy_id': vacancy['id'],
                   'vacancy_name': vacancy['name'],
                   'employer_id': vacancy['employer']['id'],
                   'employer_name': vacancy['employer']['name'],
                   'salary_from': salary_from,
                   'salary_to': salary_to,
                   'currency': currency,
                   'url': vacancy['alternate_url']
                   }
            vacancy_list.append(vac)
    return vacancy_list


def save_data_to_employers(employer_list: list, params: dict) -> None:
    """ Сохранение данных в таблицу employers """

    conn = psycopg2.connect(database='hh_info', **params)

    with conn.cursor() as cur:
        for employer in employer_list:
            cur.execute('INSERT INTO employers VALUES (%s, %s, %s, %s)', (
                employer['employer_id'],
                employer['employer_name'],
                employer['url'],
                employer['vacancies']

            ))
    conn.commit()
    conn.close()


def save_data_to_vacancies(vacancy_list: list, params: dict) -> None:
    """ Сохранение данных в таблицу vacancies """
    conn = psycopg2.connect(database='hh_info', **params)

    with conn.cursor() as cur:
        for vacancy in vacancy_list:
            cur.execute('INSERT INTO vacancies VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (
                vacancy['vacancy_id'],
                vacancy['vacancy_name'],
                vacancy['employer_id'],
                vacancy['employer_name'],
                vacancy['salary_from'],
                vacancy['salary_to'],
                vacancy['currency'],
                vacancy['url']

            ))
    conn.commit()
    conn.close()


def get_all_companies(db_manager):
    """ Выводит список всех компаний и количество вакансий у каждой компании """
    employers = db_manager.get_companies_and_vacancies_count()
    for employer in employers:
        print(employer)


def get_all_vacancies(db_manager):
    """ Выводит список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию """

    vacancies = db_manager.get_all_vacancies()
    for vacancy in vacancies:
        print(vacancy)


def get_vacancies_with_higher_salary(db_manager):
    """ Выводит список всех вакансий,
        у которых зарплата выше средней по всем вакансиям """

    vacancies = db_manager.get_vacancies_with_higher_salary()
    for vacancy in vacancies:
        print(vacancy)


def get_vacancies_with_keyword(db_manager):
    """ Получает список всех вакансий,
        в названии которых содержатся переданные в метод слова """
    keyword = input('Введите слово для поискового запроса:\n')
    filtered_vacancies = db_manager.get_vacancies_with_keyword(keyword)
    for vacancy in filtered_vacancies:
        print(vacancy)
