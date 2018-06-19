# -*- coding: utf-8 -*-
# Сервис по работе с базами данных (wrapper)

import Fixer
from DB.SQLite import SQL, CSV

tDel = [] # Список удалённых таблиц

class Worker:

    # Добавление новой таблицы или добавлене данных в таблицу
    def AddTable(NameTable, dCols, data):
        print('Создание таблицы "%s"' % NameTable)
        print('Результат: ' + SQL.Table(NameTable, dCols))
        print('Запись данных: %i строк' % len(data))
        print('Результат: ' + SQL.WriteBlock(NameTable, data))
        print('-------------------------------------')

    # Удаление старой таблицы и формирование новой таблицы
    def UpdateTable(NameTable, dCols, data):
        if NameTable not in tDel: # проверяем не удалена ли таблица уже
            print('Удаление старой таблицы "%s"' % NameTable)
            print('Результат: ' + SQL.Delete(NameTable))
            print('Создание новой таблицы "%s"' % NameTable)
            print('Результат: ' + SQL.Table(NameTable, dCols))
            tDel.append(NameTable)
        print('Запись данных: %i строк' % len(data))
        print('Результат: ' + SQL.WriteBlock(NameTable, data))
        print('-------------------------------------')

    # Создание новой таблицы (с удалением старой) на основе CSV-файла (для ЕГР)
    # dCols - соотношение данных таблицы с шапкой таблицы CSV: {nameDB: nameCSV}
    def UpdateTableCSV(NameTable, csvFile, dCols, blocks=1):
        items = 100000; block = 1000000
        print('Чтение данных файла "%s"' % NameTable)
        for iblock in range(0, blocks):
            mRows, mTable = CSV.Reader(csvFile, separator=';', items=block, istart=iblock, download=orgs)
            for row in mRows:
                ......
        

# основной блок программы
#----------------------------------

yn = input('...... Обновить таблицы и загрузить новые данные? Y/N: ')
if yn == 'Y':
