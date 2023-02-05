# -*- coding: utf-8 -*-
# Сервис Wikipedia - доступ к статьям интернет-ресурса wikipedia.org
# https://wikipedia.readthedocs.io/en/latest/code.html
import fixer
import wikipedia
from Services.Geo import Geo
from Profiler import decorator

wikipedia.set_lang('ru')

Fixer.add_fun('Wiki', 'Сервис Wikipedia - доступ к статьям интернет-ресурса wikipedia.org', sclass='Wiki')


class Wiki:

    # Поиск страниц по заданному названию
    Fixer.add_fun('SearchPage', 'Поиск страниц по заданному названию',
                  {'sname': 'свободный текст для поиска',
                  'resnum=10': 'максимальное число отображаемых страниц'},
                 'список найденных статей Wikipedia [list<string>/string]')

    @decorator.benchmark
    def SearchPage(sname, resnum=10):
        try:
            rez = []
            if sname == '':
                return rez
            rez = wikipedia.search(sname, results=resnum)
            return rez
        except Exception as e:
            Fixer.errlog('Wikipedia.SearchPage', str(e))
            return '#bug: ' + str(e)        


    # Вся информация о статье по типу: content, categories, coordinates, html, images, links
    Fixer.add_fun('Page', 'Вся информация о статье по типу',
                  {'spage': 'страница статьи wiki - залоговок статьи [string]',
                  'stype="summary"': 'информация по типу: content, categories, coordinates, html, images, links [string]'},
                 'информация из статьи по типу [string]')

    @decorator.benchmark
    def Page(spage, stype='summary'):
        try:
            rez = wikipedia.page(spage)
            if stype == 'content':
                return rez.content
            elif stype == 'categories':
                return rez.categories
            elif stype == 'coordinates':
                return rez.coordinates
            elif stype == 'html':
                return rez.html
            elif stype == 'images':
                return rez.images
            elif stype == 'links':
                return rez.links
            elif stype == 'references':
                return rez.references
            elif stype == 'sections':
                return rez.sections
            return rez.summary
        except Exception as e:
            Fixer.errlog('Wikipedia.Page', str(e))
            return '#bug: ' + str(e)         


    # Весь текстовый контент статьи
    Fixer.add_fun('FullContent', 'Весь текстовый контент статьи',
                  {'spage': 'страница статьи wiki - залоговок статьи [string]'},
                 'текстовый контент статьи [string]')

    @decorator.benchmark
    def FullContent(spage):
        try:
            rez = wikipedia.page(spage)
            if rez.content == '': return '#problem: 404'
            text = rez.content #.encode('utf8')
            return text
        except Exception as e:
            Fixer.errlog('Wikipedia.FullContent', str(e))
            return '#bug: ' + str(e)


    # Минимальный контент статьи - первый абзац
    Fixer.add_fun('MiniContent', 'Минимальный контент статьи - первый абзац',
                  {'spage': 'страница статьи wiki - залоговок статьи [string]'},
                 'первый абзац статьи [string]')

    @decorator.benchmark
    def MiniContent(spage):
        try:
            rez = wikipedia.page(spage)
            if rez.content == '':
                return '#problem: 404'
            Fixer.LastPage.append(Fixer.Page)
            Fixer.Page = spage
            num = rez.content.find('\n==')
            text = rez.content[0:num] #.encode('utf8')
            Fixer.WikiStart = num
            return text
        except Exception as e:
            Fixer.errlog('Wikipedia.MiniContent', str(e))
            return '#bug: ' + str(e)             


    # Минимальный контент статьи - следующий абзац (за предыдущим)
    Fixer.add_fun('More', 'Следующий абзац статьи (за предыдущим)',
                  {'spage': 'страница статьи wiki - залоговок статьи [string]'},
                 'первый абзац статьи [string]')

    @decorator.benchmark
    def More(spage):
        try:
            rez = wikipedia.page(spage)
            if rez.content == '':
                return '#problem: 404'
            num = rez.content.find('\n==', Fixer.WikiStart+1)
            text = rez.content[Fixer.WikiStart:num] #.encode('utf8')
            Fixer.WikiStart = num
            return text
        except Exception as e:
            Fixer.errlog('Wikipedia.More', str(e))
            return '#bug: ' + str(e)  

    # Произвольная статья в Wikipedia
    Fixer.add_fun('PageRandom', 'Произвольная статья в Wikipedia', {},
                 'первый абзац статьи [string]')
    @decorator.benchmark
    def PageRandom():
        try:
            rez = wikipedia.random()
            return Wiki.MiniContent(rez[0])
        except Exception as e:
            Fixer.errlog('Wikipedia.PageRandom', str(e))
            return '#bug: ' + str(e)                

    # Найти объекты wiki поблизости от location (x, y)
    Fixer.add_fun('GeoSearch', 'Найти объекты wiki поблизости от location (x, y)',
                  {'x': 'глобальная координата X (долгота) [float]',
                  'y': 'глобальная координата Y (широта) [float]',
                  'resnom=10': 'макисмальное количество найденных объектов [integer]',
                  'rad=1000': 'радиус поиска от указанных координат в метрах [float]'},
                 'список найденных статей Wikipedia [list<string>/string]')

    @decorator.benchmark
    def GeoSearch(x, y, resnom=10, rad=1000):
        try:
            rez = wikipedia.geosearch(y, x, title=None, results=resnom, radius=rad)
            if len(rez) == 0:
                return '#problem: no objects'
            return rez
        except Exception as e:
            Fixer.errlog('Wikipedia.GeoSearch', str(e))
            return '#bug: ' + str(e)

    # Найти ближайший объект wiki поблизости от location (x, y) - возвращает MiniContent
    Fixer.add_fun('GeoFirst', 'Найти ближайший объект wiki поблизости от location (x, y)',
                  {'x': 'глобальная координата X (долгота) [float]',
                  'y': 'глобальная координата Y (широта) [float]',
                  'rad=1000': 'радиус поиска от указанных координат в метрах [float]'},
                 'первый абзац статьи [string]')

    @decorator.benchmark
    def GeoFirst(x, y, rad=1000):
        try:
            rez = wikipedia.geosearch(y, x, title=None, results=10, radius=rad)
            if len(rez) == 0:
                return 'В радиусе '+str(rad)+' метров не найдено ни одного интересного объекта!'
            for ip in rez:
                try:
                    irez = wikipedia.page(ip)
                    dist = int(1000 * Geo.Distance(irez.coordinates[1], irez.coordinates[0], x, y))
                    return 'Найден ближайший объект в '+str(dist)+' метрах:\n' + Wiki.MiniContent(rez[1])
                except: # не удалось загрузить страницу
                    continue
            return 'Не удалось загрузить информацию :('
        except Exception as e:
            Fixer.errlog('Wikipedia.GeoFirst', str(e))
            return '#bug: ' + str(e)

    # Найти ближайший объект wiki поблизости от меня - возвращает MiniContent
    Fixer.add_fun('GeoFirstMe', 'Найти ближайший объект wiki поблизости от меня (Fixer.X/Y)',
                  {'rad=1000': 'радиус поиска от текущей позиции в метрах [float]'},
                 'первый абзац статьи [string]')

    def GeoFirstMe(rad=1000):
        try:
            return Wiki.GeoFirst(Fixer.X, Fixer.Y, rad=rad)
        except Exception as e:
            Fixer.errlog('Wikipedia.GeoFirstMe', str(e))
            return '#bug: ' + str(e)
