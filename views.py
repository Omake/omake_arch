from omake_framework.template_controller import render


class Index:
    def __call__(self, request):
        return '200 OK', render('templates/index.html')


class About:
    def __call__(self, request):
        return '200 OK', render('templates/about.html')
