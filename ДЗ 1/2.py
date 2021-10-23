import requests

api_key_ident = ''
folder_id= ''


my_params = {
            'folderId': folder_id,
            "sourceLanguageCode": "ru",
            "targetLanguageCode": "en", 
            "texts": "Привет мир"    
            }            

headers = {
           "Authorization": "Api-Key " + api_key_ident,
           }


service = 'https://translate.api.cloud.yandex.net/translate/v2/translate'

response = requests.post(service, headers=headers, params=my_params)
if response.ok:
    print(response.json()['translations'][0]['text'])

else:
    print(response.status_code)
