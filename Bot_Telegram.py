# -*- coding: utf-8 -*-
# pip install pytelegrambotapi
# pip install apiai
# pip install geolocation-python
# pip install geopy
# pip install wikipedia
# pip install urllib3
# pip install certifi
# pip install urllib3[secure]
# pip install bs4

import config
import fixer
import PreProcessor
from Processor import Processor

import telebot
# from geolocation.distance_matrix.client import DistanceMatrixApiClient
from telebot import types
from services.Yandex import Ya
from Chats.Chats import Chat

Author = '172009889'
Home = 'Telegram'

bot = telebot.TeleBot(config.TOKEN_TELEGRAM)


def send_author(text: str):
    try:
        bot.send_message(int(Author), text)
        return True
    except:
        return False


def send_message(text: str):
    if config.CHAT_ID == 0: return False
    text = Fixer.insert_substring(text)
    bot.send_message(Fixer.ChatID, text)
    Fixer.log('Bot', text)
    if Fixer.UserID != Author: send_author('~Уведомление: бот пишет пользователю TL ' + Fixer.UserID + ': ' + text)
    return True


###### Обработчик бота ######

@bot.message_handler(commands=["start"])
def start(message):
    config.CHAT_ID = message.chat.id
    Fixer.log('Command', message.text)
    if not config.NAME: message_text = 'Приветствую Вас! Давайте общаться :)'
    else: message_text = f'Привет, {config.NAME}! Я рад продолжить наше общение!'
    send_message(message_text)


@bot.message_handler(commands=["stop"])
def stop(message):
    Fixer.ChatID = message.chat.id
    Fixer.log('Command', message.text)
    smes = 'Хорошо! Больше не буду тебя отвлекать.\nЕсли понадаблюсь - просто напиши мне :)'
    # with Fixer:
    # очистка
    send_message(message.chat.id, smes)
    Fixer.log('Бот отвечает: ' + smes)


@bot.message_handler(commands=["help"])
def help(message):
    Fixer.ChatID = message.chat.id
    Fixer.log('Command', message.text)
    smes = 'Чуть позже расскажу, что я умею и как мной пользоваться :)'
    bot.send_message(message.chat.id, smes)
    Fixer.log('Bot', smes)


@bot.message_handler(content_types=["text"])
def default_test(message):
    try:
        if message.text[0] == '~': return True  # включён тихий режим сообщения
        Fixer.ChatID = message.chat.id
        Fixer.Time.append(Fixer.time_str())
        Fixer.Chat.append(message.text)
        if Chat.Load() == False: print('Данные не найдены')
        bot.send_chat_action(Fixer.ChatID, 'typing')
        # Идентификатор юзера
        Fixer.UserID = str(message.from_user.id)
        if Fixer.UserID != Author: send_author(
            '~Уведомление: пользователь TL ' + Fixer.UserID + ' пишет: ' + message.text)
        # Препроцессорный обработчик
        request = PreProcessor.read_message(message.text)
        Fixer.log('PreProcessor', request)
        # Процессорный обработчик
        request = Processor.message_form(request)
        Fixer.log('Processor', request)
        # Постпроцессорный обработчик
        # if request[0:7] == 'http://': # текст - это гиперссылка
        # ents = []
        # ents[0] = types.MessageEntity('text_link', 0, 100, request)
        # message.entities = ents
        # request = 'Гиперссылка где-то рядом'
        if request[0] == '#':  # Требуется постпроцессорная обработка
            if request[1:6] == 'LOC! ':  # Требуется определить геолокацию
                # !Доработать блок!
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                keyboard.add(types.KeyboardButton('Показать где я нахожусь', False, True))
                loc = bot.send_message(message.chat.id, request[6:], reply_markup=keyboard)
                bot.register_next_step_handler(loc, location)
            elif request[1:6] == 'bug: ':
                request = 'При обработке запроса произошла ошибка :(\nКод ошибки: ' + request[6:]
            else:
                request = 'Что-то пошло не так: ' + request
        else:  # Постпроцессорная обработка не требуется
            # Отправляем сформированое сообщение пользователю
            try:
                Fixer.log('SendMessage', request)
            except:
                Fixer.errlog('SendMessage', 'Проблемы с кодировкой!')
            if Fixer.Service != '': Fixer.LastService.append(Fixer.Service)
            send_message(request)
        if Fixer.HYPERTEXT != '':  # если есть гипперссылка
            Fixer.log('HiperText', Fixer.HYPERTEXT)
            Fixer.HYPERTEXT = Fixer.HYPERTEXT.replace(' ', '%20')
            ent = [types.MessageEntity('text_link', 10, 100, url=Fixer.HYPERTEXT)]
            message.entities = ent
            # request = 'Гиперссылка где-то рядом'
            # bot.send_message(message.chat.id, Fixer.htext)
            send_message(Fixer.HYPERTEXT)
            Fixer.HYPERTEXT = ''
        Chat.Save()
    except Exception as e:
        send_message('Ой! Я чуть не завис :( Есть ошибка в моём коде: ' + str(e))


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
        my_location = GoogleMaps(api_key=config.GOOGLE_MAPS_KEY).search(lat=Fixer.Y, lng=Fixer.X).first()
        mes += my_location.formatted_address  # + '\n'
        Fixer.Address = my_location.formatted_address
        Fixer.LastAddress.append(Fixer.Address)
        send_message(mes)
        Chat.Save()
    except Exception as e:
        Fixer.errlog('Google.Location', str(e))
        return '#bug: ' + str(e)


if __name__ == '__main__':
    Fixer.log('Start', 'Запуск Telegram-Бота', log_type='title')
    send_author('Start DiBot v2.0')
    bot.polling(none_stop=True)
