import json
import time
import requests
import functools
import random
from dataclasses import dataclass, asdict

url = "https://api.hh.ru/vacancies"
max_items_download = 2000
per_page_items = 100
default_wait_time = 0.2
vacancies_file_path = "vacancies.json"
connect_timeout = 3
read_timeout = 5

json_job_title_field = "name"
json_salary_field = "salary"
json_vacancy_url_field = "alternate_url"


class HHApiRequestError(Exception):
    pass

class HHApiNoMoreDataError(Exception):
    pass


@dataclass
class VacancyData:
    salary: str
    job_title: str
    vacancy_url: str



def make_delay(wait_time: float = 1.0):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            time.sleep(wait_time)
            return result
        return wrapper
    return decorator


def make_random_delay(delay_mean: float = 1.0, delay_std: float = 1.0):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            random_delay = max(0, random.gauss(delay_mean, delay_std))
            time.sleep(random_delay)
            return result
        return wrapper
    return decorator


def make_retry(retries: int = 3, delay: float = 1.0):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except HHApiRequestError as e:
                    print(f"Attempt {attempt + 1} failed: {e}")
                    if attempt < retries - 1:
                        time.sleep(delay)
                    else:
                        raise
        return wrapper
    return decorator


@make_retry(retries=3, delay=default_wait_time)
@make_delay(wait_time = default_wait_time)
#@make_random_delay(delay_mean=2, delay_std=1.5)
def fetch_hh_vacancies(url:str, page: int):
    query_params = {
        "text": "fastapi OR django OR flask",
        "page": page,
        "per_page": per_page_items,
    }
    resp = requests.get(
        url,
        params=query_params,
        timeout=(connect_timeout, read_timeout)
    )

    # эмитация сбоя
    #if random.randint(1, 10) > 7:
    #    raise HHApiRequestError("failed to fetch data: SIMULATIVE API FAILURE")


    if resp.status_code != 200:
        print(resp.status_code)
        print("response failed", resp.text)
        raise HHApiRequestError("failed to fetch data")
    result = resp.json()
    return result

def main():
    page_counter: int= 0

    vacancies = []

    try:
        while True:
            if page_counter == max_items_download // per_page_items:
                raise Exception("cant get more tan 2000 items")

            hh_vacancies = fetch_hh_vacancies(url, page_counter)
            if len(hh_vacancies["items"]) <=0:
                raise HHApiNoMoreDataError("no more data found. loaded: ", len(vacancies))
            print(len(hh_vacancies["items"]))

            for vacancy_raw in hh_vacancies["items"]:
                salary = f'{vacancy_raw["salary"]["from"]} {vacancy_raw["salary"]["currency"]}' if vacancy_raw["salary"] is not None else ""
                job_title = vacancy_raw["name"] if vacancy_raw["name"] is not None else "no name"
                vacancy_url = vacancy_raw["alternate_url"] if vacancy_raw["alternate_url"] is not None else "no url"
                vacancy = VacancyData(salary, job_title, vacancy_url)
                vacancies.append(vacancy)

                print(vacancy)


            #vacancies.extend(hh_vacancies["items"])

            page_counter += 1
    except Exception as ex:
        print(ex)

    with open(vacancies_file_path, mode="w") as f:
        f.write(json.dumps(
            [asdict(vacancies) for vacancies in vacancies],
            ensure_ascii=False,
            indent=4)
        )







if __name__ == "__main__":
    main()







