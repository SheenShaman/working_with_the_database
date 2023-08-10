from src.config import config
from src.utils import get_employers_data, get_vacancies_data, save_data_to_employers, save_data_to_vacancies


# id компаний
employer_id = ['3529', '1740', '80', '15478', '78638', '39305', '3776', '4219', '4233', '2180']
# Компании по которым будет запрос
# employers = ['Сбер', 'Яндекс', 'Альфа-Банк', 'VK', 'Тинькофф', 'Газпром нефть', 'МТС', 'Tele2', 'X5 Group', 'Ozon']

params = config()
# получение данных компаний
emp = get_employers_data(employer_id)
# получение данных вакансий этих компаний
vac = get_vacancies_data(employer_id)

# сохранение данных компаний
save_data_to_employers(emp, params)
# сохранение данных вакансий этих компаний
save_data_to_vacancies(vac, params)
