from random import randint

from faker import Faker

from database.models import Student
from database.db import session

fake = Faker('uk_UA')


def create_students():
    """
    Create data for table 'Students' used session and faker data

    :return: None
    """
    for _ in range(40):
        student = Student(
            fullname=fake.name(),
            group_id=randint(1, 3)
        )
        session.add(student)
    session.commit()


if __name__ == '__main__':
    create_students()
