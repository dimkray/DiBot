# -*- coding: utf-8 -*-
# DaData

import fixer
import datetime
from services.URLParser import URL

api_base = 'https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/'
api_base2 = 'https://suggestions.dadata.ru/suggestions/api/4_1/rs/findById/'
headers = {'Authorization': 'Token a06e9484ce1d11618e52392f3714634f0234027f',
           'Accept': 'application/json'}
           #  'X-Secret': 'b9408262609c04914b1e3fe4d6e2ca4e45697a28'}


# Получение адреса
def GetData(squery, api='', icount=0):
    djson = {'query': squery}
    if icount > 0:
        djson['count'] = icount
    return URL.PostData(api, dheaders=headers, djson=djson)


# основной класс
class DData:
    # Обработать ФИО
    def Name(sname, icount=10):
        return GetData(sname, api=api_base + 'fio', icount=icount)

    # Обработать адрес
    def Address(saddress, icount=10):
        return GetData(saddress, api=api_base + 'address', icount=icount)

    # Обработать организацию
    def Organization(sorg, icount=10):
        return GetData(sorg, api=api_base + 'party', icount=icount)

    def OrganizationId(sorg):
        return GetData(sorg, api=api_base2 + 'party')

    # Обработать банк
    def Bank(sbank, icount=10):
        return GetData(sbank, api=api_base + 'bank', icount=icount)

    # Обработать e-mail
    def eMail(smail, icount=10):
        return GetData(smail, api=api_base + 'email', icount=icount)

    # Обработать страну
    def Country(scountry):
        return GetData(scountry, api=api_base + 'country')

    # Обработать валюту
    def Currency(scurrency):
        return GetData(scurrency, api=api_base + 'currency')

    # Обработать почтовое отделение
    def PostOffice(spost):
        return GetData(spost, api=api_base + 'postal_office')

    # Обработать налоговую инспекцию
    def FNS(sfns):
        return GetData(sfns, api=api_base + 'fns_unit')

    # Обработать ОКВЭД
    def OKVED(sokved):
        return GetData(sokved, api=api_base + 'okved2')

    # Обработать ОКПД
    def OKPD(sokpd):
        return GetData(sokpd, api=api_base + 'okpd2')


# основной класс (получаем строкой)
class strData:
    # Обработать ФИО
    def Name(sname, bFindAll=True):
        try:
            if bFindAll: i = 10
            else: i = 1
            data = DData.Name(sname, i)
            if len(data['suggestions']) == 1 or bFindAll == False:
                dName = data['suggestions'][0]
                Fixer.stxt = ''
                Fixer.str_add(dName['value'], 'ФИО')
                Fixer.str_add(dName['unrestricted_value'], 'ФИО полное')
                Fixer.str_add(dName['data']['surname'], 'Фамилия')
                Fixer.str_add(dName['data']['name'], 'Имя')
                Fixer.str_add(dName['data']['patronymic'], 'Отчество')
                sgender = 'не удалось однозначно определить'
                if dName['data']['gender'] == 'MALE':
                    sgender = 'мужской'
                elif dName['data']['gender'] == 'FEMALE':
                    sgender = 'женский'
                Fixer.stxt += 'Пол: ' + sgender
                return Fixer.stxt
            elif len(data['suggestions']) > 1 and bFindAll:
                mName = []
                for iname in data['suggestions']:
                    mName.append(iname['value'])
                s = Fixer.list_format(mName, items=10, sobj='имён')
                s += '\n\nВыберите и напишите как надо'
                return s
            else:
                return 'Не удалось распознать'
        except Exception as e:
            Fixer.errlog('strData.Name', str(e))
            return '#bug: ' + str(e)


    # Адрес
    def Address(saddress, bFindAll=True):
        try:
            if bFindAll: i = 10
            else: i = 1
            data = DData.Address(saddress, i)
            #  print(data)
            if len(data['suggestions']) == 1 or bFindAll == False:
                dAddr = data['suggestions'][0]
                Fixer.stxt = ''
                Fixer.str_add(dAddr['value'], 'Адрес')
                Fixer.str_add(dAddr['unrestricted_value'], 'Адрес полный')
                dAddr = dAddr['data']
                Fixer.str_add(dAddr['postal_code'], 'Почтовый индекс')
                Fixer.str_add(dAddr['country'], 'Страна')
                Fixer.str_add(dAddr['region_type_full'], 'Тип региона')
                Fixer.str_add(dAddr['region'], 'Регион')
                Fixer.str_add(dAddr['area_type_full'], 'Тип района')
                Fixer.str_add(dAddr['area'], 'Район')
                Fixer.str_add(dAddr['city_type_full'], 'Тип города')
                Fixer.str_add(dAddr['city'], 'Город')
                Fixer.str_add(dAddr['city_district_type_full'], 'Тип района города')
                Fixer.str_add(dAddr['city_district'], 'Район города')
                Fixer.str_add(dAddr['settlement_type_full'], 'Тип населенного пункта')
                Fixer.str_add(dAddr['settlement'], 'Населенный пункт')
                Fixer.str_add(dAddr['street_type_full'], 'Тип улицы')
                Fixer.str_add(dAddr['street'], 'Улица')
                Fixer.str_add(dAddr['house_type_full'], 'Тип дома')
                Fixer.str_add(dAddr['house'], 'Дом')
                Fixer.str_add(dAddr['block_type_full'], 'Тип корпуса/строения')
                Fixer.str_add(dAddr['block'], 'Корпус/строение')
                Fixer.str_add(dAddr['flat_type_full'], 'Тип квартиры')
                Fixer.str_add(dAddr['flat'], 'Квартира')
                Fixer.str_add(dAddr['postal_box'], 'Абонентский ящик')
                Fixer.str_add(dAddr['fias_id'], 'Код ФИАС')
                s = ''
                if dAddr['fias_level'] == '0': s = 'страна'
                elif dAddr['fias_level'] == '1': s = 'регион'
                elif dAddr['fias_level'] == '3': s = 'район'
                elif dAddr['fias_level'] == '4': s = 'город'
                elif dAddr['fias_level'] == '5': s = 'район города'
                elif dAddr['fias_level'] == '6': s = 'населенный пункт'
                elif dAddr['fias_level'] == '7': s = 'улица'
                elif dAddr['fias_level'] == '8': s = 'дом'
                elif dAddr['fias_level'] == '65': s = 'планировочная структура'
                elif dAddr['fias_level'] == '-1': s = 'иностранный или пустой'
                else: s is None
                Fixer.str_add(s, 'Уровень детализации ФИАС')
                Fixer.str_add(dAddr['fias_code'], 'Иерархический код адреса в ФИАС')
                if dAddr['fias_actuality_state'] == '0': s = 'актуальный'
                elif dAddr['fias_actuality_state'] == '51': s = 'переподчинен'
                elif dAddr['fias_actuality_state'] == '99': s = 'удален'
                elif int(dAddr['fias_actuality_state']) > 0: s = 'переименован'
                else: s is None
                Fixer.str_add(s, 'Признак актуальности адреса в ФИАС')
                Fixer.str_add(dAddr['kladr_id'], 'Код КЛАДР')
                if dAddr['capital_marker'] == '1': s = 'центр района'
                elif dAddr['capital_marker'] == '2': s = 'центр региона'
                elif dAddr['capital_marker'] == '3': s = 'центр района и региона'
                elif dAddr['capital_marker'] == '4': s = 'центральный район региона'
                else: s is None
                Fixer.str_add(s, 'Признак')
                Fixer.str_add(dAddr['okato'], 'Код ОКАТО')
                Fixer.str_add(dAddr['oktmo'], 'Код ОКТМО')
                Fixer.str_add(dAddr['tax_office'], 'Код ИФНС для физических лиц')
                Fixer.str_add(dAddr['tax_office_legal'], 'Код ИФНС для организаций')
                Fixer.str_add(dAddr['history_values'], 'Список исторических названий')
                Fixer.str_add(dAddr['geo_lat'], 'Координаты: широта')
                Fixer.str_add(dAddr['geo_lon'], 'Координаты: долгота')
                if dAddr['qc_geo'] == '0': s = 'точные координаты'
                elif dAddr['qc_geo'] == '1': s = 'ближайший дом'
                elif dAddr['qc_geo'] == '2': s = 'улица'
                elif dAddr['qc_geo'] == '3': s = 'населенный пункт'
                elif dAddr['qc_geo'] == '4': s = 'город'
                elif dAddr['qc_geo'] == '5': s = 'координаты не определены'
                else: s is None
                Fixer.str_add(s, 'Код точности координат')
                Fixer.str_add(dAddr['city_area'], 'Административный округ')
                Fixer.str_add(dAddr['beltway_hit'], 'Внутри кольцевой?')
                Fixer.str_add(dAddr['beltway_distance'], 'Расстояние от кольцевой в километрах')
                Fixer.str_add(dAddr['flat_area'], 'Площадь квартиры')
                Fixer.str_add(dAddr['square_meter_price'], 'Рыночная стоимость м²')
                Fixer.str_add(dAddr['flat_price'], 'Рыночная стоимость квартиры')
                Fixer.str_add(dAddr['timezone'], 'Часовой пояс')
                Fixer.str_add(dAddr['metro'], 'Список ближайших станций метро')
                return Fixer.stxt
            elif len(data['suggestions']) > 1 and bFindAll:
                mAddr = []
                for iaddr in data['suggestions']:
                    mAddr.append(iaddr['value'])
                s = Fixer.list_format(mAddr, items=10, sobj='адресов')
                s += '\n\nВыберите и напишите как надо'
            else:
                s = 'Не удалось распознать'
            return s
        except Exception as e:
            Fixer.errlog('strData.Address', str(e))
            return '#bug: ' + str(e)


    # Обработать организацию
    def Organization(sorg, bId=False, bFindAll=True):
        from DB.SQLite import SQL
        s = ''
        try:
            if bFindAll: i = 10
            else: i = 1
            if bId:  # Если по ИНН/ОГРН
                data = DData.OrganizationId(sorg)
            else:
                data = DData.Organization(sorg, i)
            if len(data['suggestions']) == 1:
                dOrg = data['suggestions'][0]
                Fixer.stxt = ''
                if dOrg['data']['type'] == 'LEGAL':
                    Fixer.str_add(dOrg['value'], 'Наименование компании')
                    Fixer.str_add(dOrg['unrestricted_value'], 'Полное наименование компании')
                else:
                    Fixer.str_add(dOrg['value'], 'Наименование')
                    Fixer.str_add(dOrg['unrestricted_value'], 'Полное наименование')
                dOrg = dOrg['data']
                if dOrg['type'] == 'LEGAL': s = 'юридическое лицо'
                elif dOrg['type'] == 'INDIVIDUAL': s = 'индивидуальный предприниматель'
                else: s = 'неизвестный тип'
                Fixer.str_add(s, 'Тип организации')
                if dOrg['address'] is not None:
                    Fixer.str_add(dOrg['address']['value'], 'Адрес')
                    Fixer.str_add(dOrg['address']['unrestricted_value'], 'Полный адрес')
                    if dOrg['address']['data'] is not None:
                        Fixer.str_add(dOrg['address']['data']['source'], 'Адрес как в ЕГРЮЛ')
                if 'branch_count' in dOrg:
                    Fixer.str_add(dOrg['branch_count'], 'Количество филиалов')
                if 'branch_type' in dOrg:
                    if dOrg['branch_type'] == 'MAIN': s = 'головная организация'
                    elif dOrg['branch_type'] == 'BRANCH': s = 'филиал'
                    else: s is None
                    Fixer.str_add(s, 'Тип подразделения')
                Fixer.str_add(dOrg['inn'], 'ИНН')
                if 'kpp' in dOrg:
                    Fixer.str_add(dOrg['kpp'], 'КПП')
                Fixer.str_add(dOrg['ogrn'], 'ОГРН')
                if 'ogrn_date' and dOrg['ogrn_date'] is not None in dOrg:
                    s = datetime.datetime.fromtimestamp(int(dOrg['ogrn_date'])/1000).strftime('%Y-%m-%d')
                    Fixer.str_add(s, 'Дата выдачи ОГРН')
                if 'management' in dOrg:
                    if dOrg['management'] is not None:
                        Fixer.str_add(dOrg['management']['name'], 'Руководитель')
                        Fixer.str_add(dOrg['management']['post'], 'Должность руководителя')
                if dOrg['name'] is not None:
                    Fixer.str_add(dOrg['name']['full_with_opf'], 'Полное наименование с ОПФ')
                    Fixer.str_add(dOrg['name']['short_with_opf'], 'Краткое наименование с ОПФ')
                    Fixer.str_add(dOrg['name']['full'], 'Полное наименование')
                    Fixer.str_add(dOrg['name']['short'], 'Краткое наименование')
                Fixer.str_add(dOrg['okved'], 'Код ОКВЭД')
                Fixer.str_add(dOrg['okved_type'], 'Версия справочника ОКВЭД')
                m = SQL.ReadRows('okved', 'code', dOrg['okved'])
                if len(m) > 0: # если найдены коды ОКВЭД в справочнике
                    sName = m[0][2]
                    sDesc = m[0][3]
                    if m[0][4] != int(dOrg['okved_type']) and len(m) > 1:
                        sName = m[1][2]
                        sDesc = m[1][3]
                    Fixer.str_add(sName, 'ОКВЭД')
                    if sDesc is not None: sDesc = sDesc.replace('- ', '\n- ')
                    Fixer.str_add(sDesc, 'Пояснения')
                if bId:
                    Fixer.str_add(dOrg['okveds'], 'Коды ОКВЭД дополнительных видов деятельности')
                if dOrg['opf'] is None:
                    Fixer.str_add(dOrg['opf']['full'], 'Полное название ОПФ')
                    Fixer.str_add(dOrg['opf']['short'], 'Краткое название ОПФ')
                    Fixer.str_add(dOrg['opf']['code'], 'Код ОКОПФ')
                if dOrg['state']['status'] == 'ACTIVE': s = 'действующая'
                elif dOrg['state']['status'] == 'LIQUIDATING': s = 'ликвидируется'
                elif dOrg['state']['status'] == 'LIQUIDATED': s = 'ликвидирована'
                elif dOrg['state']['status'] == 'REORGANIZING': s = 'в процессе присоединения к другому юр.лицу, с последующей ликвидацией'
                else: s = 'статус неизвестен'
                Fixer.str_add(s, 'Статус организации')
                s = datetime.datetime.fromtimestamp(int(dOrg['state']['registration_date'])/1000).strftime('%Y-%m-%d')
                Fixer.str_add(s, 'Дата регистрации')
                if dOrg['state']['liquidation_date'] is not None:
                    s = datetime.datetime.fromtimestamp(int(dOrg['state']['liquidation_date'])/1000).strftime('%Y-%m-%d')
                    Fixer.str_add(s, 'Дата ликвидации')
                if bId:
                    if dOrg['authorities'] is not None:
                        Fixer.str_add(dOrg['authorities']['fts_registration'], 'ИФНС регистрации')
                        Fixer.str_add(dOrg['authorities']['fts_report'], 'ИФНС отчётности')
                        Fixer.str_add(dOrg['authorities']['pf'], 'Отделение Пенсионного фонда')
                        Fixer.str_add(dOrg['authorities']['sif'], 'Отделение Фонда соц. страхования')
                    if dOrg['documents'] is not None:
                        Fixer.str_add(dOrg['documents']['fts_registration'], 'Свидетельство о регистрации в налоговой')
                        Fixer.str_add(dOrg['documents']['pf_registration'], 'Свидетельство о регистрации в Пенсионном фонде')
                        Fixer.str_add(dOrg['documents']['sif_registration'], 'Свидетельство о регистрации в Фонде соц. страхования')
                    if 'citizenship' in dOrg:
                        Fixer.str_add(dOrg['citizenship'], 'Гражданство ИП')
                    if 'founders' in dOrg:
                        Fixer.str_add(dOrg['founders'], 'Учредители компании')
                    if 'managers' in dOrg:
                        Fixer.str_add(dOrg['managers'], 'Руководители компании')
                    if 'capital' in dOrg:
                        Fixer.str_add(dOrg['capital'], 'Уставной капитал компании')
                    if 'licenses' in dOrg:
                        Fixer.str_add(dOrg['licenses'], 'Лицензии')
                s = datetime.datetime.fromtimestamp(int(dOrg['state']['actuality_date'])/1000).strftime('%Y-%m-%d')
                Fixer.str_add(s, 'Дата актуальности сведений')

                return Fixer.stxt
            elif len(data['suggestions']) > 1:
                mName = []
                for iname in data['suggestions']:
                    mName.append(iname['value'])
                s = Fixer.list_format(mName, items=10, sobj='имён')
                s += '\n\nВыберите и напишите как надо'
                return s
            else:
                return 'Не удалось распознать'
        except Exception as e:
            Fixer.errlog('strData.Organization', str(e))
            return '#bug: ' + str(e)