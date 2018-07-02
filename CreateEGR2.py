# Обновление базы данных ЕГР из открытых источников
import csv
import Fixer
from DB.SQLite import SQL, CSV
from Services.StrMorph import String, Word
from DB.Worker import Worker

Fixer.DB = 'DB/egr2.db'

opf = [None, None]
tOpf = {} # словарь организационно-правовых форм
tDel = [] # Список удалённых таблиц

dOpf = {'АНО':	'АВТОНОМНАЯ НЕКОММЕРЧЕСКАЯ ОРГАНИЗАЦИЯ',
    'АОЗТ':	'АКЦИОНЕРНОЕ ОБЩЕСТВО ЗАКРЫТОГО ТИПА',
    'АО':	'АКЦИОНЕРНОЕ ОБЩЕСТВО',
    'АФКХ':	'АССОЦИАЦИЯ КРЕСТЬЯНСКИХ (ФЕРМЕРСКИХ) ХОЗЯЙСТВ',
    'БФ':	'БЛАГОТВОРИТЕЛЬНЫЙ ФОНД',
    'ГКО':	'ГОРОДСКОЕ КАЗАЧЬЕ ОБЩЕСТВО',
    'ГП':	'ГОСУДАРСТВЕННОЕ ПРЕДПРИЯТИЕ',
    'ГПК':	'ГАРАЖНО-ПОТРЕБИТЕЛЬСКИЙ КООПЕРАТИВ',
    'ГСК':	'ГАРАЖНО-СТРОИТЕЛЬНЫЙ КООПЕРАТИВ',
    'ГУП':	'ГОСУДАРСТВЕННОЕ УНИТАРНОЕ ПРЕДПРИЯТИЕ',
    'ДНП':	'ДАЧНОЕ НЕКОММЕРЧЕСКОЕ ПАРТНЕРСТВО',
    'ДПК':	'ДАЧНЫЙ ПОТРЕБИТЕЛЬСКИЙ КООПЕРАТИВ',
    'ДСПМК':	'ДОРОЖНО-СТРОИТЕЛЬНЫЙ ПРОИЗВОДСТВЕННЫЙ МЕХАНИЗИРОВАННЫЙ КООПЕРАТИВ',
    'ЖК':	'ЖИЛИЩНЫЙ КООПЕРАТИВ',
    'ЖНК':	'ЖИЛИЩНЫЙ НАКОПИТЕЛЬНЫЙ КООПЕРАТИВ',
    'ЖНПК':	'ЖИЛИЩНЫЙ НАКОПИТЕЛЬНЫЙ ПОТРЕБИТЕЛЬСКИЙ КООПЕРАТИВ',
    'ЖСК':	'ЖИЛИЩНО-СТРОИТЕЛЬНЫЙ КООПЕРАТИВ',
    'ЖСПК':	'ЖИЛИЩНЫЙ СТРОИТЕЛЬНЫЙ ПРОИЗВОДСТВЕННЫЙ КООПЕРАТИВ',
    'ЖЭК':	'ЖИЛИЩНО-ЭКСПЛУАТАЦИОННЫЙ КООПЕРАТИВ',
    'ЗАО':	'ЗАКРЫТОЕ АКЦИОНЕРНОЕ ОБЩЕСТВО',
    'ИПК':	'ИНВЕСТИЦИОННЫЙ ПОТРЕБИТЕЛЬСКИЙ КООПЕРАТИВ',
    'ИЧП':	'ИНДИВИДУАЛЬНОЕ ЧАСТНОЕ ПРЕДПРИЯТИЕ',
    'КОЛХОЗ':	'КОЛЛЕКТИВНОЕ ХОЗЯЙСТВО',
    'КПК':	'КРЕДИТНЫЙ ПОТРЕБИТЕЛЬСКИЙ КООПЕРАТИВ',
    'КПКГ':	'КРЕДИТНЫЙ ПОТРЕБИТЕЛЬСКИЙ КООПЕРАТИВ ГРАЖДАН',
    'КСПОК':	'КРЕДИТНЫЙ СЕЛЬСКОХОЗЯЙСТВЕННЫЙ ПОТРЕБИТЕЛЬСКИЙ КООПЕРАТИВ',
    'КФХ':	'КРЕСТЬЯНСКОЕ (ФЕРМЕРСКОЕ) ХОЗЯЙСТВО',
    'КХ':	'КРЕСТЬЯНСКОЕ ХОЗЯЙСТВО',
    'МБДОУ':	'МУНИЦИПАЛЬНОЕ БЮДЖЕТНОЕ ДОШКОЛЬНОЕ ОБРАЗОВАТЕЛЬНОЕ УЧРЕЖДЕНИЕ',
    'МДОУ':	'МУНИЦИПАЛЬНОЕ ДОШКОЛЬНОЕ ОБРАЗОВАТЕЛЬНОЕ УЧРЕЖДЕНИЕ',
    'МЖСК':	'МОЛОДЕЖНЫЙ ЖИЛИЩНО-СТРОИТЕЛЬНЫЙ КООПЕРАТИВ',
    'МКП':	'МАЛОЕ КОЛЛЕКТИВНОЕ ПРЕДПРИЯТИЕ',
    'МКУ':	'МУНИЦИПАЛЬНОЕ КАЗЕННОЕ УЧРЕЖДЕНИЕ',
    'МНТК':	'МЕЖОТРАСЛЕВОЙ НАУЧНО-ТЕХНИЧЕСКИЙ КОЛЛЕКТИВ',
    'МОУ':	'МУНИЦИПАЛЬНОЕ ОБРАЗОВАТЕЛЬНОЕ УЧРЕЖДЕНИЕ',
    'МП':	'МУНИЦИПАЛЬНОЕ ПРЕДПРИЯТИЕ',
    'МПК':	'МЕЖДУНАРОДНЫЙ ПОТРЕБИТЕЛЬСКИЙ КООПЕРАТИВ',
    'МУ':	'МУНИЦИПАЛЬНОЕ УЧРЕЖДЕНИЕ',
    'МУП':	'МУНИЦИПАЛЬНОЕ УНИТАРНОЕ ПРЕДПРИЯТИЕ',
    'НКО':	'НЕКОММЕРЧЕСКАЯ КОРПОРАТИВНАЯ ОРГАНИЗАЦИЯ',
    'НО':	'НЕКОММЕРЧЕСКАЯ ОРГАНИЗАЦИЯ',
    'НПК':	'НАУЧНО-ПРОИЗВОДСТВЕННЫЙ КООПЕРАТИВ',
    'НПМК':	'НАУЧНО-ПРОИЗВОДСТВЕННЫЙ МЕДИЦИНСКИЙ КООПЕРАТИВ',
    'НПП':	'НЕКОММЕРЧЕСКОЕ ПАРТНЕРСТВО ПРЕДПРИНИМАТЕЛЕЙ',
    'НХА':	'НАЦИОНАЛЬНАЯ ХОЗЯЙСТВЕННАЯ АРТЕЛЬ',
    'ОАО':	'ОТКРЫТОЕ АКЦИОНЕРНОЕ ОБЩЕСТВО',
    'ОВС':	'ОБЩЕСТВО ВЗАИМНОГО СТРАХОВАНИЯ',
    'ОО':	'ОБЩЕСТВЕННАЯ ОРГАНИЗАЦИЯ',
    'ООО':	'ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ',
    'ПАО':	'ПУБЛИЧНОЕ АКЦИОНЕРНОЕ ОБЩЕСТВО',
    'ПГК':	'ПОТРЕБИТЕЛЬСКИЙ ГАРАЖНЫЙ КООПЕРАТИВ',
    'ГК':	'ГАРАЖНЫЙ КООПЕРАТИВ',
    'ПГСК':	'ПОТРЕБИТЕЛЬСКИЙ ГАРАЖНО-СТРОИТЕЛЬНЫЙ КООПЕРАТИВ',
    'ПЖСК':	'ПОТРЕБИТЕЛЬСКИЙ ЖИЛИЩНО-СТРОИТЕЛЬНЫЙ КООПЕРАТИВ',
    'ПИК':	'ПОТРЕБИТЕЛЬСКИЙ ИПОТЕЧНЫЙ КООПЕРАТИВ',
    'ПИНК':	'ПОТРЕБИТЕЛЬСКИЙ ИПОТЕЧНО-НАКОПИТЕЛЬНЫЙ КООПЕРАТИВ',
    'ПК':	'ПОТРЕБИТЕЛЬСКИЙ КООПЕРАТИВ',
    'ПК':	'ПРОИЗВОДСТВЕННЫЙ КООПЕРАТИВ',
    'ПКООП':	'ПРОИЗВОДСТВЕННО-КОММЕРЧЕСКАЯ КОРПОРАЦИЯ',
    'ПКФ':	'ПРОИЗВОДСТВЕННАЯ КООПЕРАТИВНАЯ ФИРМА',
    'ПО':	'ПОТРЕБИТЕЛЬСКОЕ ОБЩЕСТВО',
    'ППК':	'ПОТРЕБИТЕЛЬСКИЙ ПОГРЕБНОЙ КООПЕРАТИВ',
    'ПСХК':	'ПРОИЗВОДСТВЕННЫЙ СЕЛЬСКОХОЗЯЙСТВЕННЫЙ КООПЕРАТИВ',
    'ПТКХ':	'ПОЛНОЕ ТОВАРИЩЕСТВО КРЕСТЬЯНСКИХ ХОЗЯЙСТВ',
    'ПТ':	'ПОЛНОЕ ТОВАРИЩЕСТВО',      
    'РА':	'РЫБОЛОВЕЦКАЯ АРТЕЛЬ',
    'РАЙПО':	'РАЙОННОЕ ПОТРЕБИТЕЛЬСКОЕ ОБЩЕСТВО',
    'РК':	'РЫБОЛОВЕЦКИЙ КООПЕРАТИВ',
    'РО':	'РОДОВАЯ ОБЩИНА',
    'РОО':	'РЕГИОНАЛЬНАЯ ОБЩЕСТВЕННАЯ ОРГАНИЗАЦИЯ',
    'РПК':	'РЫБОЛОВЕЦКИЙ ПРОИЗВОДСТВЕННЫЙ КООПЕРАТИВ',
    'РСХА':	'РЫБОЛОВЕЦКАЯ СЕЛЬСКОХОЗЯЙСТВЕННАЯ АРТЕЛЬ',
    'РЫБКОЛХОЗ':	'РЫБОЛОВЕЦКИЙ КОЛХОЗ',
    'СА':	'СЕЛЬСКОХОЗЯЙСТВЕННАЯ АРТЕЛЬ (КОЛХОЗ)',
    'СЕЛЬПО':	'СЕЛЬСКОЕ ПОТРЕБИТЕЛЬСКОЕ ОБЩЕСТВО',
    'СКПК':	'СЕЛЬСКОХОЗЯЙСТВЕННЫЙ КРЕДИТНЫЙ ПОТРЕБИТЕЛЬСКИЙ КООПЕРАТИВ',
    'СМК':	'СТРОИТЕЛЬНО-МОНТАЖНЫЙ КООПЕРАТИВ',
    'СНТ':	'САДОВОДЧЕСКОЕ НЕКОММЕРЧЕСКОЕ ТОВАРИЩЕСТВО',
    'СОВХОЗ':	'СОВМЕСТНОЕ ХОЗЯЙСТВО',
    'СПК':	'САДОВОДЧЕСКИЙ ПОТРЕБИТЕЛЬСКИЙ КООПЕРАТИВ',
    'СПК':	'СЕЛЬСКОХОЗЯЙСТВЕННЫЙ ПОТРЕБИТЕЛЬСКИЙ КООПЕРАТИВ',
    'СППК':	'СЕЛЬСКОХОЗЯЙСТВЕННЫЙ ПОТРЕБИТЕЛЬСКИЙ ПЕРЕРАБАТЫВАЮЩИЙ КООПЕРАТИВ',
    'СППСК':	'СЕЛЬСКОХОЗЯЙСТВЕННЫЙ ПОТРЕБИТЕЛЬСКИЙ ПЕРЕРАБАТЫВАЮЩИЙ СБЫТОВОЙ КООПЕРАТИВ',
    'СПСК':	'СЕЛЬСКОХОЗЯЙСТВЕННЫЙ ПОТРЕБИТЕЛЬСКИЙ СБЫТОВОЙ КООПЕРАТИВ',
    'СПССПК':	'СЕЛЬСКОХОЗЯЙСТВЕННЫЙ ПЕРЕРАБАТЫВАЮЩИЙ СНАБЖЕНЧЕСКО-СБЫТОВОЙ ПОТРЕБИТЕЛЬСКИЙ КООПЕРАТИВ',
    'СРО':	'СЕМЕЙНО-РОДОВАЯ ОБЩИНА',
    'СТ':	'СМЕШАННОЕ ТОВАРИЩЕСТВО',
    'СХПА':	'СЕЛЬСКОХОЗЯЙСТВЕННАЯ ПРОИЗВОДСТВЕННАЯ АРТЕЛЬ',
    'СХПК':	'СЕЛЬСКОХОЗЯЙСТВЕННЫЙ ПРОИЗВОДСТВЕННЫЙ КООПЕРАТИВ',
    'КООП':	'КООПЕРАТИВ ',
    'ТНВ':	'ТОВАРИЩЕСТВО НА ВЕРЕ',
    'ТОО':	'ТОВАРИЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ',
    'ТОС':	'ТЕРРИТОРИАЛЬНОЕ ОБЩЕСТВЕННОЕ САМОУПРАВЛЕНИЕ',
    'ТСЖ':	'ТОВАРИЩЕСТВО СОБСТВЕННИКОВ ЖИЛЬЯ',
    'ТСН':	'ТОВАРИЩЕСТВО СОБСТВЕННИКОВ НЕДВИЖИМОСТИ',
    'ТСО':	'ТЕРРИТОРИАЛЬНО-СОСЕДСКАЯ ОБЩИНА',
    'ХКО':	'ХУТОРСКОЕ КАЗАЧЬЕ ОБЩЕСТВО',
    'ЧОУ':	'ЧАСТНОЕ ОБРАЗОВАТЕЛЬНОЕ УЧРЕЖДЕНИЕ',
    'ЧП':	'ЧАСТНОЕ ПРЕДПРИЯТИЕ',
    'ЧСП':	'ЧАСТНОЕ СЕМЕЙНОЕ ПРЕДПРИЯТИЕ'}

mOpf = ['ИНСПЕКЦИЯ ГОСУДАРСТВЕННОГО НАДЗОРА', 'КОЛЛЕКТИВНЫЙ САД', 'ЖИЛИЩНО-СТРОИТЕЛЬНЫЙ КОМПЛЕКС',
        'КОМИТЕТ ПО ДЕЛАМ МОЛОДЕЖИ', 'КОМИТЕТ ПО УПРАВЛЕНИЮ МУНИЦИПАЛЬНЫМ ИМУЩЕСТВОМ',
        'МУНИЦИПАЛЬНОЕ УЧРЕЖДЕНИЕ КУЛЬТУРЫ', 'ЦЕНТР СОЦИАЛЬНОГО ОБСЛУЖИВАНИЯ',
        'ЦЕНТР ПРАВОВОЙ ПОМОЩИ', 'ДОПОЛНИТЕЛЬНОГО ПРОФЕССИОНАЛЬНОГО ОБРАЗОВАНИЯ',
        'ЦЕНТР СЕРТИФИКАЦИИ']

endOpf = ['АРТЕЛЬ', 'АССОЦИАЦИЯ', 'ИНСПЕКЦИЯ', 'КОЛХОЗ', 'КООПЕРАТИВ', 'КОРПОРАЦИЯ',
          'ОБЩЕСТВО', 'ОБЩИНА', 'ОБЪЕДИНЕНИЕ', 'ОРГАНИЗАЦИЯ', 'ПАРТНЕРСТВО',
          'ПРЕДПРИЯТИЕ', 'СОЮЗ', 'ТОВАРИЩЕСТВО', 'УЧРЕЖДЕНИЕ', 'ФИРМА', 'ФОНД',
          'ХОЗЯЙСТВО', 'ЦЕНТР']

# запись ОПФ
def setOpf(text):
    if opf[0] is not None: opf[1] = text
    elif opf[0] is None: opf[0] = text
    else: return False
    return True

# создание новой записи в таблице ОПФ
def newOpf(text):
    i = 0; rez = -1
    for val in tOpf.values():
        if val == text:
            rez = i
            break
        i += 1
    if rez == -1:
        tOpf[i] = text
        rez = i
    return rez


# основной блок программы
#----------------------------------

items = 100000
block = 1000000

#try:
yn = input('...... Обновить таблицы БД и загрузить новые данные? Y/N: ')
if yn != 'N': 

    # Таблица организаций

    for ib in range(0, 11):
        Worker.ReadBlockCSV('E:/SQL/Dossier/organization.csv', iblock=ib)
        irow = 0
        for row in Worker.mDataCSV:
            row[2] = row[2][:10]
            irow += 1
            if irow % items == 0: print('Обработано %i из %i...' % (irow, len(Worker.mDataCSV)))
        Worker.UpdateBlockCSV('organizations', {
            'id': 'int pk nn u', 'ogrn': 'text nn', 'ogrn_date': 'text', 'inn': 'text', 'kpp': 'text',
        'status_group_id': 'text', 'okved_group_id': 'int', 'okved_codes': 'text', 'region_code': 'int'},
        {'id': 0, 'ogrn': 'Ogrn', 'ogrn_date': 'OgrnDate', 'inn': 'Inn', 'kpp': 'Kpp',
        'status_group_id': 'StatusGroup', 'okved_group_id': 'OkvedGroup', 'okved_codes': 'OkvedCodes', 'region_code': 'RegionCode'})

    # Таблица названий организаций

    for ib in range(0, 15):
        Worker.ReadBlockCSV('E:/SQL/Dossier/organizationname.csv', iblock=ib)
        #mOrgs = []
        iorg = 0
        Worker.mTableCSV.append('Name')
        Worker.mTableCSV.append('Opf1')
        Worker.mTableCSV.append('Opf2')
        Worker.mTableCSV.append('Koef')
        for iOrg in Worker.mDataCSV:
            try:
                iOrg[2] = iOrg[2][:10]
                # Обработка имени
                if iOrg[5] is None: # Оригинал не может быть пустым
                    if iOrg[3] is not None: iOrg[5] = iOrg[3]
                    elif iOrg[4] is not None: iOrg[5] = iOrg[4]
                    else: iOrg[5] = '(без названия)'
                if iOrg[3] is None:  # Имя не может быть пустым
                    if iOrg[4] is not None: iOrg[3] = iOrg[4]
                    else: iOrg[3] = iOrg[5]
                iOrg[3] = iOrg[3].upper().replace('  ',' ').strip()
                name = iOrg[3]
                if iOrg[4] is not None: iOrg[4] = iOrg[4].upper().strip()
                abbr = iOrg[4]

                opf = [None, None]
                sname = name
                words = String.GetWords(name) # наименование без ОПФ
                # поиск ОПФ - dOpf - в начале и в конце строки
                for val in dOpf.values():
                    if val in sname:
                        if name.find(val+' ') == 0 or sname.find(' '+val) == len(sname)-len(val)-1:
                            setOpf(val)
                            sname = sname.replace(val,'').strip()
                            words = String.GetWords(sname)
                            break
                for key in dOpf:
                    if key in words:
                        if key == words[0]:
                            setOpf(dOpf[key])
                            del(words[0])
                            break
                        if key == words[-1]:
                            setOpf(dOpf[key])
                            del(words[-1])
                            break
                # поиск ОПФ - mOpf - в начале и в конце строки
                for iopf in mOpf:
                    if iopf in sname:
                        if sname.find(iopf+' ') == 0 or sname.find(' '+iopf) == len(sname)-len(iopf)-1:
                            setOpf(iopf)
                            sname = sname.replace(iopf,'').strip()
                            words = String.GetWords(sname)
                            break
                            #print('mOpf: ', words)
                # поиск ОПФ - endOpf
                for iopf in endOpf:
                    if iopf in words:
                        sopf = ''
                        end = words.index(iopf); start = 0
                        for i in range(end-1,0,-1):
                            if Word.Type(words[i]) < 2 or Word.Type(words[i]) > 3:
                                start = i + 1; break
                        if start == end: continue
                        for i in range(start, end+1):
                            sopf += words[i]+' '
                        sopf = sopf.strip()
                        for i in range(start, end+1):
                            del(words[start])
                        setOpf(sopf)
                sname = None
                if len(words) > 0:
                    sname = ''
                    cname = String.GetConstr(name)
                    for word in words:
                        try:
                            s = cname[cname.find('['+word+']')+len(word)+2]
                        except: s = ' '
                        sname += word+s
                    sname = sname[:-1]
                iOrg.append(sname) # name
                if opf[0] is not None:
                    iOrg.append(newOpf(opf[0])) # opf1
                else: iOrg.append(None)
                if opf[1] is not None:
                    iOrg.append(newOpf(opf[1])) # opf2
                else: iOrg.append(None)

                # проверка ОПФ - dOpf - в начале и в конце строки
                koef = 0
                if abbr is not None:
                    words2 = String.GetWords(abbr)
                    for key in dOpf:
                        if key in words2:
                            if key == words2[0]:
                                if opf[0] == dOpf[key] or opf[1] == dOpf[key]:
                                    koef += 0.4
                                    name = name.replace(dOpf[key],'')
                                    abbr = abbr.replace(key,'')
                                    del(words2[0])
                                    break
                            if key == words2[-1]:
                                if opf[0] == dOpf[key] or opf[1] == dOpf[key]:
                                    koef += 0.4
                                    name = name.replace(dOpf[key],'')
                                    abbr = abbr.replace(key,'')
                                    del(words2[-1])
                                    break
                    name = name.replace('"','').strip()
                    abbr = abbr.replace('"','').strip()
                    # проверка наименования
                    if name == abbr: koef += 0.6
                    elif words == words2: koef += 0.5
                iOrg.append(koef) # koef
                iorg += 1
                if iorg % items == 0: print('Обработано %i из %i...' % (iorg, len(Worker.mDataCSV)))
            except Exception as e:
                print('!!!Bug - '+str(e)+' : '+str(iOrg))
        
        Worker.UpdateBlockCSV('organizations_name', {'org_id': 'int nn',
            'date': 'text', 'name_full': 'text', 'name_abbr': 'text', 'name': 'text',
            'opf_name1': 'int', 'opf_name2': 'int', 'opf_id': 'int', 'name_original': 'text',
            'old_data': 'int', 'koef': 'float'},
            {'org_id': 'Organization', 'date': 'DT', 'name_full': 'Fullname', 'name_abbr': 'ShortName',
             'name': 'Name', 'opf_name1': 'Opf1', 'opf_name2': 'Opf2', 'opf_id': 'Opf',
             'name_original': 'OriginalName', 'old_data': 'OldData', 'koef': 'Koef'})

    # Отдельно записываем словарь ОПФ
    Worker.UpdateTableDict('dictionary_opf', tOpf)

    # Таблица ОПФ
    Worker.UpdateTableCSV('E:/SQL/Dossier/opf.csv', 'opf',
                          {'id': 'int pk nn u', 'name': 'text', 'code': 'int', 'ref': 'text'},
                          {'id': 0, 'name': 'Name', 'code': 'Code', 'ref': 'Reference'})

    # База адресов

    dAddress = Worker.DictionaryCSV('E:/SQL/Dossier/Address.csv', keycol='Id',
                    mCols=['Postcode', 'RegionCode', 'Area', 'City', 'Town', 'Street', 'KladrCode'])
    dPost = Worker.DictionaryCSV('E:/SQL/Dossier/AddressPostcode.csv', keycol='Id', mCols=['Value'])
    dKladr = Worker.DictionaryCSV('E:/SQL/Dossier/AddressKladr.csv', keycol='Id', mCols=['Value'])
    #dRegion = Worker.DictionaryCSV('E:/SQL/Dossier/AddressRegion.csv', keycol='Id', mCols=['Type', 'Name'])
    dArea = Worker.DictionaryCSV('E:/SQL/Dossier/AddressArea.csv', keycol='Id', mCols=['Type', 'Name'])
    dCity = Worker.DictionaryCSV('E:/SQL/Dossier/AddressCity.csv', keycol='Id', mCols=['Type', 'Name'])
    dTown = Worker.DictionaryCSV('E:/SQL/Dossier/AddressTown.csv', keycol='Id', mCols=['Type', 'Name'])
    dStreet = Worker.DictionaryCSV('E:/SQL/Dossier/AddressStreet.csv', keycol='Id', mCols=['Type', 'Name'])

    for ib in range(0, 7):
        Worker.ReadBlockCSV('E:/SQL/Dossier/AddressBuilding.csv', symb='', iblock=ib)
        Worker.mTableCSV.append('Kladr')
        Worker.mTableCSV.append('Postcode')
        Worker.mTableCSV.append('RegionCode')
        Worker.mTableCSV.append('AreaType')
        Worker.mTableCSV.append('AreaName')
        Worker.mTableCSV.append('CityType')
        Worker.mTableCSV.append('CityName')
        Worker.mTableCSV.append('TownType')
        Worker.mTableCSV.append('TownName')
        Worker.mTableCSV.append('StreetType')
        Worker.mTableCSV.append('StreetName')
    
        irow = 0
        for row in Worker.mDataCSV:
            if row[1] in dAddress:
                if row[2] is not None:
                    row[2] = row[2].upper()
                if row[3] is not None:
                    row[3] = row[3].upper()
                Id = dAddress[row[1]][6] # Kladr
                if Id is not None and Id in dKladr: 
                    row.append(dKladr[Id])
                else:
                    row.append(None)
                Id = dAddress[row[1]][0] # Postcode
                if Id is not None and Id in dPost: 
                    row.append(dPost[Id])
                else:
                    row.append(None)
                row.append(dAddress[row[1]][1]) # RegionCode
                Id = dAddress[row[1]][2] # id Area
                if Id is not None and Id in dArea:
                    row.append(dArea[Id][0].upper())
                    row.append(dArea[Id][1].upper())
                else:
                    row.append(None)
                    row.append(None)
                Id = dAddress[row[1]][3] # id City
                if Id is not None and Id in dArea: 
                    row.append(dCity[Id][0].upper())
                    row.append(dCity[Id][1].upper())
                else:
                    row.append(None)
                    row.append(None)
                Id = dAddress[row[1]][4] # id Town
                if Id is not None and Id in dTown: 
                    row.append(dTown[Id][0].upper())
                    row.append(dTown[Id][1].upper())
                else:
                    row.append(None)
                    row.append(None)
                Id = dAddress[row[1]][5] # id Street
                if Id is not None and Id in dStreet: 
                    row.append(dStreet[Id][0].upper())
                    row.append(dStreet[Id][1].upper())
                else:
                    row.append(None)
                    row.append(None)
            else:
                row.append(None)
                row.append(None)
                row.append(None)
                row.append(None)
                row.append(None)
                row.append(None)
                row.append(None)
                row.append(None)
                row.append(None)
                row.append(None)
                row.append(None)
                print('Не найден address_id = ' + row[1])
            irow += 1
            if irow % items == 0: print('Обработано %i из %i...' % (irow, len(Worker.mDataCSV)))
        Worker.UpdateBlockCSV('address', {
            'id': 'int pk nn u', 'region_code': 'int',
            'area_type': 'text', 'area_name': 'text',
            'city_type': 'text', 'city_name': 'text',
            'settlement_type': 'text', 'settlement_name': 'text',
            'street_type': 'text', 'street_name': 'text',
            'house': 'text', 'building': 'text',
            'postcode': 'text', 'kladr': 'text'},
        {'id': 0, 'region_code': 'RegionCode',
            'area_type': 'AreaType', 'area_name': 'AreaName',
            'city_type': 'CityType', 'city_name': 'CityName',
            'settlement_type': 'TownType', 'settlement_name': 'TownName',
            'street_type': 'StreetType', 'street_name': 'StreetName',
            'house': 'House', 'building': 'Building',
            'postcode': 'Postcode', 'kladr': 'Kladr'})

    for ib in range(0, 24):
        Worker.ReadBlockCSV('E:/SQL/Dossier/OrganizationAddress.csv', symb='', iblock=ib)
        irow = 0
        for row in Worker.mDataCSV:
            if row[1] is not None:
                row[1] = row[1][:10]
            if row[4] is not None:
                row[4] = row[4].upper()
            irow += 1
            if irow % items == 0: print('Обработано %i из %i...' % (irow, len(Worker.mDataCSV)))
        Worker.UpdateBlockCSV('organizations_address',
            {'organization_id': 'int nn', 'date': 'text', 
             'address_id': 'int nn', 'flat': 'text', 'address_error': 'int', 'old_data': 'int'},
            {'organization_id': 'Organization', 'date': 'DT',
             'address_id': 'AddressBuilding', 'flat': 'Flat',
             'address_error': 'AddressError', 'old_data': 'OldData'})
        

##    # База статусов
##
##    for ib in range(0, 22): # organization
##        Worker.ReadBlockCSV('DS/organizationstatus.csv', iblock=ib)
##        irow = 0
##        for row in Worker.mDataCSV:
##            row[1] = row[1][:10]
##            irow += 1
##            if irow % items == 0: print('Обработано %i из %i...' % (irow, len(Worker.mDataCSV)))       
##        Worker.UpdateBlockCSV('organizations_status',
##            {'org_id': 'int pk nn u', 'date': 'text', 'code': 'int', 'name': 'text'}, blocks=7)

##    # База ОКВЭДов
##
##    Worker.UpdateTableCSV('DB/organization_okved.csv', 'organizations_okved',
##            {'organization_id': 'int nn', # 'id': 'int pk nn u', 
##            'version_date': 'text', 'grn': 'text', 'grn_date': 'text', 'okved_id': 'int'}, blocks=113)
##
##    # Словарь ОКВЭДов
##
##    Worker.ReadBlockCSV('DB/okved.csv')
##    for row in Worker.mDataCSV:
##        row[1] = row[1].strip() # code
##        row[2] = row[2].upper() # name
##    Worker.UpdateBlockCSV('dictionary_okved',
##        {'id': 'int pk nn u', 'code': 'text nn', 'name': 'text nn', 'group_id': 'int nn', 'version': 'int nn'})
##    
##    # Словарь групп ОКВЭДов
##
##    Worker.UpdateTableCSV('DB/okved_group.csv', 'dictionary_okved_group',
##        {'id': 'int pk nn u', 'name': 'text nn'})
##    
##    # База учредителей
##
##    for ib in range(0, 2): # organization
##        Worker.ReadBlockCSV('DB/organization_founder_org.csv', iblock=ib)
##        irow = 0
##        for row in Worker.mDataCSV:
##            row[4] = row[4].upper()
##            irow += 1
##            if irow % items == 0: print('Обработано %i из %i...' % (irow, len(Worker.mDataCSV)))       
##        Worker.UpdateBlockCSV('organization_founder_org', {# 'id': 'int pk nn u', 
##            'organization_id': 'int nn', 'version_date': 'text', 'grn': 'text', 'grn_date': 'text',
##            'name': 'text', 'ogrn': 'text', 'inn': 'text',
##            'founder_organization_id': 'int', 'capital_percent': 'float', 'capital_size': 'int'},
##            {'organization_id': 'organization_id', 'version_date': 'version_date', 'grn': 'grn',
##            'grn_date': 'grn_date', 'name': 'name', 'ogrn': 'ogrnul', 'inn': 'innul',
##            'founder_organization_id': 'founder_organization_id',
##            'capital_percent': 'capital_percent', 'capital_size': 'capital_size'})
##
##    # organization foreign
##    Worker.ReadBlockCSV('DB/organization_foreign.csv')
##    for row in Worker.mDataCSV:
##        row[4] = row[4].upper()    
##    Worker.UpdateBlockCSV('organization_founder_org', {# 'id': 'int pk nn u', 
##        'organization_id': 'int nn', 'version_date': 'text', 'grn': 'text', 'grn_date': 'text',
##        'name': 'text', 'ogrn': 'text', 'inn': 'text',
##        'founder_organization_id': 'int', 'capital_percent': 'float', 'capital_size': 'int'},
##        {'organization_id': 'organization_id', 'version_date': 'version_date', 'grn': 'grn',
##        'grn_date': 'grn_date', 'name': 'name', 'ogrn': 'ogrnul', 'inn': 'innul',
##        'founder_organization_id': 'founder_organization_id',
##        'capital_percent': 'capital_percent', 'capital_size': 'capital_size'})
##
##    for ib in range(0, 15): # person
##        Worker.ReadBlockCSV('DB/organization_founder_per.csv', iblock=ib)
##        irow = 0
##        for row in Worker.mDataCSV:
##            row[4] = row[4].upper()
##            irow += 1
##            if irow % items == 0: print('Обработано %i из %i...' % (irow, len(Worker.mDataCSV)))       
##        Worker.UpdateBlockCSV('organization_founder_per', {# 'id': 'int pk nn u', 
##            'person_id': 'int', 'version_date': 'text', 'grn': 'text', 'grn_date': 'text',
##            'last_name': 'text', 'first_name': 'text', 'middle_name': 'text',
##            'inn': 'text', 'capital_percent': 'float', 'capital_size': 'int'},
##            {'organization_id': 'organization_id', 'person_id': 'person_id', 'version_date': 'version_date',
##             'grn': 'grn', 'grn_date': 'grn_date',
##            'last_name': 'lastname', 'first_name': 'firstname', 'middle_name': 'middlename',
##            'inn': 'innfl', 'capital_percent': 'capital_percent', 'capital_size': 'capital_size'})
##
##    # База руководителей
##
##    # organization
##    Worker.ReadBlockCSV('DB/organization_leader_org.csv')
##    irow = 0
##    for row in Worker.mDataCSV:
##        row[4] = row[4].upper()
##        irow += 1
##        if irow % items == 0: print('Обработано %i из %i...' % (irow, len(Worker.mDataCSV)))       
##    Worker.UpdateBlockCSV('organization_leader_org', {# 'id': 'int pk nn u', 
##        'organization_id': 'int nn', 'version_date': 'text', 'grn': 'text', 'grn_date': 'text',
##        'name': 'text', 'ogrn': 'text', 'inn': 'text',
##        'leader_organization_id': 'int'},
##        {'organization_id': 'organization_id', 'version_date': 'version_date', 'grn': 'grn',
##        'grn_date': 'grn_date', 'name': 'name', 'ogrn': 'ogrnul', 'inn': 'innul',
##        'leader_organization_id': 'leader_organization_id'})
##
##    for ib in range(0, 10): # person
##        Worker.ReadBlockCSV('DB/organization_leader_per.csv', iblock=ib)
##        irow = 0
##        for row in Worker.mDataCSV:
##            row[4] = row[4].upper()
##            irow += 1
##            if irow % items == 0: print('Обработано %i из %i...' % (irow, len(Worker.mDataCSV)))       
##        Worker.UpdateBlockCSV('organization_leader_per', {# 'id': 'int pk nn u', 
##            'person_id': 'int', 'version_date': 'text', 'grn': 'text', 'grn_date': 'text',
##            'last_name': 'text', 'first_name': 'text', 'middle_name': 'text',
##            'innfl': 'text', 'position_type': 'int', 'position_name': 'text'},
##            {'person_id': 'person_id', 'version_date': 'version_date', 'grn': 'grn', 'grn_date': 'grn_date',
##            'last_name': 'lastname', 'first_name': 'firstname', 'middle_name': 'middlename',
##            'inn': 'innfl', 'position_type': 'position_type', 'position_name': 'position_name'})

    Worker.Indexation('organizations', ['id', 'ogrn', 'inn'])
    Worker.Indexation('organizations_name', ['organization_id', 'address_id'])
    Worker.Indexation('organizations_address', ['organization_id', 'address_id'])  
