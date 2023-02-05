from Profiler import Profiler
import fixer
import config
import json
from Services.URLParser import URL
from DB.SQLite import Finder

api = 'https://dibotapi.herokuapp.com'
params = {'api_key': config.IATA_KEY, 'lang': 'ru'}

# Получение данных по коду/имени
def GetData(path=''):
    if path != '':
        http = '%s/%s/' % (api, path)
    else:
        http = api+'/'
    json = URL.GetData(http, headers = {'Content-Type':'application/json'}, bjson=True)
    return json

with Profiler() as p:
    print(GetData())

with Profiler() as p:
    print(GetData('users'))

with Profiler() as p:
    print(GetData('groups'))

with Profiler() as p:
    print(GetData('users/1'))

with Profiler() as p:
    print(GetData('groups/1'))
