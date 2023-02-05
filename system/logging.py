from termcolor2 import c
from system.function import get_fun
from datetime import datetime


# Константы цветов для консоли
color_type = {
    # цвет текста
    '#r#': 'red', '#g#': 'green', '#b#': 'blue', '#y#': 'yellow', '#m#': 'magenta', '#c#': 'cyan', '#w#': 'white',
    # цвет фона
    '#[e]#': 'on_grey', '#[r]#': 'on_red', '#[g]#': 'on_green', '#[y]#': 'on_yellow', '#[b]#': 'on_blue',
    '#[m]#': 'on_magenta', '#[c]#': 'on_cyan', '#[w]#': 'on_white',
    # другие атрибуты текста
    '**': 'bold', '__': 'underline', '^^': 'blink', '%%': 'reverse', '||': 'concealed', '&&': 'dark'}

# Журнал событий текущего сеанса
Logs: list = []


# Обработка цветных текстов
def colors(text: str) -> (str, str):
    """Обработка цветных текстов [text]"""
    is_color: bool = False
    for key in color_type:
        if key in text:
            is_color = True
            break
    if not is_color: return text, text
    s_color = text
    for key in color_type:
        if key in text:
            pos1 = 0
            count = len(s_color)
            while pos1 >= 0:
                pos1 = s_color.find(key, pos1)
                if pos1 < 0: break
                pos2 = s_color.find(key, pos1 + 2)
                if pos2 < 0: pos2 = len(s_color)
                if key[:2] == '#[':
                    s_color = s_color[:pos1] + c(s_color[pos1:pos2], on_color=color_type[key]) + s_color[pos2:]
                elif key[0] == '#':
                    s_color = s_color[:pos1] + c(s_color[pos1:pos2], color=color_type[key]) + s_color[pos2:]
                else:
                    s_color = s_color[:pos1] + c(s_color[pos1:pos2], attrs=[color_type[key]]) + s_color[pos2:]
                pos1 = pos2 + len(s_color) - count + 1
            s_color = s_color.replace(key, '')
            text = text.replace(key, '')
    return s_color, text


# Запись лога без вывода на экран
def in_log(*info: any, file: str = 'log.txt') -> str:
    f = open(file, 'a', encoding='utf-8')
    if info:
        string = str_full = ''
        for item in info:
            if string != '':
                string += ' '
            item_string = str(item)
            str_full += item_string
            string += item_string.replace('\n', ' \ ')
        string, str_log = colors(string)
        if string != str_log: s, str_full = colors(string)
        [module, fun, path] = get_fun()
        f.write(f"{datetime.now()} [{module}.{fun}]: {str_log}\n")
        f.close()
        Logs.append(str_log)
        return string
    return 'no info'


# Запись лога и вывод на экран
def log(*info: any, log_type: str = None) -> bool:
    string = in_log(*info)
    if log_type == 'title':
        count: int = round((100 - len(string)) / 2 - 1)
        count = 2 if count < 2 else count
        print('-' * count, string, '-' * count)
    elif log_type == 'select':
        print(c(string, color='yellow'))
    elif log_type in ['test', 'test_fail']:
        print(string)
    elif log_type == 'SQL':
        print(f'[{log_type}]:', c(string, color='blue'))
    elif log_type is None:
        print(string)
    else:
        print(f'[{log_type}]:', string)
    if string == 'no info': return False
    return True


# Запись лога ошибок
def err_log(*info: any) -> bool:
    string = in_log(*info, file='log_error.txt')
    print(c('[!!!error!!!]:', color='red'), string)
    if string == 'no info': return False
    return True

