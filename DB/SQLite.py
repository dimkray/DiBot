# -*- coding: utf-8 -*-
# Сервис по работе с БД

import Fixer
import sqlite3

db = 'DB/bot.db'

# Чтение по одному критерию (равенство или like)
def Read(table, colname, value, colValue = '*', bLike = False, bOne = False, bFirst = False):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    value = value.upper()
    value = value.replace('Ё','Е')
    if isinstance(value, str): value = '"'+value+'"'
    else: value = str(value)
    if bLike: sql = 'SELECT %s FROM %s WHERE UPPER(%s) LIKE %s' % (colValue, table, colname, value)
    else: sql = 'SELECT %s FROM %s WHERE %s = %s' % (colValue, table, colname, value)
    result = [] # создаём пустой масив
    Fixer.log('SQLite.Read', sql)
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
                elif colValue.find(',') > 0: result.append(row)
                else: result.append(row[0])
        if bFirst: result = result[0]
        conn.close()
        return result
    except Exception as e: # ошибка при чтении
        conn.close()
        if bFirst and colValue != '*': return '#bug: ' + str(e)
        return result

# Обновление данных по одному критерию (равенство или like)
def Update(table, colname, value, colUpdate, newValue, bLike = False):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    if isinstance(value, str): value = '"'+value+'"'
    else: value = str(value)
    slike = '='
    if bLike: slike = 'LIKE'
    sql = 'UPDATE %s SET %s = %s WHERE %s %s %s' % (table, colUpdate, newValue, colname, slike, value)
    result = [] # создаём пустой масив
    Fixer.log('SQLite.Update', sql)
    try:
        cursor.execute(sql)
        conn.commit()
        Fixer.log('SQLite.Update', 'Обновлено строк: %d' % cursor.rowcount)
        conn.close()
        return 'OK'
    except Exception as e: # ошибка при чтении
        conn.close()
        return '#bug: ' + str(e)

# основной класс
class SQL:
    
    # Создание таблицы
    def Table(table, drows):
        Fixer.log('SQLite.Table')
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        sql = 'CREATE TABLE %s (' % table
        i = 0
        for key in drows:
            sql += key
            sval = drows[key].lower()
            if sval.find('int') == 0: sql += ' INTEGER'
            elif sval.find('real') == 0 or sval.find('float') == 0: sql += ' REAL'
            elif sval.find('bool') == 0: sql += ' BOOLEAN'
            elif sval.find('blob') == 0: sql += ' BLOB'
            elif sval.find('char') == 0: sql += ' CHAR'
            else: sql += ' TEXT'
            if sval.find('(') > 0 and sval.find(')') > sval.find('('): sql += sval[sval.find('('):sval.find(')')+1]
            if sval.find(' pk') > 0 or sval.find(' primary key') > 0: sql += ' PRIMARY KEY'
            if sval.find(' nn') > 0 or sval.find(' not null') > 0: sql += ' NOT NULL'
            if sval.find(' u') > 0 or sval.find(' unique') > 0: sql += ' UNIQUE'
            i += 1
            if i == len(drows): sql += ')'
            else: sql += ', '
        Fixer.log('SQLite.Table', sql)
        try:
            cursor.execute(sql)
            conn.commit()
            conn.close()
            return 'OK'
        except Exception as e: # возможно таблица создана ранее
            conn.close()
            return '#bug: ' + str(e)  

    # Запись данных
    def WriteLine(table, sline):
        Fixer.log('SQLite.WriteLine')
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        sql = 'INSERT INTO %s VALUES (%s)' % (table, sline)
        Fixer.log('SQLite.WriteLine', sql)
        try:
            cursor.execute(sql)
            conn.commit()
            Fixer.log('SQLite.WriteLine', 'Добавлено строк: %d' % cursor.rowcount)
            conn.close()
            return 'OK'
        except Exception as e: # проблема с записью
            conn.close()
            return '#bug: ' + str(e) 

    # Запись данных [list]
    def WriteRow(table, mrow):
        Fixer.log('SQLite.WriteRow')
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        sql = 'INSERT INTO %s VALUES (' % table
        i = 0
        for item in mrow:
            if isinstance(item, str): sql += '"'+item+'"'
            else: sql += str(item)
            i += 1
            if i == len(mrow): sql += ')'
            else: sql += ', '
        Fixer.log('SQLite.WriteRow', sql)
        try:
            cursor.execute(sql)
            conn.commit()
            conn.close()
            return 'OK'
        except Exception as e: # проблема с записью
            conn.close()
            return '#bug: ' + str(e)

    # Запись данных [dict]
    def WriteDictRow(table, drow):
        Fixer.log('SQLite.WriteDictRow')
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        columns = ', '.join(drow.keys())
        placeholders = ':'+', :'.join(drow.keys())
        sql = 'INSERT INTO %s (%s) VALUES (%s)' % (table, columns, placeholders)
        Fixer.log('SQLite.WriteDictRow', sql)
        try:
            cursor.execute(sql, drow)
            conn.commit()
            conn.close()
            return 'OK'
        except Exception as e: # проблема с записью
            conn.close()
            return '#bug: ' + str(e)

    # Запись данных блоками
    def WriteBlock(table, mblock):
        Fixer.log('SQLite.WriteBlock')
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        num = len(mblock[0])
        sql = 'INSERT INTO %s VALUES (' % table
        for i in range(0, num):
            sql += '?'
            if i == num-1: sql += ')'
            else: sql += ','
        Fixer.log('SQLite.WriteBlock', sql)
        try:
            cursor.executemany(sql, mblock)
            conn.commit()
            Fixer.log('SQLite.WriteBlock', 'Добавлено строк: %d' % cursor.rowcount)
            conn.close()
            return 'OK'
        except Exception as e: # ошибка при записи
            conn.close()
            return '#bug: ' + str(e)

    # Получение числа строк (rows)
    def Count(table):
        Fixer.log('SQLite.Count')
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        sql = 'SELECT count(*) FROM %s' % table
        Fixer.log('SQLite.Count', sql)
        try:
            cursor.execute(sql)
            row = cursor.fetchone()
            #print(row)
            return row[0]
        except: # ошибка при чтении
            conn.close()
            return -1

    # Загрузка всей таблицы
    def ReadAll(table):
        Fixer.log('SQLite.ReadAll')
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        sql = 'SELECT * FROM %s' % table
        result = [] # создаём пустой масив
        Fixer.log('SQLite.ReadAll', sql)
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
        Fixer.log('SQLite.ReadRowsOne')
        return Read(table, colname, value, bOne = True)   

    # Чтение по одному критерию (равенство)
    def ReadRows(table, colname, value):
        Fixer.log('SQLite.ReadRows')
        return Read(table, colname, value)

    # Чтение первой строки по одному критерию (равенство)
    def ReadRow(table, colname, value):
        Fixer.log('SQLite.ReadRow')
        return Read(table, colname, value, bFirst = True) 

    # Чтение по одному критерию (like %text%)
    def ReadRowsLike(table, colname, svalue):
        Fixer.log('SQLite.ReadRowsLike')
        return Read(table, colname, svalue, bLike = True)

    # Чтение по одному критерию (like %text%)
    def ReadRowLike(table, colname, svalue):
        Fixer.log('SQLite.ReadRowLike')
        return Read(table, colname, svalue, bLike = True, bFirst = True)

    # Чтение одного значения по одному критерию (равенство)
    def ReadValue(table, colname, value, colvalue):
        Fixer.log('SQLite.ReadValue')
        return Read(table, colname, value, colValue = colvalue, bFirst = True)

    # Чтение нескольких значений по одному критерию (равенство)
    def ReadValues(table, colname, value, colvalue):
        Fixer.log('SQLite.ReadValues')
        return Read(table, colname, value, colValue = colvalue)

    # Чтение одного значения по одному критерию (like %text%)
    def ReadValueLike(table, colname, value, colvalue):
        Fixer.log('SQLite.ReadValueLike')
        return Read(table, colname, value, colValue = colvalue, bFirst = True)

    # Чтение нескольких значений по одному критерию (like %text%)
    def ReadValuesLike(table, colname, value, colvalue):
        Fixer.log('SQLite.ReadValuesLike')
        return Read(table, colname, value, colValue = colvalue)

    # Обновление данных по одному критерию (равенство)
    def UpdateValues(table, colname, value, colupdate, newvalue):
        Fixer.log('SQLite.UpdateValues')
        return Update(table, colname, value, colupdate, newvalue)

    # Обновление данных по одному критерию (like %text%)
    def UpdateValuesLike(table, colname, value, colupdate, newvalue):
        Fixer.log('SQLite.UpdateValuesLike')
        return Update(table, colname, value, colupdate, newvalue, bLike = True)

    # Удаление данных по одному критерию (равенство)
    def DeleteRow(table, colname, value):
        Fixer.log('SQLite.DeleteRow')
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        if isinstance(value, str): value = '"'+value+'"'
        else: value = str(value)
        sql = 'DELETE FROM %s WHERE %s = %s' % (table, colupdate, newvalue, colname, svalue)
        result = [] # создаём пустой масив
        Fixer.log('SQLite.DeleteRow', sql)
        try:
            cursor.execute(sql)
            conn.commit()
            conn.close()
            return 'OK'
        except Exception as e: # ошибка при чтении
            conn.close()
            return '#bug: ' + str(e)

    # Универсальный запрос
    def sql(query):
        Fixer.log('SQLite.sql')
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
                Fixer.log('SQLite.sql', 'Изменено строк: %d' % cursor.rowcount)
            conn.close()
            return result
        except Exception as e: # ошибка при чтении
            conn.close()
            return result

# класс поиска данных из БД
class Finder:
    # Поиск всех данных по некольким столбцам (like %text%)
    def FindAll(table, mcols, svalue, returnCol = []):
        Fixer.log('SQLite.FindAll')
        rCol = ''
        if returnCol == []: rCol = '*'
        else:
            for col in returnCol:
                rCol += ', ' + col
            rCol = rCol[2:]
        mresult = []
        for col in mcols:
            mresult += Read(table, col, svalue, colValue = rCol, bLike = True)
        return mresult

    # Поиск первой строки по некольким столбцам (like %text%)
    def Find(table, mcols, svalue, returnCol = []):
        Fixer.log('SQLite.Find')
        rCol = ''
        if returnCol == []: rCol = '*'
        else:
            for col in returnCol:
                rCol += ', ' + col
            rCol = rCol[2:]
        mresult = []
        for col in mcols:
            mresult += Read(table, col, svalue, colValue = rCol, bLike = True)
        return mresult[0]

    # Поиск всех данных по некольким столбцам (like %text%) - и отображение items строк
    def strFind(table, mcols, svalue, returnCol = [], items = 5, sFormat = ''):
        Fixer.log('SQLite.strFind')
        m = Finder.FindAll(table, mcols, svalue, returnCol=returnCol)
        s = ''
        if len(m) > 0: # если есть результат
            s = 'Найдено совпадений: ' + str(len(m))
            if items < len(m): s += '\nБудут показаны первые %i:' % items
            for i in range(0,items):
                if sFormat == '': # если не задан формат
                    if len(returnCol) > 1: # если несколько возвращаемых колонок
                        row = m[i]
                        s += '\n[%i] %s:' % (i+1, row[0])
                        ic = 0
                        for col in returnCol:
                            if col == 0: ic += 1; continue
                            s += '\n%s: %s' % (col, row[ic])
                            ic += 1              
                    else: # если одна возвращаемая колонка
                        s += '\n[%i] %s' % (i, m[0])
                else: # если задан формат
                    sitem = sFormat
                    row = m[i]
                    while sitem.find('%') >= 0:
                        x = sitem.find('%')+1
                        r = int(sitem[x:x+1])
                        sitem = sitem.replace('%'+str(r), row[r])
                    s += '\n['+str(i+1)+'] ' + sitem
        else: s = 'Поиск по строке "%s" не дал результатов :(' % svalue
        return s

    
