# -*- coding: utf-8 -*-
from datetime import datetime
import json
import pickle
import os

# общие фразы
responses = ['yesno','wait','notice']
# Загрузка всех словарей в конце файла

Response = '' # статус диалога с пользователем
Query = '' # последний запрос пользователя

# уведомление пользователя вкл/выкл
bNotice = True

# Процессорные фиксаторы
bAI = True # Признак включения сервиса ИИ

# текущая версия
Version = 20180323

# общие фиксаторы
Time = []     # фиксация времени
Chat = []     # история чата
UserID = ''   # текущий пользователь
ChatID = 0    # Текущий чат
Name = 'человек'     # имя
Family = 'без фамилии'   # фамилия
BirthDay = 'день рождения не известен' # ДР
Phone = 'телефон не указан'    # номер телефона
eMail = 'e-mail не указан'    # почта
Contacts = {} # Мессенджеры
Interests = []# Список интересов
Things = []   # Список вещей/характеристик пользователя
Age = 0       # 0 - неизвестно
Type = 0      # 0 - неизвестно, 1 - мужчина, 2 - женщина
Thema = ''    # текущая тема
LastThema = []
Mess = '' # текущий мессенджер

Service = '#' # текущий сервис
Context = False
LastService = []


def KnowUser(): # возвращает процент информации о пользователе
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
Page = 'Москва'
LastPage = []

# сервис Rate
Valute = 'RUB' # актуальная валюта
LastValute = []

# Сервис Яндекс поиск объектов
Obj = [] # Подробный список найденных объектов
sObj = [] # Список преобразованный в строку

# Сервис Notes
Notes = {} # Записи пользователя

# Запись лога
def log(s):
    f = open('log.txt', 'a', encoding='utf-8')
    if s:
        try:
            s = s.replace('\n',' \ ')
            f.write(str(datetime.today()) + ' ' + UserID + ': ' + s + '\n')
            print(s)
        except Exception as e:
            print('Ошибка при попытке записи лога! ' + str(e))
    else:
        f.write(str(datetime.today()) + ' ' + UserID + ': Ошибка записи лога!\n')
        print('Ошибка записи лога!')
    f.close()

# Запись лога ошибок
def errlog(s):
    f = open('log_error.txt', 'a', encoding='utf-8')
    if s:
        try:
            s = s.replace('\n',' \ ')
            f.write(str(datetime.today()) + ' ' + UserID + ': ' + s + '\n')
            print(s)
        except Exception as e:
            print('Ошибка при попытке записи лога! ' + str(e))
    else:
        f.write(str(datetime.today()) + ' ' + UserID + ': Ошибка записи лога!\n')
        print('Ошибка записи лога!')
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
        f = open('DB\\' + name + '.json', 'w')
        json.dump(dictionary, f, sort_keys=False, ensure_ascii=False)
        f.close()
        return True
    except Exception as e:
        errlog('Ошибка в Fixer.Save!: ' + name + '.json ' + str(e))
        return False

# Функция загрузки словаря
def Load(name):
    try:
        dictionary = {}
        if Exists('DB\\' + name + '.json') == False: return dictionary
        f = open('DB\\' + name + '.json', 'r')
        dictionary = json.load(f)
        return dictionary
    except Exception as e:
        errlog('Ошибка в Fixer.Load!: '+ name + '.json ' + str(e))
        return dictionary

# Функция записи словаря в байты
def SaveB(dictionary, name):
    try:
        f = open('DB\\' + name + '.db', 'wb')
        pickle.dump(dictionary, f)
        f.close()
        return True
    except Exception as e:
        errlog('Ошибка в Fixer.SaveB!: ' + name + '.db ' + str(e))
        return False

# Функция загрузки словаря из байт
def LoadB(name):
    try:
        dictionary = {}
        if Exists('DB\\' + name + '.db') == False: return dictionary
        f = open('DB\\' + name + '.db', 'rb')
        dictionary = pickle.load(f)
        f.close()
        return dictionary
    except Exception as e:
        errlog('Ошибка в Fixer.LoadB!: '+ name + '.db ' + str(e))
        return dictionary

# ---------------------------------------------------------
# вн.сервис Dialog - использование внутреннего диалога
def Dialog(key):
    import random
    if key in dialogs:
        return random.choice(dialogs[key])
    else:
        errlog('Ошибка в сервисе Fixer.Dialog - не найден ключ:' + key)
        return key		
	
# ---------------------------------------------------------
# вн.сервис substitution - подстановка строковых переменных
def Subs(text):
    t = 0
    text = text.replace('\\n','\n')
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
        if s.lower() == '[home]': ss = Fixer.Mess
        if s.lower() == '[notes]':
            for i in Notes:
                ss += i + ': ' + Notes[i] + '\n'
            ss = ss[:-2]
        if ss != '': text = text.replace(s, ss)
        t = t1 + 1
    log('Внутренний сервис Fixer.Substitution: ' + text)
    return text

# ---------------------------------------------------------
# вн.сервис strcleaner - упрощение строки (убирает все лишние символы)
def strcleaner(text):
    text = text.strip().lower()
    text = text.replace('ё','е')
    text = text.replace('!','')
    text = text.replace('@','')
    text = text.replace('~','')
    text = text.replace('#','')
    text = text.replace('^','')
    text = text.replace('&','')
    text = text.replace('*','')
    text = text.replace('(','')
    text = text.replace(')','')
    text = text.replace('- ',' ')
    text = text.replace('+','')
    text = text.replace('=','')
    text = text.replace('{','')
    text = text.replace('}','')
    text = text.replace('[','')
    text = text.replace(']','')
    text = text.replace(';','')
    text = text.replace(':','')
    text = text.replace('?','')
    text = text.replace('<','')
    text = text.replace('>','')
    text = text.replace(',','')
    text = text.replace('.','')
    text = text.replace('`','')
    text = text.replace('\\','')
    text = text.replace('|','')
    text = text.replace('/','')
    text = text.replace('  ',' ')
    return text

# Загрузка комплиментов
mCompliment = []
wCompliment = []
try:
    f = open('DB/mCompliment.txt')
    for line in f:
        mCompliment.append(line.replace('\n',''))
    f.close()
    f = open('DB/wCompliment.txt')
    for line in f:
        wCompliment.append(line.replace('\n',''))
    f.close()
except Exception as e:
    errlog('Ошибка при загрузке комплиментов: ' + str(e))
	
#Save(Commands,'Commands')
#Save(Word1,'Word1')
#Save(KeyWord,'KeyWord')
#Save(Valutes,'Valutes')
#Save(valutes,'Valutes2')
#Save(dialogs,'dialogs')
#print('Save!')

# Пользовательские настройки сервисов
Settings = Load('DefSettings')

# Загрузка всех полезных словарей
Commands = Load('Commands')
Word1 = Load('Word1')
KeyWord = Load('KeyWord')
Valutes = Load('Valutes')
valutes = Load('Valutes2')
dialogs = Load('dialogs')
NewDialogs = Load('NewDialogs')
Services = Load('Services')
Names = Load('Names')
print('Все словари загружены!')