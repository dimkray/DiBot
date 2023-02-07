"""Сервисы DiBot"""
import config
from system.logging import log, err_log
from system.file import load_byte, save_byte
from system.string import get_params

import apiai
import json
import random

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
from system.SQLite import DataBase
from Tests.Testing import Tests
from Tests.Autotest import AutoTest


# Работа с сервисами
# ---------------------------------------------------------
# сервис AI : #ai: всякий бред

def ai(text: str) -> str:
    """Сервис искусственного интеллекта: #ai: всякий бред"""
    log('Запуск AI')
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
    log(text)
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


# ---------------------------------------------------------
# сервис Answer : #answer: ответ
def answer(text):
    import Bot
    log('Answer')
    if text == 'yes':
        Bot.SendMessage('Отлично!')
        # if Fixer.Thema == 'Знакомство':
        #     Fixer.Service == 'acquaintance'
        #     tsend = User.Acquaintance()
    elif text == 'no':
        tsend = 'Хорошо. Значит в другой раз.\nГотов помочь, чем смогу!'
        Fixer.Thema == ''
        Fixer.Service == ''
    log('Answer', tsend)
    return tsend


# ---------------------------------------------------------
# сервис Name - #name: имя
def name(text):
    text = text.strip()
    log('Name')
    s = ''
    rName = SQL.ReadRow('names', 'nameU', text.upper().replace('Ё', 'Е'))
    if len(rName) > 0:  # если найдено имя
        s = text + ': '
        if rName[1] == 1:  # мужчина
            s += 'мужское имя'
        else:
            s += 'женское имя'
        s += '\nколичество не менее: ' + str(rName[2])
        s += '\nстрана распространения: ' + rName[3]
    else:  # если не найдено имя
        s = 'Не удалось проанализировать имя ' + text + ' :('
    log('Name', s)
    Fixer.Service == ''
    return s


# ---------------------------------------------------------
# сервис User - #user-<param>: значение
def user(param, text):
    log('User')
    tsend = User.Info(param, text)
    log('User', tsend)
    Fixer.Service == ''
    return tsend


# ---------------------------------------------------------
# сервис Acquaintance - #acquaintance:
def acquaintance():
    # log('Acquaintance')
    # tsend = User.Acquaintance()
    # log('Acquaintance', tsend)
    tsend = 'Я бы с тобой познакомился... Но я бот ('
    return tsend


# ---------------------------------------------------------
# сервиса Fixer (информация) #fixer: <Параметр>
def fixer(text):
    log('Fixer')
    text += ' '
    s = text[:text.find(' ')]
    s = s.upper()
    Fixer.Service == ''
    if s == 'XY':
        return str(Fixer.Y) + ',' + str(Fixer.X)
    elif s == 'NAME':
        return Fixer.Name
    elif s == 'AGE':
        return str(Fixer.Age)
    elif s == 'FIXER':
        return str(Chat.Save())
    elif s == 'ADDRESS':
        return Fixer.Address
    elif s == 'LASTLANG1':
        return str(Fixer.LastLang1)
    elif s == 'LASTLANG2':
        return str(Fixer.LastLang2)
    elif s == 'LASTSERVICE':
        return str(Fixer.LastService)
    elif s == 'LASTST1':
        return str(Fixer.LastSt1)
    elif s == 'LASTST2':
        return str(Fixer.LastSt2)
    else:
        Fixer.errProcess = Fixer.Process
        return '#err: неизвестный параметр: ' + s


# ---------------------------------------------------------
# Обработка результатов сервиса Яндекс.Расписание
def FormRasp(s):
    log('FormRasp')
    tstr = s
    if s[0] == '%':  # Рейсы найдены!
        nstr = s.find(' ', 1)
        num = int(s[1:nstr])  # количество рейсов
        gstr = s.find('#', 1)
        Fixer.htext = s[gstr + 1:]
        routes = s[nstr + 1:gstr - 2].strip().split('\n')
        if num == 0:
            tstr = 'Печалька. Не нашёл ни одного прямого рейса :(\nМожет я не правильно тебя понял? Попробуй по другому сделать запрос!'
        elif 0 < num < 11:
            tstr = 'Нашёл ' + str(num) + ' рейс(ов)!\n'
        elif 10 < num < 300:
            tstr = 'Нашёл ' + str(num) + ' рейс(ов). Покажу первые 10.\n'
        elif 300 < num < 1000:
            tstr = 'Нашёл дохрена рейсов! ' + str(num) + '! Покажу первые 10.\n'
            tstr += s[num + 1:gstr]
        else:
            tstr = 'Нашёл какое-то невероятное число рейсов! ' + str(
                num) + '! Может я где-то ошибся? Лучше зайди по ссылке, посмотри всё ли правильно.\n'
        if num > 0:
            x = 0
            for rout in routes:
                tstr += routes[x] + '\n'
                x += 1
                if x > 11: break
        if len(routes) - 1 != num:  # части рейсов нет
            tstr += '\n' + str(num - len(routes) - 1) + 'рейс\рейсов на сегодня уже нет.'
        if len(routes) - 1 == 0 and num > 0:  # если уже рейсов нет
            tstr = 'На сегодня уже нет ни одного прямого рейса :('
    return tstr


# ---------------------------------------------------------
# сервис Booking : #booking: $geo-city | $checkin | $checkout | $people | $order | $dormitory
def booking(text, send=False):
    import Bot
    log('Booking.com')
    from datetime import date
    tformat = '%Y-%m-%d'
    if send: Bot.SendMessage('Секундочку! Ищу подходящее жильё в сервисе Booking.com...')
    params = Fixer.get_params(text)
    bDorm = True
    if len(params) < 2: params.append('Now')
    if len(params) < 3: params.append('Next')
    if len(params) < 4: params.append('1')
    if len(params) < 5: params.append('price')
    if len(params) < 6: params.append('1')
    if params[1].upper() == 'NOW': date.today().isoformat()
    if params[2].upper() == 'NEXT': str(date.strpdate(params[1], tformat) + 1)
    if params[5] != '1': bDorm = False

    mList = Booking.List(params[0], params[1], params[2], people=float(params[3]), order=params[4], dorm=bDorm)
    if mList[0] == '#': return mList
    tsend = 'Найдены следующие варианты:'
    x = 0
    for item in mList:
        x += 1
        if x > 7: continue  # только 7 вариантов
        tsend += '\n' + item
    log('Booking.com', tsend)
    return tsend


# ---------------------------------------------------------
# сервис Яндекс.Расписание
def timetable(text, send=False):
    import Bot
    log('TimeTable')
    if send: Bot.SendMessage('Секундочку! Ищу расписание транспорта в сервисе Яндекс.Расписания...')
    tsend = Ya.FindRasp(text)
    log('Ya.Rasp', tsend)
    tsend = Processor.FormRasp(tsend)
    log('FormRasp', tsend)
    if tsend[0] != '#':
        Fixer.LastSt1.append(Fixer.St1)
        Fixer.LastSt2.append(Fixer.St2)
        Fixer.LastTr.append(Fixer.iTr)
    return tsend


# ---------------------------------------------------------
# сервис Яндекс.Переводчик
def translate(text):
    log('Translate')
    if Fixer.Context:
        lang1 = Fixer.Lang1
        lang2 = Fixer.Lang2
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
        lang1 = Fixer.Lang1
    else:
        Fixer.Lang1 = lang1
    if lang2 == '$lang-to':
        lang2 = Fixer.Lang2
    else:
        Fixer.Lang2 = lang2
    ttext = text[n2 + 2:]
    log('Translate', ttext + ' | ' + lang1 + ' | ' + lang2)
    tsend = Ya.Translate(ttext, lang1, lang2)
    log('Ya.Translate', tsend)
    if tsend[0] != '#':
        Fixer.LastLang1.append(Fixer.Lang1)
        Fixer.LastLang2.append(Fixer.Lang2)
    return tsend


# ---------------------------------------------------------
# сервис Яндекс поиск объектов : #object: objName | Radius
def yaobject(text):
    log('Ya.Object', text)
    param = Fixer.get_params(text)
    ttext = param[0]
    rad = Fixer.Radius
    if len(param) > 1: rad = param[1]
    try:
        drad = int(rad)
    except:
        if rad == 'near':
            drad = 2
        else:
            drad = 100
    tsend = Ya.Objects(ttext, Xloc=Fixer.X, Yloc=Fixer.Y, dr=drad)
    log('Ya.Object', tsend)
    return tsend


# ---------------------------------------------------------
# сервис Яндекс.Координаты : #coordinates: $geo-city
def coordinates(text):
    log('Ya.Координаты')
    if text == '': text = 'LOCATION'
    tsend = Ya.Coordinates(text)
    log('Ya.Координаты', tsend)
    return tsend


# ---------------------------------------------------------
# сервис Яндекс.Каталог : #site: type(info/find) - $site/String
def site(text):
    log('Ya.Каталог')
    param = Fixer.get_params(text)
    if len(param) < 2:
        Fixer.errProcess = Fixer.Process
        return '#err: Нет второго параметра'
    if param[0].lower() == 'info':
        tsend = Ya.Catalog(param[1])
    elif param[0].lower() == 'find':
        tsend = Ya.FindCatalog(param[1])
    else:
        Fixer.errProcess = Fixer.Process
        return '#err: Параметр "%s" не поддерживается!' % param[0]
    log('Ya.Каталог', tsend)
    return tsend


# ---------------------------------------------------------
# сервис wiki : #wiki: query
def wiki(text, send=False):
    import Bot
    log('Wikipedia')
    if send: Bot.SendMessage('Секундочку! Ищу информацию в Википедии...')
    pages = Wiki.SearchPage(text.strip())
    if len(pages) == 0: return 'Я поискал информацию в Википедии, но ничего не нашёл. Можешь уточнить запрос?'
    Fixer.htext = '"https://ru.wikipedia.org/wiki/' + pages[0] + '"'
    log('Wikipedia', Fixer.htext)
    return Wiki.MiniContent(pages[0])


# ---------------------------------------------------------
# сервис wiki-more
def wikimore(text):
    log('Wikipedia.More', text.strip())
    return Wiki.More(Fixer.Page)


# ---------------------------------------------------------
# сервис geowiki : #geowiki: [radius]
def geowiki(text, send=False):
    import Bot
    log('WikipediaGeo')
    if text == '':
        rad = Fixer.Radius
    else:
        try:
            text += ' '
            rad = str(text[:text.find(' ')])
        except:
            err_log('WikipediaGeo', 'Ошибка в определении радиуса: ' + text[:text.find(' ')])
            rad = 100
    if send: Bot.SendMessage('Секундочку! Ищу ближайшие достопримечательности по Википедии...')
    pages = Wiki.GeoSearch(Fixer.X, Fixer.Y, resnom=10, rad=rad)
    if len(pages) == 0 or pages[
        0] == '#': return 'Я поискал достопримечательности в Википедии, но ничего не нашёл. Может стоит величить радиус поиска?'
    s = 'Нашёл следующие достопримечательности:\n'
    for p in pages:
        s += p + '\n'
    Bot.SendMessage(s)
    Fixer.htext = '"https://ru.wikipedia.org/wiki/' + pages[0] + '"'
    log('WikipediaGeo', Fixer.htext)
    return Wiki.GeoFirstMe(rad)


# ---------------------------------------------------------
# сервис geowiki1 : #geowiki1: [radius]
def geowiki1(text, send=False):
    import Bot
    log('WikipediaGeo1')
    if text == '':
        rad = Fixer.Radius
    else:
        try:
            text += ' '
            rad = str(text[:text.find(' ')])
        except:
            err_log('WikipediaGeo1', 'Ошибка в определении радиуса: ' + text[:text.find(' ')])
            rad = 100
    if send: Bot.SendMessage('Секундочку! Ищу ближайшую достопримечательность по Википедии...')
    response = Wiki.GeoFirstMe(rad)
    if response[0] == '#': return 'В радиусе ' + str(rad) + ' метров не нашёл ни одной достопримечательности :('
    pages = Wiki.GeoSearch(Fixer.X, Fixer.Y, resnom=10, rad=rad)
    Fixer.htext = '"https://ru.wikipedia.org/wiki/' + pages[0] + '"'
    log('WikipediaGeo1', Fixer.htext)
    return response


# ---------------------------------------------------------
# сервис google.Define : #define: word
def define(text):
    log('Google.Define')
    stext = Google.Define(text.strip())
    log('Google.Define', stext)
    return stext


# ---------------------------------------------------------
# сервис google.Calc : #calc: formula
def calc(text):
    log('Google.Calc')
    stext = Google.Calc(text.strip())
    log('Google.Calc', stext)
    return stext


# ---------------------------------------------------------
# сервис google : #google: query / [$responce]
def google(text, map=False):
    log('Google.Search')
    if text == '$responce': text = Fixer.Query
    print(text)
    stext = Google.Search(text.strip(), bmap=map)
    log('Google.Search', stext)
    return stext


# ---------------------------------------------------------
# сервис getcoords
def getcoords(geocity):
    if geocity.strip() == '': geocity = 'LOCATION'
    if geocity.strip().upper() == 'LOCATION':
        Fixer.Coords[0] = Fixer.X
        Fixer.Coords[1] = Fixer.Y
        s = 'LOCATION'
    else:
        s = Ya.Coordinates(geocity)
    print(s)
    return s


# ---------------------------------------------------------
# сервис weather : #weather: type:full/short/day/cloud/wind/sun/night/riseset/temp | $geo-city | $date
def weather(text):
    log('Weather')
    params = Fixer.get_params(text)
    # print(params)
    if len(params) < 2: params.append('Location')
    if len(params) < 3: params.append(str(Fixer.Date))
    # print('{%s}' % params[1])
    s = Processor.getcoords(params[1])
    # print('{%s}' % s)
    if s[0] == '#': return 'Не удалось распознать город или найти его координаты :( - ' + s
    m = Weather.Forecast(Fixer.Coords[0], Fixer.Coords[1], params[2])
    print(m)
    if m[0] == '#': return m
    stext = ''
    if params[0] == 'full':  # полный прогноз погоды
        stext = m[17] + '\n\n' + m[18] + '\n\n' + m[19]
    elif params[0] == 'day':  # полный прогноз погоды (день)
        stext = m[18]
    elif params[0] == 'night':  # полный прогноз погоды (ночь)
        stext = m[19]
    elif params[0] == 'short':  # короткий прогноз погоды
        s = 'Температура от ' + m[10] + ' до ' + m[2] + '\n'
        s += 'Днём: ' + m[3] + '\n'
        s += 'Ночью: ' + m[11]
        stext = s
    elif params[0] == 'temp':  # температура
        stext = 'Температура от ' + m[10] + ' до ' + m[2] + '\n'
    elif params[0] == 'riseset':  # восход и заход солнца
        stext = 'Рассвет: ' + m[0] + '\n'
        stext += 'Закат: ' + m[1]
    elif params[0] == 'cloud':  # осадки, облачность
        s = 'Днём: ' + m[3]
        s += ', вероятность осадков ' + m[4] + '\n'
        s += 'Объём осадков: ' + m[5] + '\n'
        s += 'Продолжительность осадков: ' + m[6] + '\n'
        s += 'Облачность: ' + m[7] + '\n'
        s += '\nНочью: ' + m[11]
        s += ', вероятность осадков ' + m[12] + '\n'
        s += 'Объём осадков: ' + m[13] + '\n'
        s += 'Продолжительность осадков: ' + m[14] + '\n'
        s += 'Облачность: ' + m[15]
        stext = s
    elif params[0] == 'wind':  # ветер
        s = 'Днём: ' + m[8]
        s = '\nНочью: ' + m[16]
        stext = s
    elif params[0] == 'sun':  # солнце
        stext = 'Днём: ' + m[3] + ', солнечные часы - ' + m[9]
    else:  # необрабатываемый случай
        stext = '#problem: {' + params[0] + '}'
    log('Weather', stext)
    return stext


# ---------------------------------------------------------
# сервис timezone : #timezone: [$geo-city]
def timezone(text):
    log('TimeZone')
    # if text.strip() == '': text = 'Location' - уже есть в getcoords
    s = Processor.getcoords(text)
    if s[0] == '#': return 'Не удалось распознать город или найти его координаты :( - ' + s
    m = Weather.GetLocation(Fixer.Coords[0], Fixer.Coords[1])
    if m[0][0] == '#':
        # попытка узнать часовой пояс из Geo
        s = Geo.GetTimezone(Fixer.Coords[0], Fixer.Coords[1])
        # print(s)
        return s
    # ss = 'Часовой пояс: '
    ss = ''
    if float(m[5]) > 0: ss = '+'
    log('TimeZone', ss)
    return ss + m[5]


# ---------------------------------------------------------
# сервис population : #population: [$geo-city]
def population(text):
    log('Population')
    # if text.strip() == '': text = 'Location' - уже есть в getcoords
    s = Processor.getcoords(text)
    if s[0] == '#': return 'Не удалось распознать город или найти его координаты :( - ' + s
    m = Weather.GetLocation(Fixer.Coords[0], Fixer.Coords[1])
    # print(m)
    if m[0][0] == '#': return m[0]
    s = 'Население пункта ' + m[2] + ' [' + m[1] + '] ' + m[3] + ' (' + m[4] + ') : ' + str(m[7]) + ' чел.'
    log('Population', s)
    return s


# ---------------------------------------------------------
# сервис elevation : #elevation: [$geo-city]
def elevation(text):
    log('Elevation')
    # if text.strip() == '': text = 'Location'-  - уже есть в getcoords
    s = Processor.getcoords(text)
    if s[0] == '#': return 'Не удалось распознать город или найти его координаты :( - ' + s
    m = Weather.GetLocation(Fixer.Coords[0], Fixer.Coords[1])
    print(m)
    if m[0][0] == '#': return m[0]
    s = 'Высотная отметка ' + m[2] + ' [' + m[1] + '] ' + m[3] + ' (' + m[4] + ') : ' + str(
        m[6]) + ' метров над уровнем моря'
    log('Elevation', s)
    return s


# ---------------------------------------------------------
# сервис geodistance : #geodistance: $geo-city1 - [$geo-city2]
def geodistance(text):
    log('GeoDistance')
    params = Fixer.get_params(text)
    if len(params) < 2: params.append('Location')
    s = Processor.getcoords(params[0])
    if s[0] == '#': return 'Не удалось распознать первый город или найти его координаты :( - ' + s
    x = Fixer.Coords[0];
    y = Fixer.Coords[1]
    s = Processor.getcoords(params[1])
    if s[0] == '#': return 'Не удалось распознать второй город или найти его координаты :( - ' + s
    s = str(round(Geo.Distance(y, x, Fixer.Coords[1], Fixer.Coords[0]))) + ' км по прямой линии'
    log('GeoDistance', s)
    return s


# ---------------------------------------------------------
# сервис compliment : #compliment:
def compliment():
    log('Comliment')
    if Fixer.Type == 1:
        stext = random.choice(Fixer.COMPLIMENT_MAN[1])
    else:
        stext = random.choice(Fixer.COMPLIMENT_WOMAN[1])
    log('Comliment', stext)
    return stext


# ---------------------------------------------------------
# сервис anecdote : #anecdote:
def anecdote():
    log('Fun.Anecdote')
    stext = Fun.Anecdote()
    log('Fun.Anecdote', stext)
    return stext


# ---------------------------------------------------------
# сервис rate
def rate(text):
    log('Rates.Rate')
    params = Fixer.get_params(text)
    if params[0] == 'ALL':  # если нужны курсы всех валют
        stext = Fixer.Dialog('rate')
        for val in Fixer.CURRENCIES:
            stext += '\n' + Fixer.CURRENCIES[val] + ' : ' + Rate.RateRubValue(val, params[1], float(params[2])) + ' ' + \
                     Fixer.CURRENCIES2[params[1]]
    else:
        stext = Rate.RateRubValue(params[0], params[1], float(params[2])) + ' ' + Fixer.CURRENCIES2[params[1]]
        if stext[0] != '#': Fixer.LastValute.append(params[0])
    log('Rates.Rate', stext)
    return stext


# ---------------------------------------------------------
# сервис setrate
def setrate(text):
    log('SetRate', text)
    if Rate.isValute(text) == False: return 'Не знаю такой валюты: ' + text
    Fixer.Valute = text
    return 'Хорошо! Установлена валюта по-умолчанию: ' + Fixer.CURRENCIES[text]


# ---------------------------------------------------------
# сервис note - #notes: ALL/<Имя раздела> | Текст
def note(text):
    log('Note', text)
    params = Fixer.get_params(text)
    Fixer.Notes[params[0].upper()] = params[1]
    return Fixer.Dialog('note_section') + params[0].upper()


# ---------------------------------------------------------
# сервис notes - #notes: [ALL/<Имя раздела>]
def notes(text):
    text = text.strip()
    log('Notes', text)
    if text.upper() == 'ALL' or text == '':
        s = Fixer.Dialog('notes_all')
        for snote in Fixer.Notes.values():
            s += '\n' + snote
    else:
        s = Fixer.Dialog('notes_section') + text.upper()
        for snote in Fixer.Notes[text.upper()]:
            s += '\n' + snote
    return s


# ---------------------------------------------------------
# сервис setlocation
def setlocation(text):
    log('SetLocation')
    from geolocation.main import GoogleMaps
    try:
        params = Fixer.get_params(text, separator=',')
        Fixer.LastX.append(Fixer.X)
        Fixer.LastY.append(Fixer.Y)
        Fixer.Y = params[0]
        Fixer.X = params[1]
        mes = 'Хорошо! Установлены координаты: ' + Fixer.Y + ', ' + Fixer.X + '.\n'
        # Сервис Google.Geocoding
        my_location = GoogleMaps(api_key=config.GOOGLE_MAPS_KEY).search(lat=Fixer.Y, lng=Fixer.X).first()
        mes += my_location.formatted_address  # + '\n'
        Fixer.Address = my_location.formatted_address
        Fixer.LastAddress.append(Fixer.Address)
        return mes
    except Exception as e:
        err_log('SetLocation', str(e))
        return '#bug: ' + str(e)


# ---------------------------------------------------------
# сервис correction
def correction(text):
    import Bot
    log('Correction', text)
    Fixer.DIALOGS_NEW[Fixer.str_cleaner(Fixer.Query)] = Fixer.get_params(text, ';')
    Fixer.save(Fixer.DIALOGS_NEW, 'NewDialogs')
    s = '\nНа запрос: ' + Fixer.str_cleaner(Fixer.Query)
    for i in Fixer.get_params(text, ';'):
        s += '\nВариант ответа: ' + i
    Bot.SendAuthor('Уведомление от пользователя ' + str(Fixer.UserID) + s)
    s = Fixer.Dialog('correction') + s
    Fixer.bAI = True;
    Fixer.Service = 'ai';
    Fixer.Conext = False
    return s


# ---------------------------------------------------------
# сервис date / time / datetime : location - type
def datetime(location, ttype='datetime'):
    log('DateTime: %s | %s' % (location, ttype))
    Fixer.TimeZone = float(Processor.timezone(location))
    import datetime
    now = datetime.datetime.utcnow() + datetime.timedelta(hours=Fixer.TimeZone)
    if ttype == 'time':
        return now.strftime('%H:%M:%S')
    elif ttype == 'date':
        return now.strftime('%Y-%m-%d')
    else:
        return now.strftime('%Y-%m-%d %H:%M:%S')


# ---------------------------------------------------------
# сервис log / logerr : число последних записей
def log(snumber, etype='none'):
    log('log')
    mlog = []
    try:
        if etype == 'err':
            f = open('log_error.txt', encoding='utf-8')
            for line in f:
                mlog.append(line)
            f.close()
        else:
            f = open('log.txt', encoding='utf-8')
            for line in f:
                mlog.append(line)
            f.close()
        ilen = len(mlog)
        try:
            number = int(snumber)
        except:
            number = 10
        if number < 1: number = 1
        if number > 100: number = 100
        if ilen < number:
            start = 0
        else:
            start = ilen - number
        s = ''
        for i in range(start, ilen):
            s += '[%i] %s' % (i, mlog[i])
        return s
    except Exception as e:
        err_log('log', 'Ошибка при загрузке логов: ' + str(e))


# ---------------------------------------------------------
# сервис buglog : #buglog: numberStart | numberEnd
def buglog(text):
    from DB.SQLite import SQL
    log('buglog')
    params = Fixer.get_params(text)
    if len(params) < 2: params.append(params[0])
    m = SQL.sql('SELECT * FROM bugs WHERE id >= %s AND id <= %s' % (params[0], params[1]))
    send = ''
    if len(m) > 0:
        for im in m:
            if im[1] == 1:
                send += '\nBUG'
            elif im[1] == 2:
                send += '\nPORBLEM'
            else:
                send += '\nANOTHER'
            send += '[%i]: %s\nQuery: %s\nProcess: %s\nResponce: %s' % (im[0], im[5], im[2], im[3], im[4])
    else:  # если нет результата
        send += 'Баги №№ %s - %s не найдены!' % (params[0], params[1])
    return send


# ---------------------------------------------------------
# сервис RSS : #rss: rssurl | numberpost(3)
def rss(text):
    import Bot
    log('RSS')
    params = Fixer.get_params(text)
    params[0] = params[0].lower()  # форматирование строки
    if len(params) < 2: params.append('3')
    titles = RSS.GetTitles(params[0])
    if titles['status'] == 'ok':
        stext = '%s\n%s\nЯзык публикации: %s\nАвтор: %s\nСайт: %s' % (titles['title'], titles['subtitle'],
                                                                      titles['lang'], titles['author'], titles['link'])
        posts = RSS.GetPosts(params[0])
        for i in range(0, int(params[1])):
            stext += '\n\n[%s]\n%s\n(%s)\n%s' % (
            posts[i]['title'], posts[i]['description'], posts[i]['date'], posts[i]['link'])
        Bot.SendMessage(stext)
        brss = True
        for rss in Fixer.RSS:
            if params[0] == rss['rss']: brss = False
        smess = ''
        if brss:  # записываем rss-канал
            drss = {}
            drss['rss'] = params[0]
            drss['title'] = titles['title']
            drss['posts'] = []
            for post in posts:
                dpost = {}
                dpost['len'] = len(post['description'])
                dpost['date'] = post['date']
                drss['posts'].append(dpost)
            Fixer.RSS.append(drss)
            Fixer.LastRSS.append(params[0])
            smess = 'RSS-канал "%s" успешно поключен!\nНовости канала будут приходить по мере их поступления.' % titles[
                'title']
            from datetime import datetime, timedelta
            now = (datetime.today() + timedelta(minutes=1)).strftime('%H:%M:%S')  # форматирование времени
            Processor.task('RSS | ' + now + ' | 0 | #rss-news: ' + params[0])
        else:
            smess = 'RSS-канал "%s" был сохранён ранее.' % titles['title']

        return smess
    else:
        return 'указанная ссылка не является RSS-каналом.'


# ---------------------------------------------------------
# сервис RSS-news : #rss-news: rssurl
def rssnews(url):
    log('RSS-News')
    url = url.lower()  # форматирование строки
    s = '#null'  # 'Не удалось найти rss-канал в подписке: ' + url
    oldposts = []  # поиск старых постов
    iRSS = 0
    for rss in Fixer.RSS:
        if url == rss['rss']:
            oldposts = rss['posts']
            s = 'Новости rss-канала "%s":' % rss['title']
            posts = RSS.GetNewPosts(url, oldposts)
            if len(posts) > 0:
                for post in posts:
                    s += '\n\n[%s]\n%s\n(%s)\n%s' % (post['title'], post['description'], post['date'], post['link'])
                    dpost = {}  # запись новостей
                    dpost['len'] = len(post['description'])
                    dpost['date'] = post['date']
                    Fixer.RSS[iRSS]['posts'].append(dpost)  # добавление в Fixer
                # print(Fixer.RSS)
                Chat.Save()
            else:
                s = '#null'
            break
        iRSS += 1
    return s


# ---------------------------------------------------------
# сервис RSS-all : #rss-all:
def rssall():
    log('RSS-all')
    s = 'Список всех подключённых rss-каналов:'
    iRSS = 0
    for rss in Fixer.RSS:
        s += '\n[%i] %s - %s' % (iRSS, rss['rss'], rss['title'])
        iRSS += 1
    if iRSS == 0:
        s += '\n( список пуст )'
    else:
        s += '\n\nМожно удалить лишние каналы командой "rss-del: №"'
    return s


# ---------------------------------------------------------
# сервис RSS-del : #rss-del: №
def rssdel(text):
    log('RSS-del')
    irss = int(text)
    s = 'Удаление канала "%s" прошло успешно!' % Fixer.RSS[irss]['title']
    del (Fixer.RSS[irss])
    return s


# ---------------------------------------------------------
# сервис IATA : #IATA: №
def iata(text, stype='code'):
    log('IATA')
    colsReturn = ['code', 'name', 'cityName', 'timeZone', 'country', 'lat', 'lon',
                  'runwayLength', 'runwayElevation', 'phone', 'email', 'website']
    sfrm = '%0 - %1, г. %2, %4 (%3)\nДлина взлётной полосы: %7, высотная отметка: %8\nТелефон: %9, e-mail: %%10\nURL: %%11'
    s = '';
    s2 = ''
    if stype == 'code':
        m1 = IATA.Airport(code=text)
        m2 = IATA.City(code=text)
        if len(m2) > 0:
            s += Fixer.list_format(m2, sformat=sfrm, sobj='аэропортов в городах') + '\n'
        s += '\n' + Fixer.list_format(m1, sformat=sfrm, sobj='отдельных аэропортов')
    elif stype == 'air':
        m = IATA.Airport(name=text)
        s = Fixer.list_format(m, sformat=sfrm, sobj='аэропортов')
    elif stype == 'city':
        m = IATA.City(name=text)
        s = Fixer.list_format(m, sformat=sfrm, sobj='аэропортов в городах')
    elif stype == 'code3':
        if Word.Type(text) == 50:
            m = IATA.Country(code=text)  # если латиница
        else:
            m = IATA.Country(name=text)
        s = Fixer.list_format(m, sformat='код: %0, код3: %1, iso: %2\nназвание: %3', sobj='стран')
    return s


# ---------------------------------------------------------
# сервис skill : #skill:
def skill():
    log('skill')
    m = []  # массив сервисов
    for skey in Fixer.SERVICES:
        m.append(skey)
    ser = random.choice(m)
    print(ser)
    s = 'Сервис "%s" - %s\nАвтор: %s\n' % (Fixer.SERVICES[ser][1], Fixer.SERVICES[ser][4], Fixer.SERVICES[ser][2])
    s += 'Примеры: '
    for pr in Fixer.SERVICES[ser][7]:
        s += '"%s", ' % pr
    s = s[:-2]
    return s


# ---------------------------------------------------------
# сервис morph : #morph: слово или предложение
def morph(text):
    log('morph')
    s = ''
    if ' ' in text:  # несколько слов
        words = String.GetWords(text)
        for word in words:
            s += Word.Morph(word) + '\n'
    else:
        s = Word.Morph(text)
    return s


# ---------------------------------------------------------
# сервис AutoTest : #autotests:
def tests():
    import Bot
    log('AutoTest')
    AutoTest.Alltests()
    for iserv in Fixer.FUNCTIONS:
        Bot.SendMessage(AutoTest.Tests(iserv))
        Bot.SendMessage(AutoTest.Fails(iserv))
    return 'Все тесты успешно проведены!\nВсего проведено %i тестов.' % len(Tests)


# ---------------------------------------------------------
# сервис movies : #movies: текст поиска фильма
def movies(text):
    log('Kinopoisk.movies')
    mMovies = Movies.Find(text)
    return Fixer.list_format(mMovies, sformat='%1\n(ин: %2)\n%3 мин. (%4 год)\nРейтинг: %5 [%6]\n', sobj='фильмов')


# ---------------------------------------------------------
# сервис movie : #movie: инфорация о фильме
def movie(text):
    log('Kinopoisk.movie')
    mMovies = Movies.Find(text)
    if len(mMovies) > 0:
        dMovie = Movies.GetContent(mMovies[0][0])
        s = dMovie['title']
        if len(dMovie['title_en']) > 0:
            s += '\n(ин: %s)' % dMovie['title_en']
        s += '\nГод: %s\nПродолжительность: %i мин.\nРейтинг: %f [%i]\nIMDB: %f [%i]\n' % \
             (dMovie['year'], dMovie['runtime'], dMovie['rating'], dMovie['votes'],
              dMovie['imdb_rating'], dMovie['imdb_votes'])
        s += '\n%s\nСлоган: %s\nЖанр: %s\nСтрана: %s\n\n' % (dMovie['plot'], dMovie['tagline'],
                                                             Fixer.str_list(dMovie['genres']),
                                                             Fixer.str_list(dMovie['countries']))
        s += 'Актёры: %s\nРежиссёр: %s\nСценарист: %s\nБюджет: %s млн. $\nКассовые сборы: %s млн. $' % \
             (Fixer.str_list(dMovie['actors']), Fixer.str_list(dMovie['producers']), Fixer.str_list(dMovie['writers']),
              Fixer.str_operand(dMovie['budget'], 1000000, '/'), Fixer.str_operand(dMovie['profit'], 1000000, '/'))
    else:
        return 'Фильм с таким названием не удалось найти :('
    return s


# ---------------------------------------------------------
# сервис actors : #actors: текст поиска актёра / продюссера
def actors(text):
    log('Kinopoisk.actors')
    mPersons = Persons.Find(text)
    return Fixer.list_format(mPersons, sformat='%1\n(ин: %2)\nГоды: %3-%4\n', sobj='персон')


# ---------------------------------------------------------
# сервис actor : #actor: актёр / продюссер
def actor(text):
    from _datetime import datetime
    log('Kinopoisk.actor')
    mPersons = Persons.Find(text)
    if len(mPersons) > 0:
        dPerson = Persons.GetContent(mPersons[0][0])
        s = dPerson['name']
        if len(dPerson['name_en']) > 0:
            s += '\n(ин: %s)' % dPerson['name_en']
        last_year = int(datetime.now().year)
        if dPerson['year_death'] is not None:
            last_year = dPerson['year_death']
        if dPerson['year_birth'] is not None:
            age = str(last_year - dPerson['year_birth'])
        else:
            age = 'неизвестно'
        s += '\nГоды жизни: %s-%s\nВозраст: %s лет\nИнформация: %s\n\n' % \
             (Fixer.str_put(dPerson['year_birth']), Fixer.str_put(dPerson['year_death']), age, dPerson['information'])
        s += Fixer.dict_format(dPerson['actor'], sformat='{title} ({year})\nВ роли {name}\nРейтинг: {rating}\n',
                               sobj='ролей в фильмах') + '\n\n'
        s += Fixer.dict_format(dPerson['producer'], sformat='{title} ({year})\nВ роли {name}\nРейтинг: {rating}\n',
                               sobj='в качестве продюссера') + '\n\n'
        s += Fixer.dict_format(dPerson['director'], sformat='{title} ({year})\nВ роли {name}\nРейтинг: {rating}\n',
                               sobj='в качестве директора') + '\n\n'
        s += Fixer.dict_format(dPerson['writer'], sformat='{title} ({year})\nВ роли {name}\nРейтинг: {rating}\n',
                               sobj='в качестве сценариста')
    else:
        return 'Актёра или продюссера с таким названием не удалось найти :('
    return s
