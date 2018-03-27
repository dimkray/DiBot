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
            #print(user)
            #print(user['first_name'])
            Fixer.Name = user['first_name']
            #print(user['last_name'])
            Fixer.Family = user['last_name']
            if 'about' in user:
                #print('Обо мне: ' + user['about'])
                Fixer.About = user['about']
            if 'activities' in user:
                Fixer.Inteserts.append(user['activities'])
                #print('Деятельность: ' + user['activities'])
            #print('ДР: ' + user['bdate'])
            Fixer.BirthDay = user['bdate']
            if 'books' in user:
                Fixer.Inteserts.append(user['books'])
                #print('Книги: ' + user['books'])
            if 'career' in user:
                if 'company' in user['career']:
                    Fixer.Contacts['компания'] = user['career']['company']
                    #print('Компания: ' + user['career']['company'])
                if 'position' in user['career']:
                    Fixer.Contacts['вакансия'] = user['career']['position']
                    #print('Вакансия: ' + user['career']['position'])
            if 'city' in user:
                Fixer.Contacts['город'] = user['city']['title']
                Processor.coordinates(user['city']['title'])
                Fixer.X = Fixer.Coords[0]
                Fixer.Y = Fixer.Coords[1]
                #print('координаты: ' + Fixer.Y +', '+ Fixer.X)
                #print('город: ' + user['city']['title'])
            if 'connections' in user:
                for connect in user['connections']:
                    Fixer.Contacts[connect] = user['connections'][connect]
                    #print(connect+': '+user['connections'][connect])
            if 'contacts' in user:
                if 'mobile_phone' in user['contacts']:
                    Fixer.Phone = user['contacts']['mobile_phone']
                    #print('Тел.: ' + user['contacts']['mobile_phone'])
                if 'home_phone' in user['contacts']:
                    Fixer.Contacts['телефон'] = user['contacts']['home_phone']
                    #print('Тел.: ' + user['contacts']['home_phone'])
            Fixer.Things.append('Друзья: ' + str(user['counters']['friends']))
            #print('Друзья: ' + str(user['counters']['friends']))
            Fixer.Things.append('Группы: ' + str(user['counters']['pages']))
            #print('Группы: ' + str(user['counters']['pages']))
            Fixer.Contacts['страна'] = user['country']['title']
            #print('Страна: ' + user['country']['title'])
            Fixer.Contacts['VK'] = user['domain']
            #print('Страничка: ' + user['domain'])
            if 'interests' in user:
                m = Processor.params(user['interests'],', ')
                for im in m:
                    Fixer.Inteserts.append(im)
                #print('Интересы: ' + user['interests'])
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
    Fixer.log('Бот пишет: ' + text)
    if Fixer.UserID != Author: SendAuthor('~Уведомление: бот пишет пользователю VK '+Fixer.UserID+': ' + text)
    return True

if __name__ == '__main__':
    Fixer.log('--------------------------------------------')   
    Fixer.log('Запуск VK-Бота')   
    Fixer.log('--------------------------------------------')	
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
                    if text[0] == '~': break # включён тихий режим сообщения
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
                    # Препроцессорный обработчик
                    request = PreProcessor.ReadMessage(text)
                    Fixer.log('Препроцессор ответил: ' + request)
                    # Процессорный обработчик
                    request = Processor.FormMessage(request)
                    Fixer.log('Процессор ответил: ' + request)
                    if request[0] == '#': # Требуется постпроцессорная обработка
                        if request[1:6] == 'LOC! ': # Требуется определить геолокацию
                            # !Доработать блок!
                            request = Fixer.Dialog('no_location')
                        elif request[1:6] == 'bug: ':
                            request =Fixer.Dialog('bug') + '\nКод ошибки: '+request[6:]
                        else:
                            request = 'Что-то пошло не так: '+request
                        SendMessage(request)
                    else: # Постпроцессорная обработка не требуется
                        Fixer.log('Сообщение пользователю: ' + request)
                        if Fixer.Service != '': Fixer.LastService.append(Fixer.Service)
                        SendMessage(request)
                    if Fixer.htext != '': # если есть гипперссылка
                        Fixer.log('Сообщение пользователю: ' + Fixer.htext)
                        Fixer.htext = 'Ссылка: ' + Fixer.htext.replace(' ','%20')
                        SendMessage(Fixer.htext)
                        Fixer.htext = ''
                    Chat.Save()                    
                except Exception as e:
                    SendMessage('Ой! Я чуть не завис :( Есть ошибка в моём коде: ' + str(e))
            Notification.Process() # запуск системы уведомлений
        except Exception as e:
            SendMessage('Ой! Я чуть не завис :( Есть ошибка в моём коде: ' + str(e))  

        time.sleep(1)
