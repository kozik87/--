# Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя, 
# сохранить JSON-вывод в файле *.json.

import requests
# from pprint import pprint

user = 'kozik87'
# my_params = {'user': user}
service = f'https://api.github.com/users/{user}/repos'

response = requests.get(f'{service}') #params=my_params
if response.ok:
    # pprint(response.text)
    j_data = response.json()
    # print(j_data)
    for i in j_data:
        print(i['full_name'])
else:
    print(response.status_code)

