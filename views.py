import sqlite3
from datetime import date
from omake_framework.templator import render
from patterns.creational_patterns import Engine, Logger
from patterns.structural_patterns import AppRoute, Debug
from patterns.behavioral_patterns import ListView
from patterns.mapper import StudentMapper


# Скопировал этот момент так как не придумал рациональней
site = Engine()

connection = sqlite3.connect('patterns_database.sqlite')

logger = Logger('main_logger')

# Создаем словарь для обработки адресов
route_list = {}


# class Index:
#     def __call__(self, request):
#         logger.log('Открыт список категорий')
#         return '200 OK', render('index.html', objects_list=site.categories)


@AppRoute(route_list, '/about/')
class About:
    @Debug('About')
    def __call__(self, request):
        return '200 OK', render('about.html')


@AppRoute(route_list, '/courses-list/')
class CourseList:
    @Debug('CourseList')
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
            new_course = site.create_course('course_a', course_name, category)

            # Добавляем курс в движок
            site.courses.append(new_course)

            return '200 OK', render('course_list.html', objects_list=category.courses,
                                    name=category.name, id=category.id)

        else:
            self.category_id = int(request['request_params']['id'])
            category = site.get_category_by_id(int(self.category_id))

            return '200 OK', render('create_course.html', name=category.name)


@AppRoute(route_list, '/')
class CategoryList(ListView):
    template_name = 'index.html'
    queryset = site.categories


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


@AppRoute(route_list, url='/student-list/')
class StudentList(ListView):
    template_name = 'student_list.html'

    def get_queryset(self):
        mapper = StudentMapper(connection)

        return mapper.get_all_students()


@AppRoute(route_list, url='/study_programs/')
class StudyPrograms:
    @Debug(name='StudyPrograms')
    def __call__(self, request):
        if request['method'] == 'POST':
            user_info = request['data']

            # Декодим данные
            user_info['name'] = site.decode_value(user_info['name'])
            user_info['email'] = site.decode_value(user_info['email'])

            # Создаем студента
            student = site.create_student(name=user_info['name'], email=user_info['email'],
                                          location=user_info['location'])
            # Добавляем студента в базу
            mapper = StudentMapper(connection)
            mapper.insert_student(student)

            # Добавляем студента в движок
            site.students.append(student)

        return '200 OK', render('study-programs.html', data=date.today())


@AppRoute(route_list, url='/add-student/')
class AddStudent:
    @Debug(name='AddStudent')
    def __call__(self, request):
        if request['method'] == 'POST':
            data = request['data']
            course_name = site.decode_value(data['course_name'])
            student_name = site.decode_value(data['student_name'])

            course = site.get_course_by_name(course_name)
            student = site.get_student_by_name(student_name)

            course.students.append(student)

            print(f'Студент {student_name} успешно записался на курс {course_name}\n'
                  f'Список студентов курса: {course.students}')

            return '200 OK', render('add_student.html', courses=site.courses, students=site.students)
        else:
            return '200 OK', render('add_student.html', courses=site.courses, students=site.students)
