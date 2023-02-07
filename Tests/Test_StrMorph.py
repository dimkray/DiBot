from Profiler import Profiler
from Tests import Testing
from Tests.Testing import Test, Report
from services.StrMorph import String, Word, Modif


Testing.testService = 'StrMorth'

print('------- Запущены тесты сервиса %s --------' % Testing.testService)

# здесь тестовая обработка #
with Profiler() as p:
    # StringsCount
    Testing.testDef = 'StringsCount'
    test = String.StringsCount('Предложение один. Предложение два! Предложение три?!!! Четыре... !')
    Test.Add('normal', test, 5)

    test = String.StringsCount(' ')
    Test.Add('unreal', test, 0)

    test = String.StringsCount(5)
    Test.Add('crash', test, 0)

    # GetStrings
    Testing.testDef = 'GetStrings'
    test = String.GetStrings('Предложение один. Предложение два! Предложение три?!!! Четыре... !')
    etalon = ['Предложение один.', 'Предложение два!', 'Предложение три?!!!', 'Четыре...', '!']
    Test.Add('normal 1', test, etalon)

    test = String.GetStrings('1\n2\n\nполянка!на ! теле')
    etalon = ['1','2','полянка!на !','теле']
    Test.Add('normal 2', test, etalon)

    test = String.GetStrings(' ')
    Test.Add('unreal', test, [])

    test = String.GetStrings({'Слово':67})
    Test.Add('crash', test, [])

    # WordsCount
    Testing.testDef = 'WordsCount'
    test = String.WordsCount('Предложение - один. Пре-дложение два! Предложение три?!!! Четыре... 5 + !')
    Test.Add('normal', test, 9)

    test = String.WordsCount(' ')
    Test.Add('unreal', test, 0)

    test = String.WordsCount(5)
    Test.Add('crash', test, 0)

    # GetWords
    Testing.testDef = 'GetWords'
    test = String.GetWords('Предложение - один. Пре-дложение два! Предложение три?!!! Четыре... 5 + !')
    etalon = ['Предложение', 'один', 'Пре', 'дложение', 'два', 'Предложение', 'три', 'Четыре', '5']
    Test.Add('normal', test, etalon)

    test = String.GetWords(' ')
    Test.Add('unreal', test, [])

    test = String.GetWords(5)
    Test.Add('crash', test, [])

    # GetConstr
    Testing.testDef = 'GetConstr'
    test = String.GetConstr('Сервис по - проверке и оплате штрафов ГИБДД; через интернет онлайн. Вы + !')
    etalon = '[Сервис] [по] - [проверке] [и] [оплате] [штрафов] [ГИБДД]; [через] [интернет] [онлайн]. [Вы] + !'
    Test.Add('normal', test, etalon)

    test = String.GetConstr(' ')
    Test.Add('unreal', test, ' ')

    test = String.GetConstr(5)
    Test.Add('crash', test, 5)

    # Tags
    Testing.testDef = 'Tags'
    test = Word.Tags('Табареками')
    Test.Add('normal 1', test, ['NOUN','anim','masc','Name','plur','ablt'])

    test = Word.Tags('козе')
    Test.Add('normal 2', test, ['NOUN','anim','femn','sing','datv'])
    
    test = Word.Tags('Два слова')
    Test.Add('unreal 1', test, ['NOUN','inan','neut','sing','gent'])

    test = Word.Tags(' ')
    Test.Add('unreal 2', test, [])

    test = Word.Tags(5)
    Test.Add('crash', test, [])


    # LangDetect
    Testing.testDef = 'LangDetect'
    test = String.LangDetect('Табареками')
    Test.Add('normal 1', test, 'русский')

    # Translit
    Testing.testDef = 'Translit'
    test = Modif.Translit('Turaabad')
    Test.Add('normal 1', test, 'Тураабад')

    test = Modif.Translit('Shyukyurbeyli')
    Test.Add('normal 2', test, 'Шукюрбейли')

print('')
print('------- Отчёт тестов сервиса %s --------' % Testing.testService)
print(Report.WriteAll(service=Testing.testService))
print('')
print('------- Найдены ошибки сервиса %s  --------' % Testing.testService)
print(Report.WriteFails(service=Testing.testService))
