import abc


class Course:
    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.append(self)


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
        self.categories =[]
        self.courses = []

    @staticmethod
    def create_category(name, category_id):
        return Category(name, category_id)

    @staticmethod
    def create_course(course_type, name, category):
        return CourseFactory.create(course_type, name, category)
