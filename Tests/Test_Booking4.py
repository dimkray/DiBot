# -*- coding: utf-8 -*-
# Сервис по работе с подбором жилья (отели, хостелы, квартиры)
import fixer
#from services.URLParser import URL, Parser
from services.House import Booking

# Тест
text = input('Введите город: ')
mlist = Booking.List(text,'2018-05-10','2018-05-11', people=1, order='price', dorm=True)
for item in mlist:
    print(item)
print(Fixer.HYPERTEXT)
