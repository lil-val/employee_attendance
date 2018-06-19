from tkinter import *
from tkinter import ttk
from tkinter import messagebox


class UI:
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
        self.top_frame = ttk.Frame(panedwindow, width=400, height=100, relief=SUNKEN)

        insert_emp_id = ttk.Label(self.top_frame, text="Insert employee id:")
        insert_emp_id.grid(row=0, column=0, padx=10, pady=25)
        emp_id_entry = ttk.Entry(self.top_frame, textvariable=self.employee_id)
        emp_id_entry.grid(row=0, column=1, padx=10, pady=25)
        mark_attendance_button = ttk.Button(self.top_frame, text="Mark attendance")  # add command=
        mark_attendance_button.grid(row=0, column=2, padx=10, pady=25)

        self.bottom_frame = ttk.Frame(panedwindow, width=400, height=50, relief=SUNKEN)
        ttk.Button(self.bottom_frame, text='Add Employee').grid(row=0, column=0, padx=5, pady=10, sticky='e')  # add command=
        ttk.Button(self.bottom_frame, text='Delete Employee').grid(row=0, column=1, pady=10, sticky='w')  # add command=

        panedwindow.add(self.top_frame)
        panedwindow.add(self.bottom_frame)

        self.status_text = StringVar('')
        status = Label(master, textvariable=self.status_text, bd=1, relief=SUNKEN, anchor=W)
        status.pack(side=BOTTOM, fill=X)


if __name__ == "__main__":
    root = Tk()
    UI(root)
    root.mainloop()

#
# class GUI(Frame):
#     def __init__(self, master=None):
#         Frame.__init__(self, master)
#         self.master = master
#         self.pack()
#         self.__init_ui()
#
#     def __init_ui(self):
#         self.master.title("Employees Attendance")
#         self.master.geometry("600x400")
#         self.pack(fill=BOTH)
#         self.employee_id = StringVar()
#         self.top_frame = Frame(self, highlightbackground="blue", highlightcolor="red", highlightthickness=1, width=400, height=100, bd=0)
#         self.top_frame.pack()
#         self.top_frame.pack_propagate(False)
#         self.bottom_frame = Frame(self, width=400, height=100)
#         self.bottom_frame.pack()
#         self.bottom_frame.pack_propagate(False)
#         insert_emp_id = Label(self.top_frame, text="Insert employee id:", font=25)
#         insert_emp_id.pack(side=LEFT)
#         emp_id_entry = Entry(self.top_frame, textvariable=self.employee_id)
#         emp_id_entry.pack(side=LEFT)
#         mark_attendance_button = Button(self.top_frame, text="Mark attendance", font=25, command=self.__mark_attendance)
#         mark_attendance_button.pack(side=LEFT)
#         add_emp_button = Button(self.bottom_frame, text='Add Employee')
#         add_emp_button.pack(side=LEFT)
#         delete_emp_button = Button(self.bottom_frame, text='Delete Employee', command=self.__delete_employee)
#         delete_emp_button.pack(side=LEFT)
#         self.status_text = StringVar('')
#         status = Label(self.master, textvariable=self.status_text, bd=1, relief=SUNKEN, anchor=W)
#         status.pack(side=BOTTOM, fill=X)
#
#     def __mark_attendance(self):
#         value = self.employee_id.get()
#         if mark_attendance(value):
#             self.status_text.set("Attendance was recorded for employee {}".format(value))
#         self.employee_id.set("")
#
#     def __delete_employee(self):
#         self.top_level = Toplevel()
#         Label(self.top_level, text="Insert employee id:").pack()
#         self.employee_to_delete = StringVar()
#         Entry(self.top_level, textvariable=self.employee_to_delete).pack()
#         Button(self.top_level, text="Delete", command=self.__delete_employee_helper).pack()
#
#     def __delete_employee_helper(self):
#         if delete_employee(self.employee_to_delete.get()):
#             self.status_text.set("Employee {} was deleted".format(self.employee_to_delete.get()))
#             self.top_level.destroy()
#         else:
#             self.top_level.focus_set()
#         self.employee_to_delete.set('')
