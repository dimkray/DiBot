# -*- coding: utf-8 -*-
# pip install vk_api
# pip install apiai
# pip install geolocation-python
# pip install geopy
# pip install wikipedia
# pip install request
# pip install urllib3
# pip install certifi
# pip install urllib3[secure]
# pip install bs4
# pip install lxml

import config
import Fixer
import time
import vk_api
import PreProcessor
import Processor
import Notification

from Chats.Chats import Chat

Author = '2876041'
Home = 'ВКонтакте'

vk = vk_api.VkApi(token = config.token_VK) #Авторизоваться как сообщество
# vk.auth()

values = {'out': 0,'count': 20,'time_offset': 60}

# Получение информации о пользователе
def GetInfo():
    try:
        response = vk.method('users.get',
                             {'user_ids':Fixer.UserID,'fields':'about,activities,bdate,books,career,city,connections,contacts,counters,country,domain,education,exports,home_town,interests'})
        if response:
            user = response[0]
            Fixer.Name = user['first_name']
            Fixer.Family = user['last_name']
            if 'about' in user:
                Fixer.About = user['about']
            if 'activities' in user:
                Fixer.Inteserts.append(user['activities'])
            Fixer.BirthDay = user['bdate']
            if 'books' in user:
                Fixer.Inteserts.append(user['books'])
            if 'career' in user:
                if 'company' in user['career']:
                    Fixer.Contacts['компания'] = user['career']['company']
                if 'position' in user['career']:
                    Fixer.Contacts['вакансия'] = user['career']['position']
            if 'city' in user:
                Fixer.Contacts['город'] = user['city']['title']
                Processor.coordinates(user['city']['title'])
                Fixer.X = Fixer.Coords[0]
                Fixer.Y = Fixer.Coords[1]
            if 'connections' in user:
                for connect in user['connections']:
                    Fixer.Contacts[connect] = user['connections'][connect]
            if 'contacts' in user:
                if 'mobile_phone' in user['contacts']:
                    Fixer.Phone = user['contacts']['mobile_phone']
                if 'home_phone' in user['contacts']:
                    Fixer.Contacts['телефон'] = user['contacts']['home_phone']
            Fixer.Things.append('Друзья: ' + str(user['counters']['friends']))
            Fixer.Things.append('Группы: ' + str(user['counters']['pages']))
            Fixer.Contacts['страна'] = user['country']['title']
            Fixer.Contacts['VK'] = user['domain']
            if 'interests' in user:
                m = Processor.params(user['interests'],', ')
                for im in m:
                    Fixer.Inteserts.append(im)
            return True
    except Exception as e:
        print('Ошибка доступа к информации пользователя '+Fixer.UserID+': '+str(e))
        return False

def SendAuthor(text):
    try:
        vk.method('messages.send', {'user_id':int(Author),'message':text})
        return True
    except:
        return False

def SendMessage(text): 
    if Fixer.ChatID == 0: return False
    text = Fixer.Subs(text)
    vk.method('messages.send', {'user_id':Fixer.ChatID,'message':text})
    Fixer.log('Bot', text)
    if Fixer.UserID != Author: SendAuthor('~Уведомление: бот пишет пользователю VK '+Fixer.UserID+': ' + text)
    return True

# сервис локации
def location(scoords):
    #from geolocation.main import GoogleMaps
    from Services.Geo import Geo
    try:
        poz = scoords.find(' ')
        Fixer.Y = float(scoords[:poz])
        Fixer.X = float(scoords[poz:])
        Fixer.LastX.append(Fixer.X)
        Fixer.LastY.append(Fixer.Y)
        mes = 'Твои координаты: ' + str(Fixer.Y) + ', ' + str(Fixer.X) + '\n'
        # Сервис Google.Geocoding
        #my_location = GoogleMaps(api_key=config.GMaps_key).search(lat=Fixer.Y, lng=Fixer.X).first()
        #mes += my_location.formatted_address #+ '\n'
        sAdd = Geo.GetAddress(Fixer.Y, Fixer.X)
        mes += sAdd
        Fixer.Address = sAdd
        Fixer.LastAddress.append(Fixer.Address)
        return mes
    except Exception as e:
        Fixer.errlog('Google.Location', str(e))
        return '#bug: ' + str(e) 

if __name__ == '__main__':
    Fixer.log('Start','--------------------------------------------')   
    Fixer.log('Start','Запуск VK-Бота')   
    Fixer.log('Start','--------------------------------------------')	
    # бесконечный цикл проверки
    while True:
        try:
            response = vk.method('messages.get', values)
            #print(response)
            if response['items']:
                values['last_message_id'] = response['items'][0]['id']
                #print(values['last_message_id'])
            for item in response['items']:
                try:
                    print(item)
                    text = item[u'body']
                    if text != '':
                        if text[0] == '~': continue # включён тихий режим сообщения
                    Fixer.ChatID = item[u'user_id']
                    # Идентификатор юзера
                    Fixer.UserID = str(Fixer.ChatID)
                    if Fixer.UserID != Author: SendAuthor('~Уведомление: пользователь TL '+Fixer.UserID+' пишет: ' + text)
                    Fixer.Time.append(Fixer.time())
                    Fixer.Chat.append(text)
                    if Chat.Load() == False:
                        # Получение информации о пользователе
                        GetInfo()
                        print('Данные не найдены')
                    Fixer.Mess = Home
                    # Бот начинает писать текст
                    vk.method('messages.setActivity', {'user_id':Fixer.ChatID, 'type':u'typing'})
                    # Поиск текущей локации пользователя
                    if u'geo' in item:
                        Fixer.Process = 'Bot.GetUserLocation'
                        geo = item[u'geo']
                        s = ''
                        if u'coordinates' in geo:
                            s = location(geo[u'coordinates']) + '\n'
                        if u'place' in geo:
                            if u'country' in geo[u'place']: s += geo[u'place'][u'country'] + ', '
                            if u'city' in geo[u'place']: s += geo[u'place'][u'city']
                        if text == '': SendMessage(s); Chat.Save(); continue
                    # Поиск стикеров и вложений
                    iphoto = 0
                    if u'attachments' in item:
                        Fixer.Process = 'Bot.GetUserAttachments'
                        for att in item[u'attachments']: # иттератор по вложениям
                            if att[u'type'] == u'sticker': # найден стикер
                                SendMessage('Сорян. Я не умею распознавать стикеры.'); continue
                            elif att[u'type'] == u'photo': # найдено фото
                                iphoto += 1
                            else: # другой тип вложения
                                if text == '': SendMessage('В данных типах вложениях я не разбираюсь :('); continue
                    if text == '':
                        #s = 'Пустое сообщение'
                        if iphoto == 1: s = 'Одно фото во вложении. В будующем смогу провести анализ фото :)'
                        elif iphoto > 1: s = 'Найдено '+str(iphoto)+ ' изображений/фото во вложении.'
                        SendMessage(s)
                        continue
                    else:
                        # Препроцессорный обработчик
                        Fixer.Process = 'Bot.PreProcessor'
                        request = PreProcessor.ReadMessage(text)
                        # Процессорный обработчик
                        Fixer.Process = 'Bot.Processor'
                        request = Processor.FormMessage(request)
                        Fixer.log('Processor', request)
                        if request[0] == '#': # Требуется постпроцессорная обработка
                            if request[1:6] == 'LOC! ': # Требуется определить геолокацию
                                # !Доработать блок!
                                request = location(str(Fixer.Y) + ' ' + str(Fixer.X))
                                request += '\nДля определения более точных координаты в VK, прикрепи и отправь мне текущее местоположение на карте.'
                                #request = Fixer.Dialog('no_location')
                            elif request[1:6] == 'bug: ':
                                request = Fixer.Dialog('bug') + '\nКод ошибки: '+request[6:]
                            else:
                                request = 'Что-то пошло не так: '+request
                            Fixer.log('PostProcessor', request)
                            SendMessage(request)
                        else: # Постпроцессорная обработка не требуется
                            if Fixer.Service != '': Fixer.LastService.append(Fixer.Service)
                            SendMessage(request)
                        if Fixer.htext != '': # если есть гипперссылка
                            Fixer.log('HiperText', Fixer.htext)
                            Fixer.htext = 'Ссылка: ' + Fixer.htext.replace(' ','%20')
                            SendMessage(Fixer.htext)
                            Fixer.htext = ''
                    Chat.Save()                    
                except Exception as e:
                    s = str(e)
                    if s.find('[WinError 10061]') >= 0:
                        SendMessage('К сожалению, удалённый сервер заблокирован. Есть большая вероятность, что это связано с блокировкой Telegram :(')
                        Fixer.errlog(Fixer.Process, s)
                    else:
                        SendMessage('Ой! Я чуть не завис :( Есть ошибка в моём коде: ' + s)
                Notification.Process() # запуск системы уведомлений
        except Exception as e:
            SendAuthor('Возникла ошибка: ' + str(e))  
            Fixer.errlog(Fixer.Process, str(e))

        time.sleep(1)
