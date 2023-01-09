-- Знайти список курсів, які відвідує студент.

select DISTINCT s.name as student, su.title as discipline
from grade g
LEFT JOIN student s ON s.id = g.student_id
LEFT JOIN subject su ON su.id = g.subject_id
-- order by su.title desc
where s.name = 'Randy Dillon'
