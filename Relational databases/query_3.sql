-- Знайти середній бал у групах з певного предмета.

SELECT c.title, su.title as discipline, round(avg(g.value), 2) AS avg_grade
FROM grade g
LEFT JOIN student s on s.id = g.student_id
LEFT JOIN class c ON c.id = s.class_name_id
LEFT JOIN subject su ON su.id = g.subject_id
GROUP BY su.title
-- ORDER BY (round(avg(g.value), 2)) DESC
-- LIMIT 5