from datetime import datetime
import csv
import mysql.connector
from mysql.connector import Error

db = None
employee_fields = ['employee_id', 'name', 'age', 'phone']


def init(hostname, port, user_name, password, scheme):
    global db
    db = mysql.connector.connect(host=hostname, port=port, user=user_name, passwd=password, db=scheme)


def get_employee_from_db(employee_id):
    cursor = db.cursor()
    cursor.execute('SELECT * FROM employees WHERE employee_id = %s;', (employee_id,))
    result = cursor.fetchone()
    if result:
        return result
    else:
        return None


def get_employees_from_file(file_name='employees.csv'):
    employees = {}
    try:
        with open(file_name, 'r', newline='') as employees_file:
            next(employees_file)
            reader = csv.DictReader(employees_file, fieldnames=employee_fields, dialect='excel')
            for employee in reader:
                employees[employee['employee_id']] = employee
    except IOError:
        print("file is not available")
    return employees


def get_employees_from_db():
    employees = {}
    cursor = db.cursor(dictionary=True)
    cursor.execute('SELECT * FROM employees;')
    result = cursor.fetchall()
    for employee in result:
        employees[employee['employee_id']] = employee
    return employees


def add_employee():
    employee_id = ''
    while len(employee_id) != 6 or (any(not c.isdigit() for c in employee_id)):
        employee_id = input("Please enter employee id, employee id should contain 6 digits:")
        if len(employee_id) != 6:
            print("Please make sure to use only 6 digits id number!")
        if any(not c.isdigit() for c in employee_id):
            print("Please make sure to enter only digits!")
    if get_employee_from_db(employee_id) is not None:
        print("This employee_id already exists")
        return

    name = ''
    while name == '' or any(c.isdigit() for c in name):
        name = input("Please enter employee name:")
        if name == '':
            print("Please make sure to enter employee name!")
        if any(c.isdigit() for c in name):
            print("Please make sure that the employee name does not contain any digits")

    age = 0
    while age < 18:
        try:
            age = int(input("Please enter employee age, employee age should contain only digits:"))
            if age < 18:
                print("Please make sure to enter employee correct age!")
        except ValueError:
            print("Please make sure to enter only digits!")
            age = 0

    phone = ''
    while len(phone) != 10 or any(not c.isdigit() for c in phone):
        phone = input("Please enter employee phone, employee phone should contain 10 digits:")
        if len(phone) != 10:
            print("Please make sure to use only 10 digits phone number!")
        if any(not c.isdigit() for c in phone):
            print("Please make sure to enter only digits!")

    cursor = db.cursor()
    try:
        cursor.execute("INSERT INTO employees (`employee_id`, `name`, `age`, `phone`) "
                       "VALUES (%s, %s, %s, %s);", (employee_id, name, age, phone))
        db.commit()
    except Error as e:
        db.rollback()
        print(e)


def add_employees_from_file():
    file_name = input("Please enter the file name you would like to load:")
    new_employees = get_employees_from_file(file_name)
    employees_to_add = []
    for employee in new_employees:
        if get_employee_from_db(new_employees[employee]['employee_id']) is None:
            employees_to_add.append(new_employees[employee])
        else:
            print("Employee ID {} already exists".format(employee))
    cursor = db.cursor()
    try:
        for emp in employees_to_add:
            cursor.execute("INSERT INTO employees (`employee_id`, `name`, `age`, `phone`) VALUES (%s, %s, %s, %s);",
                           (emp['employee_id'], emp['name'], emp['age'], emp['phone']))
        db.commit()
    except Error as e:
        db.rollback()
        print(e)


def delete_employee():
    employee_id = 0
    while len(str(employee_id)) != 6 or (any(not c.isdigit() for c in employee_id)):
        employee_id = input("Please enter the employee id you would like to delete:")
        if len(str(employee_id)) != 6:
            print("Please make sure to use only 6 digits id number!")
        if any(not c.isdigit() for c in employee_id):
            print("Please make sure to enter only digits!")
    if get_employee_from_db(employee_id) is None:
        print("This employee_id does not exist")
        return

    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM employees WHERE employee_id = %s;", (employee_id,))
        db.commit()
    except Error as e:
        db.rollback()
        print(e)


def delete_employees_from_file():
    file_name = input("Please enter the file name you would like to load:")
    employees = get_employees_from_db()
    employees_from_file = get_employees_from_file(file_name)
    employees_to_delete = []
    for employee in employees_from_file:
        if employee in employees:
            employees_to_delete.append(employees[employee])
    cursor = db.cursor()
    try:
        for emp in employees_to_delete:
            cursor.execute("DELETE FROM employees WHERE employee_id = %s;", (emp['employee_id'],))
        db.commit()
    except Error as e:
        db.rollback()
        print(e)


def mark_attendance():
    employee_id = ''
    while len(employee_id) != 6 or get_employee_from_db(employee_id) is None or (any(not c.isdigit() for c in employee_id)):
        employee_id = input("Please enter your employee id:")
        if len(str(employee_id)) != 6:
            print("Please make sure to use only 6 digits id number!")
        if get_employee_from_db(employee_id) is None:
            print("This id does not exist! Please enter your employee id!")
        if any(not c.isdigit() for c in employee_id):
            print("Please make sure to enter only digits!")

    cursor = db.cursor()
    try:
        cursor.execute("INSERT INTO employees_attendance (`employee_id`, `timestamp`) "
                       "VALUES (%s, CURRENT_TIMESTAMP());", (employee_id,))
        db.commit()
    except Error as e:
        db.rollback()
        print(e)


def employee_report():
    employee_id = ''
    while len(employee_id) != 6 or get_employee_from_db(employee_id) is None or (any(not c.isdigit() for c in employee_id)):
        employee_id = input("Please enter employee id:")
        if len(str(employee_id)) != 6:
            print("Please make sure to use only 6 digits id number!")
        if get_employee_from_db(employee_id) is None:
            print("This id does not exist! Please enter employee id!")
        if any(not c.isdigit() for c in employee_id):
            print("Please make sure to enter only digits!")

    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM employees_attendance WHERE employee_id = %s;", (employee_id,))
        result = cursor.fetchall()
        for line in result:
            print(line['timestamp'])
    except Error as e:
        print(e)


def monthly_report():
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM employees_attendance WHERE timestamp BETWEEN DATE_FORMAT(NOW() - INTERVAL 1 "
                       "MONTH, '%Y-%m-01 00:00:00') AND DATE_FORMAT(LAST_DAY(NOW() - INTERVAL 1 MONTH), "
                       "'%Y-%m-%d 23:59:59')")
        result = cursor.fetchall()
        for line in result:
            print(line['employee_id'], line['timestamp'])
    except Error as e:
        print(e)


def late_report():
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM employees_attendance WHERE time(timestamp) > '09:30:00';")
        result = cursor.fetchall()
        for line in result:
            print(line['employee_id'], line['timestamp'])
    except Error as e:
        print(e)


def report_at_specific_time():
    start_date = ''
    end_date = ''
    while start_date == '':
        start_date = input("Please enter start date in the following format YYYY-MM-DD:")
        try:
            datetime.strptime(start_date, '%Y-%m-%d')
        except ValueError:
            print('invalid date')
            start_date = ''
    while end_date == '':
        end_date = input("Please enter end date in the following format YYYY-MM-DD:")
        try:
            datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError:
            print('invalid date')
            end_date = ''

    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM employees_attendance WHERE date(timestamp) BETWEEN %s and %s;",
                       (start_date, end_date,))
        result = cursor.fetchall()
        for line in result:
            print(line['employee_id'], line['timestamp'])
    except Error as e:
        print(e)
