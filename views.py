from omake_framework.templator import render
from patterns.creational_patterns import Engine, Logger
from patterns.structural_patterns import AppRoute, Debug

# Скопировал этот момент так как не придумал рациональней
site = Engine()
logger = Logger('main_logger')

# Создаем словарь для обработки адресов
route_list = {}


@AppRoute(route_list, '/')
class Index:
    def __call__(self, request):
        logger.log('Открыт список категорий')
        return '200 OK', render('index.html', objects_list=site.categories)


@AppRoute(route_list, '/about/')
class About:
    @Debug()
    def __call__(self, request):
        return '200 OK', render('about.html')


@AppRoute(route_list, '/courses-list/')
class CourseList:
    def __call__(self, request):
        logger.log('Открыт список курсов')
        category = site.get_category_by_id(int(request['request_params']['id']))
        return '200 OK', render('course_list.html', objects_list=category.courses, name=category.name, id=category.id)


@AppRoute(route_list, '/create-course/')
class CourseCreate:
    category_id = -1

    def __call__(self, request):

        if request['method'] == 'POST':
            data = request['data']
            course_name = site.decode_value(data['name'])
            category = site.get_category_by_id(int(self.category_id))
            new_course = site.create_category(course_name, self.category_id)

            # Добавляем курс в категорию
            category.courses.append(new_course)

            # Добавляем курс в движок
            site.courses.append(new_course)

            return '200 OK', render('course_list.html', objects_list=category.courses,
                                    name=category.name, id=category.id)

        else:
            self.category_id = int(request['request_params']['id'])
            category = site.get_category_by_id(int(self.category_id))

            return '200 OK', render('create_course.html', name=category.name)


@AppRoute(route_list, '/create-category/')
class CategoryCreate:
    def __call__(self, request):
        if request['method'] == 'POST':
            data = request['data']
            category_name = site.decode_value(data['name'])
            category_id = len(site.categories)

            new_category = site.create_category(category_name, category_id)

            site.categories.append(new_category)

            return '200 OK', render('index.html', objects_list=site.categories)

        else:
            categories = site.categories
            return '200 OK', render('create_category.html', categories=categories)


# Оставил на случай если в будущем уберу категории из индекса
# class CategoryList:
#     def __call__(self, request):
#         categories = site.categories
#
#         return '200 OK', render('create_category.html', categories=categories)
