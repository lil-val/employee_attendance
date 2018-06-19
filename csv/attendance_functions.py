from datetime import datetime, date, timedelta
import csv

employee_fields = ['employee_id', 'name', 'age', 'phone']
attendance_fields = ['employee_id', 'attendance_clock']


def create_files():
    try:
        with open('employees.csv', 'r', newline=''):
            pass
    except IOError:
        with open('employees.csv', 'w', newline='') as employees_file:
            writer = csv.DictWriter(employees_file, fieldnames=employee_fields, dialect='excel')
            writer.writeheader()

    try:
        with open('employees_attendance.csv', 'r', newline=''):
            pass
    except IOError:
        with open('employees_attendance.csv', 'w', newline='') as employees_file:
            writer = csv.DictWriter(employees_file, fieldnames=attendance_fields, dialect='excel')
            writer.writeheader()


def get_employee(employee_id, file_name='employees.csv'):
    try:
        with open(file_name, 'r', newline='') as employees_file:
            reader = csv.DictReader(employees_file, fieldnames=employee_fields, dialect='excel')
            for employee in reader:
                if employee['employee_id'] == employee_id:
                    return employee
    except IOError:
        print("file is not available")
    return None


def get_employees(file_name='employees.csv'):
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


def add_employee():
    employee_id = ''
    while len(employee_id) != 6 or (any(not c.isdigit() for c in employee_id)):
        employee_id = input("Please enter employee id, employee id should contain 6 digits:")
        if len(employee_id) != 6:
            print("Please make sure to use only 6 digits id number!")
        if any(not c.isdigit() for c in employee_id):
            print("Please make sure to enter only digits!")
    if get_employee(employee_id) is not None:
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

    with open('employees.csv', 'a', newline='') as employees_file:
        writer = csv.DictWriter(employees_file, fieldnames=employee_fields, dialect='excel')
        writer.writerow({'employee_id': employee_id, 'name': name, 'age': age, 'phone': phone})


def add_employees_from_file():
    file_name = input("Please enter the file name you would like to load:")
    new_employees = get_employees(file_name)
    employees_to_add = []
    for employee in new_employees:
        if get_employee(new_employees[employee]['employee_id']) is None:
            employees_to_add.append(new_employees[employee])
    with open('employees.csv', 'a', newline='') as employees_file:
        writer = csv.DictWriter(employees_file, fieldnames=employee_fields, dialect='excel')
        writer.writerows(employees_to_add)


def delete_employee():
    employee_id = 0
    while len(str(employee_id)) != 6 or (any(not c.isdigit() for c in employee_id)):
        employee_id = input("Please enter the employee id you would like to delete:")
        if len(str(employee_id)) != 6:
            print("Please make sure to use only 6 digits id number!")
        if any(not c.isdigit() for c in employee_id):
            print("Please make sure to enter only digits!")
    if get_employee(employee_id) is None:
        print("This employee_id does not exist")
        return

    employees = get_employees()
    del employees[employee_id]
    with open('employees.csv', 'w', newline='') as employees_file:
        writer = csv.DictWriter(employees_file, fieldnames=employee_fields, dialect='excel')
        writer.writeheader()
        writer.writerows(list(employees.values()))


def delete_employees_from_file():
    file_name = input("Please enter the file name you would like to load:")
    employees = get_employees()
    employees_to_delete = get_employees(file_name)
    for employee in employees_to_delete:
        if employee in employees:
            del employees[employee]
    with open('employees.csv', 'w', newline='') as employees_file:
        writer = csv.DictWriter(employees_file, fieldnames=employee_fields, dialect='excel')
        writer.writeheader()
        writer.writerows(list(employees.values()))


def mark_attendance():
    employee_id = ''
    while len(employee_id) != 6 or get_employee(employee_id) is None or (any(not c.isdigit() for c in employee_id)):
        employee_id = input("Please enter your employee id:")
        if len(str(employee_id)) != 6:
            print("Please make sure to use only 6 digits id number!")
        if get_employee(employee_id) is None:
            print("This id does not exist! Please enter your employee id!")
        if any(not c.isdigit() for c in employee_id):
            print("Please make sure to enter only digits!")

    with open('employees_attendance.csv', 'a', newline='') as employees_attendance_file:
        writer = csv.DictWriter(employees_attendance_file, fieldnames=attendance_fields, dialect='excel')
        writer.writerow({'employee_id': employee_id, 'attendance_clock': datetime.now().strftime('%Y-%m-%d %H:%M:%S')})


def employee_report():
    employee_id = ''
    while len(employee_id) != 6 or get_employee(employee_id) is None or (any(not c.isdigit() for c in employee_id)):
        employee_id = input("Please enter employee id:")
        if len(str(employee_id)) != 6:
            print("Please make sure to use only 6 digits id number!")
        if get_employee(employee_id) is None:
            print("This id does not exist! Please enter employee id!")
        if any(not c.isdigit() for c in employee_id):
            print("Please make sure to enter only digits!")
    try:
        with open('employees_attendance.csv', 'r', newline='') as employees_attendance_file:
            reader = csv.DictReader(employees_attendance_file, fieldnames=attendance_fields, dialect='excel')
            for line in reader:
                if line['employee_id'] == employee_id:
                    print(line['attendance_clock'])
    except IOError:
        print("file is not available")


def monthly_report():
    try:
        with open('employees_attendance.csv', 'r', newline='') as employees_attendance_file:
            reader = csv.DictReader(employees_attendance_file, fieldnames=attendance_fields, dialect='excel')
            today = date.today()
            first = today.replace(day=1)
            last_month = (first - timedelta(days=1)).strftime('%Y-%m')
            for line in reader:
                if last_month in line['attendance_clock']:
                    print(line['employee_id'], line['attendance_clock'])
    except IOError:
        print("file is not available")


def late_report():
    try:
        with open('employees_attendance.csv', 'r', newline='') as employees_attendance_file:
            reader = csv.DictReader(employees_attendance_file, fieldnames=attendance_fields, dialect='excel')
            at_time = '09:30'
            for line in reader:
                if line['attendance_clock'][11:] > at_time:
                    print(line['employee_id'], line['attendance_clock'])
    except IOError:
        print("file is not available")


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
    try:
        with open('employees_attendance.csv', 'r', newline='') as employees_attendance_file:
            reader = csv.DictReader(employees_attendance_file, fieldnames=attendance_fields, dialect='excel')
            for line in reader:
                if start_date <= line['attendance_clock'][:10] <= end_date:
                    print(line['employee_id'], line['attendance_clock'])
    except IOError:
        print("file is not available")
