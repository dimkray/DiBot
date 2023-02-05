# Работа с базой данных EGR2
import fixer
from DB.SQLite import SQL
from Services.StrMorph import String, Word
from Profiler import Profiler

Fixer.DB = 'DB/egr2.db'

dOPF = SQL.ReadDict('catalog_opf', bAll=False)
dFindOPF = SQL.ReadDict('dictionary_opf')
dOkved = SQL.ReadDict('dictionary_okved') # id: [code, name, note, version ...]
dStatus = SQL.ReadDict('dictionary_status') # id: [code, name]
dStatusGroup = {'0': 'Действующее',
                '1': 'В процессе ликвидации',
                '2': 'Ликвидированно',
                '3': 'В процессе реорганизации'}
dOldData = {0: 'нет',
            1: 'да'}
dTypeOkved = {1: 'главный',
              2: 'не главный'}

model = {'table=': 'organization',
         'ИНН': 'inn',
         'КПП': 'kpp',
         'ОГРН': 'ogrn',
         'Дата ОГРН': 'ogrn_date',
         'Группа статуса': 'status_group_id',
         'Регион': 'region_code',
         'Названия': {'table=': 'organization_name',
                      'Оригинал': 'name_original',
                      'Полное название': 'name_full',
                      'Сокращённое название': 'name_abbr',
                      'Название': 'name',
                      'ОПФ': 'opf_id',
                      'ОПФ найдено 1': 'opf_name1',
                      'ОПФ найдено 2': 'opf_name2',
                      'Коэффициент точности': 'koef',
                      'Старые данные': 'old_data',
                      'Дата': 'date',
                      'where=': ['org_id', 'id']},
         'Статусы': {'table=': 'organization_status',
                      'Статус': 'status_id',
                      'Старые данные': 'old_data',
                      'Дата': 'date',
                      'where=': ['org_id', 'id']},
         'Адреса': {'table=': 'organization_address',
                    'Дата': 'date',
                    'address_id': 'address_id',
                    'Помещение': 'flat',
                    'Ошибка адреса': 'address_error',
                    'Старые данные': 'old_data',
                    'Дата': 'date',
                    'where=': ['org_id', 'id']},
         'ОКВЭДы': {'table=': 'organization_okved',
                    'okved_id': 'okved_id',
                    'Тип': 'type',
                    'where=': ['org_id', 'id']}
         }
addressModel = {'table=': 'catalog_address',
                            'Код региона': 'region_code',
                            'area_type': 'area_type',
                            'area_name': 'area_name',
                            'city_type': 'city_type',
                            'city_name': 'city_name',
                            'settlement_type': 'settlement_type',
                            'settlement_name': 'settlement_name',
                            'street_type': 'street_type',
                            'street_name': 'street_name',
                            'Номер дома': 'house',
                            'Номер корпуса': 'building',
                            'Почтовый индекс': 'postcode',
                            'Код КЛАДР': 'kladr'}

# -------------------------------------------
# Основной блок программы

while True:
    tQuery = 'name'
    query = input('Введите ИНН, ОГРН, id или название организации: ')
    query = query.strip()
    print()
    if String.WordsCount(query) == 1: # одно слово
        if Word.Type(query) == 40: # Если число
            if len(query) == 10: # ИНН
                tQuery = 'inn'
            elif len(query) == 13: # ОГРН
                tQuery = 'ogrn'
            else: tQuery = 'id'
    if tQuery == 'name': # Если это поиск по имени
        if len(query) > 2:
            query = query.upper().replace('Ё','Е')
            m = SQL.ReadRow('organization_name', 'name', query)
            if m == []:
                print(SQL.ReadRowsLike('organization_name', 'name', query))
            else: print(m)
        else:
            print('Слишком мая строка для поиска!')
        print()
        continue

    with Profiler() as P:
        mOrg = SQL.Dict(model, {tQuery: query})

    for org in mOrg:
        org['Группа статуса'] = dStatusGroup[org['Группа статуса']]
        for name in org['Названия']:
            name['Старые данные'] = dOldData[name['Старые данные']]
            if name['ОПФ'] is not None:
                name['ОПФ'] = dOPF[name['ОПФ']]
            if name['ОПФ найдено 1'] is not None:
                #print(name['ОПФ найдено 1'])
                name['ОПФ найдено 1'] = dFindOPF[name['ОПФ найдено 1']]
            if name['ОПФ найдено 2'] is not None:
                #print(name['ОПФ найдено 2'])
                name['ОПФ найдено 2'] = dFindOPF[name['ОПФ найдено 2']]
        if org['Статусы'] is not None:
            for status in org['Статусы']:
                status['Старые данные'] = dOldData[status['Старые данные']]
                if status['Статус'] is not None:
                    status['Статус'] = dStatus[status['Статус']]
        if org['ОКВЭДы'] is not None:
            for okved in org['ОКВЭДы']:
                okved['Тип'] = dTypeOkved[okved['Тип']]
                okved['Код'] = dOkved[okved['okved_id']][0]
                okved['Наименование'] = dOkved[okved['okved_id']][1]
##                if dOkved[okved['okved_id']][2] is not None:
##                    okved['Описание'] = dOkved[okved['okved_id']][2]
                okved['Версия'] = dOkved[okved['okved_id']][3]
                del(okved['okved_id'])
        for address in org['Адреса']:
            address['Старые данные'] = dOldData[address['Старые данные']]
            dAddr = SQL.Dict(addressModel, {'id': address['address_id']})[0]
            if dAddr['area_name'] is not None:
                address['Район'] = '%s. %s' % (dAddr['area_type'], dAddr['area_name'])
            if dAddr['city_name'] is not None:
                address['Город'] = '%s. %s' % (dAddr['city_type'], dAddr['city_name'])
            if dAddr['settlement_name'] is not None:
                address['Населённый пункт'] = '%s. %s' % (dAddr['settlement_type'], dAddr['settlement_name'])
            if dAddr['street_name'] is not None:
                address['Улица'] = '%s. %s' % (dAddr['street_type'], dAddr['street_name'])
            address['Код региона'] = dAddr['Код региона'] + 1
            del(address['address_id'])

    print()
    if isinstance(mOrg, str): # если ошибка
        print(mOrg)
        print()
        continue  
    if len(mOrg) > 1:
        print('Найдено %i оргназиций. Будет показана только первая из них:' % len(mOrg))
        print()
    if len(mOrg) == 0:
        print('По данному запросу ничего не найдено.')
        print()
        continue

    print(mOrg[0])
    print()
