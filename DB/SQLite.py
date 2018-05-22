# -*- coding: utf-8 -*-
# Сервис по работе с БД

import sqlite3

db = 'DB/bot.db'

# Чтение по одному критерию (равенство или like)
def Read(table, colname, value, colValue = '*', bLike = False, bOne = False, bFirst = False):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    colname = colname.lower()
    colValue = colValue.lower()
    if isinstance(value, str): value = '"'+value+'"'
    else: value = str(value)
    slike = '='
    if bLike: slike = 'LIKE'
    sql = 'SELECT %s FROM %s WHERE %s %s %s' % (colValue, table, colname, slike, value)
    result = [] # создаём пустой масив
    print(sql)
    try:
        cursor.execute(sql)
        if bOne:
            row = cursor.fetchone() # загрузка данных по одной строке
            #print(row)
            while row is not None:
                if colValue == '*': result.append(row)
                else: result.append(row[0])
                row = cursor.fetchone()
                #print(row)
        else:
            for row in cursor.fetchall(): # Загрузка всех данных
                #print(row)
                if colValue == '*': result.append(row)
                else: result.append(row[0])
        if bFirst: result = result[0]
        conn.close()
        return result
    except e as Exception: # ошибка при чтении
        conn.close()
        if bFirst and colValue != '*': return '#bug: ' + str(e)
        return result

# Обновление данных по одному критерию (равенство или like)
def Update(table, colname, value, colUpdate, newValue, bLike = False):
    conn = sqlite3.connect(db)
    colname = colname.lower()
    colUpdate = colUpdate.lower()
    cursor = conn.cursor()
    if isinstance(value, str): value = '"'+value+'"'
    else: value = str(value)
    slike = '='
    if bLike: slike = 'LIKE'
    sql = 'UPDATE %s SET %s = %s WHERE %s %s %s' % (table, colUpdate, newValue, colname, slike, value)
    result = [] # создаём пустой масив
    print(sql)
    try:
        cursor.execute(sql)
        conn.commit()
        print('Обновлено строк: %d' % cursor.rowcount)
        conn.close()
        return True
    except: # ошибка при чтении
        conn.close()
        return False

# основной класс
class SQL:
    
    # Создание таблицы
    def Table(table, drows):
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        sql = 'CREATE TABLE %s (' % table.lower()
        i = 0
        for key in drows:
            sql += key.lower()
            if drows[key].lower() == 'integer' or drows[key].lower() == 'int': sql += ' integer'
            elif drows[key].lower() == 'real': sql += ' real'
            else: sql += ' text'
            i += 1
            if i == len(drows): sql += ')'
            else: sql += ', '
        print(sql)
        try:
            cursor.execute(sql)
            conn.commit()
            conn.close()
            return True
        except: # возможно таблица создана ранее
            conn.close()
            return False  

    # Запись данных
    def WriteLine(table, sline):
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        sql = 'INSERT INTO %s VALUES (%s)' % (table.lower(), sline)
        print(sql)
        try:
            cursor.execute(sql)
            conn.commit()
            print('Добавлено строк: %d' % cursor.rowcount)
            conn.close()
            return True
        except: # проблема с записью
            conn.close()
            return False 

    # Запись данных
    def WriteRow(table, mrow):
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        sql = 'INSERT INTO %s VALUES (' % table.lower()
        i = 0
        for item in mrow:
            if isinstance(item, str): sql += '"'+item+'"'
            else: sql += str(item)
            i += 1
            if i == len(mrow): sql += ')'
            else: sql += ', '
        print(sql)
        try:
            cursor.execute(sql)
            conn.commit()
            print('Добавлено строк: %d' % cursor.rowcount)
            conn.close()
            return True
        except: # проблема с записью
            conn.close()
            return False  

    # Запись данных блоками
    def WriteBlock(table, mblock):
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        num = len(mblock[0])
        sql = 'INSERT INTO %s VALUES (' % table.lower()
        for i in range(0, num):
            sql += '?'
            if i == num-1: sql += ')'
            else: sql += ','
        print(sql)
        try:
            cursor.executemany(sql, mblock)
            conn.commit()
            print('Добавлено строк: %d' % cursor.rowcount)
            conn.close()
            return True
        except: # ошибка при записи
            conn.close()
            return False 

    # Получение числа строк (rows)
    def Count(table):
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        sql = 'SELECT count(*) FROM %s' % table
        print(sql)
        try:
            cursor.execute(sql)
            row = cursor.fetchone()
            #print(row)
            return row[0]
        except: # ошибка при чтении
            conn.close()
            return 0

    # Загрузка всей таблицы
    def ReadAll(table):
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        sql = 'SELECT * FROM %s' % table
        result = [] # создаём пустой масив
        print(sql)
        try:
            cursor.execute(sql)
            for row in cursor.fetchall():
                result.append(row)
            conn.close()
            return result
        except: # ошибка при чтении
            conn.close()
            return result

    # Загрузка по одной строке
    def ReadRowsOne(table, colname, value):
        return Read(table, colname, value, bOne = True)   

    # Чтение по одному критерию (равенство)
    def ReadRows(table, colname, value):
        return Read(table, colname, value)

    # Чтение первой строки по одному критерию (равенство)
    def ReadRow(table, colname, value):
        return Read(table, colname, value, bFirst = True) 

    # Чтение по одному критерию (like %text%)
    def ReadRowsLike(table, colname, svalue):
        return Read(table, colname, svalue, bLike = True)

    # Чтение по одному критерию (like %text%)
    def ReadRowLike(table, colname, svalue):
        return Read(table, colname, svalue, bLike = True, bFirst = True)

    # Чтение одного значения по одному критерию (равенство)
    def ReadValue(table, colname, value, colvalue):
        return Read(table, colname, value, colValue = colvalue, bFirst = True)

    # Чтение нескольких значений по одному критерию (равенство)
    def ReadValues(table, colname, value, colvalue):
        return Read(table, colname, value, colValue = colvalue)

    # Чтение одного значения по одному критерию (like %text%)
    def ReadValueLike(table, colname, value, colvalue):
        return Read(table, colname, value, colValue = colvalue, bFirst = True)

    # Чтение нескольких значений по одному критерию (like %text%)
    def ReadValuesLike(table, colname, value, colvalue):
        return Read(table, colname, value, colValue = colvalue)

    # Обновление данных по одному критерию (равенство)
    def UpdateValues(table, colname, value, colupdate, newvalue):
        return Update(table, colname, value, colupdate, newvalue)

    # Обновление данных по одному критерию (like %text%)
    def UpdateValuesLike(table, colname, value, colupdate, newvalue):
        return Update(table, colname, value, colupdate, newvalue, bLike = True)

    # Удаление данных по одному критерию (равенство)
    def DeleteRow(table, colname, value):
        conn = sqlite3.connect(db)
        colname = colname.lower()
        cursor = conn.cursor()
        if isinstance(value, str): value = '"'+value+'"'
        else: value = str(value)
        sql = 'DELETE FROM %s WHERE %s = %s' % (table, colupdate, newvalue, colname, svalue)
        result = [] # создаём пустой масив
        print(sql)
        try:
            cursor.execute(sql)
            conn.commit()
            conn.close()
            return True
        except: # ошибка при чтении
            conn.close()
            return False

    # Универсальный запрос
    def sql(query):
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        result = [] # создаём пустой масив
        try:
            cursor.execute(query)
            for row in cursor.fetchall(): # Загрузка всех данных
                #print(row)
                result.append(row)
            if query.upper().find('UPDATE ') >= 0 or query.upper().find('DELETE ') >= 0:
                conn.commit()
                print('Изменено строк: %d' % cursor.rowcount)
            conn.close()
            return result
        except: # ошибка при чтении
            conn.close()
            return result
