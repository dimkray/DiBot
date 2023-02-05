
# Основной класс по работе с функциями и другими классами
Fixer.add_fun('Run', 'Основной класс по работе с функциями и другими классами', sclass='Run')

class Run:

    # Полчение списка всех функций указанного класса (включая системные)
    Fixer.add_fun('GetAllMembers', 'Получение списка всех функций указанного класса (включая системные)',
                  {'iclass': 'класс [class]'},
                 'список функций [list<string>]')

    def GetAllMembers(iclass):
        ret = dir(iclass)
        if hasattr(iclass, '__bases__'):
            for base in iclass.__bases__:
                ret = ret + Run.GetAllMembers(base)
        return ret


    # Получение всех атрибутов указанного класса/объекта (включая системные)
    Fixer.add_fun('GetAllAttrs', 'Получение всех атрибутов указанного класса/объекта (включая системные)',
                  {'iclass': 'класс или объект [class/object]'},
                 'список атрибутов [list<string>]')

    def GetAllAttrs(obj):
        ret = dir(obj)
        if hasattr(obj, '__class__'):
            ret.append('__class__')
            ret.extend(Run.GetAllMembers(obj.__class__))
            print(ret)
            ret = list(set(ret))
            print(ret)
        return ret


    # Получение всех активных глобальных объектов (списком)
    Fixer.add_fun('GetGlobals', 'Получение всех активных глобальных объектов', {},
                 'список глобальных объектов [list<string>]')

    def GetGlobals():
        mlist = []
        for key in globals():
            if not key.startswith("__"):
                mlist.append(key)
        return mlist


    # Получение указанного класса
    Fixer.add_fun('GetClass', 'Получение указанного класса',
                  {'name': 'имя класса [string]'},
                 'класс [class]')

    def GetClass(name):
        cl = globals()[name]
        return cl


    # Полчение списка всех функций указанного класса
    Fixer.add_fun('GetMemberList', 'Полчение списка всех функций указанного класса',
                  {'iclass': 'класс [class]'},
                 'список всех функций класса [list<string>]')

    def GetMemberList(iclass):
        mlist = []
        for i in Run.GetAllMembers(iclass):
            if not i.startswith("__"):
                mlist.append(i)
        return mlist


    # Полчение списка всех функций указанного класса (с функциями)
    Fixer.add_fun('GetMembers', 'Полчение списка всех функций указанного класса (с функциями)',
                  {'iclass': 'класс [class]'},
                 'список всех функций класса [list<string>]')

    def GetMembers(iclass):
        import inspect
        return inspect.getmembers(iclass, predicate=inspect.isfunction)


    # Получение всех атрибутов указанного класса
    Fixer.add_fun('GetAttrs', 'Получение всех атрибутов указанного класса/объекта',
                  {'obj': 'класс/объект [class/object]'},
                 'список всех атрибутов класса/объекта [list<string>]')

    def GetAttrs(obj):
        mlist = []
        for i in Run.GetAllAttrs(obj):
            if not i.startswith("__"):
                mlist.append(i)
        return mlist


    # Получение всех аргументов указанной функции
    Fixer.add_fun('GetArgs', 'Получение всех аргументов указанной функции',
                  {'member': 'функция [def]'},
                 'список всех аргументов функции [list<string>]')

    def GetArgs(member):
        import inspect
        argspec = inspect.getfullargspec(member)
        return argspec.args


    # Запуск кода
    Fixer.add_fun('Code', 'Запуск однострочного кода',
                  {'code': 'строка кода python [string]'},
                 'результат работы [?/string]')

    def Code(code):
        try:
            return eval(code)
        except Exception as e:
            Fixer.errlog('Def.Code', str(e))
            return '#bug: ' + str(e)


    # Запуск функции из сервиса с аргументами
    Fixer.add_fun('Run', 'Запуск функции из сервиса с аргументами',
                  {'module': 'имя модуля [string]', 'nameclass': 'имя класса [string]',
                  'namedef': 'имя функции класса [string]', '*args': 'агрументы функции через запятую [?,?,?...]'},
                 'результат работы [?/string]')

    def Run(module, nameclass, namedef, *args):
        try:
            import importlib, sys
            mod = sys.modules[module]
            if nameclass != '':
                cl = getattr(mod, nameclass)
                func = getattr(cl, namedef)
            else:
                func = getattr(mod, namedef)
            return func(*args)
        except Exception as e:
            Fixer.errlog('Def.Run', str(e))
            return '#bug: ' + str(e)


    # отображение всех записанных и используемых классов
    def WriteClasses():
        mClasses = []
        mCls = Run.GetGlobals()
        for iclass in mCls:
            if iclass in Fixer.Defs:
                mClasses.append([iclass, len(Fixer.Defs[iclass]) - 1, Fixer.Defs[iclass]['class']])
                print(iclass + ' - ' + Fixer.Defs[iclass]['class'])
            else:
                mClasses.append([iclass, '?', '? описания нет ?'])
                print(iclass + ' - ? описания нет')
        return Fixer.mFormat(mClasses, items=100, sformat='%0 : %1 функций - %2', sobj='классов')


    # отображение всех записанных и используемых функций класса/сервиса
    def WriteDefs(sclass=''):
        mDefs = []
        if sclass != '':
            mMem = Run.GetMemberList(Run.GetClass(sclass))
            print(mMem)
            for iMem in mMem:
                bDesc = False
                if sclass in Fixer.Defs:
                    if iMem in Fixer.Defs[sclass]:
                        mDefs.append([iMem, len(Fixer.Defs[sclass][iMem]['arg']), Fixer.Defs[sclass][iMem]['desc']])
                        print(iMem + ' - ' + Fixer.Defs[sclass][iMem]['desc'])
                        bDesc = True
                if bDesc == False:
                    mDefs.append([iMem, '?', '? описания нет ?'])
                    print(iMem + ' - ? описания нет')
            return Fixer.mFormat(mDefs, items=100, sformat='%0 : %1 парам. - %2', sobj='функций')
        else:  # если надо получить все классы
            for iclass in Fixer.Defs:
                for iDef in Fixer.Defs[iclass]:
                    if iDef != 'class':
                        mDefs.append([iclass, iDef, len(Fixer.Defs[sclass][iDef]['arg']), Fixer.Defs[sclass][iDef]['desc']])
                        print(iclass + '.' + iDef + ' - ' + Fixer.Defs[sclass][iDef]['desc'])
            return Fixer.mFormat(mDefs, items=100, sformat='%0.%1 : %2 парам. - %3', sobj='функций')


    # отображение всех параметров функций
    def WriteDef(ClassDef):
        m = Fixer.get_params(ClassDef, separator='.')
        sClass = m[0]
        sDef = m[1]
        if sClass in Fixer.Defs:
            if sDef in Fixer.Defs[sClass] and sDef != 'class':
                sText = sClass + '.' + sDef + '('
                print(sText)
            else:
                # if Run.GetArgs()
                return 'Функция %s в классе %s не найдена!' % (sDef, sClass)
        else:
            return 'Класс %s не найден!' % sClass
        mArgs = []
        for iArg in Fixer.Defs[sClass][sDef]['arg']:
            sText += iArg + ', '
            mArgs.append([iArg, Fixer.Defs[sClass][sDef]['arg'][iArg]])
        if len(Fixer.Defs[sClass][sDef]['arg']) < 1:
            sText += '  '
        sText = sText[:-2] + ') - ' + Fixer.Defs[sClass][sDef]['desc'] + '\n'
        sText += Fixer.mFormat(mArgs, items=10, sformat='%0 - %1', sobj='параметров')
        sText += '\nВозвращаемый параметр: ' + str(Fixer.Defs[sClass][sDef]['return'])
        print(sText)
        return sText
