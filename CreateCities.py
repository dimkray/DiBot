# Обновление базы данных ЕГР из открытых источников
import csv
import Fixer
from DB.SQLite import SQL, CSV
from DB.Worker import Worker
from Services.StrMorph import Word

Fixer.DB = 'DB/Geo.db'

# основной блок программы
#----------------------------------

items = 100000
block = 1000000

#try:
yn = input('...... Обновить таблицы БД и загрузить новые данные? Y/N: ')
if yn != 'N': 

    # Словарь типов объектов
    Worker.UpdateTableCSV('Cities/featureCodes_ru.txt', 'feature_codes',
        {'code': 'text pk nn u', 'name': 'text', 'description': 'text'}, separator='\t', symb='"')
    dType = Worker.DictionaryCSV('Cities/featureCodes_ru.txt', keycol='code', mCols=['name'], separator='\t', symb='"')

    # Таблица названий объектов

    dName = {}; dLink = {}
    for ib in range(0, 13):
        Worker.ReadBlockCSV('Cities/alternateNamesV2.txt', iblock=ib, separator='\t', symb='"')
        irow = 0
        for row in Worker.mDataCSV:
            if row[2] == 'ru' or row[2] == None:
                iType = Word.Type(row[3])
                if iType != 0 and iType != 50:
                    dType[row[1]] = row[3]
            if row[2] == 'link': dLink[row[1]] = row[3]
            irow += 1
            if irow % items == 0: print('Обработано %i из %i...' % (irow, len(Worker.mDataCSV)))
        Worker.UpdateBlockCSV('names', {
            'geo_id': 'int nn', 'iso': 'text', 'name': 'text nn',
            'is_preferred': 'int', 'is_short': 'int', 'is_colloquial': 'int',
            'is_historic': 'int', 'date': 'text'}, # 'to': 'text'
            {'geo_id': 'geonameid', 'iso': 'isolanguage', 'name': 'alternate name',
            'is_preferred': 'isPreferredName', 'is_short': 'isShortName', 'is_colloquial': 'isColloquial',
            'is_historic': 'isHistoric', 'date': 'from'})

    # Таблица городов

    for ib in range(0, 1):
        Worker.ReadBlockCSV('Cities/RU.txt', iblock=ib, separator='\t', symb='"')
        irow = 0
        Worker.mTable.append('type')
        Worker.mTable.append('link')
        Worker.mTable.append('name_ru')
        Worker.mTable.append('nameU_ru')
        for row in Worker.mDataCSV:
            idType = row[6]+'.'+row[7]
            if idType in dType: # Тип объекта
                row.append(dType[idType])
            else:
                row.append(None)
            if row[0] in dLink: # Link
                row.append(dLink[row[0]])
            else:
                row.append(None)    
            if row[0] in dName: # Русское наименование
                name = dName[row[0]]
                row.append(name)
                row.append(name.uppend())
            else:
                row.append(None)
                row.append(None)
            irow += 1
            if irow % items == 0: print('Обработано %i из %i...' % (irow, len(Worker.mDataCSV)))
        Worker.UpdateBlockCSV('cities', {
            'id': 'int pk nn u', 'name': 'text nn', 'name_ascii': 'text', 'name_ru': 'text', 'link': 'text', # 'name_alternate': 'text',
            'lat': 'float', 'lon': 'float', 'feature_class': 'text', 'feature_code': 'text', 'type': 'text',
            'country_code': 'text', 'code1': 'text', 'code2': 'text', # 'cc2': 'text', 
            'code3': 'text', 'code4': 'text', 'population': 'int', 'elevation': 'int',
            'dem': 'int', 'timezone': 'text', 'date': 'text', 'nameU_ru': 'text'},
            {'id': 'geonameid', 'name': 'name', 'name_ascii': 'asciiname', 'name_ru': 'name_ru', 'link': 'link',
            'lat': 'latitude', 'lon': 'longitude', 'feature_class': 'feature class', 'feature_code': 'feature code',
            'type': 'type',
            'country_code': 'country code', 'code1': 'admin1 code', 'code2': 'admin2 code',
            'code3': 'admin3 code', 'code4': 'admin4 code', 'population': 'population', 'elevation': 'elevation',
            'dem': 'dem', 'timezone': 'timezone', 'date': 'modification date', 'nameU_ru': 'nameU_ru'})
