import Fixer
from DB.SQLite import SQL

def AddTable(NameTable, dCols, data):
    print('Создание таблицы "%s"' % NameTable)
    print('Результат: ' + str(SQL.Table(NameTable, dCols)))
    print('Запись данных: %i строк' % len(data))
    print('Результат: ' + str(SQL.WriteBlock(NameTable, data)))
    print('-------------------------------------')

# основной блок программы

##mNames = []
##for iname in Fixer.Names:
##    mRow = []
##    mRow.append(iname)
##    iSex = 0
##    if Names[iname][0]: iSex = 1
##    mRow.append(iSex)
##    mRow.append(Names[iname][1])
##    mRow.append(Names[iname][2])
##    mNames.append(mRow)
##AddTable('names', {'name': 'text', 'sex': 'int', 'summ': 'int', 'country': 'text'}, mNames)

##db = []
##try:
##    print('Загрузка базы anecdotes.txt...')
##    f = open('DB/anecdotes.txt', encoding='utf-8')
##    for line in f:
##        db.append(line.replace('\\','\n'))
##    f.close()
##    print('База успешно загружена!')
##except Exception as e:
##    Fixer.errlog('Fun', 'Ошибка при загрузке базы anecdotes!: ' + str(e))
##
##mAnecs = []
##i = 0
##for item in db:
##    mRow = []
##    mRow.append(i)
##    mRow.append(0)
##    mRow.append(item)
##    mAnecs.append(mRow)
##    i += 1
##AddTable('anecdotes', {'id': 'int', 'type': 'int', 'text': 'text'}, mAnecs)

##mCompliment = []
##wCompliment = []
##try:
##    i = 0
##    f = open('DB/mCompliment.txt', encoding='utf-8')
##    for line in f:
##        m = []
##        m.append(i)
##        m.append(line.replace('\n',''))
##        mCompliment.append(m)
##        i += 1
##    f.close()
##    i = 0
##    f = open('DB/wCompliment.txt', encoding='utf-8')
##    for line in f:
##        m = []
##        m.append(i)
##        m.append(line.replace('\n',''))
##        wCompliment.append(m)
##        i += 1
##    f.close()
##except Exception as e:
##    errlog('compliments', 'Ошибка при загрузке комплиментов: ' + str(e))
##
##AddTable('complimentMen', {'id':'int','text':'text'}, mCompliment)
##AddTable('complimentWoman', {'id':'int','text':'text'}, wCompliment)

##mval = []
##for kval in Fixer.Valutes:
##    m = []
##    m.append(kval)
##    m.append(Fixer.Valutes[kval])
##    mval.append(m)
##AddTable('valutes', {'code':'text','name':'text'}, mval)
##
##mval = []
##for kval in Fixer.valutes:
##    m = []
##    m.append(kval)
##    m.append(Fixer.valutes[kval])
##    mval.append(m)
##AddTable('valutes2', {'code':'text','name':'text'}, mval)    

 # Загрузка базы городов/станций
i = 0
try:
    f = open('DB/stations.txt', encoding='utf-8')
    db = []
    for line in f:
        m = []
        words = line.strip().split(' : ')
        words.append(words[0])
        words.append(words[1])
        words.append(words[2])
        words.append(words[3])
        words[0] = words[0].upper() + ' '
        words[0] = words[0].replace('Ё','Е')
        words[1] = words[1].upper()
        words[1] = words[1].replace('Ё','Е')
        words[2] = words[2].upper()
        words[2] = words[2].replace('Ё','Е')
        words[3] = words[3].upper()
        words[3] = words[3].replace('Ё','Е')
        m.append(i)
        m.append(words[8])
        m.append(words[9])
        m.append(words[10])
        m.append(words[11])
        m.append(words[4])
        m.append(words[5])
        m.append(words[6])
        m.append(words[7])
        m.append(words[0])
        m.append(words[1])
        m.append(words[2])
        m.append(words[3])
        db.append(m)
        i += 1
    f.close()
    AddTable('stations', {'id':'int','name':'text',
                          'city':'text','region':'text',
                          'country':'text',
                          'type':'text',
                          'y':'real','x':'real','code':'text',
                          'nameU':'text','cityU':'text',
                          'regionU':'text','countryU':'text'}, db)
except:
    print(i)
