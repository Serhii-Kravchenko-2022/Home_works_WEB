from random import randint

from faker import Faker

from database.models import Grade
from database.db import session

fake = Faker('uk_UA')


def create_grades():
    """
    Create data for table 'Grades' used session and faker data

    :return: None
    """
    for _ in range(280):
        grade = Grade(
            student_id=randint(1, 40),
            discipline_id=randint(1, 7),
            grade=randint(1, 10),
            date_of=fake.date_between('-3y')
        )
        session.add(grade)
    session.commit()


if __name__ == '__main__':
    create_grades()
