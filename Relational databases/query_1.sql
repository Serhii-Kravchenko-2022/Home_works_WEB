-- Знайти 5 студентів із найбільшим середнім балом з усіх предметів.

-- select student_id from grade
  --                where (
SELECT student_id, max(AVG(value)) as avg_grade
FROM grade
group by subject_id
--    )







