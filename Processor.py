# -*- coding: utf-8 -*-
# Процессор - обработчик основных сервисов

import config
import Fixer
import Bot
import apiai, json
import random

from Services.Fun import Fun
from Services.Yandex import Yandex
from Services.Google import Google
from Services.Wikipedia import Wiki
from Services.User import User
from Services.Rates import Rate
from Services.Weather import Weather
from Services.Geo import Geo
from Chats.Chats import Chat

# получение переменных в массив [] из строки переменных для сервиса
def getparams(text, separator='|'):
    if text.find(separator) < 0: # нет текущего сепаратора
        if text.find(' - ') > 0: separator = ' - '
    m = text.split(separator)
    x = 0
    for im in m:
        m[x] = im.strip(); # убираем лишние пробелы
        x += 1
    #print(m)
    return m

# Работа с сервисами
# ---------------------------------------------------------
# сервис AI
def ai(text):
    print('Запуск AI')
    request = apiai.ApiAI(config.apiAI_key).text_request()
    request.lang = 'ru' # На каком языке будет послан запрос
    request.session_id = Fixer.UserID #'BatlabAIBot' # ID Сессии диалога (нужно, чтобы потом учить бота)
    # Запуск сервиса Google Dialogflow для обработки пользовательского запроса (ИИ)
    request.query = text # Посылаем запрос к ИИ с сообщением от юзера
    responseJson = json.loads(request.getresponse().read().decode('utf-8'))
    return responseJson['result']['fulfillment']['speech'] # Разбираем JSON и вытаскиваем ответ

# ---------------------------------------------------------
# сервис Task : #task: type | time | times | Notice/Service
def task(text):
    import Notification
    from datetime import date, datetime, timedelta
    tformat = '%Y-%m-%d %H:%M:%S'
    Fixer.log('Старт сервиса Task: ' + text)
    Notification.Tasks = Fixer.LoadB('Tasks')
    params = getparams(text)
    s = ''
    if params[0] == 'alarm':
        s = 'Будильник успешно установлен!'
    elif params[0] == 'alarmlater':
        s = 'Отложенное уведомление успешно установлено!'
    else:
        s = 'Неизвестная задача '+params[0]+'!'
        return s
    m = [] # наполняем массив
    smsg = params[0] +'-'+ str(random.randint(100000, 999999))
    skey = str(Fixer.ChatID) +':'+ smsg
    etime = datetime.strptime(str(date.today())+' '+params[1],tformat)
    if etime < datetime.today():
        etime = etime + timedelta(days=1)
    s += '\nНазвание: '+smsg+'\nСообщение\\сервис: '+params[3]+'\nВремя срабатывания: '+str(etime)+'\nКоличество повторений: '+params[2]
    m.append(Fixer.bNotice) # 0 - вкл/выкл уведомление пользователя
    m.append(etime) # 1 - дата-время срабатывания задачи
    m.append(timedelta(days=1)) # 2 - дельта следующего срабатывания / по умолчанию 1 день для alarm
    m.append(int(params[2])) # 3 - количество раз срабатывания (при -1 бесконечный цикл)	
    scode = params[3]
    if params[3].upper() == 'NULL': 
        params[3] = smsg+'\nТы просил меня отправить сообщение в '+str(etime)
        scode = ''
    m.append(params[3]) # 4 - сообщение при уведомлении
    m.append(scode) # 5 - запускаемый сервис	
    Notification.Tasks[skey] = m
    Fixer.SaveB(Notification.Tasks, 'Tasks') # Сохранение задач
    Fixer.log('Cервис Task ответил: ' + s)
    print(Notification.Tasks)
    return s
	
# ---------------------------------------------------------
# сервис Answer : #answer: ответ
def answer(text):
    Fixer.log('Старт сервиса Answer: ' + text)
    if text == 'yes':
        Bot.SendMessage('Отлично!')
        if Fixer.Thema == 'Знакомство': Fixer.Service == 'acquaintance'
        tsend = User.Acquaintance()
    elif text == 'no':
        tsend = 'Хорошо. Значит в другой раз.\nГотов помочь, чем смогу!'
        Fixer.Thema == ''
        Fixer.Service == ''
    Fixer.log('Cервиса Answer ответил: ' + tsend)
    return tsend

# ---------------------------------------------------------
# сервис Name - #name: имя
def name(text):
    Fixer.log('Старт сервиса Name: ' + text)
    s = ''
    for i in Fixer.Names: # поиск информации по имени
        if i.lower() == text.lower():
            s = text + ': '
            if Fixer.Names[i][0]: # мужчина
                s += 'мужское имя'
            else:
                s += 'женское имя'
            s += '\nколичество не менее: ' + str(Fixer.Names[i][1])
            s += '\nстрана распространения: ' + Fixer.Names[i][2]
    if s == '':
        s = 'Не удалось проанализировать имя '+text+' :('
    Fixer.log('Cервиса Name ответил: ' + s)
    Fixer.Service == ''
    return s

# ---------------------------------------------------------
# сервис User - #user-<param>: значение
def user(text):
    Fixer.log('Старт сервиса User: ' + text)
    tsend = User.Info(text)
    Fixer.log('Cервиса User ответил: ' + tsend)
    Fixer.Service == ''
    return tsend

# ---------------------------------------------------------
# сервис Acquaintance - #acquaintance:
def acquaintance():
    Fixer.log('Старт сервиса Acquaintance')
    tsend = User.Acquaintance()
    Fixer.log('Cервиса Acquaintance ответил: ' + tsend)
    return tsend

# ---------------------------------------------------------
# сервиса Fixer (информация) #fixer: <Параметр>
def fixer(text):
    Fixer.log('Старт информационного сервиса Fixer: ' + text)
    text += ' '
    s = text[:text.find(' ')]
    s = s.upper()
    Fixer.Service == ''
    if s == 'XY': return str(Fixer.Y)+','+str(Fixer.X)
    elif s == 'NAME': return Fixer.Name
    elif s == 'AGE': return str(Fixer.Age)
    elif s == 'FIXER': return str(Chat.Save())
    elif s == 'ADDRESS': return Fixer.Address
    elif s == 'LASTLANG1': return str(Fixer.LastLang1)
    elif s == 'LASTLANG2': return str(Fixer.LastLang2)
    elif s == 'LASTSERVICE': return str(Fixer.LastService)
    elif s == 'LASTST1': return str(Fixer.LastSt1)
    elif s == 'LASTST2': return str(Fixer.LastSt2)
    else: return '#bug: unknown parameter'

# ---------------------------------------------------------
# Обработка результатов сервиса Яндекс.Расписание
def FormRasp(s):
    tstr = s
    if s[0] == '%': # Рейсы найдены!
        nstr = s.find(' ',1)
        num = int(s[1:nstr]) # количество рейсов
        gstr = s.find('#',1)
        Fixer.htext = s[gstr+1:]
        routes = s[nstr+1:gstr-2].strip().split('\n')
        if num == 0:
            tstr = 'Печалька. Не нашёл ни одного прямого рейса :(\nМожет я не правильно тебя понял? Попробуй по другому сделать запрос!'
        elif 0 < num < 11:
            tstr = 'Нашёл ' + str(num) + ' рейс(ов)!\n'
        elif 10 < num < 300:
            tstr = 'Нашёл ' + str(num) + ' рейс(ов). Покажу первые 10.\n'
        elif 300 < num < 1000:
            tstr = 'Нашёл дохрена рейсов! ' + str(num) + '! Покажу первые 10.\n'
            tstr += s[num+1:gstr]
        else:
            tstr = 'Нашёл какое-то невероятное число рейсов! ' + str(num) + '! Может я где-то ошибся? Лучше зайди по ссылке, посмотри всё ли правильно.\n'
        if num > 0:
            x = 0
            for rout in routes:
                tstr += routes[x] + '\n'
                x += 1
                if x > 11: break
        if len(routes)-1 != num: # части рейсов нет
            tstr += '\n' + str(num-len(routes)-1) + 'рейс\рейсов на сегодня уже нет.'
        if len(routes)-1 == 0 and num > 0: # если уже рейсов нет
            tstr = 'На сегодня уже нет ни одного прямого рейса :('
    return tstr

# ---------------------------------------------------------
# сервис Яндекс.Расписание
def timetable(text, send=False):
    if send: Bot.SendMessage('Секундочку! Ищу расписание транспорта в сервисе Яндекс.Расписания...')
    Fixer.log('Передача сервису Yandex.Rasp: ' + text)
    tsend = Yandex.FindRasp(text)
    Fixer.log('Yandex.Rasp: ' + tsend)
    tsend = FormRasp(tsend)
    Fixer.log('Постобработка Yandex.Rasp: ' + tsend)
    if tsend[0] != '#':
        Fixer.LastSt1.append(Fixer.St1)
        Fixer.LastSt2.append(Fixer.St2)
        Fixer.LastTr.append(Fixer.iTr)
    return tsend

# ---------------------------------------------------------
# сервис Яндекс.Переводчик
def translate(text):
    Fixer.log('Старт сервиса Yandex.Translate: ' + text)
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
            lang2 = text[n1+3:n2]
    if lang1 == lang2: lang2 = 'английский'
    if lang1 == '$lang-from':
        lang1 = Fixer.Lang1
    else:
        Fixer.Lang1 = lang1
    if lang2 == '$lang-to':
        lang2 = Fixer.Lang2
    else:
        Fixer.Lang2 = lang2
    ttext = text[n2+2:]
    Fixer.log('Передача сервису Yandex.Translate: ' + ttext + ' | ' + lang1 + ' | ' + lang2)
    tsend = Yandex.Translate(ttext, lang1, lang2)
    Fixer.log('Yandex.Translate ответил: ' + tsend)
    if tsend[0] != '#':
        Fixer.LastLang1.append(Fixer.Lang1)
        Fixer.LastLang2.append(Fixer.Lang2)
    return tsend

# ---------------------------------------------------------
# сервис Яндекс поиск объектов
def yaobject(text):
    Fixer.log('Старт сервиса Yandex.Object: ' + text)
    n1 = text.find(' : ')
    ttext = text[:n1]
    rad = text[n1+3:]
    try:
        drad = int(rad)
    except:
        if rad == 'near': drad = 1
        else: drad = 5
    tsend = Yandex.Objects(ttext, Xloc=Fixer.X, Yloc=Fixer.Y, dr=drad)
    Fixer.log('Yandex.Object ответил: ' + tsend)
    return tsend

# ---------------------------------------------------------
# сервис Яндекс.Координаты
def coordinates(text):
    Fixer.log('Старт сервиса Yandex.Координаты: ' + text)
    tsend = Yandex.Coordinates(text)
    Fixer.log('Yandex.Координаты ответил: ' + tsend)
    return tsend

# ---------------------------------------------------------
# сервис wiki
def wiki(text, send=False):
    Fixer.log('Старт сервиса Wikipedia: ' + text)
    if send: Bot.SendMessage('Секундочку! Ищу информацию в Википедии...')
    pages = Wiki.SearchPage(text)
    if len(pages) == 0: return 'Я поискал информацию в Википедии, но ничего не нашёл. Можешь уточнить запрос?'
    Fixer.htext = '"https://ru.wikipedia.org/wiki/' + pages[0] + '"'
    Fixer.log('Cервиса Wikipedia ответил: ' + Fixer.htext)
    return Wiki.MiniContent(pages[0])

# ---------------------------------------------------------
# сервис geowiki
def geowiki(text, send=False):
    try:
        text += ' '
        rad = str(text[:text.find(' ',10)])
    except:
        Fixer.errlog('Ошибка в определении радиуса: '+text[:text.find(' ',10)])
        rad = 1000
    Fixer.log('Старт сервиса WikipediaGeo: ' + text)
    if send: Bot.SendMessage('Секундочку! Ищу ближайшие достопримечательности по Википедии...')
    pages = Wiki.GeoSearch(Fixer.X, Fixer.Y, resnom=10, rad=rad)
    if len(pages) == 0 or pages[0] == '#': return 'Я поискал достопримечательности в Википедии, но ничего не нашёл. Может стоит величить радиус поиска?'
    s = 'Нашёл следующие достопримечательности:\n'
    for p in pages:
        s += p + '\n'
    Bot.SendMessage(s)
    Fixer.htext = '"https://ru.wikipedia.org/wiki/' + pages[0] + '"'
    Fixer.log('Cервиса WikipediaGeo ответил: ' + Fixer.htext)
    return Wiki.GeoFirstMe(rad)

# ---------------------------------------------------------
# сервис geowiki1
def geowiki1(text, send=False):
    try:
        text += ' '
        rad = str(text[:text.find(' ',11)])
    except:
        Fixer.errlog('Ошибка в определении радиуса: '+text[:text.find(' ',11)])
        rad = 3000
    Fixer.log('Старт сервиса WikipediaGeo1: ' + text)
    if send: Bot.SendMessage('Секундочку! Ищу ближайшую достопримечательность по Википедии...')
    response = Wiki.GeoFirstMe(rad)
    if response[0] == '#': return 'В радиусе '+str(rad)+' метров не нашёл ни одной достопримечательности :('
    pages = Wiki.GeoSearch(Fixer.X, Fixer.Y, resnom=10, rad=rad)
    Fixer.htext = '"https://ru.wikipedia.org/wiki/' + pages[0] + '"'
    return response

# ---------------------------------------------------------
# сервис google
def google(text, map=False):
    Fixer.log('Старт сервиса Google.Search: ' + text)
    stext = Google.Search(text, bmap=map)
    Fixer.log('Cервис Google.Search ответил: ' + stext)
    if stext[0:6] == '#bug: ':
        Fixer.log('Исправление для следующего цикла: ' + stext)						
    return stext

# ---------------------------------------------------------
# сервис weather
def getcoords(geocity):
    if geocity.upper() == 'LOCATION':
        Fixer.Coords[0] = Fixer.X
        Fixer.Coords[1] = Fixer.Y
        s = 'LOCATION'
    else:
        s = Yandex.Coordinates(geocity)
    print(s)
    return s

# ---------------------------------------------------------
# сервис weather
def weather(text):
    Fixer.log('Старт сервиса Weather: ' + text)
    params = getparams(text)
    s = getcoords(params[0])
    if s[0] == '#': return 'Не удалось распознать город или найти его координаты :( - ' + s
    m = Weather.Forecast(Fixer.Coords[0], Fixer.Coords[1], params[1])
    print(m)
    stext = ''
    if params[2] == 'full': # полный прогноз погоды
        stext = m[17] + '\n\n' + m[18] + '\n\n' + m[19]
    elif params[2] == 'day': # полный прогноз погоды (день)
        stext = m[18]
    elif params[2] == 'night': # полный прогноз погоды (ночь)
        stext = m[19]
    elif params[2] == 'short': # короткий прогноз погоды
        s = 'Температура от ' + m[10] + ' до ' + m[2] + '\n'
        s += 'Днём: ' + m[3] + '\n'
        s += 'Ночью: ' + m[11]
        stext = s
    elif params[2] == 'temp': # температура
        stext = 'Температура от ' + m[10] + ' до ' + m[2] + '\n'
    elif params[2] == 'riseset': # восход и заход солнца
        stext = 'Рассвет: ' + m[0] + '\n'
        stext += 'Закат: ' + m[1]
    elif params[2] == 'cloud': # осадки, облачность
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
    elif params[2] == 'wind': # ветер
        s = 'Днём: ' + m[8]
        s = '\nНочью: ' + m[16]
        stext = s
    elif params[2] == 'sun': # солнце
        stext = 'Днём: ' + m[3] + ', солнечные часы - ' + m[9]
    else: # необрабатываемый случай
        stext = '#problem: {' + params[2] + '}'
    Fixer.log('Cервис Weather ответил: ' + stext)
    if stext[0:6] == '#bug: ':
        Fixer.log('Исправление для следующего цикла: ' + stext)						
    return stext

# ---------------------------------------------------------
# сервис timezone
def timezone(text):
    Fixer.log('Старт сервиса TimeZone: ' + text)
    s = getcoords(text)
    if s[0] == '#': return 'Не удалось распознать город или найти его координаты :( - ' + s
    m = Weather.GetLocation(Fixer.Coords[0], Fixer.Coords[1])
    if m[0][0] == '#': return m[0]
    ss = 'Часовой пояс: '
    if float(m[5]) > 0: ss += '+'
    return ss + m[5]

# ---------------------------------------------------------
# сервис population
def population(text):
    Fixer.log('Старт сервиса Population: ' + text)
    s = getcoords(text)
    if s[0] == '#': return 'Не удалось распознать город или найти его координаты :( - ' + s
    m = Weather.GetLocation(Fixer.Coords[0], Fixer.Coords[1])
    print(m)
    if m[0][0] == '#': return m[0]
    s = 'Население пункта ' + m[2] +' ['+m[1]+'] '+m[3]+' ('+m[4]+') : '+str(m[7])+' чел.'
    return s

# ---------------------------------------------------------
# сервис elevation
def elevation(text):
    Fixer.log('Старт сервиса Elevation: ' + text)
    s = getcoords(text)
    if s[0] == '#': return 'Не удалось распознать город или найти его координаты :( - ' + s
    m = Weather.GetLocation(Fixer.Coords[0], Fixer.Coords[1])
    print(m)
    if m[0][0] == '#': return m[0]
    s = 'Высотная отметка ' + m[2] +' ['+m[1]+'] '+m[3]+' ('+m[4]+') : '+str(m[6])+' метров над уровнем моря'
    return s

# ---------------------------------------------------------
# сервис geodistance
def geodistance(text):
    Fixer.log('Старт сервиса GeoDistance: ' + text)
    params = getparams(text)
    s = getcoords(params[0])
    if s[0] == '#': return 'Не удалось распознать первый город или найти его координаты :( - ' + s
    x = Fixer.Coords[0]; y = Fixer.Coords[1]
    s = getcoords(params[1])
    if s[0] == '#': return 'Не удалось распознать второй город или найти его координаты :( - ' + s
    s = str(round(Geo.Distance(y, x, Fixer.Coords[1], Fixer.Coords[0]))) + ' км по прямой линии'
    return s

# ---------------------------------------------------------
# сервис anecdote
def compliment():
    Fixer.log('Старт сервиса Comliment: ')
    if Fixer.Type == 1:
        stext = random.choice(Fixer.mCompliment)
    else:
        stext = random.choice(Fixer.wCompliment)
    Fixer.log('Cервис Comliment ответил: ' + stext)
    return stext
	
# ---------------------------------------------------------
# сервис anecdote
def anecdote():
    Fixer.log('Старт сервиса Fun.Anecdote: ')
    stext = Fun.Anecdote()
    Fixer.log('Cервис Fun.Anecdote ответил: ' + stext)
    return stext

# ---------------------------------------------------------
# сервис rate
def rate(text):
    Fixer.log('Старт сервиса Rates.Rate: ' + text)
    params = getparams(text)
    if params[0] == 'ALL': # если нужны курсы всех валют
        stext = Fixer.Dialog('rate')
        for val in Fixer.Valutes:
            stext += '\n' + Fixer.Valutes[val] + ' : ' + Rate.RateRubValue(val, params[1], float(params[2])) + ' ' + Fixer.valutes[params[1]]
    else:
        stext = Rate.RateRubValue(params[0], params[1], float(params[2])) + ' ' + Fixer.valutes[params[1]]
        if stext[0] != '#': Fixer.LastValute.append(params[0])
    Fixer.log('Cервис Rates.Rate ответил: ' + stext)
    return stext

# ---------------------------------------------------------
# сервис setrate
def setrate(text):
    Fixer.log('Старт сервиса SetRate: ' + text)
    if Rate.isValute(text) == False: return 'Не знаю такой валюты: ' + text
    Fixer.Valute = text
    return 'Хорошо! Установлена валюта по-умолчанию: ' + Fixer.Valutes[text]

# ---------------------------------------------------------
# сервис notes
def note(text):
    Fixer.log('Старт сервиса Note: ' + text)
    params = getparams(text)
    Fixer.Notes[params[0].upper()] = params[1]
    return Fixer.Dialog('note_section') + params[0].upper()

# ---------------------------------------------------------
# сервис notes
def notes(text):
    Fixer.log('Старт сервиса Notes: ' + text)
    if text.upper() == 'ALL':
        s = Fixer.Dialog('notes_all')
        for snote in Fixer.Notes.values():
            s += '\n' + snote
    else:
        s = Fixer.Dialog('notes_section')+text.upper()
        for snote in Fixer.Notes[text.upper()]:
            s += '\n' + snote
    return s

# ---------------------------------------------------------
# сервис correction
def correction(text):
    Fixer.log('Старт сервиса Correction: ' + text)
    Fixer.NewDialogs[Fixer.strcleaner(Fixer.Query)] = getparams(text, ';')
    Fixer.Save(Fixer.NewDialogs, 'NewDialogs')
    s = '\nНа запрос: ' + Fixer.strcleaner(Fixer.Query)
    for i in getparams(text, ';'):
        s += '\nВариант ответа: '+ i
    Bot.SendAuthor('Уведомление от пользователя ' + Fixer.UserID + s)
    s = Fixer.Dialog('correction') + s
    Fixer.bAI = True; Fixer.Service = 'ai'; Fixer.Conext = False
    return s

# ---------------------------------------------------------
# Основной обработчик пользовательских запросов
# ---------------------------------------------------------
def FormMessage(text):
    cl = 0
    while cl < 3:
        cl += 1
        # Автовключение сервиса
        if text[0] == '#': Fixer.bAI = False # принудительно отключаем ИИ        
        # Включение сервиса принудительной контекстной зависимости
        if Fixer.Context and Fixer.Service != '':
            print('Сработала контекстная зависимость! Включён сервис #' + Fixer.Service)
            text = '#'+Fixer.Service+': ' + text
            if text[0] == '#': Fixer.bAI = False # принудительно отключаем ИИ
        # Проверяем что ИИ отключен правильно (например, для разового запуска сервиса)
        if Fixer.bAI == False: 
            if  Fixer.Service != '':
                if text[0] != '#':
                    print('Разово запущен сервис #' + Fixer.Service)
                    text = '#'+Fixer.Service+': ' + text
            else:
                # непонятно почему отключён ИИ ?
                print('Принудительное включение AI!')
                Fixer.bAI = True # принудительное включение ИИ
        else:
            print('Включён AI!')
            Fixer.Context = False
        if Fixer.bAI: # Если включён ИИ
            response = ai(text)
        else: # Если выключен ИИ
            response = text
            Fixer.bAI = True # Включаем ИИ на тот случай, если произойдёт ошибка
        # Если есть ответ от бота - присылаем юзеру, если нет - ИИ его не понял
        if response:
            # Ищем сервисы для включения #
            if response.find('#') > 0 and response[0] != '#': # Если есть последовательный сервис
                t = response.find('#')
                Bot.SendMessage(response[:t])
                response = response[t:]
            Fixer.log('Сообщение ИИ: ' + response)
            tsend = '*' # проверка на обработку сервисом
            if response[0] == '#': # Признак особой обработки - запуск определённого сервиса
                if Fixer.Service != response[1:response.find(': ')]: # Сброс контекста если вызван другой сервис
                    Fixer.Context = False
                Fixer.Service = response[1:response.find(': ')]
                print('Текущий сервис: {' + Fixer.Service + '}')
                # Запуск сервиса Task (Задача для уведомления пользователя)
                if response[1:7] == 'task: ': tsend = task(response[7:])
                # Запуск сервиса Answer (Диалог с пользователем)
                if response[1:9] == 'answer: ': tsend = answer(response[9:])
                # Запуск сервиса Fixer (информация)
                if response[1:8] == 'fixer: ': tsend = fixer(response[8:])
                # Запуск сервиса Name
                if response[1:7] == 'name: ': tsend = name(response[7:])
                # Запуск сервиса User
                if response[1:6] == 'user-': tsend = user(response[6:])
                # Запуск сервиса Acquaintance
                if response[1:14] == 'acquaintance:': tsend = acquaintance()
                # Запуск сервиса Яндекс.Расписание
                if response[1:12] == 'timetable: ': tsend = timetable(response[12:], send=True)
                # Запуск сервиса Яндекс.Переводчик
                if response[1:12] == 'translate: ': tsend = translate(response[12:])    
                # Запуск сервиса Яндекс поиск объектов
                if response[1:9] == 'object: ': tsend = yaobject(response[9:])
                # Запуск сервиса Яндекс.Координаты
                if response[1:14] == 'coordinates: ': tsend = coordinates(response[14:])
                # Запуск сервиса Wikipedia - поиск информации 
                # #wiki: <название>
                if response[1:7] == 'wiki: ': tsend = wiki(response[7:], send=True)
                # Запуск сервиса Wikipedia - поиск ближайших достопримечательностей 
                # #geowiki: <радиус, метры>
                if response[1:10] == 'geowiki: ': tsend = geowiki(response[10:], send=True)
                # Запуск сервиса Wikipedia - поиск ближайшей достопримечательности
                # #geowiki1: <радиус, метры>
                if response[1:11] == 'geowiki1: ': tsend = geowiki1(response[11:], send=True)
                # Запуск сервиса Wikipedia - поиск дополнительной информации 
                # #wikimore: <название>
                if response[1:12] == 'wiki-more: ':
                    tsend = 'Я бы показал ещё один раздел статьи... Но я пока не умею догружать сервис Wikipedia.org :('
                # Запуск сервиса Google
                if response[1:12] == 'google-map:': tsend = google(text, map=True)
                if response[1:8] == 'google:': tsend = google(text)
                # Запуск сервиса Weather
                if response[1:10] == 'weather: ': tsend = weather(response[10:])
                # Запуск сервиса TimeZone
                if response[1:11] == 'timezone: ': tsend = timezone(response[11:])
                # Запуск сервиса Population
                if response[1:13] == 'population: ': tsend = population(response[13:])
                # Запуск сервиса Elevation
                if response[1:12] == 'elevation: ': tsend = elevation(response[12:])
                # Запуск сервиса GeoDistance
                if response[1:14] == 'geodistance: ': tsend = geodistance(response[14:])
                # Запуск сервиса Fun
                # #Compliment: 
                if response[1:12] == 'compliment:': tsend = compliment()
                # #anecdote: 
                if response[1:10] == 'anecdote:': tsend = anecdote()
                # Запуск сервиса Rate
                # #rate: 
                if response[1:7] == 'rate: ': tsend = rate(response[7:])
                if response[1:7] == 'setrate: ': tsend = setrate(response[10:]) 
                # Запуск локального сервиса Notes
                # #note: 
                if response[1:7] == 'note: ': tsend = note(response[7:])
                if response[1:8] == 'notes: ': tsend = notes(response[8:])
                # сервис геолокации Телеграм
                # #location: <текст>
                if response[1:11] == 'location: ': return '#LOC! ' + response[11:]
                # Сервис корректировки ответов
                if response[1:13] == 'correction: ': tsend = correction(response[13:])
                ### обработка результатов сервисов ###
                Fixer.Query = text # сохраняем последний запрос пользователя
                if tsend == '': tsend = '#problem: null result'
                if tsend[0] == '*': 
                    Fixer.log('Cервис не найден: ' + response[0:response.find(':')])
                    return Fixer.Dialog('no_service') + response #[0:response.find(':')])
                if tsend[0] == '#': # баг или перенаправление на другой сервис
                    return 'Не удалось обработать запрос: ' + tsend
                return tsend           
            else:
                # Если ответ ИИ не требует обработки - отсылаем пользователю
                Fixer.Query = text # сохраняем последний запрос пользователя
                Fixer.log('Ответ пользователю: ' + response)
                Fixer.Service = 'ai'
                return response
        else: # не удалось ответить
            # Не удалось ответить
            s = text
            # Попробуем найти в вики
            if len(text) < 18 and text.find('?') < 0: 
                s = wiki(text)
                if s[0] != '#':
                    return s
                else:
                    Fixer.htext = ''
                    s = text
            # Попробуем найти в поисковике Google
            if len(text) < 40 and text.find('. ') < 0: 
                s = google(text)
                if s[0] != '#':
                    return s
                else:
                    Fixer.htext = ''
            s = Fixer.strcleaner(text)
            # Ищем среди новых диалогов
            for i in Fixer.NewDialogs:
                if i == s: return random.choice(Fixer.NewDialogs[i]) # удалось найти среди новых диалогов
            #Fixer.log('Ответ пользователю: Извини, я тебя не понял...')
            Bot.SendMessage(Fixer.Dialog('null'))
            Fixer.Query = text # сохраняем последний запрос пользователя
            Fixer.Service = 'correction'
            Fixer.bAI = False
            return Fixer.Dialog('new_dialog')
