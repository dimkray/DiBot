"""Основной модуль по работе с функциями и другими классами"""
import inspect
from typing import List

from system.function import add_fun, FUNCTIONS
from system.logging import err_log
from system.string import list_format, get_params

add_fun('Run', 'Основной модуль по работе с функциями и другими классами', sclass='Run')

add_fun('GetAllMembers', 'Получение списка всех функций указанного класса (включая системные)',
        {'iclass': 'класс [class]'},
        'список функций [list<string>]')


def get_all_members(class_obj: object) -> List[str]:
    """Получение списка всех функций указанного класса [class_name] (включая системные)"""
    def_list = dir(class_obj)
    if hasattr(class_obj, '__bases__'):
        for base in class_obj.__bases__:
            def_list += get_all_members(base)
    return def_list


# Получение всех атрибутов указанного класса/объекта (включая системные)
add_fun('GetAllAttrs', 'Получение всех атрибутов указанного класса/объекта (включая системные)',
        {'iclass': 'класс или объект [class/object]'},
        'список атрибутов [list<string>]')


def get_all_attrs(obj: object):
    """Получение всех атрибутов указанного класса/объекта [obj] (включая системные)"""
    attr_list = dir(obj)
    if hasattr(obj, '__class__'):
        attr_list.append('__class__')
        attr_list.extend(get_all_members(obj.__class__))
        print(attr_list)  # !!!
        attr_list = list(set(attr_list))
        print(attr_list)  # !!!
    return attr_list


# Получение всех активных глобальных объектов (списком)
add_fun('GetGlobals', 'Получение всех активных глобальных объектов', {},
        'список глобальных объектов [list<string>]')


def get_globals():
    """Получение всех активных глобальных объектов"""
    return [key for key in globals() if key.startswith("__")]


# Получение указанного класса
add_fun('GetClass', 'Получение указанного класса',
        {'name': 'имя класса [string]'},
        'класс [class]')


def get_class(name: str) -> object:
    """Получение указанного класса по имени [name]"""
    return globals()[name]


add_fun('GetMemberList', 'Получение списка всех функций указанного класса',
        {'iclass': 'класс [class]'},
        'список всех функций класса [list<string>]')


def get_member_list(class_obj: object) -> List[str]:
    """Получение списка всех функций указанного класса [class_obj]"""
    return [fun for fun in get_all_members(class_obj) if not fun.startswith("__")]


add_fun('GetMembers', 'Получение списка всех функций указанного класса (с функциями)',
        {'iclass': 'класс [class]'},
        'список всех функций класса [list<string>]')


def get_members(class_obj: object) -> list:
    """Получение списка всех функций указанного класса (с функциями)"""
    import inspect
    return inspect.getmembers(class_obj, predicate=inspect.isfunction)


add_fun('GetAttrs', 'Получение всех атрибутов указанного класса/объекта',
        {'obj': 'класс/объект [class/object]'},
        'список всех атрибутов класса/объекта [list<string>]')


def get_attrs(obj: object) -> List[str]:
    """Получение всех атрибутов указанного класса [obj]"""
    return [attr for attr in get_all_attrs(obj) if not attr.startswith("__")]


add_fun('GetArgs', 'Получение всех аргументов указанной функции',
        {'member': 'функция [def]'},
        'список всех аргументов функции [list<string>]')


def get_args(fun_obj: object) -> List[str]:
    """Получение всех аргументов указанной функции"""
    return inspect.getfullargspec(fun_obj).args


add_fun('Code', 'Запуск однострочного кода',
        {'code': 'строка кода python [string]'},
        'результат работы [?/string]')


def code(code_text: str) -> any:
    """Запуск однострочного кода [code_text]"""
    try:
        return eval(code_text)
    except Exception as e:
        err_log(e)
        return '#bug: ' + str(e)


add_fun('Run', 'Запуск функции из сервиса с аргументами',
        {'module': 'имя модуля [string]', 'nameclass': 'имя класса [string]',
         'namedef': 'имя функции класса [string]', '*args': 'агрументы функции через запятую [?,?,?...]'},
        'результат работы [?/string]')


def run(module: str, class_name: str, fun_name: str, *args) -> any:
    """Запуск функции [fun_name] из сервиса [module][class_name] с аргументами [*args]"""
    try:
        import importlib, sys
        mod = sys.modules[module]
        func = getattr(getattr(mod, class_name), fun_name) if class_name else getattr(mod, fun_name)
        return func(*args)
    except Exception as e:
        err_log(e)
        return '#bug: ' + str(e)


def write_classes():
    """Отображение всех записанных и используемых классов"""
    mClasses = []
    mCls = get_globals()
    for iclass in mCls:
        if iclass in FUNCTIONS:
            mClasses.append([iclass, len(FUNCTIONS[iclass]) - 1, FUNCTIONS[iclass]['class']])
            print(iclass + ' - ' + FUNCTIONS[iclass]['class'])
        else:
            mClasses.append([iclass, '?', '? описания нет ?'])
            print(iclass + ' - ? описания нет')
    return list_format(mClasses, items=100, sformat='%0 : %1 функций - %2', sobj='классов')


# отображение всех записанных и используемых функций класса/сервиса
def WriteDefs(sclass=''):
    mDefs = []
    if sclass != '':
        mMem = get_member_list(get_class(sclass))
        print(mMem)
        for iMem in mMem:
            bDesc = False
            if sclass in FUNCTIONS:
                if iMem in FUNCTIONS[sclass]:
                    mDefs.append([iMem, len(FUNCTIONS[sclass][iMem]['arg']), FUNCTIONS[sclass][iMem]['desc']])
                    print(iMem + ' - ' + FUNCTIONS[sclass][iMem]['desc'])
                    bDesc = True
            if bDesc == False:
                mDefs.append([iMem, '?', '? описания нет ?'])
                print(iMem + ' - ? описания нет')
        return list_format(mDefs, items=100, sformat='%0 : %1 парам. - %2', sobj='функций')
    else:  # если надо получить все классы
        for iclass in FUNCTIONS:
            for iDef in FUNCTIONS[iclass]:
                if iDef != 'class':
                    mDefs.append([iclass, iDef, len(FUNCTIONS[sclass][iDef]['arg']), FUNCTIONS[sclass][iDef]['desc']])
                    print(iclass + '.' + iDef + ' - ' + FUNCTIONS[sclass][iDef]['desc'])
        return list_format(mDefs, items=100, sformat='%0.%1 : %2 парам. - %3', sobj='функций')


# отображение всех параметров функций
def write_def(ClassDef):
    m = get_params(ClassDef, separator='.')
    sClass = m[0]
    sDef = m[1]
    if sClass in FUNCTIONS:
        if sDef in FUNCTIONS[sClass] and sDef != 'class':
            sText = sClass + '.' + sDef + '('
            print(sText)
        else:
            # if GetArgs()
            return 'Функция %s в классе %s не найдена!' % (sDef, sClass)
    else:
        return 'Класс %s не найден!' % sClass
    mArgs = []
    for iArg in FUNCTIONS[sClass][sDef]['arg']:
        sText += iArg + ', '
        mArgs.append([iArg, FUNCTIONS[sClass][sDef]['arg'][iArg]])
    if len(FUNCTIONS[sClass][sDef]['arg']) < 1:
        sText += '  '
    sText = sText[:-2] + ') - ' + FUNCTIONS[sClass][sDef]['desc'] + '\n'
    sText += list_format(mArgs, items=10, sformat='%0 - %1', sobj='параметров')
    sText += '\nВозвращаемый параметр: ' + str(FUNCTIONS[sClass][sDef]['return'])
    print(sText)
    return sText
