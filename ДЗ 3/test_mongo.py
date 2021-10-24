from pprint import pprint
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError as dke

client = MongoClient('127.0.0.1', 27017)
db = client['works']
works = db.works  

def db_add_one_document(doc, collection):
    
    try:
        collection.insert_one(doc)
        print(f'{doc["_id"]} - Document successfuly added')
    except dke:
        print(f'{doc["_id"]} - Document already exist')

def db_full_clear(collection):
    collection.delete_many({})

doc1 = {   "_id": 8676316815313513,
                        "author": "Peter2",
                        "age": 38,
                        "text": "is cool! Wildberry",
                        "tags": ['cool', 'hot2', 'ice'],
                        "date": '14.06.1983'}

# db_add_one_dcument(doc1, works)
db_full_clear(works)

# persons.insert_many([{"author": "John",
#                "age" : 29,
#                "text": "Too bad! Strawberry",
#                "tags": 'ice',
#                "date": '04.08.1971'},
#                     { "_id": 123,
#                         "author": "Anna",
#                "age" : 36,
#                "title": "Hot Cool!!!",
#                "text": "easy too!",
#                "date": '26.01.1995'},
#                    {"author": "Jane",
#                "age" : 43,
#                "title": "Nice book",
#                "text": "Pretty text not long",
#                "date": '08.08.1975',
#                "tags":['fantastic', 'criminal']}
#       ])


# result = works_list.find({})
# pprint(list(result))

# for doc in persons.find({}):
#     pprint(doc)

# persons.count_documents({})
# result = persons.find({})
# for doc in persons.find({'author': 'Peter2', 'age': 43}):
#     pprint(doc)


# for doc in persons.find({'author': 'Peter2'}, {'age': True, 'author': True, '_id': False}):
#     pprint(doc)

# for doc in persons.find({'$or': [{'author': 'Peter2'},
#                                  {'age': 43}
#                                  ]
#                          }
#                         ):

# persons.create_index('author', unique=True, auto_increment=True)    # Псевдокод. подробнее в докмуентации

# for doc in persons.find({'age': {'$gt': 40}}):
#     pprint(doc)

# new_data = {
#     "author": "Andrey",
#                "age" : 28,
#                "text": "is hot!",
#                "date": '11.09.1991'}
#
# persons.update_one({'author': 'Peter2'}, {'$set': new_data})
#
# persons.replace_one({'author': 'Andrey'}, new_data)

# persons.delete_one({'author': 'Petya'})
# persons = db.works

# persons.delete_many({})


# for doc in persons.find({}):
#     pprint(doc)