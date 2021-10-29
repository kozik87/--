from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError as dke
from pprint import pprint
from lxml import html
import requests

def db_add_one_document(doc, collection):
    try:
        collection.insert_one(doc)
        pprint(doc)
        print('Document successfuly added')
    except dke:
        print('Document already exist')

link_news = 'https://lenta.ru/'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko)'}
response = requests.get(link_news, headers=headers)
if response.ok:
    root = html.fromstring(response.text)
    news_list = root.xpath("//div[@class='b-yellow-box__wrap']//a/@href")
    pprint(news_list)
else:
    print(response.status_code)

news_collection = []

for news_link_detail in news_list:
    news_dict = {}
    full_news_link = link_news + news_link_detail
    is_ext = news_link_detail.split('/')[1]
    if is_ext != 'extlink':
        response = requests.get(full_news_link, headers=headers)
        if response.ok:
            root = html.fromstring(response.text)
            news_date = root.xpath("//div[@class='b-topic__info']/time[@class='g-date']/@datetime")[0]
            news_topic = root.xpath("//h1[@itemprop='headline']/text()")[0].replace(u'\xa0', ' ')
            
            news_dict['news_soucre'] = link_news
            news_dict['news_topic'] = news_topic
            news_dict['news_date'] = news_date
            news_dict['full_news_link'] = full_news_link
            news_collection.append(news_dict)
        else:
            print(response.status_code)

client = MongoClient('127.0.0.1', 27017)
db = client['news']
news_list_collection = db.news

for i in news_collection:
    db_add_one_document(i, news_list_collection)