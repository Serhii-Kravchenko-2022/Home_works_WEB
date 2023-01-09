-- Список курсів, які певному студенту читає певний викладач.

SELECT DISTINCT s.name as student, t.name as teacher, su.title as discipline
FROM grade g
LEFT JOIN student s ON s.id = g.student_id
LEFT JOIN subject su ON su.id = g.subject_id
LEFT JOIN teacher t ON t.id = su.teacher_id
-- where  s.name = 'Wendy Gibson' and t.name = 'Carmen Allen'


