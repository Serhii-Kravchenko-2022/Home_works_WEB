-- Знайти середній бал, який ставить певний викладач зі своїх предметів.

select t.name, su.title, (round(avg(g.value), 2)) as avg_grade
from grade g
left join subject su on su.id = g.subject_id
left join teacher t on t.id = su.teacher_id
-- where t.name = 'Michelle Moore'
GROUP BY t.name
ORDER BY (round(avg(g.value), 2)) DESC