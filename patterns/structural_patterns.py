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
