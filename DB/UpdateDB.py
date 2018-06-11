# -*- coding: utf-8 -*-
# Обновление базы данных DiBot из открытых источников

import Fixer
from Services.IATA import IATA
from DB.SQLite import SQL

def UpdateTable(NameTable, dCols, data):
    print('Удаление старой таблицы "%s"' % NameTable)
    print('Результат: ' + SQL.Delete(NameTable))
    print('Создание новой таблицы "%s"' % NameTable)
    print('Результат: ' + SQL.Table(NameTable, dCols))
    print('Запись данных: %i строк' % len(data))
    print('Результат: ' + SQL.WriteBlock(NameTable, data))
    print('-------------------------------------')

# основной блок программы
#----------------------------------

# База аэропортов IATA

mAir = IATA.Airport()
if mAir[0] != '#':
    Airs = []
    for air in mAir:
        mRow = []
        mRow.append(air['code'])
        mRow.append(air['name'])
        mRow.append(air['name'].upper().replace('Ё','Е'))
        Airs.append(mRow)
    UpdateTable('IATA_airports', {'code': 'text nn u',
                                  'name': 'text nn',
                                  'nameU': 'text nn'}, Airs)
else: # ошибка!
    print(mAir)

