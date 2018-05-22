import Fixer
from DB.SQLite import SQL
from Services.Yandex import Yandex
from Profiler import Profiler

stest = input('Введите sql запрос: ')

# здесь тестовая обработка #
with Profiler() as p:
    stest = SQL.sql(stest)

#print('Число строк в [anecdotes]: ' + str(SQL.Count('anecdotes')))
print('Результат тестирования:')
print(len(stest))
#print(stest[0])

import time; time.sleep(5)
