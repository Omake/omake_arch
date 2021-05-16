from time import time

# структурный паттерн - Декоратор
class AppRoute:
    def __init__(self, route_list, url):
        '''
        Сохраняем значение переданного параметра
        '''
        self.route_list = route_list
        self.url = url

    def __call__(self, cls):
        '''
        Сам декоратор
        '''
        self.route_list[self.url] = cls()


# структурный паттерн - Декоратор
class Debug:

    def __init__(self, name):

        self.name = name

    def __call__(self, cls):
        '''
        сам декоратор
        '''

        # это вспомогательная функция будет декорировать каждый отдельный метод класса, см. ниже
        def timeit(method):
            '''
            нужен для того, чтобы декоратор класса wrapper обернул в timeit
            каждый метод декорируемого класса
            '''
            def timed(*args, **kw):
                ts = time()
                result = method(*args, **kw)
                te = time()
                delta = te - ts

                print(f'debug --> {self.name} выполнялся {delta:2.2f} ms')
                return result

            return timed

        return timeit(cls)
