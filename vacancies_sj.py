from dotenv import load_dotenv
import requests
import os
from api_halpers import predict_salary


def get_vacancies_sj_information(secret_key, id_category=48):
    url = 'https://api.superjob.ru/2.0/vacancies/'
    headers = {
        'X-Api-App-Id': secret_key,
    }
    params = {
        'catalogues': id_category,
        'town': 'Москва'
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()['objects']


def predict_rub_salary_sj(vacancy):
    payment_from = vacancy['payment_from']
    payment_to = vacancy['payment_to']
    predicted_salary = predict_salary(payment_from, payment_to)
    return predicted_salary
    

def main():

    load_dotenv()
    super_job_secret_key = os.getenv("SUPER_JOB_SECRET_KEY")
    
    vacancies_sj_information = get_vacancies_sj_information(super_job_secret_key)
    
    for vacancy in vacancies_sj_information:
        salary = predict_rub_salary_sj(vacancy)
        print(f"{vacancy['profession']}, {vacancy['town']['title']}, {salary}")
        
        
if __name__ == '__main__':
    main()