# -*- coding: utf-8 -*-
from datetime import date
from system.time import good_time

# Токены и ключи
# token_VK = '7a345570057d593f4dfc3407103456d1d9f300fd13b4f1788d61b985c7fe85b054de850d1415c3e421430'
# token_VK = 'fb41067a6e98d95e408171342097fef73b6493fb4ead51647dcd8c154b37da6d27738276ce4d8bda9574b'  # тестовый токен
# token_DiBotik = '57a76bd356e884e3219c209b9372b61536a0f924d96bba1b902ffd9dd3624870134d907288a2fdfda5e0b'
# DiBotik_log = 'dimkray@yandex.ru'
# DiBotik_pass = 'uxes17aUri2322'
TOKEN_TELEGRAM = '5045077460:AAHGMEoY37wm60qYIu1dJixxTBF-wZc2j4k'
AI_KEY = '5c672f996a6443c6ba6a9266264136d0'  # Токен API к Dialogflow
YA_TRANSLATE_KEY = 'trnsl.1.1.20180216T120437Z.9d62e5f60755ca65.7e75ed1535ff4b5872e9ae4e68d31a2c6c2d0737'
YA_RASP_KEY = '9a09a483-7aba-44c6-b520-a0efe58b431f'
YA_OBJ_KEY = '3576f0bf-f840-49c4-8e77-54bee5df8470'
YA_MARKET_KEY = '46ad9e2b-dcc0-4c08-98ec-218d6e4ed354'
GOOGLE_SHORT_KEY = 'AIzaSyDr8e5Wf0qgnMK9roRS25N13Wx_LyDaqKU'
GOOGLE_MAPS_KEY = 'AIzaSyCYUepsxsZxMQBiMe0J21pT9QHJua89R_0'
WEATHER_KEY = 'MsEJc54YAFZeJOumeXpehdfguhJMLK1R'
IATA_KEY = 'f09869c0-33d9-4f10-8fe3-5467b99492f7'

# текущая база данных
DB = 'DB\\bot.db'

# общие фразы
RESPONSES = ['yesno', 'wait', 'notice']

RESPONSE = ''  # статус диалога с пользователем
QUERY = ''  # последний запрос пользователя

# уведомление пользователя вкл/выкл
NOTICE = True

# Процессорные фиксаторы
AI = True  # Признак включения сервиса ИИ

# текущая версия
VERSION = 20230205

# общие фиксаторы
TIME = []  # фиксация времени
CHAT = []  # история чата
USER_ID = 0  # текущий пользователь
CHAT_ID = 0  # Текущий чат
PEER_ID = 0  # Текущее назначение - для беседы, для группы
CHAT_TYPE = 0  # Признак беседы: 0 - не беседа, 1 - беседа, 2 - беседа, где надо ответить
NAME = 'человек'  # имя
FAMILY = 'без фамилии'  # фамилия
BIRTHDAY = 'день рождения не известен'  # ДР
PHONE = 'телефон не указан'  # номер телефона
MAIL = 'e-mail не указан'  # почта
CONTACTS = {}  # Мессенджеры
INTERESTS = []  # Список интересов
THINGS = []  # Список вещей/характеристик пользователя
AGE = 0  # 0 - неизвестно
MAN = 0  # 0 - неизвестно, 1 - мужчина, 2 - женщина
Thema = ''  # текущая тема
LastThema = []  # список последних тем
TIME_ZONE = 3  # часовой пояс пользователя относительно UTF

PROCESS = ''  # текущий процесс
errProcess = ''  # процесс, в котором возникла ошибка
errMsg = ''  # сообщение об ошибке

bNow = False  # признак сейчас
Date = date.today()

SERVICE = '#'  # текущий сервис
CONTEXT = False
LAST_SERVICES = []

RADIUS_INTEREST = 100  # радиус интресера

stxt = ''  # строка для ответа

htext = ''  # гиперссылка

# сервис Локация
X = 37.618912  # global latitude
Y = 55.751455  # global longitude
LastX = []
LastY = []
ADDRESS = 'адрес не указан'
LAST_ADDRESSES = []
COORDINATES = [X, Y]  # координаты города
LAST_COORDINATES = []

# сервис Яндекс.Переводчик
Lang1 = 'авто'  # lang-from
Lang2 = 'английский'  # lang-tobytes
Ttext = ''  # переводимый текст
LastLang1 = []
LastLang2 = []

# сервис Яндекс.Расписание
nameSt = 'Москва'  # текущая станция
region = 'Москва'  # регион поиска
iTr = 0  # тип транспорта
St1 = 'Москва'  # станция отправления
St2 = ''  # станция прибытия
trDate = ''  # интересующая дата
LastSt1 = []
LastSt2 = []
LastTr = []

# сервис Wikipedia
WikiStart = 0
Page = 'Москва'
LastPage = []

# сервис Rate
CURRENCY = 'RUB'  # актуальная валюта
LastValute = []

# Сервис Яндекс поиск объектов
Obj = []  # Подробный список найденных объектов
sObj = []  # Список преобразованный в строку

# Сервис Notes
Notes = {}  # Записи пользователя

# Сервис RSS-каналов
RSS = []
LastRSS = []

WORDS = {
    '[service]': SERVICE,
    '[thema]': Thema,
    '[user_id]': USER_ID,
    '[chat_id]': str(CHAT_ID),
    '[name]':  NAME,
    '[family]': FAMILY,
    '[birthday]': BIRTHDAY,
    '[phone]': PHONE,
    '[e-mail]': MAIL,
    '[age]': str(AGE),
    '[good time]': good_time(TIME_ZONE),
    '[contacts]': str(CONTACTS),
    '[interests]': str(INTERESTS),
    '[things]': str(THINGS),
    '[location]': f'{Y}, {X}',
    '[address]': ADDRESS,
    '[currency]': CURRENCY,
    '[notes]': str(Notes),
}
