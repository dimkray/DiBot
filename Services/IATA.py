# -*- coding: utf-8 -*-
# IATA
# Key f09869c0-33d9-4f10-8fe3-5467b99492f7
# https://iatacodes.org/api/VERSION/ENDPOINT?api_key=YOUR-API-KEY&lang=ru

import Fixer
import config
import json
from Services.URLParser import URL
from DB.SQLite import Finder

api = 'https://iatacodes.org/api/v6/'
params = {'api_key': config.IATA_key, 'lang': 'ru'}

#def GetCode(stype, code, name):
    

# Основной класс
class IATA:
    # Код Аэропорта
    def Airport(code='', name='', db=True):
        jair = {}; air = []
        if code != '':
            if db: air = Finder.FindAll('IATA_airports', ['code'], code, ['code', 'name'])
            else: jair = URL.GetData(api+'airports', code, 'code', params=params, bjson=True)
        elif name != '':
            if db: air = Finder.FindAll('IATA_airports', ['nameU'], name, ['code', 'name'])
            #else: jair = URL.GetData(api+'airports', name, 'name', params=params, bjson=True)
        elif db == False:
            jair = URL.GetData(api+'airports', params=params, bjson=True)
        if len(air) > 0 and code != '': return Fixer.Sort(air,0)
        if len(air) > 0 and name != '': return Fixer.Sort(air,1)
        if jair is None: return '#problem: null result'
        if 'response' in jair:
            air = jair['response']
            if len(air) == 1: return air[0]
            elif len(air) > 1: return air
            else: return {}
        else:
            if db: return air
            else: return jair
    
    # Код Города
    def City(code='', name='', db=True):
        jair = {}; air = []
        if code != '':
            if db: air = Finder.FindAll('IATA_city', ['code'], code, ['code', 'name'])
            else: jair = URL.GetData(api+'cities', code, 'code', params=params, bjson=True)
        elif name != '':
            if db: air = Finder.FindAll('IATA_city', ['nameU'], name, ['code', 'name'])
        elif db == False:
            jair = URL.GetData(api+'cities', params=params, bjson=True)
        if len(air) > 0 and code != '': return Fixer.Sort(air,0)
        if len(air) > 0 and name != '': return Fixer.Sort(air,1)
        if jair is None: return '#problem: null result'
        if 'response' in jair:
            air = jair['response']
            if len(air) == 1: return air[0]
            elif len(air) > 1: return air
            else: return {}
        else:
            if db: return air
            else: return jair    
    
