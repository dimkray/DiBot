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

    # Словари
    Worker.UpdateTableCSV('Cities/countryInfo.txt', 'countries',
        {'iso': 'text pk nn u', 'iso3': 'text', 'iso_numeric': 'text', 'fips': 'text', 'name': 'text', 'capital': 'text', 'area': 'float',
         'population': 'int', 'continent': 'text', 'tld': 'text', 'currency_code': 'text',
         'currency_name': 'text', 'phone': 'text', 'postcode_format': 'text', 'postcode_regex': 'text',
         'languages': 'text', 'geo_id': 'int', 'neighbours': 'int', 'equivalent_fipscode': 'text'}, separator='\t', symb='"')
    Worker.UpdateTableCSV('Cities/iso-languagecodes.txt', 'languages',
        {'iso3': 'text pk nn u', 'iso2': 'text', 'iso1': 'text', 'name': 'text'}, separator='\t', symb='"')
    Worker.UpdateTableCSV('Cities/featureCodes_ru.txt', 'feature_codes',
        {'code': 'text pk nn u', 'name': 'text', 'description': 'text'}, separator='\t', symb='"')
    dType = Worker.DictionaryCSV('Cities/featureCodes_ru.txt', keycol='code', mCols=['name'], separator='\t', symb='"')

    dAdmin1 = Worker.DictionaryCSV('Cities/admin1Codes.txt', keycol='code', mCols=['geo_id'], separator='\t', symb='"')
    dAdmin2 = Worker.DictionaryCSV('Cities/admin2Codes.txt', keycol='code', mCols=['geo_id'], separator='\t', symb='"')

    Worker.ReadBlockCSV('Cities/timeZones.txt', separator='\t', symb='"')
    dTimeZones = {} # заполнения словаря timeZones
    for row in Worker.mDataCSV:
        m = []
        m.append(row[2])
        m.append(row[3])
        m.append(row[4])
        dTimeZones[row[0]+'.'+row[1]] = m

    # Таблица названий объектов

    dName = {}; dLink = {}
    for ib in range(0, 13):
        Worker.ReadBlockCSV('Cities/alternateNamesV2.txt', iblock=ib, separator='\t')
        irow = 0
        for row in Worker.mDataCSV:
            if (row[2] == 'ru' or row[2] == None) and row[3] is not None:
                iType = Word.Type(row[3])
                if iType != 0 and iType != 50:
                    dName[row[1]] = row[3]
            if row[2] == 'link': dLink[row[1]] = row[3]
            irow += 1
            if irow % items == 0: print('Обработано %i из %i...' % (irow, len(Worker.mDataCSV)))
        Worker.UpdateBlockCSV('names', {
            'geo_id': 'int nn', 'iso': 'text', 'name': 'text nn',
            'is_preferred': 'int', 'is_short': 'int', 'is_colloquial': 'int',
            'is_historic': 'int'},
            {'geo_id': 'geonameid', 'iso': 'isolanguage', 'name': 'alternate name',
            'is_preferred': 'isPreferredName', 'is_short': 'isShortName', 'is_colloquial': 'isColloquial',
            'is_historic': 'isHistoric'})

    # Таблица городов

    for ib in range(0, 1):
        Worker.ReadBlockCSV('Cities/RU.txt', iblock=ib, separator='\t', symb='"')
        irow = 0
        Worker.mTableCSV.append('type')
        Worker.mTableCSV.append('link')
        Worker.mTableCSV.append('name_ru')
        Worker.mTableCSV.append('nameU_ru')
        Worker.mTableCSV.append('tz')
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
                row.append(name.upper())
            else:
                row.append(None)
                row.append(None)
            if row[10] is not None:
                admin1 = row[8]+'.'+row[10]
                if admin1 in dAdmin1:
                    row[10] = dAdmin1[admin1]
            if row[11] is not None:
                admin2 = row[8]+'.'+row[11]
                if admin2 in dAdmin2:
                    row[11] = dAdmin2[admin2]
            if row[17] is not None:
                timeZone = row[8]+'.'+row[17]
                if timeZone in dTimeZones:
                    row.append(dTimeZones[timeZone][2])
                else:
                    row.append(None)
            else:
                row.append(None)
            irow += 1
            if irow % items == 0: print('Обработано %i из %i...' % (irow, len(Worker.mDataCSV)))
        Worker.UpdateBlockCSV('cities', {
            'id': 'int pk nn u', 'name': 'text nn', 'name_ascii': 'text', 'name_ru': 'text', 'link': 'text', # 'name_alternate': 'text',
            'lat': 'float', 'lon': 'float', 'feature_class': 'text', 'feature_code': 'text', 'type': 'text',
            'country_code': 'text', 'code1': 'text', 'code2': 'text', # 'cc2': 'text', 
            'code3': 'text', 'code4': 'text', 'population': 'int', 'elevation': 'int',
            'dem': 'int', 'timezone': 'text', 'tz': 'float', 'date': 'text', 'nameU_ru': 'text'},
            {'id': 'geonameid', 'name': 'name', 'name_ascii': 'asciiname', 'name_ru': 'name_ru', 'link': 'link',
            'lat': 'latitude', 'lon': 'longitude', 'feature_class': 'feature class', 'feature_code': 'feature code',
            'type': 'type',
            'country_code': 'country code', 'code1': 'admin1 code', 'code2': 'admin2 code',
            'code3': 'admin3 code', 'code4': 'admin4 code', 'population': 'population', 'elevation': 'elevation',
            'dem': 'dem', 'timezone': 'timezone', 'tz': 'tz', 'date': 'modification date', 'nameU_ru': 'nameU_ru'})
