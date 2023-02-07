from services.Google import Google
from services.Geo import Geo
import fixer

x = float(input('Введите координату X: '))
y = float(input('Введите координату Y: '))

# здесь тестовая обработка #
stest = Geo.GetAddress(x,y)

print('Результат тестирования: ' + stest)

import time; time.sleep(5)
