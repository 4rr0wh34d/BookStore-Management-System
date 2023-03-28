import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3


# This class includes attributes and methods that allows authentication to a program.
class Access23:

    # constructor takes variable arguments depending upon which the instance variables are initialised.
    def __init__(self, *args):

        self.filename = ''

        self.args_length = len(args)

        if self.args_length == 0:
            self.db_name = ''
            self.username = ''
            self.password = ''
            self.account_type = ''
            self.create_user_window = tk.Tk()

        elif self.args_length == 4:
            self.db_name = args[0]
            self.username = args[1]
            self.password = args[2]
            self.account_type = args[3]

    # Function definition that allows to take in the details of the new user.
    def create_user(self, filename):

        self.filename = filename

        self.create_user_window.title('Create user')
        self.create_user_window.geometry('400x300')

        # Defining window frame to put widget to get new user details
        create_user_frame = tk.Frame(self.create_user_window, padx=10, pady=10)

        l_username = tk.Label(create_user_frame, text='Create Username')
        l_username.grid(row=0, column=0, sticky=tk.E + tk.W)

        self.e_username = tk.Entry(create_user_frame)
        self.e_username.grid(row=0, column=1, sticky=tk.E + tk.W)

        l_password = tk.Label(create_user_frame, text='Create Password')
        l_password.grid(row=1, column=0, sticky=tk.E + tk.W)

        self.e_password = tk.Entry(create_user_frame)
        self.e_password.grid(row=1, column=1, sticky=tk.E + tk.W)

        l_confirm_password = tk.Label(create_user_frame, text='Confirm Password')
        l_confirm_password.grid(row=2, column=0, sticky=tk.E + tk.W)

        self.e_confirm_password = tk.Entry(create_user_frame)
        self.e_confirm_password.grid(row=2, column=1, sticky=tk.E + tk.W)

        l_account_type = tk.Label(create_user_frame, text='Account Type')
        l_account_type.grid(row=3, column=0, sticky=tk.E + tk.W)

        self.c_account_type = ttk.Combobox(create_user_frame, state='readonly', values=[
            'Administrator', 'Employee', 'Guest'])
        self.c_account_type.set('Administrator')
        self.c_account_type.grid(row=3, column=1, sticky=tk.E + tk.W)

        l_database_name = tk.Label(create_user_frame, text='Create database name')
        l_database_name.grid(row=4, column=0, sticky=tk.E + tk.W)

        self.e_database_name = tk.Entry(create_user_frame)
        self.e_database_name.grid(row=4, column=1, sticky=tk.E + tk.W)

        create_user_frame.pack(fill='both', side='top')

        # Defining button frame to include button widget to finally create user.
        btn_frame = tk.Frame(self.create_user_window, padx=10, pady=10)

        btn_create = tk.Button(btn_frame, text='Create', command=self.confirm_passwords)
        btn_create.pack(side='left')

        btn_frame.pack(fill='both')

        self.create_user_window.protocol('WM_DELETE_WINDOW', self.unsuccessful)
        self.create_user_window.mainloop()

    # Function to check if both passwords entered are same and if it is, then continue creating a database and table.
    def confirm_passwords(self):

        self.db_name = self.e_database_name.get()

        if not self.e_password.get() == self.e_confirm_password.get():
            messagebox.showinfo('Password Error', 'Passwords do not match. Try Again')
            self.e_username.delete(0, 'end')
            self.e_password.delete(0, 'end')
            self.e_confirm_password.delete(0, 'end')
            self.e_database_name.delete(0, 'end')
            self.c_account_type.set('Administrator')

            if os.path.exists('./' + self.db_name):
                messagebox.showinfo('Database Error', 'Database with that name already exists. Try again')

        else:

            self.username = self.e_username.get()
            self.password = self.e_password.get()
            self.account_type = self.c_account_type.get()

            try:

                db = sqlite3.connect(self.db_name)
                cursor = db.cursor()

                cursor.execute('CREATE TABLE IF NOT EXISTS users(User text, Password text, Account_type text)')
                db.commit()

                db.close()

                with open(self.filename, 'w+', encoding='utf-8') as file:
                    file.write('Database Name: ' + self.db_name + '\n')

                self.record_user()

            except Exception as e:
                messagebox.showinfo('Database Error', f'Error {e}')
                self.create_user_window.destroy()
                os.remove(self.db_name)

    # Function to record the user details. This function is reusable to create more users later in the future
    def record_user(self):

        db = sqlite3.connect(self.db_name)
        cursor = db.cursor()

        cursor.execute('SELECT * FROM users WHERE User = ?', (self.username, ))

        if not cursor.fetchone() is None:
            messagebox.showinfo('Error creating user', 'User already exist with that name')
            exit()

        else:
            cursor.execute('INSERT INTO users VALUES(?, ?, ?)', (self.username, self.password, self.account_type))

        db.commit()
        db.close()

        # section useful in future
        # record_user_window = Toplevel(self.create_user_window)
        # record_user_window.geometry('200x200')
        # record_user_window.title('Create database and table to store users')
        #
        # l_database_name = tk.Label(record_user_window, 'Create database')
        # l_database_name.grid(row=0, column=0, sticky=tk.E + tk.W)
        #
        # e_database_name = tk.Entry(record_user_window)
        # e_database_name.grid(row=0, column=1, sticky=tk.E + tk.W)

        messagebox.showinfo('Successful Operation', 'New User created')

        if self.args_length == 0:
            self.create_user_window.destroy()

        else:
            pass

    def check_user(self, filename):

        self.filename = filename

        self.create_user_window.title('Check Credentials')
        self.create_user_window.geometry('400x300')

        check_user_frame = tk.Frame(self.create_user_window, padx=10, pady=10)

        l_username = tk.Label(check_user_frame, text='Username:')
        l_username.grid(row=0, column=0, sticky=tk.E + tk.W)

        self.e_username = tk.Entry(check_user_frame)
        self.e_username.grid(row=0, column=1, sticky=tk.E + tk.W)

        l_password = tk.Label(check_user_frame, text='Password:')
        l_password.grid(row=1, column=0, sticky=tk.E + tk.W)

        self.e_password = tk.Entry(check_user_frame)
        self.e_password.grid(row=1, column=1, sticky=tk.E + tk.W)

        check_user_frame.pack(side='top', fill='both')

        # btn_login = tk.Button(self.root_window, text='Login', command=self.compare_credentials)
        # btn_login.pack(side='left')

        btn_frame = tk.Frame(self.create_user_window, padx=10, pady=10)

        btn_login = tk.Button(btn_frame, text='Login', command=self.compare_credentials)
        btn_login.pack(side='left')

        btn_frame.pack(fill='both')

        self.create_user_window.protocol('WM_DELETE_WINDOW', self.unsuccessful)
        self.create_user_window.mainloop()

    def compare_credentials(self):

        # with open(self.filename, 'r', encoding='utf-8') as file:
        #     for i, line in enumerate(file):
        #         if i == 0:
        #             username, password = line.replace('\n', '').split(': ')
        #
        # print(username + ' ' + password)
        #
        # if self.e_username.get() == username and self.e_password.get() == password:
        #     messagebox.showinfo('Credentials Matched', f'Welcome {username} ')
        #     self.create_user_window.destroy()
        #     # return True

        username = self.e_username.get()
        password = self.e_password.get()

        with open(self.filename, 'r', encoding='utf-8') as file:
            for i, line in enumerate(file):
                if i == 0:
                    self.db_name = line.replace('\n', '').split(': ')[1]
        db = sqlite3.connect(self.db_name)
        cursor = db.cursor()

        cursor.execute('SELECT * FROM users WHERE User = ?', (username,))

        if cursor.fetchone() is None:
            messagebox.showinfo('No User', 'User does not exist')

        else:
            cursor.execute('SELECT * FROM users WHERE User = ?', (username,))

            for i, value in enumerate(cursor.fetchone()):
                if i == 1:
                    self.password = value

            if self.password == password:
                messagebox.showinfo('Credentials Matched', f'Welcome {username} ')
                self.create_user_window.destroy()

            else:
                messagebox.showinfo('Credential not Matched', f'Try Again ')
                self.e_username.delete(0, 'end')
                self.e_password.delete(0, 'end')

    def unsuccessful(self):
        if messagebox.askyesno(title='Confirm', message='Do you want to exit. No user created'):
            self.password = ''
            exit()

    def show_user(self, filename):

        with open(filename, 'r', encoding='utf-8') as file:
            for i, line in enumerate(file):
                # Reading the first line of the configuration file and splitting the line into list. Then selecting the
                # second argument of the list
                if i == 0:
                    self.db_name = line.replace('\n', '').split(': ')[1]

            print(self.db_name)
            db = sqlite3.connect(self.db_name)
            cursor = db.cursor()

            cursor.execute(f'SELECT * FROM users')

            for row in cursor:
                print(row)


# ac = Access23()
# ac = Access23('bookstore', 'pratik', 'rai', 'Guest')
# ac.create_user('./config.txt')
# ac.show_user('./config.txt')

