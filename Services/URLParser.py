# -*- coding: utf-8 -*-
import Fixer
import requests
import certifi
import urllib3
from urllib.parse import urlencode
from urllib.parse import quote

class URL:
    # Возвращает URL
    def GetURL(shttp, stext = '', textparam = '', params = {}):
        try:
            stext = stext.replace(' ','+')
            stext = format(quote(stext))
            if len(params) > 0 or len(textparam) > 0:
                if len(textparam) > 0: params[textparam] = stext
            if len(params) > 0:
                req = ''; x = 0
                for param in params:
                    if params[param] is not str: params[param] = str(params[param])
                    if x != 0: req += '&'
                    req += param +'='+ params[param]
                    x += 1
                shttp += '?'+req             
            return shttp
        except Exception as e:
            Fixer.errlog('Ошибка в сервисе URL.GetURL!: ' + str(e))
            print('#bug: ' + str(e))        
        
    # Получение html/основного текста по запросу
    def GetData(shttp, stext = '', textparam = '', params = {}, brequest = True, bsave = False):
        try:
            stext = stext.replace(' ','+')
            stext = format(quote(stext))
            if len(textparam) > 0: params[textparam] = stext
            status = 0; d = '' # Данные для ответа
            if brequest: # Если через request
                if len(params) > 0:
                    r = requests.get(shttp, params=params)
                else:
                    r = requests.get(shttp)
                status = r.status_code
                if status == requests.codes.ok: d = r.text
            else: # Если через URL
                if len(params) > 0:
                    req = ''; x = 0
                    for param in params:
                        if params[param] is not str: params[param] = str(params[param])
                        if x != 0: req += '&'
                        req += param +'='+ params[param]
                        x += 1
                    shttp += '?'+req       
                http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
                print(shttp)
                r = http.request('GET', shttp)
                status = r.status
                if status == requests.codes.ok: d = r.data.decode('utf-8','ignore')
                
            if status != requests.codes.ok:
                return '#problem: ' + str(r.status_code)
            else:
                if bsave:
                    # Для тестирования
                    with open('url.html','w', encoding='utf-8') as f:
                        f.write(d)
                    f.close()
                return d
        except Exception as e:
            Fixer.errlog('Ошибка в сервисе URL.GetData!: ' + str(e))
            print('#bug: ' + str(e))               

    # Поиск значений в html (если ball то выводится список значений)
    def Find(data, sfind, sstart = '', send = '', ball = True):
        try:
            mtext = []
            start = 0; end = 0
            while start >= 0:
                start = data.find(sfind, start)
                if start > 0: # если есть признак
                    if sstart != '':
                        start = data.find(sstart, start + 1)
                    if send != '':
                        end = data.find(send, start + 1)
                    else: 
                        end = start + len(sfind)
                    ftext = data[start+len(sstart):end]
                    if ftext.find('<') >= 0: continue
                    if ball == False: return ftext
                    mtext.append(ftext)
                else:
                    if len(mtext) == 0: return '#bug: none'
            return mtext
        except Exception as e:
            Fixer.errlog('Ошибка в сервисе URL.Find!: ' + str(e))
            print('#bug: ' + str(e))   
