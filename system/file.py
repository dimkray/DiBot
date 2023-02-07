"""
    Модуль управления файлами
"""
import pickle
import json
import os

from system.logging import err_log

PATH = 'DB\\'   # Путь, где хранятся словари


def exist(file_path: str) -> bool:
    """Функция проверки существования файла с указанием пути [file_path]"""
    if '\\' in file_path and ':' in file_path:
        root = file_path.split('\\')[0]
        if not os.path.exists(root): err_log('Внимание! Не обнаружен диск', root)
    if os.path.exists(file_path): return True
    else: return False


def save(dictionary: dict, name: str) -> bool:
    """Функция записи словаря [dictionary] в файл [name].json"""
    try:
        with open(f'{PATH}{name}.json', 'w', encoding='utf-8') as f:
            json.dump(dictionary, f, sort_keys=False, ensure_ascii=False)
        return True
    except Exception as e:
        err_log(f'{name}.json - {e}')
        return False


def load(name: str) -> dict:
    """Функция загрузки словаря из файла [name].json"""
    dictionary = {}
    try:
        if exist(f'{PATH}{name}.json'): return dictionary
        with open(f'{PATH}{name}.json', 'r', encoding='utf-8') as f:
            dictionary = json.load(f)
        return dictionary
    except Exception as e:
        err_log(f'{name}.json - {e}')
        return dictionary


# Функция записи словаря в байты
def save_byte(dictionary: dict, name: str) -> bool:
    """Функция записи словаря [dictionary] в байтовый файл [name].dict"""
    try:
        with open(f'{PATH}{name}.dict', 'rb') as f:
            pickle.dump(dictionary, f)
        return True
    except Exception as e:
        err_log(f'{name}.dict - {e}')
        return False


# Функция загрузки байтового словаря
def load_byte(name) -> dict:
    """Функция загрузки словаря из байтового файла [name].dict"""
    dictionary = {}
    try:
        if not exist(f'{PATH}{name}.dict'): return dictionary
        with open(f'{PATH}{name}.dict', 'rb') as f:
            dictionary = pickle.load(f)
        return dictionary
    except Exception as e:
        err_log(f'{name}.dict - {e}')
        return dictionary


# ------------------------------------------------
# Тестирование сервиса
if __name__ == '__main__':
    print(save({'a': 123, 'b': 'test'}, 'test'))
    while True:
        value = dict(input('dict: '))
        print(save(value, 'test'))
