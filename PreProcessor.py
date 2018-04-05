# -*- coding: utf-8 -*-
# ПреПроцессор - стартовый обработчик пользовательских запросов
import Fixer
from Services.Yandex import Yandex

# препроцессорный обработчик пользовательских запросов
def ReadMessage(text):
    Fixer.log('Пользователь пишет: ' + text)
    # Запуск сервиса Яндекс.Спеллер для исправления пользовательских опечаток
    text = Yandex.Speller(text)
    Fixer.log('Яндекс.Спеллер: ' + text)
    stext = text.upper()
    stext = stext.replace('Ё','Е')
    # Поиск совпадений по первому слову
    for word in Fixer.Word1:
        if word == stext[0:len(word)]:
            poz = len(word)
            text = Fixer.Word1[word] + text[poz:] # убираем первое слово - добавляем сервис #
            Fixer.log('Найдено совпадение по первому слову: ' + text)
            Fixer.bAI = False
            break
    # Поиск совпадений по ключевым словам
    if Fixer.bAI:
        for word in Fixer.KeyWord:
            ktext = text.upper()
            if ktext.find(word) >= 0:
                text = Fixer.KeyWord[word] + text # добавляем сервис #
                Fixer.log('Найдено совпадение по ключевому слову [' + word + ']:' + text)
                Fixer.bAI = False
                break
    return text
