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

    def __call__(self, method):
        def wrapper(func):
            def get_time(*args, **kwargs):
                result = func(*args, **kwargs)
                print(time())

                return result

            return get_time

        return wrapper(method)
