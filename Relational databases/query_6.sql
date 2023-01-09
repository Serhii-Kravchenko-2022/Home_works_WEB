-- Знайти список студентів у певній групі.

select c.title as class_name, s.name as student
from student s
LEFT JOIN class c ON c.id = s.class_name_id
where class_name = '3C'
order by s.name