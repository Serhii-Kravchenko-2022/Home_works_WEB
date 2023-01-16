from random import choice, randint

from database.models import Discipline
from database.db import session

DISCIPLINE_LIST = ['math', 'literature', 'chemistry', 'physics', 'Biology', 'music', 'history', 'drawing']


def create_disciplines():
    """
    Create data for table 'Disciplines' from list of disciplines used session

    :return: None
    """
    for _ in range(7):
        discipline = Discipline(
            name=DISCIPLINE_LIST[_],
            teacher_id=randint(1, 5)
        )
        session.add(discipline)
    session.commit()


if __name__== '__main__':
    create_disciplines()
