import requests, json
from bs4 import BeautifulSoup as bs
from pprint import pprint
import re

def salary_determine(str):
    if str:
        work_salary_dict = {}
        pattern = re.compile(r'^от (?P<salary_start>([\w\.-]+))\u202f([\w\.-]+) (?P<valute>([\w\.-]+))', re.IGNORECASE)
        if not pattern.match(str):
            pattern = re.compile(r'^до (?P<salary_end>([\w\.-]+))\u202f([\w\.-]+) (?P<valute>([\w\.-]+))', re.IGNORECASE)
            if not pattern.match(str):
                pattern = re.compile(r'(?P<salary_start>([\w\.-]+))\u202f([\w\.-]+) – (?P<salary_end>([\w\.-]+))\u202f([\w\.-]+) (?P<valute>([\w\.-]+))', re.IGNORECASE)
                if not pattern.match(str):
                    return None
        # ([\w\.-]+)@([\w\.-]+)
        return pattern.match(str).groupdict()
    else:
        return None

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko)'}
params = {
            'clusters': True,
            'ored_clusters': True,
            'area': 113, #Россия
            'enable_snippets': True,
            'text': 'Python', #text=%D0%94%D0%B8%D1%80%D0%B5%D0%BA%D1%82%D0%BE%D1%80+%D0%BF%D0%BE+%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%B5+%D1%81+%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D0%BC%D0%B8
            # 'experience': 'between3And6',
            'search_field': 'name',
            'page': 1
}

work_source = 'https://hh.ru'
url = f'{work_source}/search/vacancy'
work_data = []

while True:
    response = requests.get(url, params=params, headers=headers)
    if response.ok and response:

        soup = bs(response.text, 'html.parser')

        for i in ['standard', 'standard_plus', 'premium']:
            if i == 'premium':
                spec_class = 'vacancy-serp-item' + i
            else:
                spec_class = ''
            work_solution_list = soup.find_all('div', attrs={'class': 'vacancy-serp-item', 'data-qa':'vacancy-serp__vacancy vacancy-serp__vacancy_' + i})
            
            for work_solution in work_solution_list:
                current_work_dict = {}
                
                work_solution_object = work_solution.find('a', attrs={'data-qa': "vacancy-serp__vacancy-title", 'target': '_blank'})
                work_solution_title = work_solution_object.text
                work_emploee = work_solution.find('a', attrs={'class': 'bloko-link bloko-link_secondary', 'data-qa': "vacancy-serp__vacancy-employer"}).text
                try:
                    work_salary = work_solution.find('span', attrs={'class': 'bloko-header-section-3 bloko-header-section-3_lite', 'data-qa': "vacancy-serp__vacancy-compensation"}).text
                except:
                    work_salary = None

                work_link = work_solution_object['href']
                
                current_work_dict['work_solution_title']= work_solution_title
                current_work_dict['work_emploee']= work_emploee
                current_work_dict['work_link']= work_link
                current_work_dict['work_salary']= salary_determine(work_salary)
                current_work_dict['work_source']= work_source
                work_data.append(current_work_dict)
        params['page'] += 1
        
    else:
        print(response.status_code)
        break

pprint(work_data)
