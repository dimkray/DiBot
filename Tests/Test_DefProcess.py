from Profiler import Profiler
from Tests import Testing
from Tests.Testing import Test, Report
from services.DefProcess import Run


Testing.testService = 'DefProcess'

print('------- Запущены тесты сервиса %s --------' % Testing.testService)

# здесь тестовая обработка #
with Profiler() as p:
    # GetAllMembers
    Testing.testDef = 'GetAllMembers'
    test = Run.get_all_members('self')
    etalon = ['__add__', '__class__', '__contains__', '__delattr__',
              '__dir__', '__doc__', '__eq__', '__format__', '__ge__',
              '__getattribute__', '__getitem__', '__getnewargs__',
              '__gt__', '__hash__', '__init__', '__init_subclass__',
              '__iter__', '__le__', '__len__', '__lt__', '__mod__',
              '__mul__', '__ne__', '__new__', '__reduce__', '__reduce_ex__',
              '__repr__', '__rmod__', '__rmul__', '__setattr__', '__sizeof__',
              '__str__', '__subclasshook__', 'capitalize', 'casefold',
              'center', 'count', 'encode', 'endswith', 'expandtabs',
              'find', 'format', 'format_map', 'index', 'isalnum',
              'isalpha', 'isdecimal', 'isdigit', 'isidentifier',
              'islower', 'isnumeric', 'isprintable', 'isspace', 'istitle',
              'isupper', 'join', 'ljust', 'lower', 'lstrip', 'maketrans',
              'partition', 'replace', 'rfind', 'rindex', 'rjust',
              'rpartition', 'rsplit', 'rstrip', 'split', 'splitlines',
              'startswith', 'strip', 'swapcase', 'title', 'translate',
              'upper', 'zfill']
    Test.Add('normal', test, etalon)

    # GetAllAttrs - пропуск, т.к. состав и порядок динамически меняется

    # GetGlobals
    Testing.testDef = 'GetGlobals'
    test = Run.get_globals()
    etalon = ['Fixer', 'inspect', 'Test', 'uniq', 'GetAllMembers',
              'GetAllAttrs', 'GetGlobals', 'GetClass', 'GetMembers',
              'GetAttrs', 'GetArgs', 'Code', 'Run']
    Test.Add('normal', test, etalon)

    # GetClass
    Testing.testDef = 'GetClass'
    test = Run.get_class('Test')
    Test.Add('normal', test, Test)

    # GetMembers
    Testing.testDef = 'GetMembers'
    test = Run.get_members('Test')
    etalon = ['capitalize', 'casefold', 'center', 'count', 'encode',
              'endswith', 'expandtabs', 'find', 'format', 'format_map',
              'index', 'isalnum', 'isalpha', 'isdecimal', 'isdigit',
              'isidentifier', 'islower', 'isnumeric', 'isprintable',
              'isspace', 'istitle', 'isupper', 'join', 'ljust', 'lower',
              'lstrip', 'maketrans', 'partition', 'replace', 'rfind',
              'rindex', 'rjust', 'rpartition', 'rsplit', 'rstrip', 'split',
              'splitlines', 'startswith', 'strip', 'swapcase', 'title',
              'translate', 'upper', 'zfill']
    Test.Add('normal', test, etalon)

    # GetAttrs - пропуск, т.к. состав и порядок динамически меняется
    test = Run.get_attrs('Test')

    # GetArgs
    Testing.testDef = 'GetArgs'
    test = Run.get_args(Test.Add)
    etalon = ['service', 'name', 'testvalue', 'etalonvalue', 'time', 'critery']
    Test.Add('normal', test, etalon)

    # Code
    Testing.testDef = 'Code'
    test = Run.code('4 + 2 / 5')
    Test.Add('normal 1', test, 4.4)

    test = Run.code('"Пять" if 5 > 4 else "Четыре"')
    Test.Add('normal 2', test, 'Пять')

    test = Run.code('4 + 2 / 0')
    etalon = '#bug: division by zero'
    Test.Add('unreal', test, etalon)

    test = Run.code(5 + 7)
    etalon = '#bug: eval() arg 1 must be a string, bytes or code object'
    Test.Add('crash', test, etalon)

    # Run
    Testing.testDef = 'Run'
    test = Run.run('Tests.Testing', 'Comp', 'fEqual', 9.99, 10)
    Test.Add('normal', test, 0.9, critery=0.99)

    test = Run.run('Tests.Testing', 'Test', 'Equal', 10, 10)
    Test.Add('crash 1', test, "#bug: type object 'Test' has no attribute 'Equal'")

    test = Run.run('Tests.Testing', 'Comp', 'Equal', 10, 10, 1)
    Test.Add('crash 2', test, '#bug: Equal() takes 2 positional arguments but 3 were given')

    test = Run.run('Tests.Testing', 'Comp', 'Equals', 10, 10)
    Test.Add('crash 3', test, "#bug: type object 'Comp' has no attribute 'Equals'")

print('')
print('------- Отчёт тестов сервиса %s --------' % Testing.testService)
print(Report.WriteAll())
print('')
print('------- Найдены ошибки сервиса %s  --------' % Testing.testService)
print(Report.WriteFails())
