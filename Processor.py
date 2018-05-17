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
from Services.House import Booking
from Services.RSS import RSS
from Chats.Chats import Chat

# получение переменных в массив [] из строки переменных для сервиса
def getparams(text, separator='|'):
    text = text.strip()
    if text.find(separator) < 0 and separator != ';' : # нет текущего сепаратора
        if text.find(' - ') > 0: separator = ' - '
        else:
            if text.find(',') > 0: separator = ','
            else: separator = ' '
    if text.find('[R') >= 0: # Признак радиуса интереса
        poz = text.find('[R')
        end = text.find(']',poz)
        print(text[poz+2,end-1])
        Fixer.Radius = float(text[poz+2,end-1])
        text = text.replace('[R'+text[poz+2,end-1]+']','') # Убираем радуис интереса
    m = text.split(separator)
    x = 0
    for im in m:
        m[x] = im.strip(); # убираем лишние пробелы
        x += 1
    #print(m)
    return m

# Работа с сервисами
# ---------------------------------------------------------
# сервис AI : #ai: всякий бред
def ai(text):
    Fixer.log('Processor.AI', 'Запуск AI')
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
    Fixer.log('Task', text)
    import Notification
    from datetime import date, datetime, timedelta
    tformat = '%Y-%m-%d %H:%M:%S'
    Notification.Tasks = Fixer.LoadB('Tasks')
    params = getparams(text)
    params[0] = params[0].lower()
    if len(params) < 2: params.append(datetime.today().strftime('%H:%M:%S')) # params[1]
    if len(params) < 3: params.append('2') # params[2]
    if len(params) < 4: params.append('NULL') # params[3]
    s = '';
    delta = timedelta(days=1) # дельта по умолчанию - сутки
    if params[0] == 'alarm':
        s = 'Будильник успешно установлен!'
    elif params[0] == 'alarmlater':
        s = 'Отложенное уведомление успешно установлено!'
    elif params[0] == 'rss':
        s = 'Подписка на RSS-канал успешно активирована!'
        delta = timedelta(minutes=1)
    elif params[0] == 'del':
        Fixer.SaveB({}, 'Tasks')
        s = 'Все задания успешно удалены!'
        return s
    elif params[0] == 'all': # показать все задания
        s = 'Список заданий:'
        i = 0
        for itask in Notification.Tasks:
            s += '\n[%i] %s' % ( i, str(itask) )
            i += 1
        if i == 0: s += '\n( список пуст )'
        else: s += '\n\nМожно удалить все задания командой "task-del: all"'
        return s
    else:
        s = 'Неизвестная задача "%s"!' % params[0]
        return s
    m = [] # наполняем массив
    smsg = params[0] +'-'+ str(random.randint(100000, 999999)) # key
    skey = str(Fixer.ChatID) +':'+ smsg
    etime = datetime.strptime(str(date.today())+' '+params[1],tformat) + timedelta(hours=Fixer.TimeZone)
    if etime < datetime.today():
        etime = etime + timedelta(days=1)
    s += '\nНазвание: '+smsg+'\nСообщение\\сервис: '+params[3]+'\nВремя срабатывания: '+str(etime + timedelta(hours=Fixer.TimeZone))+'\nКоличество повторений: '+params[2]
    m.append(Fixer.bNotice) # 0 - вкл/выкл уведомление пользователя
    m.append(etime) # 1 - дата-время срабатывания задачи
    m.append(delta) # 2 - дельта следующего срабатывания / по умолчанию 1 день для alarm
    m.append(int(params[2])) # 3 - количество раз срабатывания (при 0/-1 бесконечный цикл)	
    scode = params[3]
    if params[3].upper() == 'NULL': 
        params[3] = smsg+'\nТы просил меня отправить сообщение в '+str(etime)
        scode = ''
    m.append(params[3]) # 4 - сообщение при уведомлении
    m.append(scode) # 5 - запускаемый сервис	
    Notification.Tasks[skey] = m
    #print(m)
    Fixer.SaveB(Notification.Tasks, 'Tasks') # Сохранение задач
    Fixer.log('Processor.Task', s)
    return s
	
# ---------------------------------------------------------
# сервис Answer : #answer: ответ
def answer(text):
    Fixer.log('Answer')
    if text == 'yes':
        Bot.SendMessage('Отлично!')
        if Fixer.Thema == 'Знакомство':
            Fixer.Service == 'acquaintance'
            tsend = User.Acquaintance()
    elif text == 'no':
        tsend = 'Хорошо. Значит в другой раз.\nГотов помочь, чем смогу!'
        Fixer.Thema == ''
        Fixer.Service == ''
    Fixer.log('Answer', tsend)
    return tsend

# ---------------------------------------------------------
# сервис Name - #name: имя
def name(text):
    Fixer.log('Name')
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
    Fixer.log('Name', s)
    Fixer.Service == ''
    return s

# ---------------------------------------------------------
# сервис User - #user-<param>: значение
def user(text):
    Fixer.log('User')
    tsend = User.Info(text)
    Fixer.log('User', tsend)
    Fixer.Service == ''
    return tsend

# ---------------------------------------------------------
# сервис Acquaintance - #acquaintance:
def acquaintance():
    Fixer.log('Acquaintance')
    tsend = User.Acquaintance()
    Fixer.log('Acquaintance', tsend)
    return tsend

# ---------------------------------------------------------
# сервиса Fixer (информация) #fixer: <Параметр>
def fixer(text):
    Fixer.log('Fixer')
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
    else: return '#bug: неизвестный параметр: ' + s

# ---------------------------------------------------------
# Обработка результатов сервиса Яндекс.Расписание
def FormRasp(s):
    Fixer.log('FormRasp')
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
# сервис Booking : #booking: $geo-city | $checkin | $checkout | $people | $order | $dormitory
def booking(text, send=False):
    Fixer.log('Booking.com')
    from datetime import date
    tformat = '%Y-%m-%d'
    if send: Bot.SendMessage('Секундочку! Ищу подходящее жильё в сервисе Booking.com...')
    params = getparams(text)
    bDorm = True
    if len(params) < 2: params.append('Now')
    if len(params) < 3: params.append('Next')
    if len(params) < 4: params.append('1')
    if len(params) < 5: params.append('price')
    if len(params) < 6: params.append('1')
    if params[1].upper() == 'NOW': date.today().isoformat()
    if params[2].upper() == 'NEXT': str(date.strpdate(params[1],tformat) + 1)
    if params[5] != '1': bDorm = False
    
    mList = Booking.List(params[0], params[1], params[2], people=float(params[3]), order=params[4], dorm=bDorm)
    if mList[0] == '#': return mList
    tsend = 'Найдены следующие варианты:'
    x = 0
    for item in mList:
        x += 1
        if x > 7: continue # только 7 вариантов
        tsend += '\n' + item
    Fixer.log('Booking.com', tsend)
    return tsend

# ---------------------------------------------------------
# сервис Яндекс.Расписание
def timetable(text, send=False):
    Fixer.log('TimeTable')
    if send: Bot.SendMessage('Секундочку! Ищу расписание транспорта в сервисе Яндекс.Расписания...')
    tsend = Yandex.FindRasp(text)
    Fixer.log('Yandex.Rasp', tsend)
    tsend = FormRasp(tsend)
    Fixer.log('FormRasp', tsend)
    if tsend[0] != '#':
        Fixer.LastSt1.append(Fixer.St1)
        Fixer.LastSt2.append(Fixer.St2)
        Fixer.LastTr.append(Fixer.iTr)
    return tsend

# ---------------------------------------------------------
# сервис Яндекс.Переводчик
def translate(text):
    Fixer.log('Translate')
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
    Fixer.log('Translate', ttext + ' | ' + lang1 + ' | ' + lang2)
    tsend = Yandex.Translate(ttext, lang1, lang2)
    Fixer.log('Yandex.Translate', tsend)
    if tsend[0] != '#':
        Fixer.LastLang1.append(Fixer.Lang1)
        Fixer.LastLang2.append(Fixer.Lang2)
    return tsend

# ---------------------------------------------------------
# сервис Яндекс поиск объектов : #object: objName | Radius
def yaobject(text):
    Fixer.log('Yandex.Object', text)
    param = getparams(text)
    ttext = param[0]
    rad = Fixer.Radius
    if len(param) > 1: rad = param[1]
    try:
        drad = int(rad)
    except:
        if rad == 'near': drad = 2
        else: drad = 100
    tsend = Yandex.Objects(ttext, Xloc=Fixer.X, Yloc=Fixer.Y, dr=drad)
    Fixer.log('Yandex.Object', tsend)
    return tsend

# ---------------------------------------------------------
# сервис Яндекс.Координаты : #coordinates: $geo-city
def coordinates(text):
    Fixer.log('Yandex.Координаты')
    if text.strip() == '': text = 'LOCATION'
    tsend = Yandex.Coordinates(text)
    Fixer.log('Yandex.Координаты', tsend)
    return tsend

# ---------------------------------------------------------
# сервис Яндекс.Каталог : #site: type(info/find) - $site/String
def site(text):
    Fixer.log('Yandex.Каталог')
    param = getparams(text)
    if len(param) < 2: return '#bug: Нет второго параметра'
    if param[0].lower() == 'info':
        tsend = Yandex.Catalog(param[1])
    elif param[0].lower() == 'find':
        tsend = Yandex.FindCatalog(param[1])
    else: return '#bug: Параметр "%s" не поддерживается!' % param[0]
    Fixer.log('Yandex.Каталог', tsend)
    return tsend

# ---------------------------------------------------------
# сервис wiki : #wiki: query 
def wiki(text, send=False):
    Fixer.log('Wikipedia')
    if send: Bot.SendMessage('Секундочку! Ищу информацию в Википедии...')
    pages = Wiki.SearchPage(text)
    if len(pages) == 0: return 'Я поискал информацию в Википедии, но ничего не нашёл. Можешь уточнить запрос?'
    Fixer.htext = '"https://ru.wikipedia.org/wiki/' + pages[0] + '"'
    Fixer.log('Wikipedia', Fixer.htext)
    return Wiki.MiniContent(pages[0])
	
# ---------------------------------------------------------
# сервис wiki-more
def wikimore(text):
    Fixer.log('Wikipedia.More', text)
    return Wiki.More(Fixer.Page)
	
# ---------------------------------------------------------
# сервис geowiki : #geowiki: [radius]
def geowiki(text, send=False):
    Fixer.log('WikipediaGeo')
    if text.strip() == '':
        rad = Fixer.Radius
    else:
        try:
            text += ' '
            rad = str(text[:text.find(' ')])
        except:
            Fixer.errlog('WikipediaGeo', 'Ошибка в определении радиуса: '+text[:text.find(' ')])
            rad = 100
    if send: Bot.SendMessage('Секундочку! Ищу ближайшие достопримечательности по Википедии...')
    pages = Wiki.GeoSearch(Fixer.X, Fixer.Y, resnom=10, rad=rad)
    if len(pages) == 0 or pages[0] == '#': return 'Я поискал достопримечательности в Википедии, но ничего не нашёл. Может стоит величить радиус поиска?'
    s = 'Нашёл следующие достопримечательности:\n'
    for p in pages:
        s += p + '\n'
    Bot.SendMessage(s)
    Fixer.htext = '"https://ru.wikipedia.org/wiki/' + pages[0] + '"'
    Fixer.log('WikipediaGeo', Fixer.htext)
    return Wiki.GeoFirstMe(rad)

# ---------------------------------------------------------
# сервис geowiki1 : #geowiki1: [radius]
def geowiki1(text, send=False):
    Fixer.log('WikipediaGeo1')
    if text.strip() == '':
        rad = Fixer.Radius
    else:
        try:
            text += ' '
            rad = str(text[:text.find(' ')])
        except:
            Fixer.errlog('WikipediaGeo1', 'Ошибка в определении радиуса: '+text[:text.find(' ')])
            rad = 100
    if send: Bot.SendMessage('Секундочку! Ищу ближайшую достопримечательность по Википедии...')
    response = Wiki.GeoFirstMe(rad)
    if response[0] == '#': return 'В радиусе '+str(rad)+' метров не нашёл ни одной достопримечательности :('
    pages = Wiki.GeoSearch(Fixer.X, Fixer.Y, resnom=10, rad=rad)
    Fixer.htext = '"https://ru.wikipedia.org/wiki/' + pages[0] + '"'
    Fixer.log('WikipediaGeo1', Fixer.htext)
    return response

# ---------------------------------------------------------
# сервис google.Define : #define: word
def define(text):
    Fixer.log('Google.Define')
    stext = Google.Define(text)
    Fixer.log('Google.Define', stext)					
    return stext

# ---------------------------------------------------------
# сервис google : #google: query
def google(text, map=False):
    Fixer.log('Google.Search')
    stext = Google.Search(text, bmap=map)
    Fixer.log('Google.Search', stext)					
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
        s = Yandex.Coordinates(geocity)
    print(s)
    return s

# ---------------------------------------------------------
# сервис weather : #weather: type:full/short/day/cloud/wind/sun/night/riseset/temp | $geo-city | $date
def weather(text):
    Fixer.log('Weather')
    params = getparams(text)
    #print(params)
    if len(params) < 2: params.append('Location')
    if len(params) < 3: params.append(str(Fixer.Date))
    #print('{%s}' % params[1])
    s = getcoords(params[1])
    #print('{%s}' % s)
    if s[0] == '#': return 'Не удалось распознать город или найти его координаты :( - ' + s
    m = Weather.Forecast(Fixer.Coords[0], Fixer.Coords[1], params[1])
    #print(m)
    if m[0] == '#': return m
    stext = ''
    if params[0] == 'full': # полный прогноз погоды
        stext = m[17] + '\n\n' + m[18] + '\n\n' + m[19]
    elif params[0] == 'day': # полный прогноз погоды (день)
        stext = m[18]
    elif params[0] == 'night': # полный прогноз погоды (ночь)
        stext = m[19]
    elif params[0] == 'short': # короткий прогноз погоды
        s = 'Температура от ' + m[10] + ' до ' + m[2] + '\n'
        s += 'Днём: ' + m[3] + '\n'
        s += 'Ночью: ' + m[11]
        stext = s
    elif params[0] == 'temp': # температура
        stext = 'Температура от ' + m[10] + ' до ' + m[2] + '\n'
    elif params[0] == 'riseset': # восход и заход солнца
        stext = 'Рассвет: ' + m[0] + '\n'
        stext += 'Закат: ' + m[1]
    elif params[0] == 'cloud': # осадки, облачность
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
    elif params[0] == 'wind': # ветер
        s = 'Днём: ' + m[8]
        s = '\nНочью: ' + m[16]
        stext = s
    elif params[0] == 'sun': # солнце
        stext = 'Днём: ' + m[3] + ', солнечные часы - ' + m[9]
    else: # необрабатываемый случай
        stext = '#problem: {' + params[0] + '}'
    Fixer.log('Weather', stext)					
    return stext

# ---------------------------------------------------------
# сервис timezone : #timezone: [$geo-city]
def timezone(text):
    Fixer.log('TimeZone')
    #if text.strip() == '': text = 'Location' - уже есть в getcoords
    s = getcoords(text)
    if s[0] == '#': return 'Не удалось распознать город или найти его координаты :( - ' + s
    m = Weather.GetLocation(Fixer.Coords[0], Fixer.Coords[1])
    if m[0][0] == '#':
        # попытка узнать часовой пояс из Geo
        s = Geo.GetTimezone(Fixer.Coords[0], Fixer.Coords[1])
        #print(s)
        return s
    #ss = 'Часовой пояс: '
    ss = ''
    if float(m[5]) > 0: ss = '+'
    Fixer.log('TimeZone', ss)	
    return ss + m[5]

# ---------------------------------------------------------
# сервис population : #population: [$geo-city]
def population(text):
    Fixer.log('Population')
    #if text.strip() == '': text = 'Location' - уже есть в getcoords
    s = getcoords(text)
    if s[0] == '#': return 'Не удалось распознать город или найти его координаты :( - ' + s
    m = Weather.GetLocation(Fixer.Coords[0], Fixer.Coords[1])
    #print(m)
    if m[0][0] == '#': return m[0]
    s = 'Население пункта ' + m[2] +' ['+m[1]+'] '+m[3]+' ('+m[4]+') : '+str(m[7])+' чел.'
    Fixer.log('Population', s)	
    return s

# ---------------------------------------------------------
# сервис elevation : #elevation: [$geo-city]
def elevation(text):
    Fixer.log('Elevation')
    #if text.strip() == '': text = 'Location'-  - уже есть в getcoords
    s = getcoords(text)
    if s[0] == '#': return 'Не удалось распознать город или найти его координаты :( - ' + s
    m = Weather.GetLocation(Fixer.Coords[0], Fixer.Coords[1])
    print(m)
    if m[0][0] == '#': return m[0]
    s = 'Высотная отметка ' + m[2] +' ['+m[1]+'] '+m[3]+' ('+m[4]+') : '+str(m[6])+' метров над уровнем моря'
    Fixer.log('Elevation', s)	
    return s

# ---------------------------------------------------------
# сервис geodistance : #geodistance: $geo-city1 - [$geo-city2]
def geodistance(text):
    Fixer.log('GeoDistance')
    params = getparams(text)
    if len(params) < 2: params.append('Location')
    s = getcoords(params[0])
    if s[0] == '#': return 'Не удалось распознать первый город или найти его координаты :( - ' + s
    x = Fixer.Coords[0]; y = Fixer.Coords[1]
    s = getcoords(params[1])
    if s[0] == '#': return 'Не удалось распознать второй город или найти его координаты :( - ' + s
    s = str(round(Geo.Distance(y, x, Fixer.Coords[1], Fixer.Coords[0]))) + ' км по прямой линии'
    Fixer.log('GeoDistance', s)
    return s

# ---------------------------------------------------------
# сервис compliment : #compliment:
def compliment():
    Fixer.log('Comliment')
    if Fixer.Type == 1:
        stext = random.choice(Fixer.mCompliment)
    else:
        stext = random.choice(Fixer.wCompliment)
    Fixer.log('Comliment', stext)
    return stext
	
# ---------------------------------------------------------
# сервис anecdote : #anecdote:
def anecdote():
    Fixer.log('Fun.Anecdote')
    stext = Fun.Anecdote()
    Fixer.log('Fun.Anecdote', stext)
    return stext

# ---------------------------------------------------------
# сервис rate
def rate(text):
    Fixer.log('Rates.Rate')
    params = getparams(text)
    if params[0] == 'ALL': # если нужны курсы всех валют
        stext = Fixer.Dialog('rate')
        for val in Fixer.Valutes:
            stext += '\n' + Fixer.Valutes[val] + ' : ' + Rate.RateRubValue(val, params[1], float(params[2])) + ' ' + Fixer.valutes[params[1]]
    else:
        stext = Rate.RateRubValue(params[0], params[1], float(params[2])) + ' ' + Fixer.valutes[params[1]]
        if stext[0] != '#': Fixer.LastValute.append(params[0])
    Fixer.log('Rates.Rate', stext)
    return stext

# ---------------------------------------------------------
# сервис setrate
def setrate(text):
    Fixer.log('SetRate', text)
    if Rate.isValute(text) == False: return 'Не знаю такой валюты: ' + text
    Fixer.Valute = text
    return 'Хорошо! Установлена валюта по-умолчанию: ' + Fixer.Valutes[text]

# ---------------------------------------------------------
# сервис note - #notes: ALL/<Имя раздела> | Текст
def note(text):
    Fixer.log('Note', text)
    params = getparams(text)
    Fixer.Notes[params[0].upper()] = params[1]
    return Fixer.Dialog('note_section') + params[0].upper()

# ---------------------------------------------------------
# сервис notes - #notes: [ALL/<Имя раздела>]
def notes(text):
    text = text.strip()
    Fixer.log('Notes', text)
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
    Fixer.log('SetLocation')
    from geolocation.main import GoogleMaps
    try:
        params = getparams(text, separator=',')
        Fixer.LastX.append(Fixer.X)
        Fixer.LastY.append(Fixer.Y)
        Fixer.Y = params[0]
        Fixer.X = params[1]
        mes = 'Хорошо! Установлены координаты: ' + Fixer.Y + ', ' + Fixer.X + '.\n'
        # Сервис Google.Geocoding
        my_location = GoogleMaps(api_key=config.GMaps_key).search(lat=Fixer.Y, lng=Fixer.X).first()
        mes += my_location.formatted_address #+ '\n'
        Fixer.Address = my_location.formatted_address
        Fixer.LastAddress.append(Fixer.Address)
        return mes
    except Exception as e:
        Fixer.errlog('SetLocation', str(e))
        return '#bug: ' + str(e)
	
# ---------------------------------------------------------
# сервис correction
def correction(text):
    Fixer.log('Correction', text)
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
# сервис date / time / datetime : location - type
def datetime(location, ttype='datetime'):
    Fixer.log('DateTime: %s | %s' % (location, ttype))
    #s = Yandex.Coordinates(location)
    tz = float(timezone(location))
    import datetime
    now = datetime.datetime.utcnow() + datetime.timedelta(hours=tz)
    if ttype == 'time':
        #print('time')
        return now.strftime('%H:%M:%S')
    elif ttype == 'date':
        #print('date')
        return now.strftime('%Y-%m-%d')
    else:
        return now.strftime('%Y-%m-%d %H:%M:%S')

# ---------------------------------------------------------
# сервис log / logerr : число последних записей
def log(snumber, etype='none'):
    Fixer.log('log')
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
        if ilen < number: start = 0
        else: start = ilen - number
        s = ''
        for i in range(start, ilen):
            s += '[%i] %s' % (i, mlog[i])
        return s
    except Exception as e:
        Fixer.errlog('log','Ошибка при загрузке логов: ' + str(e))

# ---------------------------------------------------------
# сервис RSS : #rss: rssurl | numberpost(3)
def rss(text):
    Fixer.log('RSS')
    params = getparams(text)
    params[0] = params[0].lower() # форматирование строки
    if len(params) < 2: params.append('3')
    titles = RSS.GetTitles(params[0])
    if titles['status'] == 'ok':
        stext = '%s\n%s\nЯзык публикации: %s\nАвтор: %s\nСайт: %s' % (titles['title'], titles['subtitle'], titles['lang'], titles['author'], titles['link'])
        posts = RSS.GetPosts(params[0])
        for i in range(0, int(params[1])):
            stext += '\n\n[%s]\n%s\n(%s)\n%s' % (posts[i]['title'], posts[i]['description'], posts[i]['date'], posts[i]['link'])
        Bot.SendMessage(stext)
        brss = True
        for rss in Fixer.RSS:
            if params[0] == rss['rss']: brss = False
        smess = ''
        if brss: # записываем rss-канал
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
            smess = 'RSS-канал "%s" успешно поключен!\nНовости канала будут приходить по мере их поступления.' % titles['title']
            from datetime import datetime, timedelta
            now = (datetime.today() + timedelta(minutes=1)).strftime('%H:%M:%S') # форматирование времени
            task('RSS | ' + now + ' | 0 | #rss-news: ' + params[0])
        else: smess = 'RSS-канал "%s" был сохранён ранее.' % titles['title']

        return smess
    else: return 'указанная ссылка не является RSS-каналом.'

# ---------------------------------------------------------
# сервис RSS-news : #rss-news: rssurl
def rssnews(url):
    Fixer.log('RSS-News')
    url = url.strip().lower() # форматирование строки
    s = '#null' # 'Не удалось найти rss-канал в подписке: ' + url
    oldposts = [] # поиск старых постов
    iRSS = 0
    for rss in Fixer.RSS:
        if url == rss['rss']:
            oldposts = rss['posts']
            s = 'Новости rss-канала "%s":' % rss['title']
            posts = RSS.GetNewPosts(url, oldposts)
            if len(posts) > 0:
                for post in posts:
                    s += '\n\n[%s]\n%s\n(%s)\n%s' % (post['title'], post['description'], post['date'], post['link'])
                    dpost = {} # запись новостей
                    dpost['len'] = len(post['description'])
                    dpost['date'] = post['date']
                    Fixer.RSS[iRSS]['posts'].append(dpost) # добавление в Fixer
                #print(Fixer.RSS)
                Chat.Save()
            else:
                s = '#null'
            break
        iRSS += 1
    return s

# ---------------------------------------------------------
# сервис RSS-all : #rss-all: 
def rssall():
    Fixer.log('RSS-all')
    s = 'Список всех подключённых rss-каналов:'
    iRSS = 0
    for rss in Fixer.RSS:
        s += '\n[%i] %s - %s' % (iRSS, rss['rss'], rss['title'])
        iRSS += 1
    if iRSS == 0: s += '\n( список пуст )'
    else: s += '\n\nМожно удалить лишние каналы командой "rss-del: №"'
    return s

# ---------------------------------------------------------
# сервис RSS-del : #rss-del: №
def rssdel(text):
    Fixer.log('RSS-del')
    text = text.strip() # форматирование строки
    irss = int(text)
    s = 'Удаление канала "%s" прошло успешно!' % Fixer.RSS[irss]['title']
    del(Fixer.RSS[irss])
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
            #Fixer.log('ai', 'Сообщение ИИ: ' + response)
            tsend = '*' # проверка на обработку сервисом
            if response[0] == '#': # Признак особой обработки - запуск определённого сервиса
                if Fixer.Service != response[1:response.find(': ')]: # Сброс контекста если вызван другой сервис
                    Fixer.Context = False
                Fixer.Service = response[1:response.find(': ')]
                #print('Текущий сервис: {' + Fixer.Service + '}')
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
                # Запуск сервиса Booking
                if response[1:9] == 'booking:': tsend = booking(response[9:], send=True) 
                # Запуск сервиса Яндекс.Расписание
                if response[1:12] == 'timetable: ': tsend = timetable(response[12:], send=True)
                # Запуск сервиса Яндекс.Переводчик
                if response[1:12] == 'translate: ': tsend = translate(response[12:])    
                # Запуск сервиса Яндекс поиск объектов
                if response[1:9] == 'object: ': tsend = yaobject(response[9:])
                # Запуск сервиса Яндекс.Координаты
                if response[1:14] == 'coordinates: ': tsend = coordinates(response[14:])
                # Запуск сервиса Яндекс.Каталог
                if response[1:7] == 'site: ': tsend = site(response[7:])
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
                if response[1:12] == 'wiki-more: ': tsend = wikimore(response[12:])
                # Запуск сервиса Google
                if response[1:12] == 'google-map:': tsend = google(text, map=True)
                if response[1:8] == 'google:': tsend = google(text)
                # Запуск сервиса Google.Define
                if response[1:8] == 'define:': tsend = define(response[8:])
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
                # Сервис установки координат
                if response[1:14] == 'setlocation: ': tsend = setlocation(response[14:])
                # Сервис корректировки ответов
                if response[1:13] == 'correction: ': tsend = correction(response[13:])
                # Сервис времени и даты
                if response[1:6] == 'time:': tsend = datetime(response[6:], 'time')
                if response[1:6] == 'date:': tsend = datetime(response[6:], 'date')
                if response[1:10] == 'datetime:': tsend = datetime(response[10:])
                # Сервис логов
                if response[1:5] == 'log:': tsend = log(response[5:])
                if response[1:8] == 'errlog:': tsend = log(response[8:], etype='err')
                # Сервис RSS
                if response[1:5] == 'rss:': tsend = rss(response[5:])
                if response[1:10] == 'rss-news:': tsend = rssnews(response[10:])
                if response[1:9] == 'rss-all:': tsend = rssall()
                if response[1:9] == 'rss-del:': tsend = rssdel(response[9:])
                ### обработка результатов сервисов ###
                Fixer.Query = text # сохраняем последний запрос пользователя
                if tsend == '': tsend = '#problem: null result'
                if tsend == '#null': return '' # для пустых уведомлений
                if tsend[0] == '*': 
                    Fixer.log('Processor', 'Cервис не найден: ' + response[0:response.find(':')])
                    return Fixer.Dialog('no_service') + response #[0:response.find(':')])
                if tsend[0] == '#': # баг или перенаправление на другой сервис
                    if tsend.find('[WinError 10061]') >= 0:
                        tsend = 'удалённый сервер заблокирован. Большая вероятность, что это связано с блокировкой Телеграм :('
                    return 'Не удалось обработать запрос: ' + tsend
                return tsend           
            else:
                # Если ответ ИИ не требует обработки - отсылаем пользователю
                Fixer.Query = text # сохраняем последний запрос пользователя
                Fixer.log('Processor', 'Ответ пользователю: ' + response)
                Fixer.Service = 'ai'
                return response
        else: # не удалось ответить
            # Не удалось ответить
            s = text
            # Попробуем найти в вики
            if len(text) < 25 and text.find('?') < 0: 
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
