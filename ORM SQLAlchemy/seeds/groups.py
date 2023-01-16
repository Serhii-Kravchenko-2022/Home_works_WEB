from random import choice

from database.models import Group
from database.db import session

GROUP_LIST = ['3A', '3B', '3C', '4A', '4B', '4C']


def create_groups():
    """
    Create data for table 'Groups' from list of groups used session

    :return: None
    """
    for _ in range(3):
        group = Group(
            name=choice(GROUP_LIST)
        )
        session.add(group)
    session.commit()


if __name__ == '__main__':
    create_groups()
