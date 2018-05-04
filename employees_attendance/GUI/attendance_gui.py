import employees_attendance.GUI.attendance_functions_gui as funcs
from tkinter import *


if __name__ == '__main__':
    if len(sys.argv) != 6:
        print('Please run the script with the following database connection arguments:'
              'python attendance.py <hostname> <port> <user_name> <password> <scheme>')
        sys.exit(1)  # 1 means with an error
    funcs.init(sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4], sys.argv[5])
    # sample command line: python attendance_gui.py localhost 3306 root root attendance
    # tables will be created by DBA by db_script.sql
    root = Tk()
    funcs.GUI(root)
    root.mainloop()

