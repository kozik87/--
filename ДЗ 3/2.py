from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError as dke
from pprint import pprint

client = MongoClient('127.0.0.1', 27017)
db = client['works']
works_list = db.works

# salary = int(input('Введите зарплату (больше чем): '))
salary = 450000

for doc in works_list.find(
                                {'$or': 
                                    [ 
                                        {'work_salary.salary_end': {'$gt': salary}},
                                        {'work_salary.salary_start': {'$gt': salary}}

                                    ]
                                }
                            ):
    pprint(doc)

