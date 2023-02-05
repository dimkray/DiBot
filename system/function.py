from system.string import list_str
import traceback
import os

# ---------------------------------------------------------
# Внутренние сервисы по работе с функциями
Defs = {}  # Внутренний словарь всех функций


# ---------------------------------------------------------
# вн.сервис AddDef - Добавление описание функции
def add_fun(name, description, sarg={}, sreturn=None, sclass=''):
    global serv
    if sclass != '':
        serv = sclass
    if serv != '' and sclass == '':
        if serv not in Defs:
            Defs[serv] = {}
        Defs[serv][name] = {}
        Defs[serv][name]['desc'] = description
        Defs[serv][name]['arg'] = sarg
        Defs[serv][name]['return'] = sreturn
    else:
        Defs[name] = {'class': description}
    return Defs


# ------------------- основные функции fixer -------------------------


# Получить имя текущей функции
def get_fun(from_index: int = 3) -> [str, str, str]:
    """Получить имя текущей функции"""
    module = ''
    paths: list = []
    stack = traceback.extract_stack()
    items = [st[2] for st in stack]
    modules = [st[0] for st in stack]
    items.reverse()
    modules.reverse()
    items = [item for i, item in enumerate(items) if i >= from_index]
    for i, item in enumerate(items):
        if item == '<module>':
            module = os.path.basename(modules[from_index])[:-3]
            if module[0] == '<': return ['no module', '', '']
            break
        elif item == '__call__':
            paths.append(os.path.basename(modules[i + 2])[:-3])
        else:
            paths.append(item)
    paths.reverse()
    path = list_str(paths, sep='/')
    fun = items[0]
    return [module, fun, path]

