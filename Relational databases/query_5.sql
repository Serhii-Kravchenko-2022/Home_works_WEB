-- Знайти які курси читає певний викладач.

select t.name, su.title
from subject su
LEFT JOIN teacher t on su.teacher_id = t.id
where t.name = 'Stephanie Murray'
