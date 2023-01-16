from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

Base = declarative_base()


# Create tables used class Base

class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True)
    name = Column(String(5), nullable=False)
    student = relationship("Student", back_populates='group', cascade="all, delete")


class Teacher(Base):
    __tablename__ = "teachers"
    id = Column(Integer, primary_key=True)
    fullname = Column(String(150), nullable=False)
    discipline = relationship("Discipline", back_populates='teacher', cascade="all, delete")


class Discipline(Base):
    __tablename__ = "disciplines"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    teacher_id = Column(Integer, ForeignKey(Teacher.id, ondelete="CASCADE"))
    teacher = relationship(Teacher, back_populates='discipline', cascade="all, delete")
    grade = relationship("Grade", back_populates='discipline', cascade="all, delete")


class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    fullname = Column(String(150), nullable=False)
    group_id = Column(Integer, ForeignKey(Group.id, ondelete="CASCADE"))
    group = relationship(Group, back_populates='student', cascade="all, delete")
    grade = relationship("Grade", back_populates='student', cascade="all, delete")


class Grade(Base):
    __tablename__ = "grades"
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey(Student.id, ondelete="CASCADE"))
    discipline_id = Column(Integer, ForeignKey(Discipline.id, ondelete="CASCADE"))
    grade = Column(Integer, nullable=True)
    date_of = Column(Date, nullable=True)
    student = relationship(Student, back_populates='grade', cascade="all, delete")
    discipline = relationship(Discipline, back_populates='grade', cascade="all, delete")
