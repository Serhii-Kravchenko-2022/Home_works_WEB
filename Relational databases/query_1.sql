-- Знайти 5 студентів із найбільшим середнім балом з усіх предметів.

SELECT s.name as student, round(avg(g.value), 2) AS avg_grade
FROM grade g
LEFT JOIN student s ON s.id = g.student_id
GROUP BY s.id
ORDER BY (round(avg(g.value), 2)) DESC
LIMIT 5;






