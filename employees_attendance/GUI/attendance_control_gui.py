from datetime import datetime
import csv
import mysql.connector
from mysql.connector import Error
from tkinter import messagebox
from tkinter.filedialog import asksaveasfilename
from employees_attendance.GUI.attendance_view_gui import View


employee_fields = ['employee_id', 'name', 'age', 'phone']
attendance_fields = ['employee_id', 'timestamp']


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


class Control:

    def __init__(self, root, hostname, port, user_name, password, scheme):
        self.db = mysql.connector.connect(host=hostname, port=port, user=user_name, password=password, database=scheme)
        self.root = root
        self.view = View(root, self)

    def get_employee_from_db(self, employee_id):
        cursor = self.db.cursor()
        cursor.execute('SELECT * FROM employees WHERE employee_id = %s;', (employee_id,))
        result = cursor.fetchone()
        if result:
            return result
        else:
            return None

    def get_employees_from_db(self):
        employees = {}
        cursor = self.db.cursor(dictionary=True)
        cursor.execute('SELECT * FROM employees;')
        result = cursor.fetchall()
        for employee in result:
            employees[employee['employee_id']] = employee
        return employees

    def add_employee(self, employee_id, name, age, phone):
        if len(employee_id) != 6:
            messagebox.showerror(message="Please make sure to use only 6 digits id number!")
            return False
        if any(not c.isdigit() for c in employee_id):
            messagebox.showerror(message="Please make sure to enter only digits as id number!")
            return False
        if self.get_employee_from_db(employee_id) is not None:
            messagebox.showerror(message="This employee_id already exists")
            return

        if name == '':
            messagebox.showerror(message="Please make sure to enter employee name!")
            return False
        if any(c.isdigit() for c in name):
            messagebox.showerror(message="Please make sure that the employee name does not contain any digits")
            return False

        if int(age) < 18:
            messagebox.showerror(message="Please make sure to enter employee correct age!")
            return False
        if any(not c.isdigit() for c in age):
            messagebox.showerror(message="Please make sure to enter only digits as employee age!")
            return False

        if len(phone) != 10:
            messagebox.showerror(message="Please make sure to use only 10 digits phone number!")
            return False
        if any(not c.isdigit() for c in phone):
            messagebox.showerror(message="Please make sure to enter only digits as phone number!")
            return False

        cursor = self.db.cursor()
        try:
            cursor.execute("INSERT INTO employees (`employee_id`, `name`, `age`, `phone`) "
                           "VALUES (%s, %s, %s, %s);", (employee_id, name, age, phone))
            self.db.commit()
            return True
        except Error as e:
            self.db.rollback()
            messagebox.showerror(message=e)
            return False

    def add_employees_from_file(self, file_name):
        new_employees = get_employees_from_file(file_name)
        employees_to_add = []
        for employee in new_employees:
            if self.get_employee_from_db(new_employees[employee]['employee_id']) is None:
                employees_to_add.append(new_employees[employee])
            else:
                messagebox.showerror(message="Employee ID {} already exists".format(employee))
        cursor = self.db.cursor()
        try:
            for emp in employees_to_add:
                cursor.execute("INSERT INTO employees (`employee_id`, `name`, `age`, `phone`) VALUES (%s, %s, %s, %s);",
                               (emp['employee_id'], emp['name'], emp['age'], emp['phone']))
            self.db.commit()
            return True
        except Error as e:
            self.db.rollback()
            messagebox.showerror(message=e)
            return False

    def delete_employee(self, employee_id):
        if len(str(employee_id)) != 6:
            messagebox.showerror(message="Please make sure to use only 6 digits id number!")
            return False
        if any(not c.isdigit() for c in employee_id):
            messagebox.showerror(message="Please make sure to enter only digits!")
            return False
        if self.get_employee_from_db(employee_id) is None:
            messagebox.showerror(message="This employee_id does not exist")
            return False
        if not messagebox.askyesno(message="Are you sure that you want to delete employee {}?".format(employee_id)):
            return False
        cursor = self.db.cursor()
        try:
            cursor.execute("DELETE FROM employees WHERE employee_id = %s;", (employee_id,))
            self.db.commit()
            return True
        except Error as e:
            self.db.rollback()
            messagebox.showerror(message=e)
            return False

    def delete_employees_from_file(self,file_name):
        employees = self.get_employees_from_db()
        employees_from_file = get_employees_from_file(file_name)
        employees_to_delete = []
        for employee in employees_from_file:
            if employee in employees:
                employees_to_delete.append(employees[employee])
        cursor = self.db.cursor()
        try:
            for emp in employees_to_delete:
                cursor.execute("DELETE FROM employees WHERE employee_id = %s;", (emp['employee_id'],))
            self.db.commit()
            return True
        except Error as e:
            self.db.rollback()
            messagebox.showerror(message=e)
            return False

    def mark_attendance(self, employee_id):
        if len(str(employee_id)) != 6:
            messagebox.showerror(message="Please make sure to use only 6 digits id number!")
            return False
        if self.get_employee_from_db(employee_id) is None:
            messagebox.showerror(message="This id does not exist! Please enter your employee id!")
            return False
        if any(not c.isdigit() for c in employee_id):
            messagebox.showerror(message="Please make sure to enter only digits!")
            return False

        cursor = self.db.cursor()
        try:
            cursor.execute("INSERT INTO employees_attendance (`employee_id`, `timestamp`) "
                           "VALUES (%s, CURRENT_TIMESTAMP());", (employee_id,))
            self.db.commit()
            return True
        except Error as e:
            self.db.rollback()
            messagebox.showerror(message=e)
            return False

    def employee_report(self,employee_id):
        if len(str(employee_id)) != 6:
            messagebox.showerror(message="Please make sure to use only 6 digits id number!")
            return False
        if self.get_employee_from_db(employee_id) is None:
            messagebox.showerror(message="This id does not exist! Please enter employee id!")
            return False
        if any(not c.isdigit() for c in employee_id):
            messagebox.showerror(message="Please make sure to enter only digits!")
            return False

        cursor = self.db.cursor(dictionary=True)
        try:
            cursor.execute("SELECT employee_id, timestamp FROM employees_attendance WHERE employee_id = %s;", (employee_id,))
            result = cursor.fetchall()
        except Error as e:
            messagebox.showerror(message=e)
            return False
        try:
            with open(asksaveasfilename(defaultextension='.csv'), 'w', newline='') as employees_file:
                writer = csv.DictWriter(employees_file, fieldnames=attendance_fields, dialect='excel')
                writer.writeheader()
                writer.writerows(result)
            return True
        except FileNotFoundError:
            return False

    def monthly_report(self):
        cursor = self.db.cursor(dictionary=True)
        try:
            cursor.execute("SELECT employee_id, timestamp FROM employees_attendance WHERE timestamp BETWEEN "
                           "DATE_FORMAT(NOW() - INTERVAL 1 MONTH, '%Y-%m-01 00:00:00') AND "
                           "DATE_FORMAT(LAST_DAY(NOW() - INTERVAL 1 MONTH), '%Y-%m-%d 23:59:59')")
            result = cursor.fetchall()
        except Error as e:
            messagebox.showerror(message=e)
            return False
        try:
            with open(asksaveasfilename(defaultextension='.csv'), 'w', newline='') as employees_file:
                writer = csv.DictWriter(employees_file, fieldnames=attendance_fields, dialect='excel')
                writer.writeheader()
                writer.writerows(result)
            return True
        except FileNotFoundError:
            return False

    def late_report(self):
        cursor = self.db.cursor(dictionary=True)
        try:
            cursor.execute("SELECT employee_id, timestamp FROM employees_attendance WHERE time(timestamp) > '09:30:00';")
            result = cursor.fetchall()
        except Error as e:
            messagebox.showerror(message=e)
            return False
        try:
            with open(asksaveasfilename(defaultextension='.csv'), 'w', newline='') as employees_file:
                writer = csv.DictWriter(employees_file, fieldnames=attendance_fields, dialect='excel')
                writer.writeheader()
                writer.writerows(result)
            return True
        except FileNotFoundError:
            return False

    def report_at_specific_time(self, start_date, end_date):
        try:
            datetime.strptime(start_date, '%Y-%m-%d')
        except ValueError as e:
            messagebox.showerror(message=e)
            return False
        try:
            datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError as e:
            messagebox.showerror(message=e)
            return False

        cursor = self.db.cursor(dictionary=True)
        try:
            cursor.execute("SELECT employee_id, timestamp FROM employees_attendance WHERE date(timestamp) "
                           "BETWEEN %s and %s;", (start_date, end_date,))
            result = cursor.fetchall()
        except Error as e:
            messagebox.showerror(message=e)
            return False
        try:
            with open(asksaveasfilename(defaultextension='.csv'), 'w', newline='') as employees_file:
                writer = csv.DictWriter(employees_file, fieldnames=attendance_fields, dialect='excel')
                writer.writeheader()
                writer.writerows(result)
            return True
        except FileNotFoundError:
            return False
