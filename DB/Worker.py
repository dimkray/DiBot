# -*- coding: utf-8 -*-
# Сервис по работе с базами данных (wrapper)

import Fixer
from DB.SQLite import SQL, CSV

tDel = [] # Список удалённых таблиц

class Worker:
    # Добавление новой таблицы или добавление данных в таблицу
    def AddTable(NameTable, dCols, data):
        print('Создание таблицы "%s"' % NameTable)
        print('Результат: ' + SQL.Table(NameTable, dCols))
        print('Запись данных: %i строк' % len(data))
        result = SQL.WriteBlock(NameTable, data)
        print('Результат: ' + result)
        print('-------------------------------------')
        return result

    # Удаление старой таблицы и формирование новой таблицы
    def UpdateTable(NameTable, dCols, data):
        if NameTable not in tDel: # проверяем не удалена ли таблица уже
            print('Удаление старой таблицы "%s"' % NameTable)
            print('Результат: ' + SQL.Delete(NameTable))
            print('Создание новой таблицы "%s"' % NameTable)
            print('Результат: ' + SQL.Table(NameTable, dCols))
            tDel.append(NameTable)
        print('Запись данных: %i строк' % len(data))
        result = SQL.WriteBlock(NameTable, data)
        print('Результат: ' + result)
        print('-------------------------------------')
        return result

    # Создание новой таблицы (с удалением старой) на основе CSV-файла (для ЕГР)
    # dCols - соотношение данных таблицы с шапкой таблицы CSV: {nameDB: nameCSV}
    def UpdateTableCSV(NameTable, dCols, csvFile, dColsCSV={}, blocks=1):
        indexes = [] # индексы CSV для записи данных в БД
        cols = dCols.keys() # названия полей таблицы БД
        # получение шапки CSV
        row, mTable = CSV.Reader(csvFile, separator=';', items=1)
        if dColsCSV == {}:
            for col in cols:
                try:
                    i = mTable.index(col) # поиск соотвествия таблицы
                except: i = -1
                indexes.append(i)
        else:
            for col in cols:
                try:
                    i = mTable.index(dColsCSV[col]) # поиск индекса в dColsCSV
                except: i = -1    
                indexes.append(i)
        print(indexes)
        items = 100000; block = 1000000 # размер блока
        print('Чтение данных файла "%s"' % NameTable)
        for iblock in range(0, blocks): # обработка данных блоками
            mRows, mTable = CSV.Reader(csvFile, separator=';', items=block, istart=iblock, download=items)
            data = []
            for row in mRows:
                m = []
                for i in indexes:
                    if i != -1: m.append(row[i])
                    else: m.append(None)
                data.append(m)
            result = Worker.UpdateTable(NameTable, dCols, data)
        return result
