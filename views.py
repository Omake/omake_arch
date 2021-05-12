from omake_framework.templator import render
from patterns.creational_patterns import Engine

# Скопировал этот момент так как не придумал рациональней
site = Engine()


class Index:
    def __call__(self, request):
        return '200 OK', render('index.html')


class About:
    def __call__(self, request):
        return '200 OK', render('about.html')


class CourseList:
    def __call__(self, request):
        pass


class CourseCreate:
    def __call__(self, request):
        pass


class CategoryList:
    def __call__(self, request):
        pass


class CategoryCreate:
    def __call__(self, request):
        if request['method'] == 'POST':
            data = request['data']
            category_name = data['name']
            category_id = len(site.categories)

            new_category = site.create_category(category_name, category_id)

            site.categories.append(new_category)

            return '200 OK', render('index.html', objects_list=site.categories)

        else:
            categories = site.categories
            return '200 OK', render('create_category.html', categories=categories)
