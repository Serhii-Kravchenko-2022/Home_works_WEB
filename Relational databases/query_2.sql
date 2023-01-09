-- Знайти студента із найвищим середнім балом з певного предмета.

SELECT s.name, su.title as discipline, round(avg(g.value), 2) AS avg_grade
FROM grade g
LEFT JOIN student s ON s.id = g.student_id
LEFT JOIN subject su ON su.id = g.subject_id
where su.title = 'drawing'
GROUP BY s.name
ORDER BY (round(avg(g.value), 2)) DESC
LIMIT 1