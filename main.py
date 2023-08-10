from src.config import config
from src.database_manager import DBManager
from src.utils import get_all_companies, get_all_vacancies, get_vacancies_with_higher_salary, get_vacancies_with_keyword


def main():

    params = config()
    db_manager = DBManager(params)

    print('Какую информацию необходимо получить от БД?')
    print("""Возможные вариант:
1 - Вывести список всех компаний и количество вакансий у каждой компании
2 - Вывести список всех вакансий с указанием названия компании, названия вакансии, зарплаты и ссылки на вакансию
3 - Вывести среднюю зарплату по всем вакансиям
4 - Вывести список всех вакансий, у которых зарплата выше средней
5 - Вывести список всех вакансий, по ключевому слову\n""")

    user_choice = input('Введите число нужного запроса:\n')
    if user_choice == '1':
        get_all_companies(db_manager)
    elif user_choice == '2':
        get_all_vacancies(db_manager)
    elif user_choice == '3':
        print(f'Средняя зарплата по всем вакансиям: {db_manager.get_avg_salary()} рублей')
    elif user_choice == '4':
        get_vacancies_with_higher_salary(db_manager)
    elif user_choice == '5':
        get_vacancies_with_keyword(db_manager)
    else:
        print('Некоретный ввод')


if __name__ == '__main__':
    main()
