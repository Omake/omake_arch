from omake_framework.templator import render


class TemplateView:
    template_name = 'template.html'

    def get_template(self):
        return self.template_name

    def get_context(self):
        return {}

    def render_template(self):
        template = self.get_template()
        context = self.get_context()

        return '200 OK', render(template, **context)

    def __call__(self, request):
        return self.render_template()


class ListView(TemplateView):
    queryset = []
    template_name = 'list.html'
    context_object_name = 'objects_list'

    def get_queryset(self):
        return self.queryset

    def get_object_name(self):
        return self.context_object_name

    def get_context(self):
        queryset = self.get_queryset()
        context_object_name = self.get_object_name()
        context = {context_object_name: queryset}

        return context


class CreateView(TemplateView):
    pass
