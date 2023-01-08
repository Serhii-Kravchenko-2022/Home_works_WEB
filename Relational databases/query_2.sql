-- Знайти студента із найвищим середнім балом з певного предмета.

SELECT student_id, AVG(value)
FROM grade
GROUP BY subject_id