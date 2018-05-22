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
