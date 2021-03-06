# -*- coding: utf-8 -*-
# Сервис по работе с функциями и процедурами
import Fixer

# Основной класс по работе с функциями и другими классами
Fixer.AddDef('Runner', 'Класс по работе с функциями и другими классами', sclass='Runner')

class Runner:

    # Полчение списка всех функций указанного класса (включая системные)
    Fixer.AddDef('GetAllMembers', 'Получение списка всех функций указанного класса (включая системные)',
                 {'iclass': 'класс [class]'},
                 'список функций [list<string>]')

    def GetAllMembers(iclass):
        ret = dir(iclass)
        if hasattr(iclass, '__bases__'):
            for base in iclass.__bases__:
                ret = ret + Runner.GetAllMembers(base)
        return ret

    # Полчение списка всех функций указанного класса
    Fixer.AddDef('GetMemberList', 'Полчение списка всех функций указанного класса',
                 {'iclass': 'класс [class]'},
                 'список всех функций класса [list<string>]')

    def GetMemberList(iclass):
        mlist = []
        for i in Runner.GetAllMembers(iclass):
            if not i.startswith("__"):
                mlist.append(i)
        return mlist