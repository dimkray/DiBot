# -*- coding: utf-8 -*-
# Сервис работы с координатами земли и приём/возврат адреса
import Fixer
import config
from geopy.distance import great_circle
from geopy.geocoders import GoogleV3
#from geopy.geocoders import GoogleV3

def Geolocator():
    return GoogleV3(api_key=config.GMaps_key, timeout=1)

# Измерение расстояние от одной точки до другой (по глобальным координатам)
class Geo:
    def Distance(x1,y1,x2,y2):
        dist = great_circle((x1, y1),(x2, y2))
        sdist = str(dist)
        return float(sdist[:sdist.find(' ')])
    
    # поиск полного адреса и координат по отношению к локальной позиции пользователя
    def FullAddress(address):
        location = Geolocator().geocode(address, exactly_one=True, timeout=5, region=None,
                components=None, language='ru', sensor=True)
        return location.address

    def Coordinats(address):
        location = Geolocator().reverse(address, exactly_one=True, timeout=5, language='ru_RU', sensor=True)
        return location.longitude + ',' + location.latitude

    def GetAddress(xlat,ylon):
        location = Geolocator().reverse('%' + str(xlat) + 's, %' + str(ylon) + 's', exactly_one=True, timeout=5, language='ru_RU', sensor=True)
        return location.address
