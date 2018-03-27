# -*- coding: utf-8 -*-
# Простой сервис универсальных развлечений
import Fixer
import random

db = []

try:
    print('Загрузка базы anecdotes.txt...')
    f = open('DB\\anecdotes.txt')
    for line in f:
        db.append(line.replace('\\','\n'))
    f.close()
    print('База успешно загружена!')
except Exception as e:
    Fixer.errlog('Ошибка при загрузке базы anecdotes!: ' + str(e))

class Fun:
    def Anecdote():
        try:
            random.seed()
            return db[random.randint(0, len(db)-1)]
        except Exception as e:
            Fixer.errlog('Ошибка в сервисе Fun.Anecdote!: ' + str(e))
            return '#bug: ' + str(e) 