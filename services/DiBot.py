"""Сервисы DiBot"""
import config
from fixer import DB, Dialog, COMPLIMENT_MAN, COMPLIMENT_WOMAN, CURRENCIES, CURRENCIES2, DIALOGS_NEW, SERVICES
from system.logging import log, err_log
from system.file import load_byte, save_byte, save, file_strings
from system.string import get_params, str_cleaner, list_format, dict_format, list_str, str_operand, str_put
from system.function import FUNCTIONS

import apiai
import json
import random
from datetime import datetime, timedelta

from services.Fun import Fun
from services.Yandex import Ya
from services.Google import Google
from services.Wikipedia import Wiki
from services.User import User
from services.Rates import Rate
from services.Weather import Weather
from services.Geo import Geo
from services.House import Booking
from services.RSS import RSS
from services.IATA import IATA
from services.StrMorph import String, Word
from services.Kinopoisk import Movies, Persons
from Chats.Chats import Chat
from Tests.Testing import Tests
from Tests.Autotest import AutoTest
import Bot


# Работа с сервисами
# ---------------------------------------------------------
# сервис AI : #ai: всякий бред
def ai(text: str) -> str:
    """Сервис искусственного интеллекта: #ai: всякий бред [text]"""
    # log('Запуск AI')
    try:
        request = apiai.ApiAI(config.AI_KEY).text_request()
        request.lang = 'ru'  # На каком языке будет послан запрос
        request.session_id = str(config.USER_ID)  # 'BatlabAIBot' # ID Сессии диалога (нужно, чтобы потом учить бота)
        # Запуск сервиса Google Dialogflow для обработки пользовательского запроса (ИИ)
        request.query = text  # Посылаем запрос к ИИ с сообщением от юзера
        response_json = json.loads(request.getresponse().read().decode('utf-8'))
        return response_json['result']['fulfillment']['speech']  # Разбираем JSON и вытаскиваем ответ
    except Exception as e:
        err_log(e)
        return '#bug: ' + str(e)


# ---------------------------------------------------------
# сервис Task : #task: type | time | times | Notice/Service
def task(text: str) -> str:
    """Сервис заданий [text]: #task: type | time | times | Notice/Service"""
    # log(text)
    import Notification
    from datetime import date, datetime, timedelta
    time_format = '%Y-%m-%d %H:%M:%S'
    Notification.Tasks = load_byte('Tasks')
    params = get_params(text)
    params[0] = params[0].lower()
    if len(params) < 2: params.append(datetime.today().strftime('%H:%M:%S'))  # params[1]
    if len(params) < 3: params.append('2')  # params[2]
    if len(params) < 4: params.append('NULL')  # params[3]
    delta = timedelta(days=1)  # дельта по умолчанию - сутки
    if params[0] == 'alarm':
        mess = 'Будильник успешно установлен!'
    elif params[0] == 'alarmlater':
        mess = 'Отложенное уведомление успешно установлено!'
    elif params[0] == 'rss':
        mess = 'Подписка на RSS-канал успешно активирована!'
        delta = timedelta(minutes=1)
    elif params[0] == 'del':
        save_byte({}, 'Tasks')
        mess = 'Все задания успешно удалены!'
        return mess
    elif params[0] == 'all':  # показать все задания
        mess = 'Список заданий:'
        for i, itask in enumerate(Notification.Tasks):
            mess += f'\n[%i] %s' % (i, str(itask))
        if not Notification.Tasks: mess += '\n( список пуст )'
        else: mess += '\n\nМожно удалить все задания командой "task-del: all"'
        return mess
    else:
        mess = 'Неизвестная задача "%s"!' % params[0]
        return mess
    task_attrs = []  # наполняем массив
    task_message = params[0] + '-' + str(random.randint(100000, 999999))  # key
    skey = str(config.CHAT_ID) + ':' + task_message
    etime = datetime.strptime(str(date.today()) + ' ' + params[1], time_format) + timedelta(hours=config.TIME_ZONE)
    if etime < datetime.today():
        etime = etime + timedelta(days=1)
    mess += '\nНазвание: ' + task_message + '\nСообщение\\сервис: ' + params[3] + '\nВремя срабатывания: ' + str(
        etime + timedelta(hours=config.TIME_ZONE)) + '\nКоличество повторений: ' + params[2]
    task_attrs.append(config.NOTICE)    # 0 - вкл/выкл уведомление пользователя
    task_attrs.append(etime)            # 1 - дата-время срабатывания задачи
    task_attrs.append(delta)            # 2 - дельта следующего срабатывания / по умолчанию 1 день для alarm
    task_attrs.append(int(params[2]))   # 3 - количество раз срабатывания (при 0/-1 бесконечный цикл)
    service_code = params[3]
    if params[3].upper() == 'NULL':
        params[3] = task_message + '\nТы просил меня отправить сообщение в ' + str(etime)
        service_code = ''
    task_attrs.append(params[3])  # 4 - сообщение при уведомлении
    task_attrs.append(service_code)  # 5 - запускаемый сервис
    Notification.Tasks[skey] = task_attrs
    save_byte(Notification.Tasks, 'Tasks')  # Сохранение задач
    log('Processor.Task', mess)
    return mess


def answer(text: str) -> str:
    """Сервис Answer - #answer: ответ [text]"""
    import Bot
    # log('Answer')
    text_send = 'Не понял ответа'
    if text == 'yes':
        Bot.SendMessage('Отлично!')
        # if Fixer.Thema == 'Знакомство':
        #     Fixer.Service == 'acquaintance'
        #     tsend = User.Acquaintance()
    elif text == 'no':
        text_send = 'Хорошо. Значит в другой раз.\nГотов помочь, чем смогу!'
        config.THEME == ''
        config.SERVICE == ''
    log('Answer', text_send)
    return text_send


# ---------------------------------------------------------
# сервис Name - #name: имя
def name(text: str) -> str:
    """сервис Name - #name: имя [text]"""
    text = text.strip()
    # log('Name')
    find_name = DB.read_row('names', 'nameU', text.upper().replace('Ё', 'Е'))
    if len(find_name) > 0:  # если найдено имя
        send = f"{text}: {'мужское имя' if find_name[1] else 'женское имя'}\nколичество не менее: {find_name[2]}\n" \
            f"страна распространения: {find_name[3]}"
    else:  # если не найдено имя
        send = f'Не удалось проанализировать имя {text} :('
    log('Name', send)
    config.SERVICE == ''
    return send


# ---------------------------------------------------------
# сервис User - #user-<param>: значение
def user(param: str, text: str) -> str:
    """Сервис User - #user-[param]: значение [text]"""
    # log('User')
    text_send = User.Info(param, text)
    log('User', text_send)
    config.SERVICE == ''
    return text_send


# ---------------------------------------------------------
# сервис Acquaintance - #acquaintance:
def acquaintance() -> str:
    """сервис Acquaintance - #acquaintance:"""
    # log('Acquaintance')
    # text_send = User.Acquaintance()
    # log('Acquaintance', text_send)
    text_send = 'Я бы с тобой познакомился... Но я бот ('
    return text_send


# ---------------------------------------------------------
# сервиса Fixer (информация) #fixer: <Параметр>
def fixer(text: str) -> str:
    """сервиса Fixer (информация) #fixer: Параметр [text]"""
    # log('Fixer')
    param = text.split(' ')[0].upper()
    config.SERVICE == ''
    if param == 'XY': return f'{config.Y}, {config.X}'
    elif param == 'NAME': return config.NAME
    elif param == 'AGE': return str(config.AGE)
    elif param == 'FIXER': return str(Chat.Save())
    elif param == 'ADDRESS': return config.ADDRESS
    elif param == 'LASTLANG1': return str(config.LastLang1)
    elif param == 'LASTLANG2': return str(config.LastLang2)
    elif param == 'LASTSERVICE': return str(config.LAST_SERVICES)
    elif param == 'LASTST1': return str(config.LastSt1)
    elif param == 'LASTST2': return str(config.LastSt2)
    else: config.ERR_PROCESS = config.PROCESS
    return '#err: неизвестный параметр: ' + param


# ---------------------------------------------------------
# Обработка результатов сервиса Яндекс.Расписание
def FormRasp(text: str) -> str:
    """Обработка результатов сервиса Яндекс.Расписание"""
    # log('FormRasp')
    send = text
    if text[0] == '%':  # Рейсы найдены!
        find_space = text.find(' ', 1)
        num = int(text[1:find_space])  # количество рейсов
        find_symbol = text.find('#', 1)
        config.HYPERTEXT = text[find_symbol + 1:]
        routes = text[find_space + 1:find_symbol - 2].strip().split('\n')
        if num == 0:
            send = 'Печалька. Не нашёл ни одного прямого рейса :(\n' \
                   'Может я не правильно тебя понял? Попробуй по другому сделать запрос!'
        elif 0 < num < 11:
            send = f'Нашёл {num} рейс(ов)!\n'
        elif 10 < num < 300:
            send = f'Нашёл {num} рейс(ов). Покажу первые 10.\n'
        elif 300 < num < 1000:
            send = f'Нашёл дохрена рейсов! {num}! Покажу первые 10.\n'
            send += text[num + 1:find_symbol]
        else:
            send = f'Нашёл какое-то невероятное число рейсов! {num} !\n' \
                   f'Может я где-то ошибся? Лучше зайди по ссылке, посмотри всё ли правильно.\n'
        if num > 0:
            for x, rout in enumerate(routes):
                send += routes[x] + '\n'
                if x > 11: break
        if len(routes) - 1 != num:  # части рейсов нет
            send += f'\n{num - len(routes) - 1} рейс/рейсов на сегодня уже нет.'
        if not len(routes) - 1 and num > 0:  # если уже рейсов нет
            send = 'На сегодня уже нет ни одного прямого рейса :('
    return send


# ---------------------------------------------------------
# сервис Booking : #booking: $geo-city | $checkin | $checkout | $people | $order | $dormitory
def booking(text: str, wait=False) -> str:
    """сервис Booking : #booking: $geo-city | $checkin | $checkout | $people | $order | $dormitory"""
    # log('Booking.com')
    from datetime import date, timedelta
    if wait: Bot.SendMessage('Секундочку! Ищу подходящее жильё в сервисе Booking.com...')
    params = get_params(text)
    dormitory = True
    if len(params) < 2: params.append('Now')
    if len(params) < 3: params.append('Next')
    if len(params) < 4: params.append('1')
    if len(params) < 5: params.append('price')
    if len(params) < 6: params.append('1')
    if params[1].upper() == 'NOW': date.today().isoformat()
    if params[2].upper() == 'NEXT': str(date.strpdate(params[1], config.DATE_FORMAT) + 1)
    if params[5] != '1': dormitory = False

    find_list = Booking.List(params[0], params[1], params[2], people=float(params[3]), order=params[4], dorm=dormitory)
    if find_list[0] == '#': return find_list
    send = 'Найдены следующие варианты (не больше 7):'
    x = 0
    for x, item in enumerate(find_list):
        if x > 7: continue  # только 7 вариантов
        send += '\n{x}. {item}'
    log('Booking.com', send)
    return send


# ---------------------------------------------------------
# сервис Яндекс.Расписание
def timetable(text: str, wait=False) -> str:
    """Сервис Яндекс.Расписание"""
    # log('TimeTable')
    if wait: Bot.SendMessage('Секундочку! Ищу расписание транспорта в сервисе Яндекс.Расписания...')
    send = Ya.FindRasp(text)
    log('Ya.Rasp', send)
    send = FormRasp(send)
    log('FormRasp', send)
    if send[0] != '#':
        config.LastSt1.append(config.St1)
        config.LastSt2.append(config.St2)
        config.LastTr.append(config.iTr)
    return send


# ---------------------------------------------------------
# сервис Яндекс.Переводчик
def translate(text: str) -> str:
    """Сервис Яндекс.Переводчик"""
    # log('Translate')
    if config.CONTEXT:
        lang1 = config.Lang1
        lang2 = config.Lang2
    else:
        n1 = text.find(' - ')
        n2 = text.find(': ')
        if n1 > n2 or n1 < 1:
            lang1 = 'авто'
            lang2 = text[:n2]
        else:
            lang1 = text[:n1]
            lang2 = text[n1 + 3:n2]
    if lang1 == lang2: lang2 = 'английский'
    if lang1 == '$lang-from':
        lang1 = config.Lang1
    else:
        config.Lang1 = lang1
    if lang2 == '$lang-to':
        lang2 = config.Lang2
    else:
        config.Lang2 = lang2
    ttext = text[n2 + 2:]
    log('Translate', ttext + ' | ' + lang1 + ' | ' + lang2)
    send = Ya.Translate(ttext, lang1, lang2)
    log('Ya.Translate', send)
    if send[0] != '#':
        config.LastLang1.append(config.Lang1)
        config.LastLang2.append(config.Lang2)
    return send


# ---------------------------------------------------------
# сервис Яндекс поиск объектов : #object: objName | Radius
def ya_object(text: str) -> str:
    """Сервис Яндекс поиск объектов : #object: objName | Radius"""
    # log('Ya.Object', text)
    param = get_params(text)
    ttext = param[0]
    rad = param[1] if len(param) else config.RADIUS_INTEREST
    try: radius = int(rad)
    except:
        if rad == 'near': radius = 2
        else: radius = 100
    send = Ya.Objects(ttext, Xloc=config.X, Yloc=config.Y, radius=radius)
    log('Ya.Object', send)
    return send


# ---------------------------------------------------------
# сервис Яндекс.Координаты : #coordinates: $geo-city
def coordinates(text: str) -> str:
    """Сервис Яндекс.Координаты : #coordinates: $geo-city"""
    # log('Ya.Координаты')
    if not text.strip(): text = 'LOCATION'
    send = Ya.Coordinates(text)
    log('Ya.Координаты', send)
    return send


# ---------------------------------------------------------
# сервис Яндекс.Каталог : #site: type(info/find) - $site/String
def site(text: str) -> str:
    """Сервис Яндекс.Каталог : #site: type(info/find) - $site/String"""
    # log('Ya.Каталог')
    params = get_params(text)
    if len(params) < 2:
        config.ERR_PROCESS = config.PROCESS
        return '#err: Нет второго параметра'
    if params[0].lower() == 'info': send = Ya.Catalog(params[1])
    elif params[0].lower() == 'find': send = Ya.FindCatalog(params[1])
    else:
        config.ERR_PROCESS = config.PROCESS
        return f'#err: Параметр "{params[0]}" не поддерживается!'
    log('Ya.Каталог', send)
    return send


# ---------------------------------------------------------
# сервис wiki : #wiki: query
def wiki(text: str, wait: bool = False) -> str:
    """Сервис wiki : #wiki: query"""
    # log('Wikipedia')
    if wait: Bot.SendMessage('Секундочку! Ищу информацию в Википедии...')
    pages = Wiki.SearchPage(text.strip())
    if not len(pages): return 'Я поискал информацию в Википедии, но ничего не нашёл. Можешь уточнить запрос?'
    config.HYPERTEXT = f'"https://ru.wikipedia.org/wiki/{pages[0]}"'
    log('Wikipedia', config.HYPERTEXT)
    return Wiki.MiniContent(pages[0])


# ---------------------------------------------------------
# сервис wiki-more
def wiki_more(text: str) -> str:
    """Cервис wiki-more"""
    log('Wikipedia.More', text.strip())
    return Wiki.More(config.PAGE)


# ---------------------------------------------------------
# сервис geowiki : #geowiki: [radius]
def geo_wiki(text: str, wait: bool = False) -> str:
    """сервис geowiki : #geowiki: [radius]"""
    # log('WikipediaGeo')
    if text == '': rad = config.RADIUS_INTEREST
    else:
        try:
            rad = float(text.split(' ')[0])
        except:
            err_log('WikipediaGeo', 'Ошибка в определении радиуса:', rad)
            rad = 100
    if wait: Bot.SendMessage('Секундочку! Ищу ближайшие достопримечательности по Википедии...')
    pages = Wiki.GeoSearch(config.X, config.Y, resnom=10, rad=rad)
    if not len(pages) or pages[0] == '#': return 'Я поискал достопримечательности в Википедии, но ничего не нашёл.\n' \
                                                  'Может стоит увеличить радиус поиска?'
    send = 'Нашёл следующие достопримечательности:\n'
    for page in pages:
        send += page + '\n'
    Bot.SendMessage(send)
    config.HYPERTEXT = f'"https://ru.wikipedia.org/wiki/{pages[0]}"'
    log('WikipediaGeo', config.HYPERTEXT)
    return Wiki.GeoFirstMe(rad)


# ---------------------------------------------------------
# сервис geowiki1 : #geowiki1: [radius]
def geowiki1(text: str, wait: bool = False) -> str:
    """Сервис geowiki1 : #geowiki1: [radius]"""
    # log('WikipediaGeo1')
    if text == '': rad = config.RADIUS_INTEREST
    else:
        try:
            rad = float(text.split(' ')[0])
        except:
            err_log('WikipediaGeo1', 'Ошибка в определении радиуса:', rad)
            rad = 100
    if wait: Bot.SendMessage('Секундочку! Ищу ближайшую достопримечательность по Википедии...')
    response = Wiki.GeoFirstMe(rad)
    if response[0] == '#': return f'В радиусе {rad} метров не нашёл ни одной достопримечательности :('
    pages = Wiki.GeoSearch(config.X, config.Y, resnom=10, rad=rad)
    config.HYPERTEXT = f'"https://ru.wikipedia.org/wiki/{pages[0]}"'
    log('WikipediaGeo1', config.HYPERTEXT)
    return response


# ---------------------------------------------------------
# сервис google.Define : #define: word
def define(text: str) -> str:
    """Сервис google.Define : #define: word"""
    # log('Google.Define')
    send = Google.Define(text.strip())
    log('Google.Define', send)
    return send


# ---------------------------------------------------------
# сервис google.Calc : #calc: formula
def calc(text: str) -> str:
    """Сервис google.Calc : #calc: formula"""
    # log('Google.Calc')
    send = Google.Calc(text.strip())
    log('Google.Calc', send)
    return send


# ---------------------------------------------------------
# сервис google : #google: query / [$responce]
def google(text: str, map: bool = False) -> str:
    """Сервис google : #google: query / [$responce]"""
    # log('Google.Search')
    if text == '$responce': text = config.QUERY
    print(text)  # !!!
    send = Google.Search(text.strip(), bmap=map)
    log('Google.Search', send)
    return send


# ---------------------------------------------------------
# сервис getcoords
def get_coords(geocity: str) -> str:
    """Сервис getcoords"""
    if geocity.strip() == '': geocity = 'LOCATION'
    if geocity.strip().upper() == 'LOCATION':
        config.COORDINATES[0] = config.X
        config.COORDINATES[1] = config.Y
        send = 'LOCATION'
    else:
        send = Ya.Coordinates(geocity)
    print(send)  # !!!
    return send


# ---------------------------------------------------------
# сервис weather : #weather: type:full/short/day/cloud/wind/sun/night/riseset/temp | $geo-city | $date
def weather(text: str) -> str:
    """Cервис weather : #weather: type:full/short/day/cloud/wind/sun/night/riseset/temp | $geo-city | $date"""
    # log('Weather')
    params = get_params(text)
    # print(params)
    if len(params) < 2: params.append('Location')
    if len(params) < 3: params.append(str(config.DATE))
    # print('{%s}' % params[1])
    mess = get_coords(params[1])
    # print('{%s}' % s)
    if mess[0] == '#': return 'Не удалось распознать город или найти его координаты :( - ' + mess
    m = Weather.Forecast(config.COORDINATES[0], config.COORDINATES[1], params[2])
    print(m)  # !!!
    if m[0] == '#': return m
    if params[0] == 'full':  # полный прогноз погоды
        send = m[17] + '\n\n' + m[18] + '\n\n' + m[19]
    elif params[0] == 'day':  # полный прогноз погоды (день)
        send = m[18]
    elif params[0] == 'night':  # полный прогноз погоды (ночь)
        send = m[19]
    elif params[0] == 'short':  # короткий прогноз погоды
        mess = 'Температура от ' + m[10] + ' до ' + m[2] + '\n'
        mess += 'Днём: ' + m[3] + '\n'
        mess += 'Ночью: ' + m[11]
        send = mess
    elif params[0] == 'temp':  # температура
        send = 'Температура от ' + m[10] + ' до ' + m[2] + '\n'
    elif params[0] == 'riseset':  # восход и заход солнца
        send = 'Рассвет: ' + m[0] + '\n'
        send += 'Закат: ' + m[1]
    elif params[0] == 'cloud':  # осадки, облачность
        mess = 'Днём: ' + m[3]
        mess += ', вероятность осадков ' + m[4] + '\n'
        mess += 'Объём осадков: ' + m[5] + '\n'
        mess += 'Продолжительность осадков: ' + m[6] + '\n'
        mess += 'Облачность: ' + m[7] + '\n'
        mess += '\nНочью: ' + m[11]
        mess += ', вероятность осадков ' + m[12] + '\n'
        mess += 'Объём осадков: ' + m[13] + '\n'
        mess += 'Продолжительность осадков: ' + m[14] + '\n'
        mess += 'Облачность: ' + m[15]
        send = mess
    elif params[0] == 'wind':  # ветер
        mess = 'Днём: ' + m[8]
        mess = '\nНочью: ' + m[16]
        send = mess
    elif params[0] == 'sun':  # солнце
        send = 'Днём: ' + m[3] + ', солнечные часы - ' + m[9]
    else:  # необрабатываемый случай
        send = '#problem: {' + params[0] + '}'
    log('Weather', send)
    return send


# ---------------------------------------------------------
# сервис timezone : #timezone: [$geo-city]
def timezone(text: str) -> str:
    """Сервис timezone : #timezone: [$geo-city]"""
    # log('TimeZone')
    # if text.strip() == '': text = 'Location' - уже есть в getcoords
    send = get_coords(text)
    if send[0] == '#': return 'Не удалось распознать город или найти его координаты :( - ' + send
    result = Weather.GetLocation(config.COORDINATES[0], config.COORDINATES[1])
    if result[0][0] == '#':
        # попытка узнать часовой пояс из Geo
        send = Geo.GetTimezone(config.COORDINATES[0], config.COORDINATES[1])
        return send
    # ss = 'Часовой пояс: '
    send = ''
    if float(result[5]) > 0: send = '+'
    log('TimeZone', send)
    return send + result[5]


# ---------------------------------------------------------
# сервис population : #population: [$geo-city]
def population(text: str) -> str:
    """Сервис население : #population: [$geo-city]"""
    # log('Population')
    send = get_coords(text)
    if send[0] == '#': return 'Не удалось распознать город или найти его координаты :( - ' + send
    result = Weather.GetLocation(config.COORDINATES[0], config.COORDINATES[1])
    if result[0][0] == '#': return result[0]
    send = f'Население пункта {result[2]} [{result[1]}] {result[3]} ({result[4]}) : {result[7]} чел.'
    log('Population', send)
    return send


# ---------------------------------------------------------
# сервис elevation : #elevation: [$geo-city]
def elevation(text: str) -> str:
    """Сервис высотная отметка : #elevation: [$geo-city]"""
    # log('Elevation')
    send = get_coords(text)
    if send[0] == '#': return 'Не удалось распознать город или найти его координаты :( - ' + send
    result = Weather.GetLocation(config.COORDINATES[0], config.COORDINATES[1])
    print(result)  # !!!
    if result[0][0] == '#': return result[0]
    send = f'Высотная отметка {result[2]} [{result[1]}] {result[3]} ({result[4]}) : {result[6]} метров над уровнем моря'
    log('Elevation', send)
    return send


# ---------------------------------------------------------
# сервис geodistance : #geodistance: $geo-city1 - [$geo-city2]
def geo_distance(text: str) -> str:
    """Сервис географическая дистанция : #geodistance: $geo-city1 - [$geo-city2]"""
    # log('GeoDistance')
    params = get_params(text)
    if len(params) < 2: params.append('Location')
    send = get_coords(params[0])
    if send[0] == '#': return 'Не удалось распознать первый город или найти его координаты :( - ' + send
    x = config.COORDINATES[0]
    y = config.COORDINATES[1]
    send = get_coords(params[1])
    if send[0] == '#': return 'Не удалось распознать второй город или найти его координаты :( - ' + send
    send = str(round(Geo.Distance(y, x, config.COORDINATES[1], config.COORDINATES[0]))) + ' км по прямой линии'
    log('GeoDistance', send)
    return send


# ---------------------------------------------------------
# сервис compliment : #compliment:
def compliment() -> str:
    """Сервис комплимент : #compliment:"""
    # log('Comliment')
    if config.MAN: send = random.choice(COMPLIMENT_MAN[1])
    else: send = random.choice(COMPLIMENT_WOMAN[1])
    log('Comliment', send)
    return send


# ---------------------------------------------------------
# сервис anecdote : #anecdote:
def anecdote() -> str:
    """сервис анекдот : #anecdote:"""
    # log('Fun.Anecdote')
    send = Fun.Anecdote()
    log('Fun.Anecdote', send)
    return send


# ---------------------------------------------------------
# сервис rate
def rate(text: str) -> str:
    """Сервис rate"""
    # log('Rates.Rate')
    params = get_params(text)
    if params[0] == 'ALL':  # если нужны курсы всех валют
        send = Dialog('rate')
        for val in CURRENCIES:
            send += '\n' + CURRENCIES[val] + ' : ' + Rate.RateRubValue(val, params[1], float(params[2])) + ' ' + \
                     CURRENCIES2[params[1]]
    else:
        send = Rate.RateRubValue(params[0], params[1], float(params[2])) + ' ' + CURRENCIES2[params[1]]
        if send[0] != '#': config.LastValute.append(params[0])
    log('Rates.Rate', send)
    return send


# ---------------------------------------------------------
# сервис setrate
def set_rate(text: str) -> str:
    """сервис setrate"""
    # log('SetRate', text)
    if not Rate.isValute(text): return 'Не знаю такой валюты: ' + text
    config.CURRENCY = text
    return 'Хорошо! Установлена валюта по-умолчанию: ' + CURRENCIES[text]


# ---------------------------------------------------------
# сервис note - #notes: ALL/<Имя раздела> | Текст
def note(text: str) -> str:
    """Сервис note - #notes: ALL/<Имя раздела> | Текст"""
    # log('Note', text)
    params = get_params(text)
    config.Notes[params[0].upper()] = params[1]
    return Dialog('note_section') + params[0].upper()


# ---------------------------------------------------------
# сервис notes - #notes: [ALL/<Имя раздела>]
def notes(text: str) -> str:
    """сервис notes - #notes: [ALL/<Имя раздела>]"""
    text = text.strip()
    # log('Notes', text)
    if text.upper() == 'ALL' or text == '':
        send = Dialog('notes_all')
        for snote in config.Notes.values():
            send += '\n' + snote
    else:
        send = Dialog('notes_section') + text.upper()
        for snote in config.Notes[text.upper()]:
            send += '\n' + snote
    return send


# ---------------------------------------------------------
# сервис setlocation
def set_location(text: str) -> str:
    """сервис setlocation"""
    # log('SetLocation')
    from geolocation.main import GoogleMaps
    try:
        params = get_params(text, separator=',')
        config.LastX.append(config.X)
        config.LastY.append(config.Y)
        config.Y = params[0]
        config.X = params[1]
        mes = f'Хорошо! Установлены координаты: {config.Y}, {config.X}.\n'
        # Сервис Google.Geocoding
        my_location = GoogleMaps(api_key=config.GOOGLE_MAPS_KEY).search(lat=config.Y, lng=config.X).first()
        mes += my_location.formatted_address  # + '\n'
        config.ADDRESS = my_location.formatted_address
        config.LAST_ADDRESSES.append(config.ADDRESS)
        return mes
    except Exception as e:
        err_log('SetLocation', str(e))
        return '#bug: ' + str(e)


# ---------------------------------------------------------
# сервис correction
def correction(text: str) -> str:
    """сервис correction"""
    log('Correction', text)
    DIALOGS_NEW[str_cleaner(config.QUERY)] = get_params(text, ';')
    save(DIALOGS_NEW, 'NewDialogs')
    send = '\nНа запрос: ' + str_cleaner(config.QUERY)
    for i in get_params(text, ';'):
        send += '\nВариант ответа: ' + i
    Bot.SendAuthor('Уведомление от пользователя ' + str(config.USER_ID) + send)
    send = Dialog('correction') + send
    config.AI = True
    config.SERVICE = 'ai'
    config.CONTEXT = False
    return send


# ---------------------------------------------------------
# сервис date / time / datetime : location - type
def date_time(location: str, time_type: bool = 'datetime') -> str:
    """сервис date / time / datetime : location - type"""
    log(f'DateTime: {location} | {time_type}')
    config.TimeZone = float(timezone(location))
    now = datetime.utcnow() + timedelta(hours=config.TIME_ZONE)
    if time_type == 'time': return now.strftime(config.TIME_FORMAT)
    elif time_type == 'date': return now.strftime(config.DATE_FORMAT)
    else: return now.strftime(config.DATE_TIME_FORMAT)


# ---------------------------------------------------------
# сервис logging / logerr : число последних записей
def logging(count: str, etype: str = 'none') -> str:
    """сервис logging / logerr : число последних записей"""
    # log('log')
    try:
        if etype == 'err': file = 'log_error.txt'
        else: file = 'log.txt'
        log_strings = file_strings(file)
        logs = len(log_strings)
        try: number = int(count)
        except: number = 10
        if number < 1: number = 1
        if number > 100: number = 100
        if logs < number: start = 0
        else: start = logs - number
        send = ''
        for i in range(start, logs):
            send += '[%i] %s' % (i, log_strings[i])
        return send
    except Exception as e:
        err_log('log', 'Ошибка при загрузке логов: ' + str(e))


# ---------------------------------------------------------
# сервис buglog : #buglog: numberStart | numberEnd
def bug_log(text: str) -> str:
    """сервис buglog : #buglog: numberStart | numberEnd"""
    # log('buglog')
    params = get_params(text)
    if len(params) < 2: params.append(params[0])
    bugs = DB.sql('SELECT * FROM bugs WHERE id >= %s AND id <= %s' % (params[0], params[1]))
    send = ''
    if len(bugs) > 0:
        for item in bugs:
            if item[1] == 1: send += '\nBUG'
            elif item[1] == 2: send += '\nPORBLEM'
            else: send += '\nANOTHER'
            send += f'[{item[0]}]: {item[5]}\nQuery: {item[2]}\nProcess: {item[3]}\nResponce: {item[4]}'
    else:  # если нет результата
        send += f'Баги №№ {params[0]} - {params[1]} не найдены!'
    return send


# ---------------------------------------------------------
# сервис RSS : #rss: rssurl | numberpost(3)
def rss(text: str) -> str:
    """сервис RSS : #rss: rssurl | numberpost(3)"""
    # log('RSS')
    params = get_params(text)
    params[0] = params[0].lower()  # форматирование строки
    if len(params) < 2: params.append('3')
    titles = RSS.GetTitles(params[0])
    if titles['status'] == 'ok':
        send = f"{titles['title']}\n{titles['subtitle']}\nЯзык публикации: {titles['lang']}\n" \
               f"Автор: {titles['author']}\nСайт: {titles['link']}"
        posts = RSS.GetPosts(params[0])
        for i in range(0, int(params[1])):
            send += f"\n\n[{posts[i]['title']}]\n{posts[i]['description']}\n({posts[i]['date']})\n{posts[i]['link']}"
        Bot.SendMessage(send)
        brss = True
        for rss in config.RSS:
            if params[0] == rss['rss']: brss = False
        if brss:  # записываем rss-канал
            rss_dict = {'rss': params[0], 'title': titles['title'], 'posts': []}
            for post in posts:
                post_dict = {'len': len(post['description']), 'date': post['date']}
                rss_dict['posts'].append(post_dict)
            config.RSS.append(rss_dict)
            config.LastRSS.append(params[0])
            send = 'RSS-канал "%s" успешно подключен!\n' \
                   'Новости канала будут приходить по мере их поступления.' % titles['title']
            now = (datetime.today() + timedelta(minutes=1)).strftime(config.DATE_FORMAT)  # форматирование времени
            task(f'RSS | {now} | 0 | #rss-news: {params[0]}')
        else: send = 'RSS-канал "%s" был сохранён ранее.' % titles['title']
        return send
    else: return 'указанная ссылка не является RSS-каналом.'


# ---------------------------------------------------------
# сервис RSS-news : #rss-news: rssurl
def rss_news(url: str) -> str:
    """сервис RSS-news : #rss-news: rssurl"""
    # log('RSS-News')
    url = url.lower()  # форматирование строки
    send = '#null'  # 'Не удалось найти rss-канал в подписке: ' + url
    for num, rss in enumerate(config.RSS):
        if url == rss['rss']:
            old_posts = rss['posts']  # поиск старых постов
            send = 'Новости rss-канала "%s":' % rss['title']
            posts = RSS.GetNewPosts(url, old_posts)
            if len(posts) > 0:
                for post in posts:
                    send += f"\n\n[{post['title']}]\n{post['description']}\n({post['date']})\n{post['link']}"
                    post_dict = {'len': len(post['description']), 'date': post['date']}  # запись новостей
                    config.RSS[num]['posts'].append(post_dict)  # добавление в Fixer
                # print(Fixer.RSS)
                Chat.Save()
            else: send = '#null'
            break
    return send


# ---------------------------------------------------------
# сервис RSS-all : #rss-all:
def rss_all() -> str:
    """сервис RSS-all : #rss-all:"""
    # log('RSS-all')
    send = 'Список всех подключённых rss-каналов:'
    for num, rss in enumerate(config.RSS):
        send += '\n[%i] %s - %s' % (num, rss['rss'], rss['title'])
    if not len(config.RSS): send += '\n( список пуст )'
    else: send += '\n\nМожно удалить лишние каналы командой "rss-del: №"'
    return send


# ---------------------------------------------------------
# сервис RSS-del : #rss-del: №
def rss_del(text: str) -> str:
    """сервис RSS-del : #rss-del: №"""
    # log('RSS-del')
    num = int(text)
    del config.RSS[num]
    return 'Удаление канала "%s" прошло успешно!' % config.RSS[num]['title']


# ---------------------------------------------------------
# сервис IATA : #IATA: №
def iata(text: str, stype: str = 'code') -> str:
    """сервис IATA : #IATA: №"""
    # log('IATA')
    colsReturn = ['code', 'name', 'cityName', 'timeZone', 'country', 'lat', 'lon',
                  'runwayLength', 'runwayElevation', 'phone', 'email', 'website']
    sfrm = '%0 - %1, г. %2, %4 (%3)\nДлина взлётной полосы: %7, высотная отметка: %8\nТелефон: %9, e-mail: %%10\nURL: %%11'
    send = ''
    if stype == 'code':
        m1 = IATA.Airport(code=text)
        m2 = IATA.City(code=text)
        if len(m2) > 0:
            send += list_format(m2, sformat=sfrm, sobj='аэропортов в городах') + '\n'
        send += '\n' + list_format(m1, sformat=sfrm, sobj='отдельных аэропортов')
    elif stype == 'air':
        m = IATA.Airport(name=text)
        send = list_format(m, sformat=sfrm, sobj='аэропортов')
    elif stype == 'city':
        m = IATA.City(name=text)
        send = list_format(m, sformat=sfrm, sobj='аэропортов в городах')
    elif stype == 'code3':
        if Word.Type(text) == 50:
            m = IATA.Country(code=text)  # если латиница
        else:
            m = IATA.Country(name=text)
        send = list_format(m, sformat='код: %0, код3: %1, iso: %2\nназвание: %3', sobj='стран')
    return send


# ---------------------------------------------------------
# сервис skill : #skill:
def skill() -> str:
    """сервис skill : #skill:"""
    # log('skill')
    services = [key for key in SERVICES]  # массив сервисов
    service = SERVICES[random.choice(services)]
    print(service)  # !!!
    send = f'Сервис "{service[1]}" - {service[4]}\nАвтор: {service[2]}\n'
    send += 'Примеры: '
    send += list_str([f"{example}" for example in SERVICES[service][7]])
    return send


# ---------------------------------------------------------
# сервис morph : #morph: слово или предложение
def morph(text: str) -> str:
    """сервис morph : #morph: слово или предложение"""
    # log('morph')
    send = ''
    if ' ' in text:  # несколько слов
        words = String.GetWords(text)
        for word in words:
            send += Word.Morph(word) + '\n'
    else:
        send = Word.Morph(text)
    return send


# ---------------------------------------------------------
# сервис AutoTest : #autotests:
def tests() -> str:
    """сервис AutoTest : #autotests:"""
    # log('AutoTest')
    AutoTest.Alltests()
    for fun in FUNCTIONS:
        Bot.SendMessage(AutoTest.Tests(fun))
        Bot.SendMessage(AutoTest.Fails(fun))
    return 'Все тесты успешно проведены!\nВсего проведено %i тестов.' % len(Tests)


# ---------------------------------------------------------
# сервис movies : #movies: текст поиска фильма
def movies(text: str) -> str:
    """сервис Kinopoisk.movies : #movies: текст поиска фильма"""
    # log('Kinopoisk.movies')
    mov = Movies.Find(text)
    return list_format(mov, sformat='%1\n(ин: %2)\n%3 мин. (%4 год)\nРейтинг: %5 [%6]\n', sobj='фильмов')


# ---------------------------------------------------------
# сервис movie : #movie: инфорация о фильме
def movie(text: str) -> str:
    """сервис Kinopoisk.movie : #movie: информация о фильме"""
    # log('Kinopoisk.movie')
    mov = Movies.Find(text)
    if len(mov) > 0:
        dmov = Movies.GetContent(mov[0][0])
        send = dmov['title']
        if len(dmov['title_en']) > 0:
            send += '\n(ин: %s)' % dmov['title_en']
        send += f"\nГод: {dmov['year']}\nПродолжительность: {dmov['runtime']} мин.\n" \
                f"Рейтинг: {dmov['rating']} [{dmov['votes']}]\nIMDB: {dmov['imdb_rating']} [{dmov['imdb_votes']}]\n"
        send += f"\n{dmov['plot']}\nСлоган: {dmov['tagline']}\nЖанр: {list_str(dmov['genres'])}\n" \
                f"Страна: {list_str(dmov['countries'])}\n\n"
        send += f"Актёры: {list_str(dmov['actors'])}\nРежиссёр: {list_str(dmov['producers'])}\n" \
                f"Сценарист: {list_str(dmov['writers'])}\nБюджет: {str_operand(dmov['budget'], 1000000, '/')} млн. $" \
                f"\nКассовые сборы: {str_operand(dmov['profit'], 1000000, '/')} млн. $"
    else:
        return 'Фильм с таким названием не удалось найти :('
    return send


# ---------------------------------------------------------
# сервис actors : #actors: текст поиска актёра / продюссера
def actors(text: str) -> str:
    """сервис Kinopoisk.actors : #actors: текст поиска актёра / продюсера"""
    # log('Kinopoisk.actors')
    return list_format(Persons.Find(text), sformat='%1\n(ин: %2)\nГоды: %3-%4\n', sobj='персон')


# ---------------------------------------------------------
# сервис actor : #actor: актёр / продюссер
def actor(text: str) -> str:
    """сервис actor : #actor: актёр / продюсер"""
    log('Kinopoisk.actor')
    persons = Persons.Find(text)
    if len(persons):
        pers = Persons.GetContent(persons[0][0])
        send = pers['name']
        if len(pers['name_en']) > 0:
            send += f"\n(ин: {pers['name_en']})"
        last_year = int(datetime.now().year)
        if pers['year_death']: last_year = pers['year_death']
        if pers['year_birth']: age = str(last_year - pers['year_birth'])
        else: age = 'неизвестно'
        send += f"\nГоды жизни: {pers['year_birth']}-{pers['year_death']}\nВозраст: {age} лет\n" \
                f"Информация: {pers['information']}\n\n"
        send += dict_format(pers['actor'], sformat='{title} ({year})\nВ роли {name}\nРейтинг: {rating}\n',
                            sobj='ролей в фильмах') + '\n\n'
        send += dict_format(pers['producer'], sformat='{title} ({year})\nВ роли {name}\nРейтинг: {rating}\n',
                            sobj='в качестве продюсера') + '\n\n'
        send += dict_format(pers['director'], sformat='{title} ({year})\nВ роли {name}\nРейтинг: {rating}\n',
                            sobj='в качестве директора') + '\n\n'
        send += dict_format(pers['writer'], sformat='{title} ({year})\nВ роли {name}\nРейтинг: {rating}\n',
                            sobj='в качестве сценариста')
    else:
        return 'Актёра или продюсера с таким именем не удалось найти :('
    return send
