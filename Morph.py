# -*- coding: utf-8 -*-
# Морфологический анализ
# https://pymorphy2.readthedocs.io/en/0.2/user/index.html
# pip install pymorphy2
import re
import Fixer
import pymorphy2

dic = Fixer.Load('morth')
morph = pymorphy2.MorphAnalyzer()

test = input('Предложение для анализа: ')

# Разбиение на предложения
test = test.replace('\n','. ') # учитываем перенос строк
test = test.replace('	',' ')
poz = 0; newpoz = 0
mstr = [] # массив предложений
while newpoz <= len(test):
    x1 = 0; x2 = 0; x3 = 0 
    if test.find('. ', poz) > 0: x1 = test.find('. ', poz)
    else: x1 = 1000000
    if test.find('! ', poz) > 0: x2 = test.find('! ', poz)
    else: x2 = 1000000
    if test.find('? ', poz) > 0: x3 = test.find('? ', poz)
    else: x3 = 1000000
    newpoz = min(x1, x2, x3) + 1 # Ищем ближайший разделитель предложения
    s = test[poz:newpoz].strip()
    if s != '': mstr.append(s)
    poz = newpoz

print(mstr)
for item in mstr:
    print(item)

# Разбиение на слова
for item in mstr:
    words = re.split(':|;|,| ', item)
    mwords = []
    for word in words:
        s = Fixer.strcleaner(word).strip().lower()
        if s != '': mwords.append(s)
    print(mwords)

    for word in mwords:
        p = morph.parse(word)[0]
        print('%s - [%s]' % (word, p.normal_form))
        m = re.split(',| ', str(p.tag))
        #print(m)
        for tag in m:
            s = ''
            if dic[tag][1] != '': s = ' (%s)' % dic[dic[tag][1]][0]
            print(' - ' + dic[tag][0] + s )


