# -*- coding: utf-8 -*-

import config
import Fixer
import certifi
import urllib3
import requests
import json
from urllib.parse import urlencode
from urllib.parse import quote
from Services.URLParser import URL

class Google:
    # Сервис получения коротких гиперссылок
    def Shorten(url):
        try:
            req_url = 'https://www.googleapis.com/urlshortener/v1/url?key=' + config.GShort_Key
            payload = {'longUrl': url}
            headers = {'content-type': 'application/json'}
            r = requests.post(req_url, data=json.dumps(payload), headers=headers)
            if r.status_code == requests.codes.ok:      
                data = json.loads(r.text)
                rez = data['id']
            else:
                # Если ошибка - то спец.сообщение с номером ошибки
                rez = '#problem: '+ str(r.status_code)
            return rez
        except Exception as e:
            Fixer.errlog('Ошибка в сервисе Google.Shorten!: ' + str(e))
            return '#bug: ' + str(e)

    def Short(url):
        try:
            #http = 'https://www.googleapis.com/urlshortener/v1/url'
            #payload = {'key': config.GShort_Key, 'longUrl': url} 
            #r = requests.post(http, params=payload)
            post_url = 'https://www.googleapis.com/urlshortener/v1/url'
            payload = {'key': config.GShort_key, 'longUrl': url}
            headers = {'content-type': 'application/json'}
            r = requests.post(post_url, data=json.dumps(payload), headers=headers)
            #client = googl.Googl(config.GShort_Key)
            #r = client.shorten(url)
            if r.status_code == requests.codes.ok:      
                data = r.json()
                rez = data['id']
            else:
                # Если ошибка - то спец.сообщение с номером ошибки
                rez = '#problem: '+ str(r.status_code)
            return rez
        except Exception as e:
            Fixer.errlog('Ошибка в сервисе Google.Short!: ' + str(e))
            return '#bug: ' + str(e)

    # Сервис поиска универсальной карты (с маршрутами или обозначениями)
    def Search(text, bmap=False):
        try:
            data = URL.GetData('https://www.google.ru/search',stext=text,textparam='q',brequest=False)
            if data[0] != '#':
                # поиск карты
                if bmap:
                    ftext = URL.Find(data,'https://maps.google.ru/maps?q=', send='"', ball=False)
                    if ftext[0] != '#':
                        ftext = ftext.replace('%2B','%20')
                        Fixer.htext = ftext #назначаем гиперссылку
                        #Fixer.htext = Google.Short(Fixer.htext) # делаем её короткой
                        # Поиск картинки
                        #start = d.find('/maps/vt/data')
                        #if start > 0: # признак картинки к карте
                        #    end = d.find('"',start)
                        #    ftext = 'https://www.google.ru' + d[start+5:end]
                        #    print(ftext)
                        #    return ftext
                        #else: # если картинки нет
                        return 'Я нашёл ответ! Открывай ниже ссылку!'
                    else:
                        print('#bug: none map')
                # поиск текста
                ftext = URL.Find(data,'href="/search?newwindow', sstart=':', send='+', ball=True)
                #atext = URL.Find(data,' target="_blank">', sstart='>', send='<', ball=True)
                if ftext[0] != '#':
                    s = 'Статья или информация по теме:\n'
                    #s += atext[0]
                    s += ftext[0]
                    data = URL.GetData(ftext[0], brequest=False)
                    if data[0] != '#':
                        text = URL.Find(data,'<p>', sstart='>', send='</p>', ball=True)
                        if text[0] != '#':
                            for ss in text:
                                s += '\n' + ss
                                if len(s) > 500: s += '...'; break
                    i = 1; sl = ''
                    for ss in ftext:
                        i += 1
                        if i > 2: sl += '\n' + ss # '\n' + atext[i-1] + '\n' + ss
                        if i > 8: break
                    Fixer.htext = sl #назначаем гиперссылку
                    return s
                else:
                    print('#bug: none')
                    return '#bug: none'
            else:
                return data
        except Exception as e:
            Fixer.errlog('Ошибка в сервисе Google.Search!: ' + str(e))
            return '#bug: ' + str(e)            
