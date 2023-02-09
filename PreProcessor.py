# -*- coding: utf-8 -*-
# ПреПроцессор - стартовый обработчик пользовательских запросов
from typing import List

import fixer
import config
from system.logging import log
from system.string import str_spec
from services.Yandex import Ya
from services.Analyzer import TextFinder
from services.StrMorph import String, Word


# мультипроцессор, препроцессорная обработка, препроцессорное автоопределение сервиса
# возвращаемый формат: [[текст для процессора],[предполагаемый сервис]]
def list_processor(text: str) -> List[str]:
    """Получение списка процессов"""
    log('PreProcessor.MultiProcessor')
    return [process for process in String.GetStrings(text) if process.strip()]


# препроцессорный обработчик пользовательских запросов
def read_message(text):
    log('PreProcessor.ReadMessage', text)
    # Фиксация слов
    fix = ''
    text = str_spec(text)
    if '"' in text:
        fix_start = text.find('"')
        fix_end = text.find('"', fix_start + 1)
        if fix_end > 0:
            no_fix = text[:fix_start] + '["]' + text[fix_end + 1:]
        else:
            no_fix = text[:fix_start] + '["]'
        fix = text[fix_start + 1:fix_end]
        text = no_fix
    # Запуск сервиса Яндекс.Спеллер для исправления пользовательских опечаток
    if text[:4].upper() != 'DEF:' and text[:5].upper() != 'DEFS:' and text[:5].upper() != 'CODE:' and text[0] != '=':
        if text[0] == '~':  # Принудительное отключение Спеллера
            text = text[1:].strip()
        else:
            text = Ya.Speller(text)
            log('Яндекс.Спеллер: ' + text)
    stext = text.upper()
    stext = stext.replace('Ё', 'Е')
    # Возвращаем зафиксированные слова
    stext = stext.replace('["]', fix)
    # Поиск совпадений по первому слову
    log('PreProcessor.Word1')
    for word in fixer.WORD1:
        if word == stext[0:len(word)]:
            poz = len(word)
            text = fixer.WORD1[word] + text[poz:]  # убираем первое слово - добавляем сервис #
            log('PreProcessor.Word1', 'Найдено совпадение по первому слову: ' + text)
            break
    # Поиск совпадений по ключевым словам
    fixer.log('PreProcessor.KeyWord')
    if config.AI:
        for word in fixer.KEY_WORD:
            ktext = text.upper()
            if ktext.find(word) >= 0:
                text = fixer.KEY_WORD[word] + text  # добавляем сервис #
                log('PreProcessor.KeyWord', 'Найдено совпадение по ключевому слову [' + word + ']:' + text)
                break
    # Анализ сообщения
    if ': ' not in text:
        log('PreProcessor.Analyzer')
        text_type, count = TextFinder.AnalyzeType(text)
        if text_type == 50 and count > 3: text = '#translate: русский: ' + text
        if text_type == 40 and count > 1: text = '#calculator: ' + text
    if text[0] == '#': config.AI = False  # отключаем искусственный интеллект
    return text
