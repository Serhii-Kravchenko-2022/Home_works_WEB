from faker import Faker

from database.models import Teacher
from database.db import session

fake = Faker('uk_UA')


def create_teachers():
    """
    Create data for table 'Teachers' used session and faker data

    :return: None
    """
    for _ in range(5):
        teacher = Teacher(
            fullname=fake.name()
        )
        session.add(teacher)
    session.commit()


if __name__ == '__main__':
    create_teachers()
