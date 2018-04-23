# -*- coding: utf-8 -*-
import requests
import json
import config
import Fixer
from Services.Geo import Geo

tformat = '%Y-%m-%d %H:%M:%S'
path = 'rasp-yandex.json'
dir_lang = ["az-ru", "be-bg", "be-cs", "be-de", "be-en", "be-es", "be-fr", "be-it", "be-pl", "be-ro", "be-ru", "be-sr", "be-tr", "bg-be", "bg-ru", "bg-uk", "ca-en", "ca-ru", "cs-be", "cs-en", "cs-ru", "cs-uk", "da-en", "da-ru", "de-be", "de-en", "de-es", "de-fr", "de-it", "de-ru", "de-tr", "de-uk", "el-en", "el-ru", "en-be", "en-ca", "en-cs", "en-da", "en-de", "en-el", "en-es", "en-et", "en-fi", "en-fr", "en-hu", "en-it", "en-lt", "en-lv", "en-mk", "en-nl", "en-no", "en-pt", "en-ru", "en-sk", "en-sl", "en-sq", "en-sv", "en-tr", "en-uk", "es-be", "es-de", "es-en", "es-ru", "es-uk", "et-en", "et-ru", "fi-en", "fi-ru", "fr-be", "fr-de", "fr-en", "fr-ru", "fr-uk", "hr-ru", "hu-en", "hu-ru", "hy-ru", "it-be", "it-de", "it-en", "it-ru", "it-uk", "lt-en", "lt-ru", "lv-en", "lv-ru", "mk-en", "mk-ru", "nl-en", "nl-ru", "no-en", "no-ru", "pl-be", "pl-ru", "pl-uk", "pt-en", "pt-ru", "ro-be", "ro-ru", "ro-uk", "ru-az", "ru-be", "ru-bg", "ru-ca", "ru-cs", "ru-da", "ru-de", "ru-el", "ru-en", "ru-es", "ru-et", "ru-fi", "ru-fr", "ru-hr", "ru-hu", "ru-hy", "ru-it", "ru-lt", "ru-lv", "ru-mk", "ru-nl", "ru-no", "ru-pl", "ru-pt", "ru-ro", "ru-sk", "ru-sl", "ru-sq", "ru-sr", "ru-sv", "ru-tr", "ru-uk", "sk-en", "sk-ru", "sl-en", "sl-ru", "sq-en", "sq-ru", "sr-be", "sr-ru", "sr-uk", "sv-en", "sv-ru", "tr-be", "tr-de", "tr-en", "tr-ru", "tr-uk", "uk-bg", "uk-cs", "uk-de", "uk-en", "uk-es", "uk-fr", "uk-it", "uk-pl", "uk-ro", "uk-ru", "uk-sr", "uk-tr"]
langs = {"АФРИКААНС":"af","АМХАРСКИЙ":"am","АРАБСКИЙ":"ar","АЗЕРБАЙДЖАНСКИЙ":"az","БАШКИРСКИЙ":"ba","БЕЛОРУССКИЙ":"be","БОЛГАРСКИЙ":"bg","БЕНГАЛЬСКИЙ":"bn","БОСНИЙСКИЙ":"bs","КАТАЛАНСКИЙ":"ca","СЕБУАНСКИЙ":"ceb","ЧЕШСКИЙ":"cs","ВАЛЛИЙСКИЙ":"cy","ДАТСКИЙ":"da","НЕМЕЦКИЙ":"de","ГРЕЧЕСКИЙ":"el","ЭМОДЗИ":"emj","АНГЛИЙСКИЙ":"en","ЭСПЕРАНТО":"eo","ИСПАНСКИЙ":"es","ЭСТОНСКИЙ":"et","БАСКСКИЙ":"eu","ПЕРСИДСКИЙ":"fa","ФИНСКИЙ":"fi","ФРАНЦУЗСКИЙ":"fr","ИРЛАНДСКИЙ":"ga","ШОТЛАНДСКИЙ (ГЭЛЬСКИЙ)":"gd","ГАЛИСИЙСКИЙ":"gl","ГУДЖАРАТИ":"gu","ИВРИТ":"he","ХИНДИ":"hi","ХОРВАТСКИЙ":"hr","ГАИТЯНСКИЙ":"ht","ВЕНГЕРСКИЙ":"hu","АРМЯНСКИЙ":"hy","ИНДОНЕЗИЙСКИЙ":"id","ИСЛАНДСКИЙ":"is","ИТАЛЬЯНСКИЙ":"it","ЯПОНСКИЙ":"ja","ЯВАНСКИЙ":"jv","ГРУЗИНСКИЙ":"ka","КАЗАХСКИЙ":"kk","КХМЕРСКИЙ":"km","КАННАДА":"kn","КОРЕЙСКИЙ":"ko","КИРГИЗСКИЙ":"ky","ЛАТЫНЬ":"la","ЛЮКСЕМБУРГСКИЙ":"lb","ЛАОССКИЙ":"lo","ЛИТОВСКИЙ":"lt","ЛАТЫШСКИЙ":"lv","МАЛАГАСИЙСКИЙ":"mg","МАРИЙСКИЙ":"mhr","МАОРИ":"mi","МАКЕДОНСКИЙ":"mk","МАЛАЯЛАМ":"ml","МОНГОЛЬСКИЙ":"mn","МАРАТХИ":"mr","ГОРНОМАРИЙСКИЙ":"mrj","МАЛАЙСКИЙ":"ms","МАЛЬТИЙСКИЙ":"mt","БИРМАНСКИЙ":"my","НЕПАЛЬСКИЙ":"ne","ГОЛЛАНДСКИЙ":"nl","НОРВЕЖСКИЙ":"no","ПАНДЖАБИ":"pa","ПАПЬЯМЕНТО":"pap","ПОЛЬСКИЙ":"pl","ПОРТУГАЛЬСКИЙ":"pt","РУМЫНСКИЙ":"ro","РУССКИЙ":"ru","СИНГАЛЬСКИЙ":"si","СЛОВАЦКИЙ":"sk","СЛОВЕНСКИЙ":"sl","АЛБАНСКИЙ":"sq","СЕРБСКИЙ":"sr","СУНДАНСКИЙ":"su","ШВЕДСКИЙ":"sv","СУАХИЛИ":"sw","ТАМИЛЬСКИЙ":"ta","ТЕЛУГУ":"te","ТАДЖИКСКИЙ":"tg","ТАЙСКИЙ":"th","ТАГАЛЬСКИЙ":"tl","ТУРЕЦКИЙ":"tr","ТАТАРСКИЙ":"tt","УДМУРТСКИЙ":"udm","УКРАИНСКИЙ":"uk","УРДУ":"ur","УЗБЕКСКИЙ":"uz","ВЬЕТНАМСКИЙ":"vi","КОСА":"xh","ИДИШ":"yi","КИТАЙСКИЙ":"zh"}
tr_type = [['САМОЛ','plane', 3],['ПОЕЗД','train', 1],['ЭЛЕКТР','suburban', 1],['АВТОБУС','bus', 2],['ВОДН','water', 4],['ВЕРТОЛ','helicopter', 3]]
trd = {'All':'любой транспорт', 'plane':'самолёт', 'train':'поезд', 'suburban':'электричка', 'bus':'автобус', 'water':'водный транспорт', 'helicopter':'вертолёт'}
mounth = ['ЯНВАРЯ', 'ФЕВРАЛЯ', 'МАРТА', 'АПРЕЛЯ', 'МАЯ', 'ИЮНЯ', 'ИЮЛЯ', 'АВГУСТА', 'СЕНТЯБРЯ', 'ОКТЯБРЯ', 'НОЯБРЯ', 'ДЕКАБРЯ']
trSt = {'': 0, 'unknown': 0, 'train_station': 1, 'platform': 1, 'station': 1, 'bus_station': 2, 'bus_stop': 2, 'airport':3, 'whafr': 4, 'river_port': 4, 'port': 4}

# Загрузка базы городов/станций
try:
    print('Загрузка базы stations.txt...')
    f = open('DB/stations.txt', encoding='utf-8')
    db = []
    for line in f:
        words = line.strip().split(' : ')
        words[0] = words[0].upper() + ' '
        words[0] = words[0].replace('Ё','Е')
        words[1] = words[1].upper()
        words[2] = words[2].upper()
        words[3] = words[3].upper()
        db.append(words)
    f.close()
    print('База успешно загружена!')
except Exception as e:
    Fixer.errlog('Ошибка в сервисе Yandex - при загрузке stations.txt!: ' + str(e))

# Поиск идентификатора языка
def FindLang(slang):
    try:
        if langs[slang.upper()]:
            return langs[slang.upper()]
    except:
        return ''
    return ''

# Функция - есть ли станция/город в базе
def isStation(station):  
    for words in db:
        if station in words[0]:
            return True		
    return False

# Функция - есть ли станция/город в базе
def isStational(station):
    iSt = 0
    for words in db:
        if station == words[0]:
            iSt += 1
    if Fixer.region == '':
        if words[1] != '':
            Fixer.region = words[1]
        elif words[2] != '':
            Fixer.region = words[2]
        elif words[3] != '':
            Fixer.region = words[3]

    return True if iSt > 0 else False

# Функция вариантов станции/города в базе
def eStation(stat):
    if isStational('Г. ' + stat + ' '): 
        return 'Г. ' + stat + ' '
    if isStation('Г. ' + stat + ' '): 
        return 'Г. ' + stat + ' '
    if isStation(stat + ' '): 
        return stat + ' '
    if isStation(stat):
        return stat
    return ''

# Функция поиска станции/города в базе
def FindStation(station):
    db1 = []; db2 = []; st = []
    sstation = ''
    istation = ''
    for words in db:
        if station == words[0]:
            db1.append(words)
    for words in db:
        if station in words[0] and station != words[0]:
             db1.append(words)
    print('Анализ станции/города: ' + station)
    x = 0
    for sg in db1:
        print(str(x) +' - '+ db1[x][0] + ' ' + db1[x][1] + ' ' + db1[x][2] + ' ' + db1[x][3] + ' ' + db1[x][4] )
        x += 1
        if x >= 100:
            print('...')
            break
    if x < 1:
        print('В базе данных не найдены соотвествия :(')
    elif x == 1:
        print('Станция назначена автоматически!')
        istation = db1[0][7]
        Fixer.nameSt = db1[0][0]
        Fixer.LastCoords.append(Fixer.Coords)
        Fixer.Coords = []
        Fixer.Coords.append(db1[0][6])
        Fixer.Coords.append(db1[0][5])
    else:
        print('Регион поиска: ' + Fixer.region)
        for wordz in db1:
            bApp = False
            if Fixer.region != '':
                if Fixer.region in wordz[1] or Fixer.region in wordz[2] or Fixer.region in wordz[3]:
                    db2.append(wordz); bApp = True
            if Fixer.iTr > 0 and trSt[wordz[4]] > 0 and bApp == False:
                if Fixer.iTr == trSt[wordz[4]]:
                    db2.append(wordz)
        if len(db2) > 0:
            print('Фильтрация...')
            x = 0
            for sg in db2:
                print(str(x) +' - '+ db2[x][0] + ' ' + db2[x][1] + ' ' + db2[x][2] + ' ' + db2[x][3] + ' ' + db2[x][4])
                x += 1
            st = db2[0]
        else:
            for wordz in db1:
                if wordz[0][1:3] == 'г.':
                    st = wordz
                    break
            if sstation == '':
                st = db1[0]
        if Fixer.region == '':
            Fixer.region = st[1]
        if Fixer.region == '':
            Fixer.region = st[2]
        if Fixer.region == '':
            Fixer.region = st[3]
        print('Назначена станция: ' + st[0] + '\n' )
        istation = st[7]
        Fixer.nameSt = st[0]
        Fixer.LastCoords.append(Fixer.Coords)		
        Fixer.Coords = []
        Fixer.Coords.append(st[6])
        Fixer.Coords.append(st[5])
    return istation

class Yandex:
    
    # Сервис Яндекс.Расписание
    # Сервис с актуальными расписаниями самолётов, поездов, электричек, автобусов, теплоходов и паромов
    # https://tech.yandex.ru/rasp/

    ##### ОСНОВНОЙ КОД #####

    def FindRasp(s):
        try:
            rez = '#bug: Yandex.Rasp'
            Fixer.iTr = 0
            Fixer.region = ''; Fixer.nameSt = ''
            stime = ''; bnow = True
            st1 = ''; st2 = ''
            from datetime import date, datetime, timedelta

            words = s.strip().split(' ')
            sdate = str(date.today());
            stype = 'All'; x = 0
            for word in words:
                x += 1
                isCon = False
                Uw = word.upper()
                Uw = Uw.replace('Ё','Е')
                Uw = Uw.replace('_',' ')
                # если указан регион поиска
                if Uw[0] == '(':
                    Fixer.region = Uw[1:-1]
                    continue
                # временные параметры
                if Uw == 'СЕЙЧАС':
                    bnow = True
                    sdate = str(date.today()); continue
                if Uw == 'СЕГОДНЯ':
                    bnow = False
                    sdate = str(date.today()); continue
                if Uw == 'ЗАВТРА':
                    bnow = False
                    sdate = str(date.today() + timedelta(days=1)); continue
                if Uw == 'ПОСЛЕЗАВТРА':
                    bnow = False
                    sdate = str(date.today() + timedelta(days=2)); continue
                if Uw == 'ВЧЕРА':
                    bnow = False
                    sdate = str(date.today() - timedelta(days=1)); continue
                if Uw.count('-')>1 or Uw.count('.')>1 or Uw.count('/')>1:
                    bnow = False
                    sdate = Uw 
                    sdate = sdate.replace('.','-')
                    sdate = sdate.replace('/','-')
                    Fixer.trDate = sdate
                    continue
                if Uw.isdigit():
                    m = 0
                    for mou in mounth: 
                        if mou in words[x].upper() and words[x].upper().find(mou) == 0:
                            bnow = False
                            if m < 9:
                                sdate = '2018-0'+ str(m+1) + '-' + Uw
                            else:
                                sdate = '2018-'+ str(m+1) + '-' + Uw
                            isCon = True
                            continue
                        m += 1

                # ключевые признаки
                if Uw == '-' or Uw == '->' or Uw == 'В' or Uw == 'ДО':
                    st1 = eStation(words[x-2].upper())
                    st2 = eStation(words[x].upper())
                    continue
                if Uw == 'ИЗ' or Uw == 'ОТ':
                    st1 = eStation(words[x-2].upper())
                    continue
                if Uw == '<-':
                    st1 = eStation(words[x].upper())
                    st2 = eStation(words[x-2].upper())
                    continue
                for wordz in tr_type: # тип транспорного средства
                    if wordz[0] in Uw: 
                        stype = wordz[1]
                        Fixer.iTr = wordz[2]
                        isCon = True
                        continue
                if isCon:
                    continue
                # Проверяем не город/станция ли это
                if len(Uw) < 4:
                    continue
                if len(st1) > 0 and len(st2) > 0:
                    continue
                if st1 == '':
                    st1 = eStation(Uw)
                    continue
                if st2 == '':
                    st2 = eStation(Uw)
                    continue
            print('Город 1: ' + st1 + ' Город 2:' + st2)
            # Поиск города/станции в базе и сохранение
            if st1 != '' and st2 != '':
                st1 = FindStation(st1)
                Fixer.St1 = Fixer.nameSt
                st2 = FindStation(st2)
                Fixer.St2 = Fixer.nameSt
            else:
                rez = 'В запросе не указана начальная и/или конечная станция/город.\n'
                if st1 != '' or st2 != '':
                    rez += 'Найдена станция/город: '+st1+st2
                return rez
            
            if bnow == True:
                stime = str(datetime.today())

            http = 'https://api.rasp.yandex.net/v3.0/search/'
            payload = {'from': st1, 'to': st2, 'format': 'json', 
                            'lang': 'ru_RU', 
                            'apikey': config.YaRasp_key, 
                            'date': sdate,
                            'transport_types': stype,
                            'limit': '100'} 
            if stype == 'All': del payload['transport_types']

            r = requests.get(http, params=payload)

            sAdd = ' - OK\n' if r.status_code == requests.codes.ok else ' - have a problem'
            if r.status_code != requests.codes.ok:
                return '#problem: ' + str(r.status_code)

            if r.status_code == requests.codes.ok:
                data = r.json()
                # сохранение ответа в файл
                with open('rasp.json', 'w') as f:
                    json.dump(r.json(), f)
                f.close()
                print('Найдено рейсов: ' + str(data['pagination']['total']))
                rez = '%' + str(data['pagination']['total']) + ' Расписание: ' + trd[stype] + ' на дату ' + sdate + ':\n'
                for i in data['segments']:
                    t1 = i['departure']
                    t1 = t1[t1.find('T') + 1:t1.find('+')]
                    etime = datetime.strptime(sdate+' '+t1,tformat)
                    now = datetime.utcnow() + timedelta(hours=Fixer.TimeZone)
                    if stime == '' or now < etime:
                        t1 = t1[:-3]
                        t2 = i['arrival']
                        t2 = t2[t2.find('T') + 1:t2.find('+')]
                        t2 = t2[:-3]
                        no = i['thread']['number'] + ': '
                        title = i['thread']['title'] + ' '
                        dur = str(int((i['duration']%3600)/60)) + ' мин. '
                        if i['duration']//3600>0:
                            dur = str(int(i['duration']//3600)) + ' ч. ' + dur
                        tt = i['thread']['transport_type']
                        prc = ''
                        try:
                            minPrc = 10000000
                            maxPrc = 0
                            for j in i['tickets_info']['places']:
                                if j['price']['whole'] < minPrc: minPrc = j['price']['whole']
                                if j['price']['whole'] > maxPrc: maxPrc = j['price']['whole']
                                if minPrc == maxPrc:
                                    prc = str(maxPrc) +' '+ j['currency']
                                else:
                                    prc = str(minPrc) +'-'+ str(maxPrc) +' '+ j['currency']
                        except:
                            prc = ''            
                        sR = t1 + ' - ' + t2 + ' : ' + trd[tt] + ' ' + no + title + ' : ' + dur + prc + '\n'
                        rez += sR
                        # Добавляем гиперссылку
                rez += '#https://rasp.yandex.ru/search/?fromId='+st1+'&toId='+st2+'&when='+sdate
            return rez
        except Exception as e:
            Fixer.errlog('Ошибка в сервисе Yandex.FindRasp!: ' + str(e))
            return '#bug: ' + str(e)
    
    # Сервис Яндекс.Спеллер
    # Яндекс.Спеллер помогает находить и исправлять орфографические ошибки
    # в русском, украинском или английском тексте. Языковые модели Спеллера
    # включают сотни миллионов слов и словосочетаний.
    # https://tech.yandex.ru/speller/doc/dg/reference/checkText-docpage/
    def Speller(s):
        try:
            rez = '#bug: Yandex.Speller'
            http = 'https://speller.yandex.net/services/spellservice.json/checkText'
            payload = {'text': s, 'options': 4} 
            r = requests.get(http, params=payload)
            if r.status_code == requests.codes.ok:      
                data = r.json()
                rez = ''; x = 0
                for word in data:
                    if word['code'] == 2: # Повтор слова
                        rez += s[x:word['pos']] # вырезаем слово
                        x = word['pos'] + word['len']
                    if word['code'] == 1 or word['code'] == 3: # Неверное употребление прописных и строчных букв
                        if word['s']:
                            rez += s[x:word['pos']] + word['s'][0] # заменяем слово
                            x = word['pos'] + word['len']  
                rez += s[x:]
            else:
                # Если ошибка - то спец.сообщение с номером ошибки
                rez = '#problem: '+ str(r.status_code)
            return rez
        except Exception as e:
            Fixer.errlog('Ошибка в сервисе Yandex.Speller!: ' + str(e))
            return '#bug: ' + str(e)

    # Сервис Яндекс.Переводчик
    def Translate(s, lang1, lang2):
        try:
            rez = ''
            #автоопределение языка
            if lang1 == 'авто':
                http = 'https://translate.yandex.net/api/v1.5/tr.json/detect'
                payload = {'key': config.YaTranc_key, 'text': s, 'hint': 'ru,en,fr,it,de'}
                r = requests.get(http, params=payload)
                if r.status_code == requests.codes.ok:      
                    data = r.json()
                    if data['lang']: lang1 = data['lang']
                else:
                    # Если ошибка - то спец.сообщение с номером ошибки
                    return '#problem: '+ str(r.status_code)
                lang2 = FindLang(lang2)
            else:
                lang1 = FindLang(lang1)
                lang2 = FindLang(lang2)
            dir_tr = lang1 + '-' + lang2
            http = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
            payload = {'key': config.YaTranc_key,
                        'text': s, 'lang': dir_tr, 'options': 1} 
            r = requests.get(http, params=payload)
            if r.status_code == requests.codes.ok:      
                data = r.json()
                rez = data['text'][0]
            else:
                # Если ошибка - то спец.сообщение с номером ошибки
                rez = '#problem: '+ str(r.status_code)
            return rez
        except Exception as e:
            Fixer.errlog('Ошибка в сервисе Yandex.Translate!: ' + str(e))
            return '#bug: ' + str(e)

    # Сервис Яндекс поиск объектов/организаций
    def Objects(text, Xloc=Fixer.X, Yloc=Fixer.Y, dr=10, fix=1):
        try:
            rez = ''
            if Xloc == Yloc == 0: # если координаты не заданы
                Xloc = 37.619955
                Yloc = 55.753767
                rez = 'Не определены координаты старта поиска. Ищу ближайшие объекты от мавзалея :)\nЧтобы поиск можно было осуществлять от текущего местоположения, необходимо включить геолокацию (кнопочка в меню).'
            dxy = dr/55 # преобразование км в угловые расстояния
            http = 'https://search-maps.yandex.ru/v1/'
            payload = { 'apikey': config.YaObj_key,
                        'text': text,
                        'lang': 'ru_RU',
                        'll': str(Xloc) + ',' + str(Yloc), #координаты центра поиска - по умолчанию Геолокация
                        'spn': str(dxy) + ',' + str(dxy), #размер области поиска (протяжённость по долготе и широте)
                        'rspn': fix, #Признак «жесткого» ограничения области поиска, 1 - ограничить поиск
                        'results': 500}                
            r = requests.get(http, params=payload)
            print(payload)
            if r.status_code == requests.codes.ok:      
                Fixer.Obj = []
                data = r.json()
                #print(data)
                for ft in data['features']:
                    if 'CompanyMetaData' in ft['properties']: # Если это организация
                        address = ''; url = ''; cats = ''; tels = ''; hours = ''
                        if 'address' in ft['properties']['CompanyMetaData']:
                            address = ft['properties']['CompanyMetaData']['address']
                        if 'Categories' in ft['properties']['CompanyMetaData']:
                            for cat in ft['properties']['CompanyMetaData']['Categories']:
                                cats += cat['name'] + ', '
                        if 'Phones' in ft['properties']['CompanyMetaData']:
                            for tel in ft['properties']['CompanyMetaData']['Phones']:
                                tels += tel['formatted'] + ', '
                        if 'Hours' in ft['properties']['CompanyMetaData']:
                            hours = ft['properties']['CompanyMetaData']['Hours']['text']
                        if 'url' in ft['properties']['CompanyMetaData']:
                            url = ft['properties']['CompanyMetaData']['url']
                        aft = [True, ft['properties']['CompanyMetaData']['name'],  # название организации
                               address, # полный адрес
                               cats, hours, tels, url,
                               ft['geometry']['coordinates'][0], # Координата X
                               ft['geometry']['coordinates'][1]] # Координата Y
                    else:
                        aft = [False, # признак географического объекта
                               ft['properties']['name'], # Название объекта
                               ft['properties']['GeocoderMetaData']['text'], # Полное название (географический адрес)
                               '','','','',
                               ft['geometry']['coordinates'][0], # Координата X
                               ft['geometry']['coordinates'][1]] # Координата Y
                    Fixer.Obj.append(aft)                
            else:
                return '#problem: ' + str(r.status_code)

            # Обработка результатов поиска
            gObj = 0; oObj = 0
            for i in Fixer.Obj:
                if i[0]: oObj +=1 # число организаций
                else: gObj +=1 # число геогр. объектов				
            sorg = ''; sobj = ''; sand = ''
            if oObj > 0: sorg = str(oObj) + ' организаций/ию'
            if gObj > 0: sobj = str(gObj) + ' географических/ий объект/ов'
            if oObj != 0 and gObj != 0: sand = ' и '
            if oObj == 0 and gObj == 0:
                rez = 'Не нашёл ни одного объекта с названием "'+text+'" в радиусе '+str(dr)+'км :(\nМожет надо указать другие параметры поиска? Либо задать больший радуис поиска, указав дополнительно ...в пределах 500 км, например.'
            print(oObj)
            print(gObj)
            rez = 'Нашёл ' + sorg + sand + sobj + ' в радиусе '+ str(dr) + ' км.\n'
            #print(Fixer.Obj)
            if oObj + gObj > 5: rez += 'Из них будут показаны 5 ближайших:'
            srez = []; dis = 0; stext = ''
            for i in Fixer.Obj:
                if i[0]:
                    stext = 'Организация: '+i[1]+'\nАдрес: '+i[2]+'\nGPS-координаты: '+str(i[8])+','+str(i[7]) + '\n'
                    stext += 'Категории: '+i[3]+'\nЧасы работы: '+i[4]+'\nТелефоны: '+i[5]+'\nURL: '+i[6]
                else: # геогр. объект
                    stext = 'Объект: '+i[1]+'Расположение: '+i[2]+'\nGPS-координаты: '+str(i[8])+','+str(i[7])
                dis = Geo.Distance(Xloc, Yloc, i[7], i[8])
                drez = [dis, stext]
                srez.append(drez)
            srez.sort()
            Fixer.sObj = srez
            x = 1
            for i in srez:
                if x > 5: break
                rez += '\n['+str(x)+'] '+ i[1] + '\n'
                if i[0] > 1:
                    dis = 10 * i[0]
                    dis = int(dis) / 10
                    rez += '  Расстояние до объекта: ' + str(dis) + ' км.'
                else:
                    dis = 100 * i[0]
                    dis = int(dis) * 10
                    rez += '  Расстояние до объекта: ' + str(dis) + ' м.'
                x += 1
            return rez
        except Exception as e:
            Fixer.errlog('Ошибка в сервисе Yandex.Objects!: ' + str(e))
            return '#bug: ' + str(e)

    # Сервис Яндекс.Координаты
    # Яндекс.Координаты возвращает географические координаты города/станции
    def Coordinates(station):
        try:
            s = eStation(station.upper())
            print(s)
            if s == '': return '#problem: 0 station'
            s = FindStation(s)
            if s == '': return '#problem: 0 station'
            if Fixer.Coords[0] == Fixer.Coords[1] == '': return '#poblem: no coordinates'
            return Fixer.Coords[1] + ', ' + Fixer.Coords[0]
        except Exception as e:
            Fixer.errlog('Ошибка в сервисе Yandex.Coordinates!: ' + str(e))
            return '#bug: ' + str(e)
        
