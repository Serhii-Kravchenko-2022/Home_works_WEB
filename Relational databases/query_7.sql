-- Знайти оцінки студентів у окремій групі з певного предмета.

select c.title as class_name, s.name as student, su.title as discipline ,g.value
from grade g
LEFT JOIN student s on s.id = g.student_id
LEFT JOIN class c on c.id = s.class_name_id
LEFT JOIN subject su on su.id = g.subject_id
where c.title = '3C' and su.title = 'chemistry'
order by s.name