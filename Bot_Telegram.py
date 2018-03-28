# -*- coding: utf-8 -*-
# pip install pytelegrambotapi
# pip install apiai
# pip install geolocation-python
# pip install geopy
# pip install wikipedia
# pip install urllib3
# pip install certifi
# pip install urllib3[secure]

import config
import Fixer
import PreProcessor
import Processor

import telebot
#from geolocation.distance_matrix.client import DistanceMatrixApiClient
from telebot import types
from Services.Yandex import Yandex
from Chats.Chats import Chat

Author = '172009889'
Home = 'Telegram'

bot = telebot.TeleBot(config.token)

def SendAuthor(text):
    try:
        bot.send_message(int(Author), text)
        return True
    except:
        return False

def SendMessage(text):
    if Fixer.ChatID == 0: return False
    text = Fixer.Subs(text)
    bot.send_message(Fixer.ChatID, text)
    Fixer.log('Бот пишет: ' + text)
    if Fixer.UserID != Author: SendAuthor('~Уведомление: бот пишет пользователю TL '+Fixer.UserID+': ' + text)
    return True

###### Обработчик бота ######

@bot.message_handler(commands=["start"])
def start(message):
    Fixer.ChatID = message.chat.id
    Fixer.log('Пользователь запустил команду: ' + message.text)
    if Fixer.UserID != Author: SendAuthor('~Уведомление: пользователь '+Fixer.UserID+' стартовал бот TL!')
    if Fixer.Name == '':
        smes = 'Приветствую Вас! Давайте общаться :)'
    else:
        smes = 'Привет, '+Fixer.Name+'! Я рад продолжить наше общение!'
    SendMessage(smes)
    if Fixer.KnowUser() == 0: 
        smes = 'Для начала предлагаю познакомиться, чтобы узнать друг друга лучше и перейти на "ты" :)\nСогласны?'
        Fixer.Responce = Fixer.responses[0]
        Fixer.Thema = 'Знакомство'
    elif Fixer.KnowUser() < 50:
        smes = 'Предлагаю продолжить наше знакомство!\nХорошо?'
        Fixer.Responce = Fixer.responses[0]
        Fixer.Thema = 'Знакомство'
    else:
        smes = 'Готов к труду и обороне!'
        Fixer.Responce = Fixer.responses[1]
    SendMessage(smes)

@bot.message_handler(commands=["stop"])
def stop(message):
    Fixer.ChatID = message.chat.id
    Fixer.log('Пользователь запустил команду: ' + message.text)
    smes = 'Хорошо! Больше не буду тебя отвлекать.\nЕсли понадаблюсь - просто напиши мне :)'
    #with Fixer:
        # очистка
    bot.send_message(message.chat.id, smes)
    Fixer.log('Бот отвечает: ' + smes)

@bot.message_handler(commands=["help"])
def help(message):
    Fixer.ChatID = message.chat.id
    Fixer.log('Пользователь запустил команду: ' + message.text)
    smes = 'Чуть позже расскажу, что я умею и как мной пользоваться :)'
    bot.send_message(message.chat.id, smes)
    Fixer.log('Бот отвечает: ' + smes)

@bot.message_handler(content_types=["text"])
def default_test(message):
    try:
        if message.text[0]=='~': return True # включён тихий режим сообщения
        Fixer.ChatID = message.chat.id
        Fixer.Time.append(Fixer.time())
        Fixer.Chat.append(message.text)
        if Chat.Load() == False: print('Данные не найдены')
        bot.send_chat_action(Fixer.ChatID, 'typing')
        # Идентификатор юзера
        Fixer.UserID = str(message.from_user.id)
        if Fixer.UserID != Author: SendAuthor('~Уведомление: пользователь TL '+Fixer.UserID+' пишет: ' + message.text)
        # Препроцессорный обработчик
        request = PreProcessor.ReadMessage(message.text)
        Fixer.log('Препроцессор ответил: ' + request)
        # Процессорный обработчик
        request = Processor.FormMessage(request)
        Fixer.log('Процессор ответил: ' + request)
        # Постпроцессорный обработчик
        #if request[0:7] == 'http://': # текст - это гиперссылка
            #ents = []
            #ents[0] = types.MessageEntity('text_link', 0, 100, request)
            #message.entities = ents
            #request = 'Гиперссылка где-то рядом' 
        if request[0] == '#': # Требуется постпроцессорная обработка
            if request[1:6] == 'LOC! ': # Требуется определить геолокацию
                # !Доработать блок!
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                keyboard.add(types.KeyboardButton('Показать где я нахожусь',False,True))
                loc = bot.send_message(message.chat.id, request[6:], reply_markup=keyboard)
                bot.register_next_step_handler(loc, location)
            elif request[1:6] == 'bug: ':
                request = 'При обработке запроса произошла ошибка :(\nКод ошибки: '+request[6:]
            else:
                request = 'Что-то пошло не так: '+request    
        else: # Постпроцессорная обработка не требуется
            # Отправляем сформированое сообщение пользователю
            try:
                Fixer.log('Сообщение пользователю: ' + request)
            except:
                Fixer.log('Сообщение пользователю: (Проблемы с кодировкой!)')
            if Fixer.Service != '': Fixer.LastService.append(Fixer.Service)
            SendMessage(request)
        if Fixer.htext != '': # если есть гипперссылка
            Fixer.log('Сообщение пользователю: ' + Fixer.htext)
            Fixer.htext = Fixer.htext.replace(' ','%20')
            ent = [types.MessageEntity('text_link', 10, 100, url=Fixer.htext)]
            message.entities = ent
            #request = 'Гиперссылка где-то рядом' 
            #bot.send_message(message.chat.id, Fixer.htext)
            SendMessage(Fixer.htext)
            Fixer.htext = ''
        Chat.Save()
    except Exception as e:
        SendMessage('Ой! Я чуть не завис :( Есть ошибка в моём коде: ' + str(e))        

@bot.message_handler(content_types=["location"])
def location(message):
    from geolocation.main import GoogleMaps
    try:
        if Chat.Load() == False: print('Данные не найдены')
        Fixer.X = message.location.longitude
        Fixer.Y = message.location.latitude
        mes = 'Твои координаты: ' + str(Fixer.Y) + ', ' + str(Fixer.X) + '\n'
        Fixer.LastX.append(Fixer.X)
        Fixer.LastY.append(Fixer.Y)
        # Сервис Google.Geocoding
        my_location = GoogleMaps(api_key=config.GMaps_key).search(lat=Fixer.Y, lng=Fixer.X).first()
        mes += my_location.formatted_address #+ '\n'
        Fixer.Address = my_location.formatted_address
        Fixer.LastAddress.append(Fixer.Address)
        SendMessage(mes)
        Chat.Save()
    except Exception as e:
        Fixer.errlog('Ошибка в сервисе Google.Location!: ' + str(e))
        return '#bug: ' + str(e) 

if __name__ == '__main__':
     Fixer.log('--------------------------------------------')   
     Fixer.log('Запуск Telegram-Бота')
     Fixer.log('--------------------------------------------')
     bot.polling(none_stop=True)

