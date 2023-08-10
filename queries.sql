-- Создание базы данных
CREATE DATABASE hh_info;

-- Создание таблицы работодателей
CREATE TABLE IF NOT EXISTS employers
(
    employer_id int PRIMARY KEY,
    employer_name varchar(50),
    url text,
    vacancies int
);

-- Создание таблицы вакансий
CREATE TABLE IF NOT EXISTS vacancies
(
    vacancy_id int PRIMARY KEY,
    vacancy_name varchar(100),
    employer_id int REFERENCES employers(employer_id) ON DELETE CASCADE,
    employer_name varchar(50),
    salary_from int,
    salary_to int,
    currency varchar(10),
    url text
);
