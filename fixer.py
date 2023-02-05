# -*- coding: utf-8 -*-
from datetime import datetime, date, timedelta
from DB.SQLite import SQL
import config
import json
import os


serv = ''  # Название текущего сервиса для добавления описания функции


# Функция проверки существования файла
def exist(file_path: str) -> bool:
    if os.path.exists(file_path): return True
    else: return False


# Функция записи словаря
def Save(dictionary, name):
    try:
        f = open('DB/' + name + '.json', 'w', encoding='utf-8')
        json.dump(dictionary, f, sort_keys=False, ensure_ascii=False)
        f.close()
        return True
    except Exception as e:
        err_log('Fixer.Save', name + '.json - ' + str(e))
        return False


# Функция загрузки словаря
def Load(name):
    try:
        dictionary = {}
        if exist('DB/' + name + '.json') == False: return dictionary
        f = open('DB/' + name + '.json', 'r', encoding='utf-8')
        dictionary = json.load(f)
        return dictionary
    except Exception as e:
        err_log('Fixer.Load', name + '.json - ' + str(e))
        return dictionary


# ---------------------------------------------------------
# вн.сервис Dialog - использование внутреннего диалога
def Dialog(key):
    import random
    if key in dialogs:
        return random.choice(dialogs[key])
    else:
        err_log('Fixer.Dialog', 'не найден ключ: ' + key)
        return key


# ---------------------------------------------------------
# вн.сервис substitution - подстановка строковых переменных
def insert_substring(text: str):
    text = text.replace('\\n', '\n')
    while text.find('['):
        for word in config.WORDS:
            if word in text: text.replace(word, config.WORDS[word])
    return text


# ---------------------------------------------------------
# вн.сервис strOperand - преобразование различных операций с возможными числами
def strOperand(value, number, operand='*'):
    s = ''
    if value is not None:
        value = float(value)
        if operand == '*':
            return str(value * number)
        elif operand == '/':
            return str(value / number)
        elif operand == '-':
            return str(value - number)
        else:
            return str(value + number)
    return s


# ---------------------------------------------------------
# вн.сервис strfind - поиск строки и обрезка по найденному (регистронезависимый)
def strfind(text, mfind, poz=0):
    textU = text.upper()
    for sfind in mfind:
        ilen = len(sfind)
        if poz >= 0:  # если ищем по тексту в определённой позиции
            if textU.find(sfind.upper()) == poz:
                return sfind, (text[:poz] + text[poz + ilen:]).strip()  # вырезание
        else:  # если ищем везде
            if textU.find(sfind.upper()) >= 0:
                while textU.find(sfind.upper()) >= 0:
                    text = text[:poz] + text[poz + ilen:]  # вырезание
                    textU = text.upper()
                return sfind, text.strip()
    return '', text  # ничего не нашлось


# ---------------------------------------------------------
# вн.сервис servicefind - поиск сервиса и обрезка по найденному (регистронезависимый)
def servicefind(text):
    m = []  # массив сервисов
    for skey in Services:
        m.append('#%s:' % skey)
        if len(Services[skey][9]) > 0:  # если есть подсервисы
            for subser in Services[skey][9]:
                m.append('#%s-%s:' % (skey, subser))
    return strfind(text, m)  # поиск сервиса


# ---------------------------------------------------------
# вн.сервис strCleaner - упрощение строки (убирает все лишние символы)
def strCleaner(text):
    dFormat = {'ё': 'е', '«': '', '»': '', '!': '', '@': '', '~': '', '#': '', '^': '', '&': '', '*': '',
               '(': '', ',': '', '- ': ' ', '+': '', '=': '', '{': '', '}': '', '[': '', ']': '', ';': '',
               ':': '', '?': '', '<': '', '>': '', '.': '', '`': '', '\\': '', '|': '', '/': '', '  ': ' '}
    text = text.strip().lower()
    for key in dFormat:
        text = text.replace(key, dFormat[key])
    return text


# ---------------------------------------------------------
# вн.сервис strSpec - заменяет спецсимволы на номальные символы
def strSpec(text):
    dFormat = {'&quot;': '"', '&nbsp;': ' ', '&ensp;': ' ', '&emsp;': '  ', '&ndash;': '-', '&mdash;': '—',
               '&shy;': ' ', '&copy;': '©', '&reg;': '®', '&trade;': '™', '&permil;': '‰', '&deg;': '°'}
    for key in dFormat:
        text = text.replace(key, dFormat[key])
    return text


# ---------------------------------------------------------
# вн.сервис strAdd - добавление строки, если есть
def strAdd(value, text=''):
    global stxt
    s = ''
    if value is not None:
        if text != '':
            s = '%s: %s\n' % (text, str(value))
        else:
            s = '%s\n' % str(value)
    stxt += s
    return s


# ---------------------------------------------------------
# вн.сервис strPut - добавление строки, если есть
def strPut(value, aletertext=''):
    if value is not None:
        s = str(value)
    else:
        s = aletertext
    return s


# ---------------------------------------------------------
# вн.сервис strList - преобразование списка в строку с разделителями
def strList(mlist, separator=', '):
    s = ''
    if len(mlist) > 0:
        for item in mlist:
            s += str(item) + separator
        s = s[:-len(separator)]
    return s


# ---------------------------------------------------------
# вн.сервис dFormat - преобразование результата dict в форматированный текст - список
# если задан формат: sformat = 'Номер: {number} - значение: {value}' - приоритетно
# если заданы подписи ключей: nameKey = {'number': 'номер', 'value': 'значение', 'no_write': '#'}  # - не подписывать
def dFormat(dresult, items=5, sformat='', nameKey={}, sobj='объектов'):
    if len(dresult) > 0:  # если есть результат
        s = 'По запросу найдено %s: %i' % (sobj, len(dresult))
        if items < len(dresult):
            s += '\nБудут показаны первые %i:' % items
        else:
            items = len(dresult)
        for i in range(0, items):
            obj = dresult[i]
            if sformat == '':  # если не задан формат
                if len(nameKey) == 1:  # если нужен только один ключ
                    s += '\n[%i] %s' % (i + 1, obj[nameKey.keys()[0]])
                elif len(nameKey) > 1:  # если есть подписи для ключей
                    s += '\n[%i] ' % (i + 1)
                    for key in nameKey.keys():
                        if nameKey[key] == '#':
                            s += '%s' % (obj[key])
                        else:
                            s += '\n%s: %s' % (nameKey[key], obj[key])
                else:  # если нет подписей для ключей
                    s += '\n[%i] %s' % (i + 1, obj[nameKey.keys()[0]])
                    for key in nameKey.keys():
                        s += '\n%s: %s' % (nameKey[key], dresult[i])
            else:  # если задан формат: sformat = 'Номер: {number} - значение: {value}'
                sitem = sformat
                for key in obj.keys():
                    sitem = sitem.replace('{%s}' % key, str(obj[key]))
                s += '\n[' + str(i + 1) + '] ' + sitem
    else:
        s = 'По данному запросу нет результата'
    return s


# ---------------------------------------------------------
# вн.сервис mFormat - преобразование результата list в форматированный текст - список
# если задан формат: sformat = 'Номер: %0 - значение: %1 \\%' - приоритетно
# если заданы названия колонок: nameCol = ['номер', 'значение'] - название первой колонка игнорируется
def mFormat(mresult, items=5, sformat='', nameCol=[], sobj='объектов'):
    if len(mresult) > 0:  # если есть результат
        s = 'По запросу найдено %s: %i' % (sobj, len(mresult))
        if items < len(mresult):
            s += '\nБудут показаны первые %i:' % items
        else:
            items = len(mresult)
        for i in range(0, items):
            if sformat == '':  # если не задан формат
                if len(nameCol) > 1:  # если несколько возвращаемых колонок
                    row = mresult[i]
                    s += '\n[%i] %s:' % (i + 1, row[0])
                    ic = 0
                    for col in nameCol:
                        if col == 0: ic += 1; continue
                        s += '\n%s: %s' % (col, row[ic])
                        ic += 1
                else:  # если одна возвращаемая колонка
                    s += '\n[%i] %s' % (i + 1, mresult[i])
            else:  # если задан формат: sformat = 'Номер: %0 - значение: %1 \\%'
                sitem = sformat
                row = mresult[i]
                while sitem.find('%%') >= 0:
                    x = sitem.find('%%') + 2
                    r = int(sitem[x:x + 2])
                    sitem = sitem.replace('%%' + str(r), str(row[r]))
                while sitem.find('%') >= 0:
                    x = sitem.find('%') + 1
                    r = int(sitem[x:x + 1])
                    sitem = sitem.replace('%' + str(r), str(row[r]))
                while sitem.find('\\%') >= 0:
                    sitem = sitem.replace('\\%', '%')
                s += '\n[' + str(i + 1) + '] ' + sitem
    else:
        s = 'По данному запросу нет результата'
    return s


# ---------------------------------------------------------
# вн.сервис getparams - получение переменных в массив [] из строки переменных для сервиса
def get_params(text: str, separator='|'):
    """Получение переменных в массив [] из строки переменных для сервиса"""
    if text.find(separator) < 0 and separator != ';':  # нет текущего сепаратора
        if text.find(' - ') > 0: separator = ' - '
        else:
            if text.find(',') > 0: separator = ','
            else: separator = ' '
    if text.find('[R') >= 0:  # Признак радиуса интереса
        poz = text.find('[R')
        end = text.find(']', poz)
        print(text[poz + 2:end - 1])
        config.RADIUS_INTEREST = float(text[poz + 2:end - 1])
        text = text.replace('[R' + text[poz + 2:end - 1] + ']', '')  # Убираем радиус интереса
    params = text.split(separator)
    for x, im in enumerate(params):
        params[x] = im.strip()  # убираем лишние пробелы
    return params


# ---------------------------------------------------------
# вн.сервис Sort для сортировки двухмерных массивов (сортировка по номеру колонки)
def Sort(massive, colnum, reverse=False):
    try:
        massive = sorted(massive, key=lambda st: st[colnum], reverse=reverse)
    except:
        pass
    return massive


# ---------------------------------------------------------
# вн.сервис inList - Добавление элемента в список (List), если его нет
def inList(mList, item):
    if item not in mList:
        mList.append(item)
    return mList


# ---------------------------------------------------------
# вн.сервис ListToDict - Преобразование двух списков в словарь внутри списка
def ListToDict(mNames, mRows, namesRez=[]):
    if namesRez == []: namesRez = mNames
    mRez = [];
    mIdx = []
    for name in namesRez:
        i = 0
        try:
            i = mNames.index(name)
        except:
            i = -1
        mIdx.append(i)
    for row in mRows:
        drow = {}
        i = 0
        for name in namesRez:
            if mIdx[i] >= 0:
                drow[name] = row[mIdx[i]]
            i += 1
        mRez.append(drow)
    return mRez


add_fun('uniq', 'Получение списка уникальных записей',
        {'seq': 'список записей [list]'},
       'список уникальных записей [list]')


# Загрузка таблиц из БД
log('Fixer.Start', '------ Загрузка данных ------')
mCompliment = SQL.ReadAll('complimentMan')
wCompliment = SQL.ReadAll('complimentWoman')
Valutes = SQL.ReadDict('valutes')
valutes = SQL.ReadDict('valutes2')
yaLangs = SQL.ReadDict('yaLangs')
yaDirLang = SQL.ReadAll('yaDirLang')

# Пользовательские настройки сервисов
Settings = Load('DefSettings')

# Загрузка всех полезных словарей
Commands = Load('Commands')
Word1 = Load('Word1')
KeyWord = Load('KeyWord')
dialogs = Load('dialogs')
NewDialogs = Load('NewDialogs')
Services = Load('Services')
# Names = Load('Names')
log('Fixer.Start', 'Все словари загружены!')

# Создание базы данных
# import DB.CreateDB

# Обновление базы данных (из открытых источников)
# import DB.UpdateDB
