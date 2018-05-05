from tkinter import *
from tkinter import ttk, colorchooser
from tkinter.filedialog import askopenfilename


class View:
    def __init__(self, master, control):
        master.title('Employees Attendance')
        master.resizable(False, False)
        master.configure(background='#e1d8b9')
        self.control = control

        self.style = ttk.Style()  # check if instead self.style we can changed ti ttk.Style().configure...
        self.color = '#e1d8b9'
        self.__change_color()

        self.employee_id = StringVar()
        panedwindow = ttk.Panedwindow(master, orient=VERTICAL)
        panedwindow.pack(fill=BOTH, expand=True)

        top_frame = ttk.Frame(panedwindow, width=500, height=200, relief=SUNKEN)
        ttk.Label(top_frame, text="Insert employee id:").grid(row=0, column=0, padx=10, pady=30)
        emp_id_entry = ttk.Entry(top_frame, textvariable=self.employee_id)
        emp_id_entry.grid(row=0, column=1, padx=10, pady=30)
        ttk.Button(top_frame, text="Mark attendance", command=self.__mark_attendance).grid(row=0, column=2, padx=10, pady=30)

        bottom_frame = ttk.Frame(panedwindow, width=400, height=50, relief=SUNKEN)
        ttk.Button(bottom_frame, text='Add employee', command=self.__add_employee_top_level).grid(row=0, column=0, padx=25, pady=15)
        ttk.Button(bottom_frame, text='Delete employee', command=self.__delete_employee_top_level).grid(row=0, column=1, pady=15)
        ttk.Button(bottom_frame, text='Employees list', command=self.__employees_list).grid(row=0, column=2, padx=25, pady=15)

        panedwindow.add(top_frame)
        panedwindow.add(bottom_frame)

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
        view.add_command(label='Change color', command=self.__choose_color)
        view.add_cascade(menu=font_size, label='Font size')
        help_.add_command(label='About', command=self.__about)

        self.font_size = IntVar()
        font_size.add_radiobutton(label='Small', variable=self.font_size, value=10, command=self.__change_font_size)
        font_size.add_radiobutton(label='Normal', variable=self.font_size, value=12, command=self.__change_font_size)
        font_size.add_radiobutton(label='Large', variable=self.font_size, value=14, command=self.__change_font_size)
        self.font_size.set(12)
        self.__change_font_size()

    def __mark_attendance(self):
        value = self.employee_id.get()
        if self.control.mark_attendance(value):
            self.status_text.set("Attendance was recorded for employee {}".format(value))
        self.employee_id.set("")

    def __add_employee_top_level(self):
        self.top_level = Toplevel()
        top_level_frame = ttk.Frame(self.top_level)
        top_level_frame.pack()
        self.top_level.title('Add new employee')
        self.top_level.resizable(False, False)
        self.new_employee_id = StringVar()
        self.new_employee_name = StringVar()
        self.new_employee_age = StringVar()
        self.new_employee_phone = StringVar()
        ttk.Label(top_level_frame, text="ID:").grid(row=0, column=0, padx=10, pady=10, sticky='sw')
        ttk.Entry(top_level_frame, textvariable=self.new_employee_id).grid(row=0, column=1, padx=10)
        ttk.Label(top_level_frame, text="Name:").grid(row=1, column=0, padx=10, pady=10, sticky='sw')
        ttk.Entry(top_level_frame, textvariable=self.new_employee_name).grid(row=1, column=1, padx=10)
        ttk.Label(top_level_frame, text="Age:").grid(row=2, column=0, padx=10, pady=10, sticky='sw')
        ttk.Entry(top_level_frame, textvariable=self.new_employee_age).grid(row=2, column=1, padx=10)
        ttk.Label(top_level_frame, text="Phone:").grid(row=3, column=0, padx=10, pady=10, sticky='sw')
        ttk.Entry(top_level_frame, textvariable=self.new_employee_phone).grid(row=3, column=1, padx=10)
        ttk.Button(top_level_frame, text="Add", command=self.__add_employee).grid(row=4, pady=10, column=0, columnspan=2)

    def __add_employee(self):
        if self.control.add_employee(self.new_employee_id.get(), self.new_employee_name.get(),
                                     self.new_employee_age.get(), self.new_employee_phone.get()):
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
        if self.control.add_employees_from_file(filename):
            self.status_text.set("Employees were added")

    def __delete_employee_top_level(self):
        self.top_level = Toplevel()
        top_level_frame = ttk.Frame(self.top_level)
        top_level_frame.pack()
        self.top_level.title('Delete employee')
        self.top_level.resizable(False, False)
        ttk.Label(top_level_frame, text="Insert employee id:").grid(row=0, column=0, padx=10, pady=25)
        self.employee_to_delete = StringVar()
        ttk.Entry(top_level_frame, textvariable=self.employee_to_delete).grid(row=0, column=1, padx=10, pady=25)
        ttk.Button(top_level_frame, text="Delete", command=self.__delete_employee).grid(row=0, column=2, padx=10, pady=25)

    def __delete_employee(self):
        if self.control.delete_employee(self.employee_to_delete.get()):
            self.status_text.set("Employee {} was deleted".format(self.employee_to_delete.get()))
            self.top_level.destroy()
        else:
            self.top_level.focus_set()
        self.employee_to_delete.set('')

    def __delete_employees_from_file(self):
        filename = askopenfilename()
        if self.control.delete_employees_from_file(filename):
            self.status_text.set("Employees were deleted")

    def __employee_report_top_level(self):
        self.top_level = Toplevel()
        top_level_frame = ttk.Frame(self.top_level)
        top_level_frame.pack()
        self.top_level.title('Employee report')
        self.top_level.resizable(False, False)
        ttk.Label(top_level_frame, text="Insert employee id:").grid(row=0, column=0, padx=10, pady=25)
        self.employee_for_report = StringVar()
        ttk.Entry(top_level_frame, textvariable=self.employee_for_report).grid(row=0, column=1, padx=10, pady=25)
        ttk.Button(top_level_frame, text="Issue report", command=self.__employee_report).grid(row=0, column=2, padx=10, pady=25)

    def __employee_report(self):
        if self.control.employee_report(self.employee_for_report.get()):
            self.status_text.set("Employee report was issued and saved for employee {}".format(self.employee_for_report.get()))
            self.top_level.destroy()
        else:
            self.top_level.focus_set()
        self.employee_for_report.set('')

    def __monthly_report(self):
        if self.control.monthly_report():
            self.status_text.set("Attendance report for previous month was issued and saved")

    def __late_report(self):
        if self.control.late_report():
            self.status_text.set("Attendance report for late employees was issued and saved")

    def __report_at_specific_time_top_level(self):
        self.top_level = Toplevel()
        top_level_frame = ttk.Frame(self.top_level)
        top_level_frame.pack()
        self.top_level.title('Employees report at selected time')
        self.top_level.resizable(False, False)
        self.start_date = StringVar()
        self.end_date = StringVar()
        ttk.Label(top_level_frame, text="Start date:").grid(row=0, column=0, padx=10, pady=10)
        ttk.Entry(top_level_frame, textvariable=self.start_date).grid(row=0, column=1, padx=10, pady=10)
        ttk.Label(top_level_frame, text="End date:").grid(row=1, column=0, padx=10, pady=10)
        ttk.Entry(top_level_frame, textvariable=self.end_date).grid(row=1, column=1, padx=10, pady=10)
        ttk.Button(top_level_frame, text="Issue report", command=self.__report_at_specific_time
                   ).grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    def __report_at_specific_time(self):
        if self.control.report_at_specific_time(self.start_date.get(), self.end_date.get()):
            self.status_text.set("Employee report was issued and saved for dates {} to {}".format(self.start_date.get(),
                                                                                                  self.end_date.get()))
            self.top_level.destroy()
        else:
            self.top_level.focus_set()
        self.start_date.set('')
        self.end_date.set('')

    def __employees_list(self):
        self.top_level = Toplevel()
        top_level_frame = ttk.Frame(self.top_level)
        top_level_frame.pack()
        self.top_level.title('Employees List')
        ttk.Label(top_level_frame, text="Record id").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        ttk.Label(top_level_frame, text="Employee id").grid(row=0, column=1, padx=5, pady=5, sticky='w')
        ttk.Label(top_level_frame, text="Name").grid(row=0, column=2, padx=5, pady=5, sticky='w')
        ttk.Label(top_level_frame, text="Age").grid(row=0, column=3, padx=5, pady=5, sticky='w')
        ttk.Label(top_level_frame, text="Phone").grid(row=0, column=4, padx=5, pady=5, sticky='w')
        employees = self.control.get_employees_from_db()
        counter = 1
        for employee in employees.values():
            ttk.Label(top_level_frame, text=counter).grid(row=counter, column=0, padx=5, pady=5, sticky='w')
            ttk.Label(top_level_frame, text=(employee['employee_id'])).grid(row=counter, column=1, padx=5, pady=5, sticky='w')
            ttk.Label(top_level_frame, text=(employee['name'])).grid(row=counter, column=2, padx=5, pady=5, sticky='w')
            ttk.Label(top_level_frame, text=(employee['age'])).grid(row=counter, column=3, padx=5, pady=5, sticky='w')
            ttk.Label(top_level_frame, text=(employee['phone'])).grid(row=counter, column=4, padx=5, pady=5, sticky='w')
            counter += 1

    def __choose_color(self):
        self.color = colorchooser.askcolor(initialcolor=self.color)[1]
        self.__change_color()

    def __change_color(self):
        self.style.configure('TFrame', background=self.color)
        self.style.configure('TButton', background=self.color)
        self.style.configure('TLabel', background=self.color)

    def __change_font_size(self):
        self.style.configure('TButton', font=('Arial', self.font_size.get()))
        self.style.configure('TLabel', font=('Arial', self.font_size.get()))

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

