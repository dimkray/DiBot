import Fixer
from Profiler import Profiler
from Tests.Testing import Comp, Test, Report

service = 'Testing'

# здесь тестовая обработка #
with Profiler() as p:
    # isWork
    ftest = Comp.isWork(None,None)
    Test.Add(service+'.isWork','автопроверка', ftest, 0)

    ftest = Comp.isWork(1,None)
    Test.Add(service+'.isWork','автопроверка', ftest, 1)

    ftest = Comp.isWork('Работает', None, ['Работает'], 1, 'работает', {'Работает':'Работает'})
    Test.Add(service+'.isWork','автопроверка', ftest, 1)

    ftest = Comp.isWork('Работает', None, ['Работает'], 1, u'Работает', {'Работает':'Работает'})
    Test.Add(service+'.isWork','автопроверка', ftest, 0)

    # sWork
    ftest = Comp.sWork('Всё хорошо!')
    Test.Add(service+'.sWork','автопроверка', ftest, 1)

    ftest = Comp.sWork('#bug: Всё плохо :(')
    Test.Add(service+'.sWork','автопроверка', ftest, 0)

    ftest = Comp.sWork('#critical: Всё ужасно :(')
    Test.Add(service+'.sWork','автопроверка', ftest, 0)

    ftest = Comp.sWork('#probem Всё не так плохо :)')
    Test.Add(service+'.sWork','автопроверка', ftest, 1)

    ftest = Comp.sWork(['Другой тип'])
    Test.Add(service+'.sWork','автопроверка', ftest, 0)

    # isType
    ftest = Comp.isType(1, 100)
    Test.Add(service+'.isType','автопроверка', ftest, 1)

    ftest = Comp.isType(5.0, 5)
    Test.Add(service+'.isType','автопроверка', ftest, 0)

    ftest = Comp.isType({},[])
    Test.Add(service+'.isType','автопроверка', ftest, 0)

    ftest = Comp.isType('строка',"другая строка")
    Test.Add(service+'.isType','автопроверка', ftest, 1)    

    # Equal
    ftest = Comp.Equal(100, 99)
    Test.Add(service+'.Equal','автопроверка', ftest, 0)

    ftest = Comp.Equal(5.0, 5)
    Test.Add(service+'.Equal','автопроверка', ftest, 1)

    ftest = Comp.Equal({'тест':'тест'},['тест'])
    Test.Add(service+'.Equal','автопроверка', ftest, 0)

    ftest = Comp.Equal('строка',"строка")
    Test.Add(service+'.Equal','автопроверка', ftest, 1)

    ftest = Comp.Equal('строка2',u'строка2')
    Test.Add(service+'.Equal','автопроверка', ftest, 1)

    ftest = Comp.Equal('строка2','строка 2')
    Test.Add(service+'.Equal','автопроверка', ftest, 0)

    ftest = Comp.Equal(['тест1'],['тест'])
    Test.Add(service+'.Equal','автопроверка', ftest, 0)

    ftest = Comp.Equal(['тест','тест2'],['тест'])
    Test.Add(service+'.Equal','автопроверка', ftest, 0) 

    # fEqual
    ftest = Comp.fEqual('строка2','строка2 ')
    Test.Add(service+'.fEqual','автопроверка', ftest, 0)

    ftest = Comp.fEqual(1, 2)
    Test.Add(service+'.fEqual','автопроверка', ftest, 0)

    ftest = Comp.fEqual(1.000, 0.995)
    Test.Add(service+'.fEqual','автопроверка', ftest, 0.5, critery=0.49)

    ftest = Comp.fEqual(0.0001, 0)
    Test.Add(service+'.fEqual','автопроверка', ftest, 0)

    ftest = Comp.fEqual(0.998, 0.998)
    Test.Add(service+'.fEqual','автопроверка', ftest, 1)

    ftest = Comp.fEqual(1, '1')
    Test.Add(service+'.fEqual','автопроверка', ftest, 0)

    # strEqual
    ftest = Comp.strEqual(' тест','тест')
    Test.Add(service+'.strEqual','автопроверка', ftest, 0.95)
    
    ftest = Comp.strEqual('Тест','тест')
    Test.Add(service+'.strEqual','автопроверка', ftest, 0.9)
    
    ftest = Comp.strEqual('тест','тест')
    Test.Add(service+'.strEqual','автопроверка', ftest, 1)

    ftest = Comp.strEqual(1,'тест')
    Test.Add(service+'.strEqual','автопроверка', ftest, 0.0)

    # доработать...
    ftest = Comp.strEqual('тест тестов','тестов тест')
    Test.Add(service+'.strEqual','автопроверка', ftest, 0.0)
    
    ftest = Comp.strEqual('Предложение один. Предложение два','Предложение два. Предложение один')
    Test.Add(service+'.strEqual','автопроверка', ftest, 0.0)
    
    ftest = Comp.strEqual('слово дело слово дело','слово делать')
    Test.Add(service+'.strEqual','автопроверка', ftest, 0.0)

    ftest = Comp.strEqual('Квартира в центре Петербурга со скидкой 20%! Дом сдан!','Квартира в центре Петербурга со скидкой 25%! Дом сдан!')
    Test.Add(service+'.strEqual','автопроверка', ftest, 0.45)

    # listEqual
    ftest = Comp.listEqual('тесты','тест')
    Test.Add(service+'.listEqual','автопроверка', ftest, 0.8)
    
    ftest = Comp.listEqual([1,2,3,4,5],[1,2,3,5,4])
    Test.Add(service+'.listEqual','автопроверка', ftest, 0.6, critery=0.9)
    
    ftest = Comp.listEqual(['1','2','6'],['1','2','3'])
    Test.Add(service+'.listEqual','автопроверка', ftest, 0.666, critery=0.8)

    ftest = Comp.listEqual([1,2,3,4.1,5],[1,2,3,4.101,5])
    Test.Add(service+'.listEqual','автопроверка', ftest, 0.8)

    # Add
    test = Test.Add('Test','Name','test','Test',critery=0.9)
    Test.Add(service+'.Add','автопроверка', test, ['Test','Name','test','Test',0.9,True,0,"Сравнение <class 'str'>"])    

print('------- Запущены тесты --------')
print(Report.WriteAll())
print('')
print('------- Найдены ошибки --------')
print(Report.WriteFails())
