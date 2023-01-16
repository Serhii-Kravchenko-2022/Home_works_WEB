# from sqlalchemy.orm import joinedload
from sqlalchemy import func, desc, and_

from database.db import session
from database.models import Group, Discipline, Student, Teacher, Grade

query1 = session.query(Student.fullname, func.round(func.avg(Grade.grade), 2).label('avg_grade'))\
        .select_from(Grade).join(Student).group_by(Student.id).order_by(desc('avg_grade')).limit(5).all()


# SELECT s.name as student, round(avg(g.value), 2) AS avg_grade
# FROM grade g
# LEFT JOIN student s ON s.id = g.student_id
# GROUP BY s.id
# ORDER BY (round(avg(g.value), 2)) DESC
# LIMIT 5;

query2 = session.query(Student.fullname, Discipline.name, func.round(func.avg(Grade.grade), 2).label('avg_grade'))\
            .select_from(Grade).join(Discipline).join(Student).filter(Discipline.name == 'math').\
            group_by(Student.id).order_by(desc('avg_grade')).limit(5).all()

# SELECT s.name, su.title as discipline, round(avg(g.value), 2) AS avg_grade
# FROM grade g
# LEFT JOIN student s ON s.id = g.student_id
# LEFT JOIN subject su ON su.id = g.subject_id
# where su.title = 'drawing'
# GROUP BY s.name
# ORDER BY (round(avg(g.value), 2)) DESC
# LIMIT 1

query3 = session.query(Group.name, Discipline.name, func.round(func.avg(Grade.grade), 2).label('avg_grade')).\
    select_from(Grade).join(Group).join(Discipline).group_by(Discipline.id)

# SELECT c.title, su.title as discipline, round(avg(g.value), 2) AS avg_grade
# FROM grade g
# LEFT JOIN student s on s.id = g.student_id
# LEFT JOIN class c ON c.id = s.class_name_id
# LEFT JOIN subject su ON su.id = g.subject_id
# GROUP BY su.title

query4 = session.query(func.round(func.avg(Grade.grade), 2).label('avg_grade')).select_from(Grade)
# SELECT AVG(value) as avg_grade FROM grade

query5 = session.query(Teacher.fullname, Discipline.name).select_from(Discipline).join(Teacher). \
    filter(Teacher.fullname == 'Алла Шовкопляс').all()
# select t.name, su.title
# from subject su
# LEFT JOIN teacher t on su.teacher_id = t.id
# where t.name = 'Stephanie Murray'

query6 = session.query(Group.name, Student.fullname).select_from(Student).join(Group).filter(Group.name == '4C'). \
    order_by(Student.name).all()
# select c.title as class_name, s.name as student
# from student s
# LEFT JOIN class c ON c.id = s.class_name_id
# where class_name = '3C'
# order by s.name

query7 = session.query(Group.name, Student.fullname, Discipline.name, Grade.grade).select_from(Grade).join(Student). \
    join(Group).join(Discipline).filter(and_(Group.name == '4C', Discipline.name == 'chemistry')).order_by(Student.name).\
    all()

# select c.title as class_name, s.name as student, su.title as discipline ,g.value
# from grade g
# LEFT JOIN student s on s.id = g.student_id
# LEFT JOIN class c on c.id = s.class_name_id
# LEFT JOIN subject su on su.id = g.subject_id
# where c.title = '3C' and su.title = 'chemistry'
# order by s.name

query8 = session.query(Teacher.fullname, Discipline.name, func.round(func.avg(Grade.grade), 2).label('avg_grade')).\
    select_from(Grade).join(Discipline).join(Teacher).group_by(Teacher.fullname).order_by(desc('avg_grade')).all()
# select t.name, su.title, (round(avg(g.value), 2)) as avg_grade
# from grade g
# left join subject su on su.id = g.subject_id
# left join teacher t on t.id = su.teacher_id
# -- where t.name = 'Michelle Moore'
# GROUP BY t.name
# ORDER BY (round(avg(g.value), 2)) DESC

query9 = session.query(Student.fullname, Discipline.name).distinct().select_from(Grade).join(Student).join(Discipline).\
    filter(Student.fullname == 'Симон Дашкевич').all()
# select DISTINCT s.name as student, su.title as discipline
# from grade g
# LEFT JOIN student s ON s.id = g.student_id
# LEFT JOIN subject su ON su.id = g.subject_id
# -- order by su.title desc
# where s.name = 'Randy Dillon'

query10 = session.query(Student.fullname, Teacher.fullname, Discipline.name).distinct().select_from(Grade).\
    join(Student).join(Discipline).join(Teacher).filter(and_(Student.fullname == 'Симон Дашкевич',
                                                             Teacher.fullname == 'Едита Онищенко')).all()
# SELECT DISTINCT s.name as student, t.name as teacher, su.title as discipline
# FROM grade g
# LEFT JOIN student s ON s.id = g.student_id
# LEFT JOIN subject su ON su.id = g.subject_id
# LEFT JOIN teacher t ON t.id = su.teacher_id
# -- where  s.name = 'Wendy Gibson' and t.name = 'Carmen Allen'


def select(query):
    """
    Execute query from database

    :param query: session.query object
    :return: list of tuple
    """
    result_list = []
    for d in query:
        result_list.append(d)
    return result_list


if __name__ == '__main__':
    select_1 = select(query1)
    select_2 = select(query2)
    select_3 = select(query3)
    select_4 = select(query4)
    select_5 = select(query5)
    select_6 = select(query6)
    select_7 = select(query7)
    select_8 = select(query8)
    select_9 = select(query9)
    select_10 = select(query10)
