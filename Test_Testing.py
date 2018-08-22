from Profiler import Profiler
from Tests import Testing
from Tests.Testing import Comp, Test, Report

Testing.testService = 'Testing'
print('------- Запущены тесты сервиса %s --------' % Testing.testService)


with Profiler() as p:
    # strEqual
    Testing.testDef = 'strEqual'
    test = Testing.strEqual('Тест', 'тест')
    Test.Add('normal', test, 0.9)

# здесь тестовая обработка #
with Profiler() as p:
    Testing.testService = 'Comp'
    Testing.testDef = 'isWork'
    test = Comp.isWork(None, None)
    Test.Add('автопроверка', test, 0)

    test = Comp.isWork(1, None)
    Test.Add('автопроверка', test, 1)

    test = Comp.isWork('Работает', None, ['Работает'], 1, 'работает', {'Работает': 'Работает'})
    Test.Add('автопроверка', test, 1)

    test = Comp.isWork('Работает', None, ['Работает'], 1, u'Работает', {'Работает': 'Работает'})
    Test.Add('автопроверка', test, 0)

    Testing.testDef = 'sWork'
    test = Comp.sWork('Всё хорошо!')
    Test.Add('автопроверка', test, 1)

    test = Comp.sWork('#bug: Всё плохо :(')
    Test.Add('автопроверка', test, 0)

    test = Comp.sWork('#critical: Всё ужасно :(')
    Test.Add('автопроверка', test, 0)

    test = Comp.sWork('#probem Всё не так плохо :)')
    Test.Add('автопроверка', test, 1)

    test = Comp.sWork(['Другой тип'])
    Test.Add('автопроверка', test, 0)

    Testing.testDef = 'isType'
    test = Comp.isType(1, 100)
    Test.Add('автопроверка', test, 1)

    test = Comp.isType(5.0, 5)
    Test.Add('автопроверка', test, 0)

    test = Comp.isType({}, [])
    Test.Add('автопроверка', test, 0)

    test = Comp.isType('строка', "другая строка")
    Test.Add('автопроверка', test, 1)

    Testing.testDef = 'Equal'
    test = Comp.Equal(100, 99)
    Test.Add('автопроверка', test, 0)

    test = Comp.Equal(5.0, 5)
    Test.Add('автопроверка', test, 1)

    test = Comp.Equal({'тест': 'тест'}, ['тест'])
    Test.Add('автопроверка', test, 0)

    test = Comp.Equal('строка', "строка")
    Test.Add('автопроверка', test, 1)

    test = Comp.Equal('строка2', u'строка2')
    Test.Add('автопроверка', test, 1)

    test = Comp.Equal('строка2', 'строка 2')
    Test.Add('автопроверка', test, 0)

    test = Comp.Equal(['тест1'], ['тест'])
    Test.Add('автопроверка', test, 0)

    test = Comp.Equal(['тест', 'тест2'], ['тест'])
    Test.Add('автопроверка', test, 0)

    Testing.testDef = 'fEqual'
    test = Comp.fEqual('строка2', 'строка2 ')
    Test.Add('автопроверка', test, 0)

    test = Comp.fEqual(1, 2)
    Test.Add('автопроверка', test, 0)

    test = Comp.fEqual(1.000, 0.995)
    Test.Add('автопроверка', test, 0.5, critery=0.49)

    test = Comp.fEqual(0.0001, 0)
    Test.Add('автопроверка', test, 0)

    test = Comp.fEqual(0.998, 0.998)
    Test.Add('автопроверка', test, 1)

    test = Comp.fEqual(1, '1')
    Test.Add('автопроверка', test, 0)

    Testing.testDef = 'strEqual'
    test = Comp.strEqual(' тест', 'тест')
    Test.Add('автопроверка', test, 0.95)
    
    test = Comp.strEqual('Тест', 'тест')
    Test.Add('автопроверка', test, 0.9)
    
    test = Comp.strEqual('тест', 'тест')
    Test.Add('автопроверка', test, 1)

    test = Comp.strEqual(1, 'тест')
    Test.Add('автопроверка', test, 0.0)

    # доработать...
    test = Comp.strEqual('тест тестов', 'тестов тест')
    Test.Add('автопроверка', test, 0.0)
    
    test = Comp.strEqual('Предложение один. Предложение два', 'Предложение два. Предложение один')
    Test.Add('автопроверка', test, 0.0)
    
    test = Comp.strEqual('слово дело слово дело', 'слово делать')
    Test.Add('автопроверка', test, 0.0)

    test = Comp.strEqual('Квартира в центре Петербурга со скидкой 20%! Дом сдан!',
                         'Квартира в центре Петербурга со скидкой 25%! Дом сдан!')
    Test.Add('автопроверка', test, 0.45)

    Testing.testDef = 'listEqual'
    test = Comp.listEqual('тесты', 'тест')
    Test.Add('автопроверка', test, 0.8)
    
    test = Comp.listEqual([1, 2, 3, 4, 5], [1, 2, 3, 5, 4])
    Test.Add('автопроверка', test, 0.6, critery=0.9)
    
    test = Comp.listEqual(['1', '2', '6'], ['1', '2', '3'])
    Test.Add('автопроверка', test, 0.666, critery=0.8)

    test = Comp.listEqual([1, 2, 3, 4.1, 5], [1, 2, 3, 4.101, 5])
    Test.Add('автопроверка', test, 0.8)

    # Add
    Testing.testService = 'Test'
    Testing.testDef = 'Add'
    test = Test.Add('Name', 'test', 'Test', critery=0.9)
    etalon = ['Test.Add', 'Name', 'test', 'Test', 0.9, True, 0, "Сравнение <class 'str'>", 'Test']
    Test.Add('автопроверка', test, etalon)

print('------- Запущены тесты --------')
print(Report.WriteAll(service='Testing'))
print(Report.WriteAll(service='Comp'))
print(Report.WriteAll(service='Test'))
print('')
print('------- Найдены ошибки --------')
print(Report.WriteFails(service='Testing'))
print(Report.WriteFails(service='Comp'))
print(Report.WriteFails(service='Test'))
