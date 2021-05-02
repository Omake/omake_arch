class PageNotFound404:
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


class Framework:
    def __init__(self, routes, fronts):
        self.routes = routes
        self.fronts = fronts

    def __call__(self, environ, start_response):
        # Запрашиваемый адрес
        requested_url = environ['PATH_INFO'].lower()

        request_method = environ['REQUEST_METHOD']

        if requested_url in self.routes:
            view = self.routes[requested_url]

        else:
            view = PageNotFound404()

        # Создаем реквест
        request = {}

        # Пропускаем реквест через Front Controller
        for f in self.fronts:
            f(request)

        # Передаем запрос контроллеру
        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])

        return [body.encode('utf-8')]
