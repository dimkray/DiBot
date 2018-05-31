# -*- coding: utf-8 -*-
# ПреПроцессор - стартовый обработчик пользовательских запросов
import Fixer
from Services.Yandex import Yandex

# мультипроцессор, препроцессорная обработка, препроцессорное автоопределение сервиса
# возвращаемый формат: [[текст для процессора],[предполагаемый сервис]]
def MultiProcessor(text):
    Fixer.log('PreProcessor.MultiProcessor')
    # происк мультизапроса и выполнение запроса (анализ)
    bMulti = False
    if text.find('. ') > 0: bMulti = True
    if text.find('? ') > 0: bMulti = True
    if text.find('! ') > 0: bMulti = True
    if bMulti: # если есть признак мультизапроса
        mText = []
        m = text.split('. ')
        for im in m:
            im = text.split('. ')
            #ДОРАБОТАТЬ!!!
    return False
        

# препроцессорный обработчик пользовательских запросов
def ReadMessage(text):
    Fixer.log('PreProcessor.ReadMessage', text)
    # Запуск сервиса Яндекс.Спеллер для исправления пользовательских опечаток
    text = Yandex.Speller(text)
    Fixer.log('Яндекс.Спеллер: ' + text)
    stext = text.upper()
    stext = stext.replace('Ё','Е')
    # Поиск совпадений по первому слову
    Fixer.log('PreProcessor.Word1')
    for word in Fixer.Word1:
        if word == stext[0:len(word)]:
            poz = len(word)
            text = Fixer.Word1[word] + text[poz:] # убираем первое слово - добавляем сервис #
            Fixer.log('PreProcessor.Word1', 'Найдено совпадение по первому слову: ' + text)
            Fixer.bAI = False
            break
    # Поиск совпадений по ключевым словам
    Fixer.log('PreProcessor.KeyWord')
    if Fixer.bAI:
        for word in Fixer.KeyWord:
            ktext = text.upper()
            if ktext.find(word) >= 0:
                text = Fixer.KeyWord[word] + text # добавляем сервис #
                Fixer.log('PreProcessor.KeyWord', 'Найдено совпадение по ключевому слову [' + word + ']:' + text)
                Fixer.bAI = False
                break
    return text
