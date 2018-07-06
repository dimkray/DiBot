# Работа с базой данных EGR2
import Fixer
from DB.SQLite import SQL

Fixer.DB = 'DB/egr2.db'

dOPF = SQL.ReadDict('opf', bAll=False)
dFindOPF = SQL.ReadDict('dictionary_opf')
dOkved = SQL.ReadDict('dictionary_okved') # id: [code, name, note, version ...]
dStatus = SQL.ReadDict('status') # id: [code, name]
dStatusGroup = {'0': 'Действующее',
                '1': 'В процессе ликвидации',
                '2': 'Ликвидированно',
                '3': 'В процессе реорганизации'}
dOldData = {0: 'нет',
            1: 'да'}

while True:

    inn = input('Введите ИНН: ')

    model = {'table=': 'organizations',
         'ИНН': 'inn',
         'КПП': 'kpp',
         'ОГРН': 'ogrn',
         'Дата ОГРН': 'ogrn_date',
         'Группа статуса': 'status_group_id',
         'Регион': 'region_code',
         'Названия': {'table=': 'organizations_name',
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
         'Статусы': {'table=': 'organizations_status',
                      'Статус': 'status_id',
                      'Старые данные': 'old_data',
                      'Дата': 'date',
                      'where=': ['org_id', 'id']}
         }          

    mOrg = SQL.Dict(model, {'inn': inn})

    for org in mOrg:
        org['Группа статуса'] = dStatusGroup[org['Группа статуса']]
        for name in org['Названия']:
            name['Старые данные'] = dOldData[name['Старые данные']]
            if name['ОПФ'] is not None:
                name['ОПФ'] = dOPF[name['ОПФ']]
            if name['ОПФ найдено 1'] is not None:
                name['ОПФ найдено 1'] = dFindOPF[str(name['ОПФ найдено 1'])]
            if name['ОПФ найдено 2'] is not None:
                name['ОПФ найдено 2'] = dFindOPF[str(name['ОПФ найдено 2'])]
        if org['Статусы'] is not None:
            for status in org['Статусы']:
                name['Старые данные'] = dOldData[name['Старые данные']]
                if name['Статус'] is not None:
                    name['Статус'] = dStatus[str(name['Статус'])]

    print()
    print(mOrg)
    print()
