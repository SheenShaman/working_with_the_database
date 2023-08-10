import psycopg2


class DBManager:
    def __init__(self, params):

        self.params = params

    def get_companies_and_vacancies_count(self):
        """ Получает список всех компаний и количество вакансий у каждой компании """

        conn = psycopg2.connect(database='hh_info', **self.params)

        with conn.cursor() as cur:
            cur.execute("""
            SELECT employer_name, vacancies FROM employers
            ORDER BY vacancies DESC    
            """)
            result = cur.fetchall()
        conn.commit()
        conn.close()
        return result

    def get_all_vacancies(self):
        """ Получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию """

        conn = psycopg2.connect(database='hh_info', **self.params)

        with conn.cursor() as cur:
            cur.execute("""
                    SELECT employer_name, vacancy_name, salary_from, salary_to, url 
                    FROM vacancies 
                    ORDER BY employer_name    
                    """)
            result = cur.fetchall()
        conn.commit()
        conn.close()
        return result

    def get_avg_salary(self):
        """ Получает среднюю зарплату по вакансиям """

        conn = psycopg2.connect(database='hh_info', **self.params)

        with conn.cursor() as cur:
            cur.execute("""
                    SELECT AVG((salary_from + salary_to)/2) 
                    FROM vacancies
                    """)
            result = cur.fetchall()
        conn.commit()
        conn.close()
        return result

    def get_vacancies_with_higher_salary(self):
        """ Получает список всех вакансий,
         у которых зарплата выше средней по всем вакансиям """

        conn = psycopg2.connect(database='hh_info', **self.params)

        with conn.cursor() as cur:
            cur.execute(f"""
                    SELECT vacancy_name, (salary_from + salary_to) / 2 AS salary, url
                    FROM vacancies
                    WHERE (salary_from + salary_to) / 2 > {self.get_avg_salary()}
                    ORDER BY salary DESC
                    """)
            result = cur.fetchall()
        conn.commit()
        conn.close()
        return result

    def get_vacancies_with_keyword(self, keyword: str):
        """ Получает список всех вакансий,
        в названии которых содержатся переданные в метод слова """

        conn = psycopg2.connect(database='hh_info', **self.params)

        with conn.cursor() as cur:
            cur.execute(f"""
                    SELECT vacancy_name, url
                    FROM vacancies
                    WHERE vacancy_name LIKE '%{keyword}%'
                    """)
            result = cur.fetchall()
        conn.commit()
        conn.close()
        return result
