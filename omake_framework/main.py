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

        # Проверяем слэш в конце адреса
        if not requested_url.endswith('/'):
            requested_url = f"{requested_url}/"

        request_method = environ['REQUEST_METHOD']
        query_str = environ['QUERY_STRING']

        # Создаем реквест
        request = {
            'method': request_method
        }

        # Выполняем действия в зависимости от типа запроса и заполняем request
        if request_method == 'GET':
            params = self.parse_input(query_str)

            request['request_params'] = params

        elif request_method == 'POST':
            data = Framework.get_data(environ)
            data = Framework.parse_wsgi_input_data(data)

            request['data'] = data

        # Пропускаем запрос через Page Controller
        if requested_url in self.routes:
            view = self.routes[requested_url]
        else:
            view = PageNotFound404()

        # Пропускаем реквест через Front Controller
        for f in self.fronts:
            f(request)

        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])

        return [body.encode('utf-8')]

    @staticmethod
    def parse_input(data):
        """
        Получаем словарь из строки с параметрами
        """
        result = {}

        if data:
            params = data.split('&')

            for item in params:
                key, value = item.split('=')
                result[key] = value

        return result

    @staticmethod
    def get_data(environ) -> bytes:
        """
        Получаем тело запроса из environ в байтах
        """
        content_length_data = environ.get('CONTENT_LENGTH')
        content_length = int(content_length_data) if content_length_data else 0
        data = environ['wsgi.input'].read(content_length) if content_length > 0 else b''

        return data

    @staticmethod
    def parse_wsgi_input_data(data: bytes) -> dict:
        """
        Получаем словарь из тела запроса
        """
        result = {}
        if data:
            # Декодируем данные
            data_str = data.decode(encoding='utf-8')
            # Собираем их в словарь
            result = Framework.parse_input(data_str)
        return result
