# -*- coding: utf-8 -*-
# простейший профайлер
# with Profiler() as p:
#    // your code to be profiled here

import time


class Profiler(object):

    def __enter__(self):
        self._startTime = time.time()
         
    def __exit__(self, type, value, traceback):
        self.time = time.time() - self._startTime
        print('Время выполнения: {:.3f} сек.'.format(self.time))

    def getTime(self):
        return time.time() - self._startTime


class decorator:
    def benchmark(func):
        def wrapper(*args, **kwargs):
            t = time.clock()
            res = func(*args, **kwargs)
            print(func.__name__, '- {:.3f} сек.'.format(time.clock() - t))
            return res
        return wrapper