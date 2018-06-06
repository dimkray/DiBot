# -*- coding: utf-8 -*-
# Морфологический анализ
# https://pymorphy2.readthedocs.io/en/0.2/user/index.html
# pip install pymorphy2
import re
import Fixer
import pymorphy2

dic = Fixer.Load('morth')
morph = pymorphy2.MorphAnalyzer()

mph = {} #Словарь
phr = {'NOUN':'СУЩ', 'ADJF':'ПРИЛ', 'ADJS':'ПРИЛ', 'COMP':'КОМП',
       'VERB':'ГЛГ', 'INFN':'ГЛГ', 'PRTF':'ПРИЧ', 'PRTS':'ПРИЧ',
       'GRND':'ДЕЕП', 'NUMR':'ЧИСЛ', 'ADVB':'НАР', 'NPRO':'МЕСТ',
       'PRED':'ПРЕД', 'PREP':'ПРДЛ', 'CONJ':'СОЮЗ', 'PRCL':'ЧАСТ',
       'INTJ':'МЕЖД', 'UNKN':'НЕИЗВ', 'NUMB':'ЦИФР', 'LATN':'ЛАТН'}

test = input('Предложение для анализа: ')
text = ''

# Разбиение на предложения
test = test.replace('	','  ') # учитываем табы
poz = 0; newpoz = 0
mstr = [] # массив предложений
while newpoz <= len(test):
    x1 = 0; x2 = 0; x3 = 0; x4 = 0
    if test.find('. ', poz) > 0: x1 = test.find('. ', poz)
    else: x1 = 1000000
    if test.find('! ', poz) > 0: x2 = test.find('! ', poz)
    else: x2 = 1000000
    if test.find('? ', poz) > 0: x3 = test.find('? ', poz)
    else: x3 = 1000000
    if test.find('\n', poz) > 0: x4 = test.find('\n', poz)
    else: x4 = 1000000    
    newpoz = min(x1, x2, x3, x4) + 1 # Ищем ближайший разделитель предложения
    s = test[poz:newpoz].strip()
    if s != '': mstr.append(s)
    poz = newpoz

print(mstr)
for item in mstr:
    print(item)

# Разбиение на слова
for row in mstr:
    words = re.split('\s|/|\\|\*|"|`|<|>|\]|\[|\}|\{|=|\+|\)|\(|&|\^|#|\~|@|»|«|:|;|,|\.|!|\?|-', row)
    mwords = []
    poz = 0; pozold = 0
    for word in words:
        s = word.strip().lower()
        if s != '' and s != '-' and s != '—':
            poz = row.find(word,poz)
            text += row[pozold:poz] + '[' + s + ']'
            poz += len(word); pozold = poz
            mwords.append(s)
    text += row[poz:] # окончание предложения
    print(mwords)

    for word in mwords:
        p = morph.parse(word)[0]
        print('%s - [%s]' % (word, p.normal_form))
        m = re.split(',| ', str(p.tag))
        #print(m)
        for tag in m:
            s = ''
            if dic[tag][1] != '': s = ' {%s}' % dic[dic[tag][1]][0]
            print(' - ' + dic[tag][0] + s )
            if dic[tag][1] == 'POST':
                if tag in phr:
                    mph[word] = phr[tag]
                else:
                    mph[word] = 'UNCN'
    text += ' '

print(text)
tmorth = text

for word in mph:
    tmorth = tmorth.replace('['+word+']', mph[word])
print(tmorth)


