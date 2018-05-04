SELECT employees_attendance.employee_id, sec_to_time(avg(time_to_sec(date_format(timestamp, '%H:%i:%s')))) as avg_arrival_time
FROM employees_attendance
group by employee_id;

SELECT employees_attendance.employee_id, date_format(timestamp, '%H:%i:%s')
FROM employees_attendance;

SELECT employees_attendance.employee_id, COUNT(*) as num_of_working_days
FROM employees_attendance
GROUP BY employees_attendance.employee_id; 

SELECT employees_attendance.employee_id, COUNT(*) as num_of_working_days
FROM employees_attendance
GROUP BY employees_attendance.employee_id
ORDER BY num_of_working_days DESC
LIMIT 1; 