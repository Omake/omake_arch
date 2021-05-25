from creational_patterns import Student


class StudentMapper:
    def __init__(self, connection):
        self.con = connection
        self.cursor = connection.cursor()

    def get_all_students(self):
        statement = 'SELECT * FROM students'
        self.cursor.execute(statement)
        student_list = []

        for item in self.cursor.fetchall():
            student_id, name, email, location, membership = item
            student = Student(name, email, location, membership)

            student_list.append(student)

        return student_list

    def insert_student(self, student):
        statement = 'INSERT INTO students (name, email, location, membership) VALUES (?,?,?,?)'
        self.cursor.execute(statement, (student.name, student.email, student.location, student.membership))
        self.con.commit()
