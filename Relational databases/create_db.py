import sqlite3


def create_db():
    # read file with script for DB creating
    with open('education_data.sql', 'r') as file:
        sql = file.read()

    # make connection to db (if db not exist, create them)
    with sqlite3.connect('education.db') as connect:
        cursor = connect.cursor()
        # execute script from file, that creating db
        cursor.executescript(sql)


if __name__ == "__main__":
    create_db()
