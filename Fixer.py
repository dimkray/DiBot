# -*- coding: utf-8 -*-
from datetime import datetime, date, timedelta
from DB.SQLite import SQL
import json
import pickle
import os

# текущая база данных
DB = 'DB/bot.db'

# общие фразы
responses = ['yesno', 'wait', 'notice']
# Загрузка всех словарей в конце файла

Response = ''  # статус диалога с пользователем
Query = ''  # последний запрос пользователя

# уведомление пользователя вкл/выкл
bNotice = True

# Процессорные фиксаторы
bAI = True  # Признак включения сервиса ИИ

# текущая версия
Version = 20180427

# общие фиксаторы
Time = []     # фиксация времени
Chat = []     # история чата
UserID = 0    # текущий пользователь
ChatID = 0    # Текущий чат
PeerID = 0    # Текущее назначение - для беседы, для группы
bChats = 0    # Признак беседы: 0 - не беседа, 1 - беседа, 2 - беседа, где надо ответить
Name = 'человек'     # имя
Family = 'без фамилии'   # фамилия
BirthDay = 'день рождения не известен'  # ДР
Phone = 'телефон не указан'    # номер телефона
eMail = 'e-mail не указан'    # почта
Contacts = {}   # Мессенджеры
Interests = []  # Список интересов
Things = []   # Список вещей/характеристик пользователя
Age = 0       # 0 - неизвестно
Type = 0      # 0 - неизвестно, 1 - мужчина, 2 - женщина
Thema = ''    # текущая тема
LastThema = []  # список последних тем
Mess = ''     # текущий мессенджер
TimeZone = 3  # часовой пояс пользователя относительно UTF

Process = ''  # текущий процесс
errProcess = ''  #процесс, в котором возникла ошибка
errMsg = ''   #сообщение об ошибке

bNow = False  # признак сейчас
Date = date.today()

Service = '#'  # текущий сервис
Context = False
LastService = []

Radius = 100   # радиус интресера

stxt = ''      # строка для ответа

htext = ''    # гиперссылка

# сервис Локация
X = 37.618912 # global latitude
Y = 55.751455 # global longitude
LastX = []
LastY = []
Address = 'адрес не указан'
LastAddress = []
Coords = [X, Y] # координаты города
LastCoords = []

# сервис Яндекс.Переводчик
Lang1 = 'авто'    # lang-from
Lang2 = 'английский'    # lang-tobytes
Ttext = ''    # переводимый текст
LastLang1 = []
LastLang2 = []

# сервис Яндекс.Расписание
nameSt = 'Москва'   # текущая станция
region = 'Москва'   # регион поиска
iTr = 0       # тип транспорта
St1 = 'Москва'      # станция отправления
St2 = ''      # станция прибытия
trDate = ''   # интересующая дата
LastSt1 = []
LastSt2 = []
LastTr = []

# сервис Wikipedia
WikiStart = 0
Page = 'Москва'
LastPage = []

# сервис Rate
Valute = 'RUB'  # актуальная валюта
LastValute = []

# Сервис Яндекс поиск объектов
Obj = []   # Подробный список найденных объектов
sObj = []  # Список преобразованный в строку

# Сервис Notes
Notes = {}  # Записи пользователя

# Сервис RSS-каналов
RSS = []
LastRSS = []


# ---------------------------------------------------------
# Внутренние сервисы по работе с функциями
Defs = {}  # Внутренний словарь всех функций
serv = ''  # Название текущего сервиса для добавления описания функции
# ---------------------------------------------------------
# вн.сервис AddDef - Добавление описание функции
def AddDef(name, description, sarg={}, sreturn=None, sclass=''):
    global serv
    if sclass != '':
        serv = sclass
    if serv != '' and sclass == '':
        if serv not in Defs:
            Defs[serv] = {}
        Defs[serv][name] = {}
        Defs[serv][name]['desc'] = description
        Defs[serv][name]['arg'] = sarg
        Defs[serv][name]['return'] = sreturn
    else:
        Defs[name] = {'class': description}
    return Defs


# ------------------- основные функции Fixer -------------------------

# возвращает процент информации о пользователе
def KnowUser():
    rez = 0
    if Name != '': rez += 20
    if Family != '': rez += 10
    if BirthDay != '': rez += 10
    if Phone != '': rez += 10
    if eMail != '': rez += 10
    if Age > 0: rez += 10
    if Type > 0: rez += 10
    if len(Contacts) > 0: rez += 10
    if len(Interests) > 0: rez += 10
    return rez


# Запись лога
def log(process, s=''):
    f = open('log.txt', 'a', encoding='utf-8')
    Process = process
    if s:
        try:
            s = s.replace('\n', ' \ ')
            f.write('%s %s {%s}: %s\n' % (str(datetime.today()), UserID, Process, s))
            print('{%s}: %s' % (Process, s))
        except Exception as e:
            print('Ошибка при попытке записи лога! ' + str(e))
    f.close()


# Запись лога ошибок
def errlog(errprocess, s):
    f = open('log_error.txt', 'a', encoding='utf-8')
    try:
        s = s.replace('\n', ' \ ')
        errProcess = errprocess
        f.write('%s %s {%s}: %s\n' % (str(datetime.today()), UserID, errProcess, s))
        print('Ошибка! {%s}: %s' % (errProcess, s))
        # errMsg = s
    except Exception as e:
        print('Ошибка при попытке записи лога! ' + str(e))
    f.close()


# Запись времени и даты
def time():
    s = str(datetime.today())
    return s[0:s.find('.')]


# Функция проверки существования файла
def Exists(path):
    try:
        os.stat(path)
    except OSError:
        return False
    return True

# Функция записи словаря
def Save(dictionary, name):
    try:
        f = open('DB/' + name + '.json', 'w', encoding='utf-8')
        json.dump(dictionary, f, sort_keys=False, ensure_ascii=False)
        f.close()
        return True
    except Exception as e:
        errlog('Fixer.Save', name + '.json - ' + str(e))
        return False

# Функция загрузки словаря
def Load(name):
    try:
        dictionary = {}
        if Exists('DB/' + name + '.json') == False: return dictionary
        f = open('DB/' + name + '.json', 'r', encoding='utf-8')
        dictionary = json.load(f)
        return dictionary
    except Exception as e:
        errlog('Fixer.Load', name + '.json - ' + str(e))
        return dictionary

# Функция записи словаря в байты
def SaveB(dictionary, name):
    try:
        f = open('DB/' + name + '.db', 'wb')
        pickle.dump(dictionary, f)
        f.close()
        return True
    except Exception as e:
        errlog('Fixer.SaveB', name + '.db - ' + str(e))
        return False

# Функция загрузки словаря из байт
def LoadB(name):
    try:
        dictionary = {}
        if Exists('DB/' + name + '.db') == False: return dictionary
        f = open('DB/' + name + '.db', 'rb')
        dictionary = pickle.load(f)
        f.close()
        return dictionary
    except Exception as e:
        errlog('Fixer.LoadB', name + '.db - ' + str(e))
        return dictionary

# ---------------------------------------------------------
# вн.сервис TimeNow - узнать текущее время пользователя
def TimeNow():
    log('Fixer.TimeNow')
    return datetime.utcnow() + timedelta(hours=TimeZone)

# ---------------------------------------------------------
# вн.сервис GoodTime - определить текущее привествие по времени
def GoodTime():
    log('Fixer.GoodTime')
    tNow = TimeNow()
    print(tNow.hour)
    if tNow.hour < 6:
        return('Доброй ночи')
    if tNow.hour < 13:
        return('Доброе утро')
    if tNow.hour < 19:
        return('Добрый день')
    return('Добрый вечер')

# ---------------------------------------------------------
# вн.сервис Dialog - использование внутреннего диалога
def Dialog(key):
    import random
    if key in dialogs:
        return random.choice(dialogs[key])
    else:
        errlog('Fixer.Dialog', 'не найден ключ: ' + key)
        return key

# ---------------------------------------------------------
# вн.сервис substitution - подстановка строковых переменных
def Subs(text):
    t = 0
    text = text.replace('\\n', '\n')
    while text.find('[', t) >= 0:
        t1 = text.find('[', t)
        t2 = text.find(']', t1)
        s = text[t1:t2+1]; ss = ''
        if s.lower() == '[service]': ss = Service
        if s.lower() == '[thema]': ss = Thema
        if s.lower() == '[userid]': ss = UserID
        if s.lower() == '[chatid]': ss = str(ChatID)
        if s.lower() == '[name]': ss = Name
        if s.lower() == '[family]': ss = Family
        if s.lower() == '[birthday]': ss = BirthDay
        if s.lower() == '[phone]': ss = Phone
        if s.lower() == '[email]': ss = eMail
        if s.lower() == '[age]': ss = str(Age)
        if s.lower() == '[good time]': ss = GoodTime()
        if s.lower() == '[contacts]':
            for i in Contacts:
                ss += i + ': ' + Contacts[i] + '\n'
            ss = ss[:-2]
        if s.lower() == '[interests]':
            for i in Interests:
                ss += i + ', '
            ss = ss[:-2]
        if s.lower() == '[things]':
            for i in Things:
                ss += i + ', '
            ss = ss[:-2]
        if s.lower() == '[location]': ss = str(Y)+','+str(X)
        if s.lower() == '[address]': ss = Address
        if s.lower() == '[valute]': ss = Valute
        if s.lower() == '[home]': ss = Mess
        if s.lower() == '[notes]':
            for i in Notes:
                ss += i + ': ' + Notes[i] + '\n'
            ss = ss[:-2]
        if ss != '': text = text.replace(s, ss)
        t = t1 + 1
    #log('Fixer.Substitution', text)
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
def strfind(text, mfind, poz = 0):
    textU = text.upper()
    for sfind in mfind:
        ilen = len(sfind)
        if poz >= 0: # если ищем по тексту в определённой позиции
            if textU.find(sfind.upper()) == poz:
                return sfind, (text[:poz] + text[poz+ilen:]).strip() # вырезание
        else: # если ищем везде
            if textU.find(sfind.upper()) >= 0:
                while textU.find(sfind.upper()) >= 0:
                    text = text[:poz] + text[poz+ilen:] # вырезание
                    textU = text.upper()
                return sfind, text.strip()
    return '', text # ничего не нашлось


# ---------------------------------------------------------
# вн.сервис servicefind - поиск сервиса и обрезка по найденному (регистронезависимый)
def servicefind(text):
    m = [] # массив сервисов
    for skey in Services:
        m.append('#%s:' % skey)
        if len(Services[skey][9]) > 0: # если есть подсервисы
            for subser in Services[skey][9]:
                m.append('#%s-%s:' % (skey, subser))
    return strfind(text, m) # поиск сервиса


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
                s += '\n['+str(i+1)+'] ' + sitem
    else: s = 'По данному запросу нет результата'
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
                    s += '\n[%i] %s:' % (i+1, row[0])
                    ic = 0
                    for col in nameCol:
                        if col == 0: ic += 1; continue
                        s += '\n%s: %s' % (col, row[ic])
                        ic += 1
                else:  # если одна возвращаемая колонка
                    s += '\n[%i] %s' % (i+1, mresult[i])
            else:  # если задан формат: sformat = 'Номер: %0 - значение: %1 \\%'
                sitem = sformat
                row = mresult[i]
                while sitem.find('%%') >= 0:
                    x = sitem.find('%%')+2
                    r = int(sitem[x:x+2])
                    sitem = sitem.replace('%%'+str(r), str(row[r]))
                while sitem.find('%') >= 0:
                    x = sitem.find('%')+1
                    r = int(sitem[x:x+1])
                    sitem = sitem.replace('%'+str(r), str(row[r]))
                while sitem.find('\\%') >= 0:
                    sitem = sitem.replace('\\%', '%')
                s += '\n['+str(i+1)+'] ' + sitem
    else: s = 'По данному запросу нет результата'
    return s

# ---------------------------------------------------------
# вн.сервис getparams - получение переменных в массив [] из строки переменных для сервиса
def getparams(text, separator='|'):
    global Radius
    if text.find(separator) < 0 and separator != ';':  # нет текущего сепаратора
        if text.find(' - ') > 0:
            separator = ' - '
        else:
            if text.find(',') > 0:
                separator = ','
            else:
                separator = ' '
    if text.find('[R') >= 0:  # Признак радиуса интереса
        poz = text.find('[R')
        end = text.find(']', poz)
        print(text[poz+2, end-1])
        Radius = float(text[poz+2, end-1])
        text = text.replace('[R'+text[poz+2, end-1]+']', '')  # Убираем радуис интереса
    m = text.split(separator)
    x = 0
    for im in m:
        m[x] = im.strip();  # убираем лишние пробелы
        x += 1
    return m

# ---------------------------------------------------------
# вн.сервис Sort для сортировки двухмерных массивов (сортировка по номеру колонки)
def Sort(massive, colnum, reverse = False):
    try:
        massive = sorted(massive, key=lambda st: st[colnum], reverse=reverse)
    except: pass
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
    mRez = []; mIdx = []
    for name in namesRez:
        i = 0
        try:
            i = mNames.index(name)
        except: i = -1
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


AddDef('uniq', 'Получение списка уникальных записей',
       {'seq': 'список записей [list]'},
       'список уникальных записей [list]')

def uniq(seq):
    return list(set(seq))


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
#Names = Load('Names')
log('Fixer.Start', 'Все словари загружены!')

# Создание базы данных
# import DB.CreateDB

# Обновление базы данных (из открытых источников)
# import DB.UpdateDB
