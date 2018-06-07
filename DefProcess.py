# -*- coding: utf-8 -*-
# Сервис по работе с функциями и процедурами
from Services.Yandex import Yandex
import inspect

def getMembers(iclass):
    ret = dir(iclass)
    if hasattr(iclass,'__bases__'):
        for base in iclass.__bases__:
            ret = ret + getMembers(base)
    return ret

def uniq(seq): 
    return list(set(seq))

def getAttrs(obj):
    ret = dir(obj)
    if hasattr(obj,'__class__'):
        ret.append('__class__')
        ret.extend(getMembers(obj.__class__))
        ret = uniq(ret)
    return ret

class Def:
    # Получение указанного класса
    def GetClass(name):
        cl = globals()[name]
        return cl

    # Полчение списка всех функций указанного класса
    def GetMembers(iclass):
        mlist = []
        for i in getMembers(iclass):
            if not i.startswith("__"):
                mlist.append(i)
        return mlist

    # Получение всех атрибутов указанного класса
    def GetAttrs(obj):
        mlist = []
        for i in getAttrs(obj):
            if not i.startswith("__"): mlist.append(i)
        return mlist

    # Получение всех аргументов указанной функции
    def GetArgs(member):
        argspec = inspect.getfullargspec(member)
        print(argspec)
        return argspec.args

    # Запуск кода
    def Code(code):
        try:
            return eval(code)
        except Exception as e: 
            Fixer.errlog('Def.Run', str(e))
            return '#bug: ' + str(e)

    # Запуск функции из сервиса с аргументами
    def Run(module, nameclass, namedef, *args):
        import importlib, sys
        #mod_name, func_name = namedef.rsplit('.',1)
        #print(mod_name)
        #print(func_name)
        mod = sys.modules[module]
        #mod = importlib.import_module(mod_name)
        if nameclass != '':
            cl = getattr(mod, nameclass)
            func = getattr(cl, namedef)
        else: func = getattr(mod, namedef)
        return func(*args)

    #def WriteMembers(iclass):

#s = input('название функции')
cl = Def.GetClass('Yandex')

print(Def.GetMembers(cl))
#print(Def.GetAttrs(cl))
print(Def.GetArgs(cl.FindRasp))
print(Def.Run('Services.Yandex', 'Yandex', 'FindRasp', 'Москва - Минск'))

test = input('Введите код: ')
print(Def.Code(test))
