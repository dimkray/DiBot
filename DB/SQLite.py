# -*- coding: utf-8 -*-
# Сервис по работе с БД

import Fixer
import sqlite3
import csv

# Чтение по одному критерию (равенство или like)
def Read(table, colname, value, colValue = '*', bLike = False, bOne = False, bFirst = False):
    conn = sqlite3.connect(Fixer.DB)
    cursor = conn.cursor()  
    if isinstance(value, str):
        if bLike: value = '%' + value + '%'
        value = '"'+value.upper()+'"'
        value = value.replace('Ё','Е')   
    else: value = str(value)
    if bLike:
        sql = 'SELECT %s FROM %s WHERE UPPER(%s) LIKE %s' % (colValue, table, colname, value)
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
        Fixer.errlog(Fixer.Process, str(e))
        if bFirst and colValue != '*': return '#bug: ' + str(e)
        return result

# Обновление данных по одному критерию (равенство или like)
def Update(table, colname, value, colUpdate, newValue, bLike = False):
    conn = sqlite3.connect(Fixer.DB)
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
        Fixer.errlog(Fixer.Process, str(e))
        return '#bug: ' + str(e)

# основной класс
class SQL:
    
    # Создание таблицы
    def Table(table, drows):
        Fixer.log('SQLite.Table')
        conn = sqlite3.connect(Fixer.DB)
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
            Fixer.errlog(Fixer.Process, str(e))
            return '#bug: ' + str(e)  

    # Запись данных
    def WriteLine(table, sline):
        Fixer.log('SQLite.WriteLine')
        conn = sqlite3.connect(Fixer.DB)
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
            Fixer.errlog(Fixer.Process, str(e))
            return '#bug: ' + str(e) 

    # Запись данных [list]
    def WriteRow(table, mrow):
        Fixer.log('SQLite.WriteRow')
        conn = sqlite3.connect(Fixer.DB)
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
            Fixer.errlog(Fixer.Process, str(e))
            return '#bug: ' + str(e)

    # Запись данных [dict]
    def WriteDictRow(table, drow):
        Fixer.log('SQLite.WriteDictRow')
        conn = sqlite3.connect(Fixer.DB)
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
            Fixer.errlog(Fixer.Process, str(e))
            return '#bug: ' + str(e)

    # Запись данных блоками
    def WriteBlock(table, mblock):
        Fixer.log('SQLite.WriteBlock')
        conn = sqlite3.connect(Fixer.DB)
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
            Fixer.errlog(Fixer.Process, str(e))
            return '#bug: ' + str(e)

    # Запись словаря целиком
    def WriteDictBlock(table, dictionary):
        mDict = []
        for key in dictionary:
            m = []
            m.append(key)
            m.append(dictionary[key])
            mDict.append(m)
        return SQL.WriteBlock(table, mDict)

    # Получение числа строк (rows)
    def Count(table):
        Fixer.log('SQLite.Count')
        conn = sqlite3.connect(Fixer.DB)
        cursor = conn.cursor()
        sql = 'SELECT count(*) FROM %s' % table
        Fixer.log('SQLite.Count', sql)
        try:
            cursor.execute(sql)
            row = cursor.fetchone()
            #print(row)
            return int(row[0])
        except: # ошибка при чтении
            conn.close()
            Fixer.errlog(Fixer.Process, str(e))
            return -1

    # Загрузка всей таблицы
    def ReadAll(table):
        Fixer.log('SQLite.ReadAll')
        conn = sqlite3.connect(Fixer.DB)
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
        except Exception as e: # ошибка при чтении
            conn.close()
            Fixer.errlog(Fixer.Process, str(e))
            return result

    # Загрузка всей таблицы в виде словаря
    def ReadDict(table):
        m = SQL.ReadAll(table)
        Fixer.log('SQLite.ReadDict')
        dic = {}
        try:
            for item in m:
                dic[item[0]] = item[1] # формируем словарь по первым двум колонкам
            return dic
        except Exception as e: # ошибка при чтении
            Fixer.errlog(Fixer.Process, str(e))
            return dic

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
        conn = sqlite3.connect(Fixer.DB)
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
            Fixer.errlog(Fixer.Process, str(e))
            return '#bug: ' + str(e)

    # Удаление всей таблицы!
    def Delete(table):
        Fixer.log('SQLite.Delete')
        conn = sqlite3.connect(Fixer.DB)
        cursor = conn.cursor()
        sql = 'DROP TABLE %s' % (table)
        Fixer.log('SQLite.Delete', sql)
        try:
            cursor.execute(sql)
            conn.commit()
            conn.close()
            return 'OK'
        except Exception as e: # ошибка при чтении
            conn.close()
            Fixer.errlog(Fixer.Process, str(e))
            return '#bug: ' + str(e)

    # Универсальный запрос
    def sql(query):
        Fixer.log('SQLite.sql', query)
        conn = sqlite3.connect(Fixer.DB)
        cursor = conn.cursor()
        result = [] # создаём пустой масив
        try:
            cursor.execute(query)
            if query.upper().find('SELECT ') < 0: conn.commit()
            Fixer.log('SQLite.sql', 'Изменено строк: %d' % cursor.rowcount)
            conn.close()
            return 'OK'
        except Exception as e: # ошибка при чтении
            conn.close()
            Fixer.errlog(Fixer.Process, str(e))
            return '#bug: ' + str(e)

# класс поиска данных из БД
class Finder:
    # Поиск всех данных по некольким столбцам (like %text%)
    def FindAll(table, mcols, svalue, returnCol = [], bLike = True):
        Fixer.log('SQLite.FindAll')
        rCol = ''
        if returnCol == []: rCol = '*'
        else:
            for col in returnCol:
                rCol += ', ' + col
            rCol = rCol[2:]
        mresult = []
        for col in mcols:
            mresult += Read(table, col, svalue, colValue = rCol, bLike=bLike)
        return mresult

    # Поиск первой строки по некольким столбцам (like %text%)
    def Find(table, mcols, svalue, returnCol = [], bLike = True):
        m = Finder.FindAll(table, mcols, svalue, returnCol, bLike=bLike)
        if len(m) > 0: return m[0]
        else: return []

    # Поиск всех данных по некольким столбцам (like %text%) - и отображение items строк
    def strFind(table, mcols, svalue, returnCol = [], items = 5, sFormat = ''):
        Fixer.log('SQLite.strFind')
        m = Finder.FindAll(table, mcols, svalue, returnCol=returnCol)
        return Fixer.strformat(m, items=items, sformat=sFormat, nameCol=returnCol)

# класс работы с SVN-файлами
class CSV:
    # Автоматизированное чтение csv-файла
    def AutoReader(fullname, separator=';', quotechar='\\', items=0, istart=0, download=1000):
        data = []; table = []; i = 0; ist = 0
        with open(fullname, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=separator, quotechar=quotechar)
            for row in reader:
                i += 1
                if i < istart+1: continue # запуск со старта
                ist += 1
                for item in row:
                    if item == '' or item == 'NULL': item = None
                if i == 1: table = row
                else: data.append(row)
                if items != 0 and ist >= items: break
                if i % download == 0:
                    print('Загружено %i записей...' % i)
        return data, table
    
    # Ручное чтение csv-файла
    def Reader(fullname, separator=';', items=0, istart=0, download=1000, symb='\\"'):
        valcount = 0; row = ''
        data = []; table = []; i = 0; ist = 0
        with open(fullname, "r", encoding='utf-8') as f:
            for line in f:
                ierr = 0
                i += 1
                if i < istart+1: continue # запуск со старта
                ist += 1
                if valcount != 0:
                    if line.count(separator) < valcount - 1:
                        row += line.replace('\n','')
                    else: row = line
                    if row.count(separator) < valcount - 1: continue
                else: row = line
                m = []
                if symb != '': row = row.replace(symb,'|^')
                poz = 0; start = 0; end = 0; bChar = False
                while poz >= 0: # ручной поиск разделителей
                    ierr += 1
                    if ierr > 10000:
                        print('BUG! - ошибка в строке ' + str(row))
                        poz = -1
                        continue
                    sep = row.find(separator, poz)
                    if separator != '\t': start = row.find('"', poz)
                    else: start = -1
                    if sep < start or start == -1:
                        start = poz
                        end = sep
                        bChar = False
                    else:
                        start += 1
                        end = row.find('"'+separator, start+1)
                        ss = row[end-2:end]
                        if ss[1] == '"' and ss[0] != '"': # поиск "";
                            end = row.find('"'+separator, end+2)
                        bChar = True
                    if end == -1: end = len(row); poz = -1
                    else: poz = end+2 if bChar else end+1
                    s = row[start:end]
                    try:
                        if len(s) > 0:
                            if s[0] == '"': s = s[1:]
                            if s[-1] == '"': s = s[:-1]
                    except:
                        s = s; print('!!!bug!!! - ' + s)
                    s = s.strip()
                    if '|^' in s: s = s.replace('|^','"')
                    if '""' in s: s = s.replace('""','"')
                    if s != '' and s != 'NULL': m.append(s)
                    else: m.append(None)
                if i == 1: # шапка
                    table = m
                else: data.append(m)
                if valcount == 0: valcount = len(m)
                row = ''
                if items != 0 and ist >= items: break
                if i % download == 0:
                    print('Загружено %i записей...' % i)
        return data, table
    
