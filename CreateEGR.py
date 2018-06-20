# Обновление базы данных ЕГР из открытых источников
import csv
import Fixer
from DB.SQLite import SQL, CSV
from Services.StrMorph import String, Word
from DB.Worker import Worker

Fixer.DB = 'DB/egr.db'

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

def UpdateTable(NameTable, dCols, data):
    if NameTable not in tDel: # проверяем не удалена ли таблица
        print('Удаление старой таблицы "%s"' % NameTable)
        print('Результат: ' + SQL.Delete(NameTable))
        print('Создание новой таблицы "%s"' % NameTable)
        print('Результат: ' + SQL.Table(NameTable, dCols))
        tDel.append(NameTable)
    print('Запись данных: %i строк' % len(data))
    print('Результат: ' + SQL.WriteBlock(NameTable, data))
    print('-------------------------------------')

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
yn = input('...... Обновить таблицу адресов и загрузить новые данные? Y/N: ')
if yn != 'N': 

    # Словарь адресов

    for ib in range(0, 2):
        Worker.ReadBlockCSV('DB/address.csv', iblock=ib)
        irow = 0
        for row in Worker.mDataCSV:
            row.append(row[6].upper().strip()) # type
            row.append(row[2].upper().strip()) # nameU
            Worker.mTableCSV.append('type')
            Worker.mTableCSV.append('nameU')
            irow += 1
            if irow % items == 0: print('Обработано %i из %i...' % (irow, len(Worker.mDataCSV)))       
        Worker.UpdateBlockCSV('fias_address', {'guid': 'text pk nn u', 'parent_guid': 'text',
            'level': 'int', 'region_code': 'int', 'type_short': 'text', 'type': 'text',
            'name': 'text', 'nameU': 'text', 'postalcode': 'text', 'update_date': 'text'},
            {'guid': 'ao_guid', 'parent_guid': 'parent_guid', 'level': 'ao_level',
             'region_code': 'region_code', 'type_short': 'short_name', 'type': 'type',
             'name': 'formal_name', 'nameU': 'nameU', 'postalcode': 'postal_code', 'update_date':
             'update_date'}, iblock=ib)

    # База адресов

    for ib in range(0, 11):
        Worker.UpdateTableCSV('DB/organization_address.csv', 'organizations_address',
            {'id': 'int pk nn u', 'organization_id': 'text nn',
            'version_date': 'text', 'grn': 'text', 'grn_date': 'text', 'region_code': 'int',
            'area_type': 'text', 'area_name': 'text', 
            'city_type': 'text', 'city_name': 'text',
            'settlement_type': 'text', 'settlement_name': 'text',
            'street_type': 'text', 'street_name': 'text',
            'house': 'text', 'building': 'text', 'flat': 'text',
            'postcode': 'text', 'fias_house': 'text', 'fias': 'text'})
        
    Worker.Indexation('fias_address', ['level', 'type', 'nameU', 'postalcode'])
    Worker.Indexation('organizations_address', ['organization_id'])    

        # База организаций

##        mOrg, mTable = CSV.Reader('DB/organization.csv', separator=';', items=block, istart=iblock*block, download=orgs)
##        print(mTable)
##
##        mOrgs = []
##        iorg = 0
##        for iOrg in mOrg:
##            try:
##                m = []
##                m.append(iOrg[0]) # id
##                m.append(iOrg[1]) # version_date
##                m.append(iOrg[2]) # ogrn
##                m.append(iOrg[3]) # ogrn_date
##                m.append(iOrg[4]) # inn
##                m.append(iOrg[9]) # kpp
##                m.append(iOrg[5]) # okved
##                m.append(iOrg[6]) # okved_version
##
##                # Обработка имени
##                name = iOrg[7].upper().replace('  ',' ').strip()
##                abbr = iOrg[8]
##                if abbr is not None: abbr = abbr.upper().strip()
##                m.append(name) # name_full
##                m.append(abbr) # name_abbr
##
##                opf = [None, None]
##                sname = name
##                #print(sname)
##                words = String.GetWords(name) # наименование без ОПФ
##                #print(words)
##                # поиск ОПФ - dOpf - в начале и в конце строки
##                for val in dOpf.values():
##                    if val in sname:
##                        if name.find(val+' ') == 0 or sname.find(' '+val) == len(sname)-len(val)-1:
##                            setOpf(val)
##                            sname = sname.replace(val,'').strip()
##                            words = String.GetWords(sname)
##                            break
##                            #print('dOpf: ', words)
##                for key in dOpf:
##                    if key in words:
##                        if key == words[0]:
##                            setOpf(dOpf[key])
##                            del(words[0])
##                            break
##                        if key == words[-1]:
##                            setOpf(dOpf[key])
##                            del(words[-1])
##                            break
##                        #print('dOpf-key: ', words)
##                # поиск ОПФ - mOpf - в начале и в конце строки
##                for iopf in mOpf:
##                    if iopf in sname:
##                        if sname.find(iopf+' ') == 0 or sname.find(' '+iopf) == len(sname)-len(iopf)-1:
##                            setOpf(iopf)
##                            sname = sname.replace(iopf,'').strip()
##                            words = String.GetWords(sname)
##                            break
##                            #print('mOpf: ', words)
##                # поиск ОПФ - endOpf
##                for iopf in endOpf:
##                    if iopf in words:
##                        sopf = ''
##                        end = words.index(iopf); start = 0
##                        for i in range(end-1,0,-1):
##                            if Word.Type(words[i]) < 2 or Word.Type(words[i]) > 3:
##                                start = i + 1; break
##                        if start == end: continue
##                        for i in range(start, end+1):
##                            sopf += words[i]+' '
##                        sopf = sopf.strip()
##                        for i in range(start, end+1):
##                            del(words[start])
##                        #print('endOpf: ', words)
##                        setOpf(sopf)
##                sname = None
##                if len(words) > 0:
##                    sname = ''
##                    cname = String.GetConstr(name)
##                    #print(cname)
##                    for word in words:
##                        try:
##                            s = cname[cname.find('['+word+']')+len(word)+2]
##                        except: s = ' '
##                        sname += word+s
##                    sname = sname[:-1]
##                #print('name: ', sname)
##
##                m.append(sname) # name
##                if opf[0] is not None:
##                    m.append(newOpf(opf[0])) # opf1
##                else: m.append(None)
##                if opf[1] is not None:
##                    m.append(newOpf(opf[1])) # opf2
##                else: m.append(None)
##
##                if iOrg[10] == 'КОПФ': m.append(0) # opf_spr
##                elif iOrg[10] == 'ОКОПФ': m.append(1)
##                elif iOrg[10] is None: m.append(None)
##                else: m.append(100)
##
##                m.append(iOrg[11]) # opf
##
##                # проверка ОПФ - dOpf - в начале и в конце строки
##                koef = 0
##                if abbr is not None:
##                    words2 = String.GetWords(abbr)
##                    for key in dOpf:
##                        if key in words2:
##                            if key == words2[0]:
##                                if opf[0] == dOpf[key] or opf[1] == dOpf[key]:
##                                    koef += 0.4
##                                    name = name.replace(dOpf[key],'')
##                                    abbr = abbr.replace(key,'')
##                                    del(words2[0])
##                                    break
##                            if key == words2[-1]:
##                                if opf[0] == dOpf[key] or opf[1] == dOpf[key]:
##                                    koef += 0.4
##                                    name = name.replace(dOpf[key],'')
##                                    abbr = abbr.replace(key,'')
##                                    del(words2[-1])
##                                    break
##                    name = name.replace('"','').strip()
##                    abbr = abbr.replace('"','').strip()
##                    # проверка наименования
##                    if name == abbr: koef += 0.6
##                    elif words == words2: koef += 0.5
##                m.append(koef) # koef
##                mOrgs.append(m)
##                iorg += 1
##                if iorg % orgs == 0: print('Обработано %i из %i...' % (iorg, len(mOrgs)))
##            except Exception as e:
##                print('!!!Bug - '+str(e)+' : '+str(iOrg))
##        
##        UpdateTable('organizations', {'id': 'int nn u', 'version_date': 'text',
##            'ogrn': 'text', 'ogrn_date': 'text', 'inn': 'text', 'kpp': 'text',
##            'okved': 'text', 'okved_version': 'int', 'name_full': 'text',
##            'name_abbr': 'text', 'name': 'text', 'opf_name': 'int', 'opf_name2': 'int',
##            'opf_spr': 'int', 'opf': 'int', 'koef': 'float'}, mOrgs)
        # Индексы: CREATE INDEX ogrn_inn ON organizations (ogrn, inn);

# Отдельно записываем словарь ОПФ

##mopf = []
##for key in tOpf:
##    m = []
##    m.append(key)
##    m.append(tOpf[key])
##    mopf.append(m)
##    
##UpdateTable('opf_dict', {'id': 'int nn u', 'name': 'text nn'}, mopf)
    
