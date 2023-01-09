from datetime import datetime
import faker
from random import randint, choice
import sqlite3

NUMBER_STUDENTS = 40
CLASS_LIST = ['3A', '3B', '3C', '4A', '4B', '4C']
NUMBER_CLASS = 3
SUBJECT_LIST = ['math', 'literature', 'chemistry', 'physics', 'Biology', 'music', 'history', 'drawing']
NUMBER_SUBJECT = 7
NUMBER_TEACHER = 5
NUMBER_GRADE = 15


def generate_fake_data(number_students, number_class, number_subject, number_teachers, number_grade) -> tuple:
    """
    generate fake data for quantity from parameters
    :param number_students: int
    :param number_class: int
    :param number_subject: int
    :param number_teachers: int
    :param number_grade: int
    :return: tuple of lists tuple
    """

    fake_students = []  # students name
    fake_class_names = []  # class name
    fake_subjects = []  # subject name
    fake_teachers = []  # teachers name
    fake_grades = []  # grade number

    fake_data = faker.Faker()

    # make students name in quantity number_students
    for _ in range(number_students):
        fake_students.append(fake_data.name())

    # make teachers name in quantity number_teachers
    for _ in range(number_teachers):
        fake_teachers.append(fake_data.name())

    # make class name from CLASS_LIST in quantity number_class
    while len(fake_class_names) < number_class:
        name = choice(CLASS_LIST)
        if name not in fake_class_names:
            fake_class_names.append(name)

    # make subject name from SUBJECT_LIST in quantity number_class
    while len(fake_subjects) < number_subject:
        name = choice(SUBJECT_LIST)
        if name not in fake_subjects:
            fake_subjects.append(name)

    # make grade from 1 to 10 in quantity number_grade
    for _ in range(number_grade):
        fake_grades.append(fake_data.random_int(min=1, max=10))

    return fake_students, fake_class_names, fake_subjects, fake_teachers, fake_grades


def prepare_data(students, class_names, subjects, teachers, grades) -> tuple:
    """
    prepare data for fill db tables

    :param students: list
    :param class_names: list
    :param subjects: list
    :param teachers: list
    :param grades: list
    :return: tuple of lists tuple
    """

    for_students = []
    # prepare list of tuple for students table
    for stud in students:
        for_students.append((stud, randint(1, NUMBER_CLASS)))

    for_class_names = []
    # prepare list of tuple for class_name table
    for name in class_names:
        for_class_names.append((name,))

    for_subject = []
    # prepare list of tuple for subjects table
    for subj in subjects:
        for_subject.append((subj, randint(1, NUMBER_TEACHER)))

    for_teachers = []
    # prepare list of tuple for teachers table
    for teach in teachers:
        for_teachers.append((teach,))

    for_grades = []
    # prepare list of tuple for grades table
    for stud in range(1, NUMBER_STUDENTS + 1):
        for grad in range(1, len(grades) + 1):
            grade_date = datetime(2022, randint(1, 5), randint(10, 20)).date()
            for_grades.append((stud, randint(1, len(subjects)), choice(grades), grade_date))

    return for_students, for_class_names, for_subject, for_teachers, for_grades


def insert_data_to_db(students, class_names, subjects, teachers, grades) -> None:
    """
    insert data to db
    :param students: tuple
    :param class_names: tuple
    :param subjects: tuple
    :param teachers: tuple
    :param grades: tuple
    :return: None
    """
    with sqlite3.connect('education.db') as connect:
        cursor = connect.cursor()

        sql_to_students = """INSERT INTO student(name, class_name_id)
                                 VALUES (?, ?)"""
        cursor.executemany(sql_to_students, students)

        sql_to_class_names = """INSERT INTO class(title)
                                    VALUES (?)"""
        cursor.executemany(sql_to_class_names, class_names)

        sql_to_subject = """INSERT INTO subject(title, teacher_id)
                                    VALUES (?, ?)"""
        cursor.executemany(sql_to_subject, subjects)

        sql_to_teachers = """INSERT INTO teacher(name)
                                    VALUES (?)"""
        cursor.executemany(sql_to_teachers, teachers)

        sql_to_grades = """INSERT INTO grade(student_id, subject_id, value, data)
                                    VALUES (?, ?, ?, ?)"""
        cursor.executemany(sql_to_grades, grades)

        connect.commit()


if __name__ == "__main__":
    student, class_name, subject, teacher, grade = prepare_data(*generate_fake_data(NUMBER_STUDENTS,
                                                                                    NUMBER_CLASS,
                                                                                    NUMBER_SUBJECT,
                                                                                    NUMBER_TEACHER,
                                                                                    NUMBER_GRADE))
    insert_data_to_db(student, class_name, subject, teacher, grade)
