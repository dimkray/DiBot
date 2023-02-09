"""
    Модуль работы над строками / текстами
"""
import config


# ---------------------------------------------------------
# вн.сервис отобразить список строкой
def list_str(listing: any, sep=', ') -> str:
    """Функция преобразования любого списка [listing] в строку с разделителем [sep]"""
    if not listing: return ''
    string = ''
    for item in listing:
        string += str(item) + sep
    return string[:-len(sep)]


# ---------------------------------------------------------
# вн.сервис substitution - подстановка строковых переменных
def insert_substring(text: str):
    text = text.replace('\\n', '\n')
    if text.find('[') >= 0:
        for word in config.WORDS:
            if word in text: text.replace(word, config.WORDS[word])
    return text


# ---------------------------------------------------------
# вн.сервис getparams - получение переменных в массив [] из строки переменных для сервиса
def get_params(text: str, separator='|') -> list:
    """Получение переменных в список [list] из строки переменных [text] для сервиса"""
    if text.find(separator) < 0 and separator != ';':  # нет текущего сепаратора
        if text.find(' - ') > 0: separator = ' - '
        else:
            if text.find(',') > 0: separator = ','
            else: separator = ' '
    if text.find('[R') >= 0:  # Признак радиуса интереса
        poz = text.find('[R')
        end = text.find(']', poz)
        print(text[poz + 2:end - 1])
        config.RADIUS_INTEREST = float(text[poz + 2:end - 1])
        text = text.replace('[R' + text[poz + 2:end - 1] + ']', '')  # Убираем радиус интереса
    params = text.split(separator)
    for x, im in enumerate(params):
        params[x] = im.strip()  # убираем лишние пробелы
    return params



# ---------------------------------------------------------
# вн.сервис strOperand - преобразование различных операций с возможными числами
def str_operand(value, number, operand='*'):
    s = ''
    if value is not None:
        value = float(value)
        if operand == '*':
            return str(value * number)
        elif operand == '/':
            return str(value / number)
        elif operand == '-':
            return str(value - number)
        else:
            return str(value + number)
    return s


# ---------------------------------------------------------
# вн.сервис strfind - поиск строки и обрезка по найденному (регистронезависимый)
def str_find(text: str, mfind: list, poz=0) -> (str, str):
    textU = text.upper()
    for sfind in mfind:
        ilen = len(sfind)
        if poz >= 0:  # если ищем по тексту в определённой позиции
            if textU.find(sfind.upper()) == poz:
                return sfind, (text[:poz] + text[poz + ilen:]).strip()  # вырезание
        else:  # если ищем везде
            if textU.find(sfind.upper()) >= 0:
                while textU.find(sfind.upper()) >= 0:
                    text = text[:poz] + text[poz + ilen:]  # вырезание
                    textU = text.upper()
                return sfind, text.strip()
    return '', text  # ничего не нашлось


# ---------------------------------------------------------
# вн.сервис strCleaner - упрощение строки (убирает все лишние символы)
def str_cleaner(text):
    dFormat = {'ё': 'е', '«': '', '»': '', '!': '', '@': '', '~': '', '#': '', '^': '', '&': '', '*': '',
               '(': '', ',': '', '- ': ' ', '+': '', '=': '', '{': '', '}': '', '[': '', ']': '', ';': '',
               ':': '', '?': '', '<': '', '>': '', '.': '', '`': '', '\\': '', '|': '', '/': '', '  ': ' '}
    text = text.strip().lower()
    for key in dFormat:
        text = text.replace(key, dFormat[key])
    return text


# ---------------------------------------------------------
# вн.сервис strSpec - заменяет спецсимволы на номальные символы
def str_spec(text):
    dFormat = {'&quot;': '"', '&nbsp;': ' ', '&ensp;': ' ', '&emsp;': '  ', '&ndash;': '-', '&mdash;': '—',
               '&shy;': ' ', '&copy;': '©', '&reg;': '®', '&trade;': '™', '&permil;': '‰', '&deg;': '°'}
    for key in dFormat:
        text = text.replace(key, dFormat[key])
    return text


# ---------------------------------------------------------
# вн.сервис strAdd - добавление строки, если есть
def str_add(value, text=''):
    global stxt
    s = ''
    if value is not None:
        if text != '':
            s = '%s: %s\n' % (text, str(value))
        else:
            s = '%s\n' % str(value)
    stxt += s
    return s


# ---------------------------------------------------------
# вн.сервис strPut - добавление строки, если есть
def str_put(value: str, alternative: str = '') -> str:
    if value: return str(value)
    else: return alternative


# ---------------------------------------------------------
# вн.сервис dFormat - преобразование результата dict в форматированный текст - список
# если задан формат: sformat = 'Номер: {number} - значение: {value}' - приоритетно
# если заданы подписи ключей: nameKey = {'number': 'номер', 'value': 'значение', 'no_write': '#'}  # - не подписывать
def dict_format(dresult, items=5, sformat='', nameKey={}, sobj='объектов'):
    if len(dresult) > 0:  # если есть результат
        s = 'По запросу найдено %s: %i' % (sobj, len(dresult))
        if items < len(dresult):
            s += '\nБудут показаны первые %i:' % items
        else:
            items = len(dresult)
        for i in range(0, items):
            obj = dresult[i]
            if sformat == '':  # если не задан формат
                if len(nameKey) == 1:  # если нужен только один ключ
                    s += '\n[%i] %s' % (i + 1, obj[nameKey.keys()[0]])
                elif len(nameKey) > 1:  # если есть подписи для ключей
                    s += '\n[%i] ' % (i + 1)
                    for key in nameKey.keys():
                        if nameKey[key] == '#':
                            s += '%s' % (obj[key])
                        else:
                            s += '\n%s: %s' % (nameKey[key], obj[key])
                else:  # если нет подписей для ключей
                    s += '\n[%i] %s' % (i + 1, obj[nameKey.keys()[0]])
                    for key in nameKey.keys():
                        s += '\n%s: %s' % (nameKey[key], dresult[i])
            else:  # если задан формат: sformat = 'Номер: {number} - значение: {value}'
                sitem = sformat
                for key in obj.keys():
                    sitem = sitem.replace('{%s}' % key, str(obj[key]))
                s += '\n[' + str(i + 1) + '] ' + sitem
    else:
        s = 'По данному запросу нет результата'
    return s


# ---------------------------------------------------------
# вн.сервис mFormat - преобразование результата list в форматированный текст - список
# если задан формат: sformat = 'Номер: %0 - значение: %1 \\%' - приоритетно
# если заданы названия колонок: nameCol = ['номер', 'значение'] - название первой колонка игнорируется
def list_format(mresult, items=5, sformat='', nameCol=[], sobj='объектов'):
    if len(mresult) > 0:  # если есть результат
        s = 'По запросу найдено %s: %i' % (sobj, len(mresult))
        if items < len(mresult):
            s += '\nБудут показаны первые %i:' % items
        else:
            items = len(mresult)
        for i in range(0, items):
            if sformat == '':  # если не задан формат
                if len(nameCol) > 1:  # если несколько возвращаемых колонок
                    row = mresult[i]
                    s += '\n[%i] %s:' % (i + 1, row[0])
                    ic = 0
                    for col in nameCol:
                        if col == 0: ic += 1; continue
                        s += '\n%s: %s' % (col, row[ic])
                        ic += 1
                else:  # если одна возвращаемая колонка
                    s += '\n[%i] %s' % (i + 1, mresult[i])
            else:  # если задан формат: sformat = 'Номер: %0 - значение: %1 \\%'
                sitem = sformat
                row = mresult[i]
                while sitem.find('%%') >= 0:
                    x = sitem.find('%%') + 2
                    r = int(sitem[x:x + 2])
                    sitem = sitem.replace('%%' + str(r), str(row[r]))
                while sitem.find('%') >= 0:
                    x = sitem.find('%') + 1
                    r = int(sitem[x:x + 1])
                    sitem = sitem.replace('%' + str(r), str(row[r]))
                while sitem.find('\\%') >= 0:
                    sitem = sitem.replace('\\%', '%')
                s += '\n[' + str(i + 1) + '] ' + sitem
    else:
        s = 'По данному запросу нет результата'
    return s