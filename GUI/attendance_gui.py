from GUI.attendance_control_gui import Control
from tkinter import *


if __name__ == '__main__':
    if len(sys.argv) != 6:
        print('Please run the script with the following database connection arguments:'
              'python attendance.py <hostname> <port> <user_name> <password> <scheme>')
        sys.exit(1)  # 1 means with an error
    root = Tk()
    Control(root, sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4], sys.argv[5])
    # sample command line: python attendance_gui.py localhost 3306 root root attendance
    # tables will be created by DBA by db_script.sql
    root.mainloop()
