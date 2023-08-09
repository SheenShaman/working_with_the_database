import requests


def get_employers_data(emp_ids: list) -> list:
    """ Принимает id компаний
     Возвращает информацию о работодателях """

    employer_list = []
    employer_data = []

    for id in emp_ids:
        url = f"https://api.hh.ru/employers/{id}"
        response = requests.get(url).json()
        # можно добавить исключение (if response.status_code != 200: raise DataError)
        employer_data.append(response)

    for item in employer_data:
        emp = {'employer_id': item['id'],
               'employer_name': item['name'],
               'url': item['alternate_url'],
               'vacancies': item['open_vacancies']
               }
        employer_list.append(emp)
    return employer_list


def get_vacancies_data(emp_ids: list) -> list:

    vacancy_data = []
    url = "https://api.hh.ru/vacancies/"
    for i in range(10):
        params = {
            'page': i,
            'per_page': 100,
            'employer_id': emp_ids,
            'currency': 'RUR',
            'only_with_salary': True
        }
        response = requests.get(url, params=params).json()
        # можно добавить исключение (if response.status_code != 200: raise DataError)
        vacancy_data.append(response)

    vacancies = []
    for vac in data_list:
        salary_from, salary_to, currency = get_salary(vac['salary'])
        vacancy = Vacancy(vac['id'],
                          vac['name'],
                          vac['alternate_url'],
                          salary_from,
                          salary_to,
                          currency,
                          vac['employer']['name'],
                          'HeadHunter')
        vacancies.append(vacancy)
    return vacancies


def get_salary(salary: dict) -> list:
    """ Преобразует параметр salary в нужный формат """

    new_salary = [0, 0, None]
    if salary and salary['from']:
        new_salary[0] = salary['from']
        new_salary[2] = salary['currency']
    if salary and salary['to']:
        new_salary[0] = salary['to']
    return new_salary



# employer = ['Сбер', 'Яндекс', 'Альфа-Банк', 'VK', 'Тинькофф', 'Газпром нефть', 'МТС', 'Tele2', 'X5 Group', 'Ozon']
employer_id = ['3529', '1740', '80', '15478', '78638', '39305', '3776', '4219', '4233', '2180']
emp = get_employers_data(employer_id)
vac = get_vacancies_data(employer_id)
print(vac)

