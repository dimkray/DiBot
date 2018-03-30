import Fixer
from Services.New_ import Service

stest = input('Введите тестовую фразу: ')

# здесь тестовая обработка #
stest = Service.Search(stest)

print('Результат тестирования: ' + stest)

import time; time.sleep(5)
