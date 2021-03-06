from datetime import date, timedelta

import requests

from api_halpers import predict_salary, get_table


def predict_rub_salary_hh(vacancy):
    if not vacancy['salary']:
        return
    salary = vacancy['salary']
    if salary['currency'] != 'RUR':
        return
    salary_from = salary['from']
    salary_to = salary['to']
    predicted_salary = predict_salary(salary_from, salary_to)
    return predicted_salary


def get_vacancies_hh(language='Python',
                     page=0, area=1,
                     date_from=30):
    url = 'https://api.hh.ru/vacancies/'
    params = {
            'text': f'Программист {language}',
            'area': area,
            'date_from': date_from,
            'page': page,
        }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def main():
    popular_programming_languages = [
        'Python',
        'Java',
        'Javascript',
        'Go',
        'sdbhjsdg',
        'C',
        'C#',
        'C++',
        'PHP',
        'Ruby',
    ]

    date_from = date.today() - timedelta(days=30)
    popular_languages_statistics = {}

    for language in popular_programming_languages:

        pages_number = 1
        page, total_salary, vacancies_processed = 0, 0, 0

        while page < pages_number:
            vacancies_hh = get_vacancies_hh(language=language,
                                            page=page,
                                            date_from=date_from)
            vacancy_counts = vacancies_hh['found']
            pages_number = vacancies_hh['pages']

            for vacancy in vacancies_hh['items']:
                salary = predict_rub_salary_hh(vacancy)
                if salary:
                    vacancies_processed += 1
                    total_salary += salary
            page += 1

        if vacancies_processed == 0:
            continue

        popular_languages_statistics[language] = {
            'vacancies_found': vacancy_counts,
            'vacancies_processed': vacancies_processed,
            'average_salary': int(total_salary / vacancies_processed),
        }

    table = get_table(popular_languages_statistics, title='HeadHunter Москва')
    print(table)


if __name__ == '__main__':
    main()
