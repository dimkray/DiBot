# -*- coding: utf-8 -*-
import feedparser

# обработка абзацев
def formatting(text):
    text = text.replace('<br>','\n')
    return text

# Класс для парсинга RSS-лент
class RSS:
    # Получить весь RSS
    def GetRSS(urlRSS):
        return feedparser.parse(urlRSS)

    # Получить заголовки RSS
    def GetHeaders(urlRSS):
        d = feedparser.parse(urlRSS)
        return d.headers

    # Получить дату последней публикации
    def GetDate(urlRSS):
        d = feedparser.parse(urlRSS)
        return d['feed']['updated']

    # Получить оглавление и часть постов (0 - все посты)
    def GetFeed(urlRSS, items=0):
        stext = ''
        d = feedparser.parse(urlRSS)
        stext = '%s\n%s\n' % (d.feed.title, d.feed.subtitle)
        #Fixer.htext = d['feed']['link']
        i = len(d['entries'])
        if i < items: items = i
        if items == 0: items = i
        for item in range(0, items-1):
            post = d.entries[item]
            stext += '\n%s\n%s\n' % (post.title, formatting(post.description))
        return stext

    # Получить отдельный пост (с заголовком или нет)
    def GetPost(urlRSS, item=0, btitle=True, bdate=False):
        d = feedparser.parse(urlRSS)
        i = len(d['entries'])-1
        if i < item: item = i
        post = d.entries[item]
        #Fixer.htext = post.link
        sdate = ''
        if bdate: sdate = '\n' + post.published
        if btitle:
            return '%s : %s\n%s' % (d.feed.title, post.title, formatting(post.description))+sdate
        else: return formatting(post.description)+sdate


# тестирование
print(RSS.GetPost('https://rss.newsru.com/all_news/'))
#print(RSS.GetPost('https://www.anekdot.ru/rss/export_j.xml',1,False))
#print(RSS.GetDate('https://www.anekdot.ru/rss/export_j.xml'))
