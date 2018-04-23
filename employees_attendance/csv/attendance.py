import employees_attendance.csv.attendance_functions as funcs


manual_options = {1: 'Add employee manually', 2: 'Add employees from file', 3: 'Delete employee manually',
                  4: 'Delete employees from file', 5: 'Mark attendance', 6: 'Generate employee report',
                  7: 'Generate monthly report', 8: 'Generate late report', 9: 'Generate report for time range',
                  10: 'Exit'}

if __name__ == '__main__':
    funcs.create_files()
    print(manual_options)
    x = 0
    while x != 10:
        try:
            x = int(input('Select the required action by printing the relevant number:'))
            if x not in range(1, 11):
                print('Please make sure to print only one number between 1 to 10')
        except ValueError:
            print('Please make sure to print one number')
            x = 0
        if x == 1:
            funcs.add_employee()
        elif x == 2:
            funcs.add_employees_from_file()
        elif x == 3:
            funcs.delete_employee()
        elif x == 4:
            funcs.delete_employees_from_file()
        elif x == 5:
            funcs.mark_attendance()
        elif x == 6:
            funcs.employee_report()
        elif x == 7:
            funcs.monthly_report()
        elif x == 8:
            funcs.late_report()
        elif x == 9:
            funcs.report_at_specific_time()

