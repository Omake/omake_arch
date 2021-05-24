import quopri


class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email


class Student(User):
    def __init__(self, name, email, location, membership):
        super().__init__(name, email)
        self.location = location
        self.membership = membership


class Teacher(User):
    pass


class Course:
    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.courses.append(self)
        self.students = []


class Category:
    def __init__(self, name, category_id):
        self.name = name
        self.courses = []
        self.id = category_id

    def get_courses_count(self):
        return len(self.courses)


class CourseA(Course):
    pass


class CourseB(Course):
    pass


# По условиям текущей задачи нет смысла в реальном использовании фабрики
# По этому написал логику под "заглушки" чтобы в будущем заменить на боевые примеры
class CourseFactory:
    course_types = {
        'course_a': CourseA,
        'course_b': CourseB,
    }

    @classmethod
    def create(cls, course_type, name, category):
        return cls.course_types[course_type](name, category)


class Engine:
    def __init__(self):
        self.categories = []
        self.courses = []
        self.students = []

    @staticmethod
    def create_student(name, email, location, membership='no'):
        return Student(name, email, location, membership)

    @staticmethod
    def create_category(name, category_id):
        return Category(name, category_id)

    @staticmethod
    def create_course(course_type, name, category):
        return CourseFactory.create(course_type, name, category)

    @staticmethod
    def decode_value(val):
        val_b = bytes(val.replace('%', '=').replace("+", " "), 'UTF-8')
        val_decode_str = quopri.decodestring(val_b)
        return val_decode_str.decode('UTF-8')

    def get_category_by_id(self, category_id):
        for item in self.categories:
            if item.id == category_id:
                return item

    def get_course_by_name(self, course_name):
        for item in self.courses:
            if item.name == course_name:
                return item

    def get_student_by_name(self, student_name):
        for item in self.students:
            if item.name == student_name:
                return item


# порождающий паттерн Синглтон
class SingletonByName(type):

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        if kwargs:
            name = kwargs['name']

        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]


class Logger(metaclass=SingletonByName):

    def __init__(self, name):
        self.name = name

    def log(self, text):
        with open(f'{self.name}_log.txt', 'a', encoding='utf-8') as logfile:
            logfile.write(f'Запись в логе {self.name}: {text}\n')
