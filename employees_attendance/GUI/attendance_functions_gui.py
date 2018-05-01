from datetime import datetime
import csv
import MySQLdb
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

db = None
employee_fields = ['employee_id', 'name', 'age', 'phone']


def init(hostname, port, user_name, password, scheme):
    global db
    db = MySQLdb.connect(host=hostname, port=port, user=user_name, passwd=password, db=scheme)


def get_employee_from_db(employee_id):
    cursor = db.cursor(MySQLdb.cursors.DictCursor)
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
    cursor = db.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM employees;')
    result = cursor.fetchall()
    for employee in result:
        employees[employee['employee_id']] = employee
    return employees


def add_employee(employee_id, name, age, phone):
    # employee_id = ''
    # while len(employee_id) != 6 or (any(not c.isdigit() for c in employee_id)):
    #     employee_id = input("Please enter employee id, employee id should contain 6 digits:")
    if len(employee_id) != 6:
        messagebox.showerror(message="Please make sure to use only 6 digits id number!")
        return False
    if any(not c.isdigit() for c in employee_id):
        messagebox.showerror(message="Please make sure to enter only digits as id number!")
        return False
    if get_employee_from_db(employee_id) is not None:
        messagebox.showerror(message="This employee_id already exists")
        return

    # name = ''
    # while name == '' or any(c.isdigit() for c in name):
    #     name = input("Please enter employee name:")
    if name == '':
        messagebox.showerror(message="Please make sure to enter employee name!")
        return False
    if any(c.isdigit() for c in name):
        messagebox.showerror(message="Please make sure that the employee name does not contain any digits")
        return False

    # age = 0
    # while age < 18:
    #     try:
    #         age = int(input("Please enter employee age, employee age should contain only digits:"))
    if int(age) < 18:
        messagebox.showerror(message="Please make sure to enter employee correct age!")
        return False
    if any(not c.isdigit() for c in age):
        messagebox.showerror(message="Please make sure to enter only digits as employee age!")
        return False
        # except ValueError:
        #     print("Please make sure to enter only digits!")
        #     age = 0

    # phone = ''
    # while len(phone) != 10 or any(not c.isdigit() for c in phone):
    #     phone = input("Please enter employee phone, employee phone should contain 10 digits:")
    if len(phone) != 10:
        messagebox.showerror(message="Please make sure to use only 10 digits phone number!")
        return False
    if any(not c.isdigit() for c in phone):
        messagebox.showerror(message="Please make sure to enter only digits as phone number!")
        return False

    cursor = db.cursor()
    try:
        cursor.execute("INSERT INTO employees (`employee_id`, `name`, `age`, `phone`) "
                       "VALUES (%s, %s, %s, %s);", (employee_id, name, age, phone))
        db.commit()
        return True
    except MySQLdb.Error as e:
        db.rollback()
        messagebox.showerror(message=e)
        return False


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
    except MySQLdb.Error as e:
        db.rollback()
        print(e)


def delete_employee(employee_id):
    # employee_id = 0
    # while len(str(employee_id)) != 6 or (any(not c.isdigit() for c in employee_id)):
    #     employee_id = input("Please enter the employee id you would like to delete:")
    if len(str(employee_id)) != 6:
        messagebox.showerror(message="Please make sure to use only 6 digits id number!")
        return False
    if any(not c.isdigit() for c in employee_id):
        messagebox.showerror(message="Please make sure to enter only digits!")
        return False
    if get_employee_from_db(employee_id) is None:
        messagebox.showerror(message="This employee_id does not exist")
        return False
    if not messagebox.askyesno(message="Are you sure that you want to delete employee {}?".format(employee_id)):
        return False
    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM employees WHERE employee_id = %s;", (employee_id,))
        db.commit()
        return True
    except MySQLdb.Error as e:
        db.rollback()
        messagebox.showerror(message=e)
        return False


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
    except MySQLdb.Error as e:
        db.rollback()
        print(e)


def mark_attendance(employee_id):
    if len(str(employee_id)) != 6:
        messagebox.showerror(message="Please make sure to use only 6 digits id number!")
        return False
    if get_employee_from_db(employee_id) is None:
        messagebox.showerror(message="This id does not exist! Please enter your employee id!")
        return False
    if any(not c.isdigit() for c in employee_id):
        messagebox.showerror(message="Please make sure to enter only digits!")
        return False

    cursor = db.cursor()
    try:
        cursor.execute("INSERT INTO employees_attendance (`employee_id`, `timestamp`) "
                       "VALUES (%s, CURRENT_TIMESTAMP());", (employee_id,))
        db.commit()
        return True
    except MySQLdb.Error as e:
        db.rollback()
        messagebox.showerror(message=e)
        return False


def employee_report():
    employee_id = ''
    while len(employee_id) != 6 or get_employee_from_db(employee_id) is None or (any(not c.isdigit() for c in employee_id)):
        employee_id = input("Please enter employee id:")
        if len(str(employee_id)) != 6:
            print("Please make sure to use only 6 digits id number!")
            return
        if get_employee_from_db(employee_id) is None:
            print("This id does not exist! Please enter employee id!")
            return
        if any(not c.isdigit() for c in employee_id):
            print("Please make sure to enter only digits!")
            return

    cursor = db.cursor(MySQLdb.cursors.DictCursor)
    try:
        cursor.execute("SELECT * FROM employees_attendance WHERE employee_id = %s;", (employee_id,))
        result = cursor.fetchall()
        for line in result:
            print(line['timestamp'])
    except MySQLdb.Error as e:
        print(e)


def monthly_report():
    cursor = db.cursor(MySQLdb.cursors.DictCursor)
    try:
        cursor.execute("SELECT * FROM employees_attendance WHERE timestamp BETWEEN DATE_FORMAT(NOW() - INTERVAL 1 "
                       "MONTH, '%Y-%m-01 00:00:00') AND DATE_FORMAT(LAST_DAY(NOW() - INTERVAL 1 MONTH), "
                       "'%Y-%m-%d 23:59:59')")
        result = cursor.fetchall()
        for line in result:
            print(line['employee_id'], line['timestamp'])
    except MySQLdb.Error as e:
        print(e)


def late_report():
    cursor = db.cursor(MySQLdb.cursors.DictCursor)
    try:
        cursor.execute("SELECT * FROM employees_attendance WHERE time(timestamp) > '09:30:00';")
        result = cursor.fetchall()
        for line in result:
            print(line['employee_id'], line['timestamp'])
    except MySQLdb.Error as e:
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

    cursor = db.cursor(MySQLdb.cursors.DictCursor)
    try:
        cursor.execute("SELECT * FROM employees_attendance WHERE date(timestamp) BETWEEN %s and %s;",
                       (start_date, end_date,))
        result = cursor.fetchall()
        for line in result:
            print(line['employee_id'], line['timestamp'])
    except MySQLdb.Error as e:
        print(e)


class GUI:
    def __init__(self, master):
        master.title('Employees Attendance')
        master.resizable(False, False)
        master.configure(background='#e1d8b9')

        self.style = ttk.Style()
        self.style.configure('TFrame', background='#e1d8b9')
        self.style.configure('TButton', background='#e1d8b9', font=('Arial', 10))
        self.style.configure('TLabel', background='#e1d8b9', font=('Arial', 10))

        self.employee_id = StringVar()
        panedwindow = ttk.Panedwindow(master, orient=VERTICAL)
        panedwindow.pack(fill=BOTH, expand=True)

        self.top_frame = ttk.Frame(panedwindow, width=500, height=200, relief=SUNKEN)
        ttk.Label(self.top_frame, text="Insert employee id:").grid(row=0, column=0, padx=10, pady=30)
        emp_id_entry = ttk.Entry(self.top_frame, textvariable=self.employee_id)
        emp_id_entry.grid(row=0, column=1, padx=10, pady=30)
        ttk.Button(self.top_frame, text="Mark attendance", command=self.__mark_attendance).grid(row=0, column=2, padx=10, pady=30)

        self.bottom_frame = ttk.Frame(panedwindow, width=400, height=50, relief=SUNKEN)
        ttk.Button(self.bottom_frame, text='Add Employee', command=self.__add_employee_top_level).grid(row=0, column=0, padx=5, pady=15, sticky='e')
        ttk.Button(self.bottom_frame, text='Delete Employee', command=self.__delete_employee_top_level).grid(row=0, column=1, pady=15, sticky='w')

        panedwindow.add(self.top_frame)
        panedwindow.add(self.bottom_frame)

        self.status_text = StringVar('')
        status = Label(master, textvariable=self.status_text, bd=1, relief=SUNKEN, anchor=W)
        status.pack(side=BOTTOM, fill=X)

    def __mark_attendance(self):
        value = self.employee_id.get()
        if mark_attendance(value):
            self.status_text.set("Attendance was recorded for employee {}".format(value))
        self.employee_id.set("")

    def __add_employee_top_level(self):
        self.top_level = Toplevel()
        self.top_level.title('Add new employee')
        self.top_level.geometry('210x210')
        self.top_level.resizable(False, False)
        self.top_level.configure(background='#e1d8b9')
        self.new_employee_id = StringVar()
        self.new_employee_name = StringVar()
        self.new_employee_age = StringVar()
        self.new_employee_phone = StringVar()
        ttk.Label(self.top_level, text="ID:").grid(row=0, column=0, padx=10, pady=10, sticky='sw')
        ttk.Entry(self.top_level, textvariable=self.new_employee_id).grid(row=0, column=1)
        ttk.Label(self.top_level, text="Name:").grid(row=1, column=0, padx=10, pady=10, sticky='sw')
        ttk.Entry(self.top_level, textvariable=self.new_employee_name).grid(row=1, column=1)
        ttk.Label(self.top_level, text="Age:").grid(row=2, column=0, padx=10, pady=10, sticky='sw')
        ttk.Entry(self.top_level, textvariable=self.new_employee_age).grid(row=2, column=1)
        ttk.Label(self.top_level, text="Phone:").grid(row=3, column=0, padx=10, pady=10, sticky='sw')
        ttk.Entry(self.top_level, textvariable=self.new_employee_phone).grid(row=3, column=1)
        ttk.Button(self.top_level, text="Add", command=self.__add_employee).grid(row=4, pady=10, column=0, columnspan=2)

    def __add_employee(self):
        if add_employee(self.new_employee_id.get(), self.new_employee_name.get(), self.new_employee_age.get(),
                        self.new_employee_phone.get()):
            self.status_text.set("Employee {} was created".format(self.new_employee_id.get()))
            self.top_level.destroy()
        else:
            self.top_level.focus_set()
            self.new_employee_id.set('')
            self.new_employee_name.set('')
            self.new_employee_age.set('')
            self.new_employee_phone.set('')

    def __delete_employee_top_level(self):
        self.top_level = Toplevel()
        self.top_level.title('Delete employee')
        self.top_level.geometry('400x100')
        self.top_level.resizable(False, False)
        self.top_level.configure(background='#e1d8b9')
        ttk.Label(self.top_level, text="Insert employee id:").grid(row=0, column=0, padx=10, pady=25)
        self.employee_to_delete = StringVar()
        ttk.Entry(self.top_level, textvariable=self.employee_to_delete).grid(row=0, column=1, padx=10, pady=25)
        ttk.Button(self.top_level, text="Delete", command=self.__delete_employee).grid(row=0, column=2, padx=10, pady=25)

    def __delete_employee(self):
        if delete_employee(self.employee_to_delete.get()):
            self.status_text.set("Employee {} was deleted".format(self.employee_to_delete.get()))
            self.top_level.destroy()
        else:
            self.top_level.focus_set()
        self.employee_to_delete.set('')


