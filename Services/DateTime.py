# -*- coding: utf-8 -*-
# Сервис работы с датой и временем
import Fixer
import random
from datetime import date, datetime, timedelta

def FindDate(text):
    try:
        s = text.upper()
        # временные параметры
        if s.find('СЕЙЧАС') > 0:
            Fixer.bNow = True
            Fixer.Date = date.today(); continue
        if s.find('СЕГОДНЯ'):
            Fixer.bNow = False
            Fixer.Date = date.today(); continue
        if s.find('ЗАВТРА'):
            Fixer.bNow = False
            Fixer.Date = date.today() + timedelta(days=1); continue
        if s.find('ПОСЛЕЗАВТРА'):
            Fixer.bNow = False
            Fixer.Date = date.today() + timedelta(days=2); continue
        if s.find('ВЧЕРА'):
            Fixer.bNow = False
            Fixer.Date = date.today() - timedelta(days=1); continue
        # поиск формы даты
        if s.count('-')>1 or s.count('.')>1 or s.count('/')>1:
            Fixer.bNow = False
            sdate = s 
            sdate = sdate.replace('.','-')
            sdate = sdate.replace('/','-')
            Fixer.trDate = sdate
            continue
        
        return text
    except Exception as e:
        Fixer.errlog('DateTime.FindDate', str(e))
        return '#bug: ' + str(e) 
