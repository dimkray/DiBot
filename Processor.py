# -*- coding: utf-8 -*-
"""Процессор - обработчик основных сервисов"""
import random

import config
import fixer
from system.logging import log
from system.string import str_cleaner
from services import DiBot, run
from services.DaData import strData


# ---------------------------------------------------------
# Обработчик сервисов - на вход строка с сервисом (#servicename:)
# ---------------------------------------------------------
def service_process(response):
    """Обработчик сервисов - на вход строка с сервисом (#servicename:)"""
    ser, send = fixer.service_find(response)
    if ser == '':   # не найден сервис в описании
        return '#problem: Сервис {%s} не зарегестрирован!' % config.SERVICE
    # Запуск сервиса Task (Задача для уведомления пользователя)
    if ser == '#task:': text_send = DiBot.task(send)
    # Запуск сервиса Answer (Диалог с пользователем)
    elif ser == '#answer:': text_send = DiBot.answer(send)
    # Запуск сервиса Fixer (информация)
    elif ser == '#fixer:': text_send = DiBot.fixer(send)
    # Запуск сервиса Name
    elif ser == '#name:': text_send = DiBot.name(send)
    # Запуск сервиса User
    elif ser == '#user-age:': text_send = DiBot.user('age', send)
    elif ser == '#user-name:': text_send = DiBot.user('name', send)
    elif ser == '#user-type:': text_send = DiBot.user('type', send)
    elif ser == '#user-birthday:': text_send = DiBot.user('birthday', send)
    elif ser == '#user-family:': text_send = DiBot.user('family', send)
    elif ser == '#user-phone:': text_send = DiBot.user('phone', send)
    elif ser == '#user-email:': text_send = DiBot.user('email', send)
    elif ser == '#user-interest:': text_send = DiBot.user('interest', send)
    elif ser == '#user-contact:': text_send = DiBot.user('contact', send)
    elif ser == '#user-thing:': text_send = DiBot.user('thing', send)
    # Запуск сервиса Acquaintance
    elif ser == '#acquaintance:': text_send = DiBot.acquaintance()
    # Запуск сервиса Booking
    elif ser == '#booking:': text_send = DiBot.booking(send, wait=True)
    # Запуск сервиса Яндекс.Расписание
    elif ser == '#timetable:': text_send = DiBot.timetable(send, wait=True)
    # Запуск сервиса Яндекс.Переводчик
    elif ser == '#translate:': text_send = DiBot.translate(send)
    # Запуск сервиса Яндекс поиск объектов
    elif ser == '#object:': text_send = DiBot.ya_object(send)
    # Запуск сервиса Яндекс.Координаты
    elif ser == '#coordinates:': text_send = DiBot.coordinates(send)
    # Запуск сервиса Яндекс.Каталог
    elif ser == '#site:': text_send = DiBot.site(send)
    # Запуск сервиса Wikipedia - поиск информации
    # #wiki: <название>
    elif ser == '#wiki:': text_send = DiBot.wiki(send, wait=True)
    # Запуск сервиса Wikipedia - поиск ближайших достопримечательностей
    # #geowiki: <радиус, метры>
    elif ser == '#geowiki:': text_send = DiBot.geo_wiki(send, wait=True)
    # Запуск сервиса Wikipedia - поиск ближайшей достопримечательности
    # #geowiki1: <радиус, метры>
    elif ser == '#geowiki1:': text_send = DiBot.geowiki1(send, wait=True)
    # Запуск сервиса Wikipedia - поиск дополнительной информации
    # #wikimore: <название>
    elif ser == '#wiki-more:': text_send = DiBot.wiki_more(send)
    # Запуск сервиса Google
    elif ser == '#google-map:': text_send = DiBot.google(send, map=True)
    elif ser == '#google:': text_send = DiBot.google(send)
    # Запуск сервиса Google.Define
    elif ser == '#define:': text_send = DiBot.define(send)
    # Запуск сервиса Google.Calc
    elif ser == '#calculator:': text_send = DiBot.calc(send)
    # Запуск сервиса Weather
    elif ser == '#weather:': text_send = DiBot.weather(send)
    # Запуск сервиса TimeZone
    elif ser == '#timezone:': text_send = DiBot.timezone(send)
    # Запуск сервиса Population
    elif ser == '#population:': text_send = DiBot.population(send)
    # Запуск сервиса Elevation
    elif ser == '#elevation:': text_send = DiBot.elevation(send)
    # Запуск сервиса GeoDistance
    elif ser == '#geodistance:': text_send = DiBot.geo_distance(send)
    # Запуск сервиса Fun
    # #Compliment:
    elif ser == '#compliment:': text_send = DiBot.compliment()
    # #anecdote:
    elif ser == '#anecdote:': text_send = DiBot.anecdote()
    # Запуск сервиса Rate
    # #rate:
    elif ser == '#rate:': text_send = DiBot.rate(send)
    elif ser == '#setrate:': text_send = DiBot.set_rate(send)
    # Запуск локального сервиса Notes
    # #note:
    elif ser == '#note:': text_send = DiBot.note(send)
    elif ser == '#note-all:': text_send = DiBot.notes(send)
    # сервис геолокации Телеграм
    # #location: <текст>
    elif ser == '#location:': return '#LOC! ' + send
    # Сервис установки координат
    elif ser == '#setlocation:': text_send = DiBot.set_location(send)
    # Сервис корректировки ответов
    elif ser == '#correction:': text_send = DiBot.correction(send)
    # Сервис времени и даты
    elif ser == '#time:': text_send = DiBot.date_time(send, 'time')
    elif ser == '#date:': text_send = DiBot.date_time(send, 'date')
    elif ser == '#datetime:': text_send = DiBot.date_time(send)
    # Сервис логов и багов
    elif ser == '#log:': text_send = DiBot.log(send)
    elif ser == '#errlog:': text_send = DiBot.log(send, etype='err')
    elif ser == '#buglog:': text_send = DiBot.bug_log(send)
    # Сервис RSS
    elif ser == '#rss:': text_send = DiBot.rss(send)
    elif ser == '#rss-news:': text_send = DiBot.rss_news(send)
    elif ser == '#rss-all:': text_send = DiBot.rss_all()
    elif ser == '#rss-del:': text_send = DiBot.rss_del(send)
    # Сервис IATA
    elif ser == '#iata:': text_send = DiBot.iata(send)
    elif ser == '#iata-air:': text_send = DiBot.iata(send, 'airport')
    elif ser == '#iata-city:': text_send = DiBot.iata(send, 'city')
    elif ser == '#code3:': text_send = DiBot.iata(send, 'code3')
    # Сервис информирования о возможностях
    elif ser == '#skill:': text_send = DiBot.skill()
    # Сервис морфологического анализа
    elif ser == '#morph:': text_send = DiBot.morph(send)
    # Спецсервис для кодирования
    elif ser == '#code:': text_send = str(run.code(send))
    # Сервисы DaData
    elif ser == '#dataname:': text_send = strData.Name(send, False)
    elif ser == '#dataaddress:': text_send = strData.Address(send, False)
    elif ser == '#dataorg:': text_send = strData.Organization(send, False, False)
    elif ser == '#dataorgid:':
        print(send)  # !!!
        text_send = strData.Organization(send, True, False)
    elif ser == '#classes:': text_send = run.write_classes()
    elif ser == '#defs:': text_send = run.WriteDefs(send)
    elif ser == '#def:': text_send = run.write_def(send)
    elif ser == '#autotests:': text_send = DiBot.tests()
    elif ser == '#movies:': text_send = DiBot.movies(send)
    elif ser == '#movies-essay:': text_send = DiBot.movies(send)
    elif ser == '#movie:': text_send = DiBot.movie(send)
    elif ser == '#actors:': text_send = DiBot.actors(send)
    elif ser == '#actor:': text_send = DiBot.actor(send)

    # Все остальные случаи
    else: text_send = '#problem: Сервис {%s} не найден!' % config.SERVICE
    return text_send


# ---------------------------------------------------------
# Основной обработчик пользовательских запросов
# ---------------------------------------------------------
def message_form(text):
    import Bot
    times = 0
    while times < 3:
        times += 1
        # Автовключение сервиса
        if text[0] == '#': config.AI = False  # принудительно отключаем ИИ
        # Включение сервиса принудительной контекстной зависимости
        if config.CONTEXT and config.SERVICE != '':
            print('Сработала контекстная зависимость! Включён сервис #' + config.SERVICE)
            text = '#'+config.SERVICE + ': ' + text
            if text[0] == '#': config.bAI = False # принудительно отключаем ИИ
        # Проверяем что ИИ отключен правильно (например, для разового запуска сервиса)
        if not config.AI:
            if config.SERVICE != '':
                if text[0] != '#':
                    print('Разово запущен сервис #' + config.SERVICE)
                    text = '#'+config.SERVICE + ': ' + text
            else:
                # непонятно почему отключён ИИ ?
                print('Принудительное включение AI!')
                config.bAI = True # принудительное включение ИИ
        else:
            print('Включён AI!')
            config.Context = False
        if config.AI:  # Если включён ИИ
            response = DiBot.ai(text)
        else:  # Если выключен ИИ
            response = text
            config.bAI = True  # Включаем ИИ на тот случай, если произойдёт ошибка
        # Если есть ответ от бота - присылаем юзеру, если нет - ИИ его не понял
        if response:
            # Ищем сервисы для включения #
            if response.find('#') > 0 and response[0] != '#':  # Если есть последовательный сервис
                t = response.find('#')
                Bot.SendMessage(response[:t])
                response = response[t:]
            #config.log('ai', 'Сообщение ИИ: ' + response)
            tsend = '*' # проверка на обработку сервисом
            if response[0] == '#' and response[:5] != '#bug:':  # Признак особой обработки - запуск определённого сервиса
                if config.SERVICE != response[1:response.find(': ')]:  # Сброс контекста если вызван другой сервис
                    config.Context = False
                config.Service = response[1:response.find(': ')]
                #print('Текущий сервис: {' + config.Service + '}')
                config.Query = text  # сохраняем последний запрос пользователя
                ### Запуск обработчика сервисов ###
                tsend = service_process(response)
                ### обработка результатов сервисов ###
                if tsend == '': tsend = '#problem: null result'
                if tsend == '#null': return '' # для пустых уведомлений
                try: # проверка на корректность ответа
                    if tsend[0] == '*':
                        log('DiBot', 'Cервис не найден: ' + response[0:response.find(':')])
                        return config.Dialog('no_service') + response #[0:response.find(':')])
                except:
                    tsend = '#bug: responce type [%s] = %s' % (str(type(tsend)),str(tsend))
                return tsend
            else:
                # Если ответ ИИ не требует обработки - отсылаем пользователю
                config.Query = text # сохраняем последний запрос пользователя
                log('DiBot', 'Ответ пользователю: ' + response)
                config.Service = 'ai'
                return response
        else: # не удалось ответить
            # Не удалось ответить
            s = text
            # Попробуем найти в вики
            if len(text) < 20 and text.endswith('?') == False:
                s = DiBot.wiki(text)
                if s[0] != '#':
                    return s
                else:
                    config.HYPERTEXT = ''
                    s = text
            # Попробуем найти в ответах
##            elif text.endswith('?'):
##                s = Web.Otvet(text)
##                if s[0] != '#': return s
            # Попробуем найти в поисковике Google
            s = DiBot.google(text)
            if s[0] != '#':
                return s
            else:
                config.HYPERTEXT = ''
            s = str_cleaner(text)
            # Ищем среди новых диалогов
            for i in fixer.DIALOGS_NEW:
                if i == s: return random.choice(fixer.DIALOGS_NEW[i]) # удалось найти среди новых диалогов
            log('Ответ пользователю: Извини, я тебя не понял...')
            # Bot.SendMessage(config.Dialog('null'))
            config.Query = text # сохраняем последний запрос пользователя
            #config.Service = 'correction'
            config.AI = False
            return fixer.Dialog('null')  # config.Dialog('new_dialog')
