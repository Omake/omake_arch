from time import time, ctime


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

    def __call__(self, method):
        def wrapper(func):
            def get_time(*args, **kwargs):

                start_time = time()
                result = func(*args, **kwargs)
                end_time = time()

                delta_time = end_time - start_time

                print(f'{ctime()} Метод: {self.name} выполнялся {delta_time} секунд')

                return result

            return get_time

        return wrapper(method)
