import pickle
from fixer import err_log


# Функция записи словаря в байты
def save_byte(dictionary: dict, name: str) -> bool:
    """Функция записи словаря [dictionary] в байтовый файл [name].dict"""
    try:
        with open(f'DB\\{name}.dict', 'rb') as f:
            pickle.dump(dictionary, f)
        return True
    except Exception as e:
        err_log(f'{name}.db - {e}')
        return False


# Функция загрузки байтового словаря
def load_byte(name) -> dict:
    """Функция загрузки словаря из байтового файла [name].dict"""
    dictionary = {}
    try:
        if not exist(f'DB\\{name}.dict'): return dictionary
        with open(f'DB\\{name}.dict', 'rb') as f:
            dictionary = pickle.load(f)
        return dictionary
    except Exception as e:
        err_log(f'{name}.db - {e}')
        return dictionary