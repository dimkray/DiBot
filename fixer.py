# -*- coding: utf-8 -*-
from system.logging import log, err_log
from system.file import load
from system.SQLite import DataBase
from system.string import str_find
from system.function import add_fun
import config


# ---------------------------------------------------------
# вн.сервис Dialog - использование внутреннего диалога
def Dialog(key):
    import random
    if key in DIALOGS:
        return random.choice(DIALOGS[key])
    else:
        err_log('Fixer.Dialog', 'не найден ключ: ' + key)
        return key


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


# ---------------------------------------------------------
# вн.сервис servicefind - поиск сервиса и обрезка по найденному (регистронезависимый)
def service_find(text):
    services = []  # массив сервисов
    for skey in SERVICES:
        services.append(f'#{skey}:')
        if len(SERVICES[skey][9]) > 0:  # если есть подсервисы
            for subser in SERVICES[skey][9]:
                services.append(f'#{skey}-{subser}:')
    return str_find(text, services)  # поиск сервиса


add_fun('uniq', 'Получение списка уникальных записей',
        {'seq': 'список записей [list]'},
       'список уникальных записей [list]')


# Загрузка таблиц из БД
DB = DataBase(config.DB)

log('Загрузка данных', log_type='title')
COMPLIMENT_MAN = DB.read_all('complimentMan')
COMPLIMENT_WOMAN = DB.read_all('complimentWoman')
CURRENCIES = DB.read_dict('valutes')
CURRENCIES2 = DB.read_dict('valutes2')
YA_LANGS = DB.read_dict('yaLangs')
YA_LANG_DIRECTIONS = DB.read_all('yaDirLang')

# Пользовательские настройки сервисов
SETTINGS = load('DefSettings')

# Загрузка всех полезных словарей
COMMANDS = load('Commands')
WORD1 = load('Word1')
KEY_WORD = load('KeyWord')
DIALOGS = load('dialogs')
DIALOGS_NEW = load('NewDialogs')
SERVICES = load('services')
# Names = load('Names')
log('Все словари загружены!')

# Создание базы данных
# import DB.CreateDB

# Обновление базы данных (из открытых источников)
# import DB.UpdateDB
