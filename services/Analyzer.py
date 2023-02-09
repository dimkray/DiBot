# -*- coding: utf-8 -*-
# Анализатор строк (поиск города/страны/времени/даты/обращения)
import fixer
import random
from datetime import date, datetime, timedelta
from services.StrMorph import String, Word
from DB.SQLite import SQL

class TextFinder:
    # Получение всех слов из строки в нормальной форме
    def WordsNormal(text):
        words = String.GetWords(text)
        nwords = []
        for word in words:
            nwords.append(Word.Normal(word))
        return nwords

    # Определение типов
    def AnalyzeType(text):
        words = String.GetWords(text)
        if len(words) == 0:
            return 1, 0
        sumType = 0
        for word in words:
            sumType += Word.Type(word)
        if sumType/len(words) > 40:
            return 50, len(words)  # латиница
        if sumType/len(words) > 30:
            return 40, len(words)  # цифры
        if sumType/len(words) > 0:
            return 1, len(words)  # предложение
        else:
            return 1, len(words)  # неизвестные слова
    
    #def FindCity(text):

    def FindDate(text):
        try:
            s = text.upper()
            # временные параметры
            if s.find('СЕЙЧАС') > 0:
                Fixer.NOW = True
                Fixer.DATE = date.today()
            if s.find('СЕГОДНЯ'):
                Fixer.NOW = False
                Fixer.DATE = date.today()
            if s.find('ЗАВТРА'):
                Fixer.NOW = False
                Fixer.DATE = date.today() + timedelta(days=1)
            if s.find('ПОСЛЕЗАВТРА'):
                Fixer.NOW = False
                Fixer.DATE = date.today() + timedelta(days=2)
            if s.find('ВЧЕРА'):
                Fixer.NOW = False
                Fixer.DATE = date.today() - timedelta(days=1)
            # поиск формы даты
            if s.count('-')>1 or s.count('.')>1 or s.count('/')>1:
                Fixer.NOW = False
                sdate = s 
                sdate = sdate.replace('.','-')
                sdate = sdate.replace('/','-')
                Fixer.trDate = sdate
            
            return text
        except Exception as e:
            Fixer.errlog('DateTime.FindDate', str(e))
            return '#bug: ' + str(e) 