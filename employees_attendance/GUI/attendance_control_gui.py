from datetime import datetime
import csv
import mysql.connector
from mysql.connector import Error
from tkinter import *
from tkinter import ttk, messagebox, colorchooser
from tkinter.filedialog import askopenfilename, asksaveasfilename

db = None
employee_fields = ['employee_id', 'name', 'age', 'phone']
attendance_fields = ['employee_id', 'timestamp']


def init(hostname, port, user_name, password, scheme):
    global db
    db = mysql.connector.connect(host=hostname, port=port, user=user_name, password=password, database=scheme)


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


def add_employee(employee_id, name, age, phone):
    if len(employee_id) != 6:
        messagebox.showerror(message="Please make sure to use only 6 digits id number!")
        return False
    if any(not c.isdigit() for c in employee_id):
        messagebox.showerror(message="Please make sure to enter only digits as id number!")
        return False
    if get_employee_from_db(employee_id) is not None:
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

    cursor = db.cursor()
    try:
        cursor.execute("INSERT INTO employees (`employee_id`, `name`, `age`, `phone`) "
                       "VALUES (%s, %s, %s, %s);", (employee_id, name, age, phone))
        db.commit()
        return True
    except Error as e:
        db.rollback()
        messagebox.showerror(message=e)
        return False


def add_employees_from_file(file_name):
    new_employees = get_employees_from_file(file_name)
    employees_to_add = []
    for employee in new_employees:
        if get_employee_from_db(new_employees[employee]['employee_id']) is None:
            employees_to_add.append(new_employees[employee])
        else:
            messagebox.showerror(message="Employee ID {} already exists".format(employee))
    cursor = db.cursor()
    try:
        for emp in employees_to_add:
            cursor.execute("INSERT INTO employees (`employee_id`, `name`, `age`, `phone`) VALUES (%s, %s, %s, %s);",
                           (emp['employee_id'], emp['name'], emp['age'], emp['phone']))
        db.commit()
        return True
    except Error as e:
        db.rollback()
        messagebox.showerror(message=e)
        return False


def delete_employee(employee_id):
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
    except Error as e:
        db.rollback()
        messagebox.showerror(message=e)
        return False


def delete_employees_from_file(file_name):
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
        return True
    except Error as e:
        db.rollback()
        messagebox.showerror(message=e)
        return False


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
    except Error as e:
        db.rollback()
        messagebox.showerror(message=e)
        return False


def employee_report(employee_id):
    if len(str(employee_id)) != 6:
        messagebox.showerror(message="Please make sure to use only 6 digits id number!")
        return False
    if get_employee_from_db(employee_id) is None:
        messagebox.showerror(message="This id does not exist! Please enter employee id!")
        return False
    if any(not c.isdigit() for c in employee_id):
        messagebox.showerror(message="Please make sure to enter only digits!")
        return False

    cursor = db.cursor(dictionary=True)
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


def monthly_report():
    cursor = db.cursor(dictionary=True)
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


def late_report():
    cursor = db.cursor(dictionary=True)
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


def report_at_specific_time(start_date, end_date):
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

    cursor = db.cursor(dictionary=True)
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


class GUI:
    def __init__(self, master):
        master.title('Employees Attendance')
        master.resizable(False, False)
        master.configure(background='#e1d8b9')

        self.style = ttk.Style()
        self.style.configure('TFrame', background='#e1d8b9')
        self.style.configure('TButton', background='#e1d8b9', font=('Arial', 12))
        self.style.configure('TLabel', background='#e1d8b9', font=('Arial', 12))

        self.employee_id = StringVar()
        panedwindow = ttk.Panedwindow(master, orient=VERTICAL)
        panedwindow.pack(fill=BOTH, expand=True)

        self.top_frame = ttk.Frame(panedwindow, width=500, height=200, relief=SUNKEN)
        ttk.Label(self.top_frame, text="Insert employee id:").grid(row=0, column=0, padx=10, pady=30)
        emp_id_entry = ttk.Entry(self.top_frame, textvariable=self.employee_id)
        emp_id_entry.grid(row=0, column=1, padx=10, pady=30)
        ttk.Button(self.top_frame, text="Mark attendance", command=self.__mark_attendance).grid(row=0, column=2, padx=10, pady=30)

        self.bottom_frame = ttk.Frame(panedwindow, width=400, height=50, relief=SUNKEN)
        ttk.Button(self.bottom_frame, text='Add employee', command=self.__add_employee_top_level).grid(row=0, column=0, padx=25, pady=15)
        ttk.Button(self.bottom_frame, text='Delete employee', command=self.__delete_employee_top_level).grid(row=0, column=1, pady=15)
        ttk.Button(self.bottom_frame, text='Employees list', command=self.__employees_list).grid(row=0, column=2, padx=25, pady=15)

        panedwindow.add(self.top_frame)
        panedwindow.add(self.bottom_frame)

        self.status_text = StringVar('')
        status = Label(master, textvariable=self.status_text, bd=1, relief=SUNKEN, anchor=W)
        status.pack(side=BOTTOM, fill=X)

        master.option_add('*tearOff', False)
        menu = Menu(master)
        master.config(menu=menu)
        file = Menu(menu)
        view = Menu(menu)
        help_ = Menu(menu)
        reports = Menu(file)
        font_size = Menu(view)

        menu.add_cascade(menu=file, label='File')
        menu.add_cascade(menu=view, label='View')
        menu.add_cascade(menu=help_, label='Help')

        file.add_command(label='Add employees from file', command=self.__add_employees_from_file)
        file.add_command(label='Delete employees from file', command=self.__delete_employees_from_file)
        file.add_separator()
        file.add_cascade(menu=reports, label='Generate reports')
        reports.add_command(label='Employee report', command=self.__employee_report_top_level)
        reports.add_command(label='Monthly report', command=self.__monthly_report)
        reports.add_command(label='Late employees report', command=self.__late_report)
        reports.add_command(label='Employees report at selected time', command=self.__report_at_specific_time_top_level)
        file.add_separator()
        file.add_command(label='Exit', command=master.destroy)
        view.add_command(label='Change color', command=self.__change_color)
        view.add_cascade(menu=font_size, label='Font size')
        help_.add_command(label='About', command=self.__about)

        self.choice = IntVar()
        font_size.add_radiobutton(label='Small', variable=self.choice, value=10, command=self.__change_font_size)
        font_size.add_radiobutton(label='Normal', variable=self.choice, value=12, command=self.__change_font_size)
        font_size.add_radiobutton(label='Large', variable=self.choice, value=14, command=self.__change_font_size)

    def __mark_attendance(self):
        value = self.employee_id.get()
        if mark_attendance(value):
            self.status_text.set("Attendance was recorded for employee {}".format(value))
        self.employee_id.set("")

    def __add_employee_top_level(self):
        self.top_level = Toplevel()
        self.top_level_frame = ttk.Frame(self.top_level)
        self.top_level_frame.pack()
        self.top_level.title('Add new employee')
        self.top_level.resizable(False, False)
        self.new_employee_id = StringVar()
        self.new_employee_name = StringVar()
        self.new_employee_age = StringVar()
        self.new_employee_phone = StringVar()
        ttk.Label(self.top_level_frame, text="ID:").grid(row=0, column=0, padx=10, pady=10, sticky='sw')
        ttk.Entry(self.top_level_frame, textvariable=self.new_employee_id).grid(row=0, column=1, padx=10)
        ttk.Label(self.top_level_frame, text="Name:").grid(row=1, column=0, padx=10, pady=10, sticky='sw')
        ttk.Entry(self.top_level_frame, textvariable=self.new_employee_name).grid(row=1, column=1, padx=10)
        ttk.Label(self.top_level_frame, text="Age:").grid(row=2, column=0, padx=10, pady=10, sticky='sw')
        ttk.Entry(self.top_level_frame, textvariable=self.new_employee_age).grid(row=2, column=1, padx=10)
        ttk.Label(self.top_level_frame, text="Phone:").grid(row=3, column=0, padx=10, pady=10, sticky='sw')
        ttk.Entry(self.top_level_frame, textvariable=self.new_employee_phone).grid(row=3, column=1, padx=10)
        ttk.Button(self.top_level_frame, text="Add", command=self.__add_employee).grid(row=4, pady=10, column=0, columnspan=2)

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

    def __add_employees_from_file(self):
        filename = askopenfilename()
        if add_employees_from_file(filename):
            self.status_text.set("Employees were added")

    def __delete_employee_top_level(self):
        self.top_level = Toplevel()
        self.top_level_frame = ttk.Frame(self.top_level)
        self.top_level_frame.pack()
        self.top_level.title('Delete employee')
        self.top_level.resizable(False, False)
        ttk.Label(self.top_level_frame, text="Insert employee id:").grid(row=0, column=0, padx=10, pady=25)
        self.employee_to_delete = StringVar()
        ttk.Entry(self.top_level_frame, textvariable=self.employee_to_delete).grid(row=0, column=1, padx=10, pady=25)
        ttk.Button(self.top_level_frame, text="Delete", command=self.__delete_employee).grid(row=0, column=2, padx=10, pady=25)

    def __delete_employee(self):
        if delete_employee(self.employee_to_delete.get()):
            self.status_text.set("Employee {} was deleted".format(self.employee_to_delete.get()))
            self.top_level.destroy()
        else:
            self.top_level.focus_set()
        self.employee_to_delete.set('')

    def __delete_employees_from_file(self):
        filename = askopenfilename()
        if delete_employees_from_file(filename):
            self.status_text.set("Employees were deleted")

    def __employee_report_top_level(self):
        self.top_level = Toplevel()
        self.top_level_frame = ttk.Frame(self.top_level)
        self.top_level_frame.pack()
        self.top_level.title('Employee report')
        self.top_level.resizable(False, False)
        ttk.Label(self.top_level_frame, text="Insert employee id:").grid(row=0, column=0, padx=10, pady=25)
        self.employee_for_report = StringVar()
        ttk.Entry(self.top_level_frame, textvariable=self.employee_for_report).grid(row=0, column=1, padx=10, pady=25)
        ttk.Button(self.top_level_frame, text="Issue report", command=self.__employee_report).grid(row=0, column=2, padx=10, pady=25)

    def __employee_report(self):
        if employee_report(self.employee_for_report.get()):
            self.status_text.set("Employee report was issued and saved for employee {}".format(self.employee_for_report.get()))
            self.top_level.destroy()
        else:
            self.top_level.focus_set()
        self.employee_for_report.set('')

    def __monthly_report(self):
        if monthly_report():
            self.status_text.set("Attendance report for previous month was issued and saved")

    def __late_report(self):
        if late_report():
            self.status_text.set("Attendance report for late employees was issued and saved")

    def __report_at_specific_time_top_level(self):
        self.top_level = Toplevel()
        self.top_level_frame = ttk.Frame(self.top_level)
        self.top_level_frame.pack()
        self.top_level.title('Employees report at selected time')
        self.top_level.resizable(False, False)
        self.start_date = StringVar()
        self.end_date = StringVar()
        ttk.Label(self.top_level_frame, text="Start date:").grid(row=0, column=0, padx=10, pady=10)
        ttk.Entry(self.top_level_frame, textvariable=self.start_date).grid(row=0, column=1, padx=10, pady=10)
        ttk.Label(self.top_level_frame, text="End date:").grid(row=1, column=0, padx=10, pady=10)
        ttk.Entry(self.top_level_frame, textvariable=self.end_date).grid(row=1, column=1, padx=10, pady=10)
        ttk.Button(self.top_level_frame, text="Issue report", command=self.__report_at_specific_time
                   ).grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    def __report_at_specific_time(self):
        if report_at_specific_time(self.start_date.get(), self.end_date.get()):
            self.status_text.set("Employee report was issued and saved for dates {} to {}".format(self.start_date.get(),
                                                                                                  self.end_date.get()))
            self.top_level.destroy()
        else:
            self.top_level.focus_set()
        self.start_date.set('')
        self.end_date.set('')

    def __employees_list(self):
        self.top_level = Toplevel()
        self.top_level_frame = ttk.Frame(self.top_level)
        self.top_level_frame.pack()
        self.top_level.title('Employees List')
        ttk.Label(self.top_level_frame, text="Record id").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        ttk.Label(self.top_level_frame, text="Employee id").grid(row=0, column=1, padx=5, pady=5, sticky='w')
        ttk.Label(self.top_level_frame, text="Name").grid(row=0, column=2, padx=5, pady=5, sticky='w')
        ttk.Label(self.top_level_frame, text="Age").grid(row=0, column=3, padx=5, pady=5, sticky='w')
        ttk.Label(self.top_level_frame, text="Phone").grid(row=0, column=4, padx=5, pady=5, sticky='w')
        employees = get_employees_from_db()
        counter = 1
        for employee in employees.values():
            ttk.Label(self.top_level_frame, text=counter).grid(row=counter, column=0, padx=5, pady=5, sticky='w')
            ttk.Label(self.top_level_frame, text=(employee['employee_id'])).grid(row=counter, column=1, padx=5, pady=5, sticky='w')
            ttk.Label(self.top_level_frame, text=(employee['name'])).grid(row=counter, column=2, padx=5, pady=5, sticky='w')
            ttk.Label(self.top_level_frame, text=(employee['age'])).grid(row=counter, column=3, padx=5, pady=5, sticky='w')
            ttk.Label(self.top_level_frame, text=(employee['phone'])).grid(row=counter, column=4, padx=5, pady=5, sticky='w')
            counter += 1

    def __change_color(self):
        new_color = colorchooser.askcolor(initialcolor='#e1d8b9')[1]
        self.style.configure('TFrame', background=new_color)
        self.style.configure('TButton', background=new_color)
        self.style.configure('TLabel', background=new_color)

    def __change_font_size(self):
        self.style.configure('TButton', font=('Arial', self.choice.get()))
        self.style.configure('TLabel', font=('Arial', self.choice.get()))

    def __about(self):
        self.top_level = Toplevel()
        self.top_level.geometry('350x80')
        self.top_level.resizable(False, False)
        self.top_level.configure(background='light blue')
        ttk.Label(self.top_level, background='light blue', text="Attendance employee application",
                  font=('Times New Roman', 14, 'bold')).pack()
        ttk.Label(self.top_level, background='light blue', text="built on Apr 2018",
                  font=('Times New Roman', 12)).pack()
        ttk.Label(self.top_level, background='light blue', text="by Lilach Vald-Levi",
                  font=('Times New Roman', 12)).pack()
        self.top_level.after(5000, self.top_level.destroy)


