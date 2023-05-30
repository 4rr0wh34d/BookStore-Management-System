import os
import tkinter as tk
from tkinter import ttk
from tkinter import Toplevel
from tkinter import messagebox
import sqlite3


# This class includes attributes and methods that allows authentication to a program.
class Access23:

    # constructor takes variable arguments depending upon which the instance variables are initialised.
    def __init__(self):

        self.filename = ''

        # boolean value to check if the user has been created or not.
        self.user_created = False
        # boolean value to check if the database exist already.
        self.database_check = False

        self.db_name = ''
        self.username = ''
        self.password = ''
        self.account_type = ''

        self.user_credential_window = tk.Tk()
        self.width, self.height = self.user_credential_window.winfo_screenwidth(), self.user_credential_window.winfo_screenheight()

        # self.user_credential_window.protocol('WM_DELETE_WINDOW', lambda: self.unsuccessful('create'))
        # self.user_credential_window.mainloop()

    # Function definition that allows to take in the details of the first user and the database.
    def create_user(self, filename):

        # File to  store the name of database name, table name and its headings
        self.filename = filename

        self.user_credential_window.title('Create user')

        self.user_credential_window.geometry(f'{self.width // 4}x{self.height // 3}+{self.width//3}+{self.height//3}')
        self.user_credential_window.resizable(0, 0)

        # Defining window frame to put widget to get new user details
        create_user_frame = tk.Frame(self.user_credential_window, padx=10, pady=10)

        l_username = tk.Label(create_user_frame, text='Create Username', anchor='center')
        l_username.grid(row=0, column=0, sticky=tk.E + tk.W)

        self.create_username = tk.Entry(create_user_frame)
        self.create_username.grid(row=0, column=1, sticky=tk.E + tk.W)

        l_password = tk.Label(create_user_frame, text='Create Password', anchor='center')
        l_password.grid(row=1, column=0, sticky=tk.E + tk.W)

        self.create_password = tk.Entry(create_user_frame)
        self.create_password.config(show='*')
        self.create_password.grid(row=1, column=1, sticky=tk.E + tk.W)

        l_confirm_password = tk.Label(create_user_frame, text='Confirm Password', anchor='center')
        l_confirm_password.grid(row=2, column=0, sticky=tk.E + tk.W)

        self.confirm_password = tk.Entry(create_user_frame)
        self.confirm_password.config(show='*')
        self.confirm_password.grid(row=2, column=1, sticky=tk.E + tk.W)

        l_account_type = tk.Label(create_user_frame, text='Account Type', anchor='center')
        l_account_type.grid(row=3, column=0, sticky=tk.E + tk.W)

        self.c_account_type = ttk.Combobox(create_user_frame, state='readonly', values=[
            'Administrator', 'Employee', 'Guest'])
        self.c_account_type.set('Administrator')
        self.c_account_type.grid(row=3, column=1, sticky=tk.E + tk.W)

        # This section only gets called if the program is running for the first time to create new database
        # and create the configuration file which contains database name, table name and headings details.
        if not os.path.exists(self.filename):

            l_database_name = tk.Label(create_user_frame, text='Create database name', anchor='center')
            l_database_name.grid(row=4, column=0, sticky=tk.E + tk.W)

            self.e_database_name = tk.Entry(create_user_frame)
            self.e_database_name.grid(row=4, column=1, sticky=tk.E + tk.W)

        create_user_frame.pack(fill='both', side='top')

        # Defining button frame to include button widget to finally create user.
        btn_frame = tk.Frame(self.user_credential_window, padx=10, pady=10)

        btn_create = tk.Button(btn_frame, text='Create', command=self.confirm_passwords)
        btn_create.pack(side='left')

        btn_frame.pack(fill='both')

        self.user_credential_window.protocol('WM_DELETE_WINDOW', lambda: self.unsuccessful('create'))
        self.user_credential_window.mainloop()

    # Function to check if both passwords entered are same and if it is, then continue creating a database and table.
    def confirm_passwords(self):

        # Get the database name from the database entry field if the program is running for the first time to create the
        # first user and check if there is a database with the same name. Otherwise, skips in case if the configuration
        # file already exist. This section checks two same passwords of the given user to continue creating credentials.
        if not os.path.exists(self.filename):
            self.db_name = self.e_database_name.get()

            if os.path.exists('./' + self.db_name):
                messagebox.showinfo('Database Error', 'Database with that name already exists. Try again')
                self.e_database_name.delete(0, 'end')
                self.db_name = ''
                self.database_check = False
            else:
                with open(self.filename, 'w+', encoding='utf-8') as file:
                    file.write('Database Name: ' + self.db_name + '\n')
                # Creating a database and table when all criteria are met. Section only executed
                # once at the beginning

                try:
                    db = sqlite3.connect(self.db_name)
                    cursor = db.cursor()

                    # Create a table call users to store username and password for a given user
                    cursor.execute('CREATE TABLE IF NOT EXISTS users(User text, Password text, Account_type text)')

                    db.commit()
                    db.close()

                except Exception as e:
                    messagebox.showinfo('Database Error', f'Error {e}')
                    self.user_credential_window.destroy()
                    os.remove(self.db_name)
                self.database_check = True

        else:
            with open('./config.txt', 'r', encoding='utf-8') as file:
                for i, line in enumerate(file):
                    if i == 0:
                        self.db_name = line.replace('\n', '').split(': ')[1]

            if os.path.exists(self.db_name):
                self.database_check = True

        if self.database_check:

            if not self.create_password.get() == self.confirm_password.get():

                messagebox.showinfo('Password Error', 'Passwords do not match. Try Again')
                self.create_username.delete(0, 'end')
                self.create_password.delete(0, 'end')
                self.confirm_password.delete(0, 'end')
                self.c_account_type.set('Administrator')

            else:

                self.username = self.create_username.get()
                self.password = self.create_password.get()
                self.account_type = self.c_account_type.get()

                # Finally calling add function to add user details to database
                self.add_user()

    # Function to record the user details. This function is reusable to create more users later in the future
    def add_user(self):

        db = sqlite3.connect(self.db_name)
        cursor = db.cursor()

        cursor.execute('SELECT * FROM users WHERE User = ?', (self.username, ))

        if not cursor.fetchone() is None:
            messagebox.showinfo('Error creating user', 'User already exist with that name')
            self.user_created = False
        else:
            cursor.execute('INSERT INTO users VALUES(?, ?, ?)', (self.username, self.password, self.account_type))
            self.user_created = True

        db.commit()
        db.close()

        messagebox.showinfo('Successful Operation', 'New User created')

        # Destroying the windows after successful creation of the user
        if self.user_created:
            self.user_credential_window.destroy()

    def check_user(self, filename):

        self.filename = filename

        self.user_credential_window.focus()
        self.user_credential_window.title('Check Credentials')
        self.user_credential_window.resizable(0, 0)
        self.user_credential_window.geometry(
            f'{self.width//4}x{self.height//4}+{self.width//3}+{self.height//3}')

        check_user_frame = tk.Frame(self.user_credential_window, padx=10, pady=10, height=self.height//4)

        l_username = tk.Label(check_user_frame, text='Username:', anchor='e')
        l_username.place(x=20, y=30)
        # l_username.grid(row=0, column=0, sticky=tk.E + tk.W)

        self.e_username = tk.Entry(check_user_frame)
        self.e_username.place(x=150, y=30)

        l_password = tk.Label(check_user_frame, text='Password', anchor='e')
        l_password.place(x=20, y=60)

        self.e_password = tk.Entry(check_user_frame)
        self.e_password.config(show='*')
        self.e_password.place(x=150, y=60)

        btn_login = tk.Button(check_user_frame, text='Login', width=10, command=self.compare_credentials)
        btn_login.place(x=180, y=100)

        check_user_frame.pack(side='top', fill='both')

        self.user_credential_window.protocol('WM_DELETE_WINDOW', lambda: self.unsuccessful('check'))
        # # self.check_user_window.eval('tk::PlaceWindow . center')
        self.user_credential_window.mainloop()

    def compare_credentials(self):

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
                self.user_credential_window.destroy()

            else:
                messagebox.showinfo('Credential not Matched', f'Try Again ')
                self.e_username.delete(0, 'end')
                self.e_password.delete(0, 'end')

    def unsuccessful(self, options):
        if options == 'create':
            if messagebox.askyesno(title='Confirm', message='Do you want to exit. No user created'):
                self.password = ''
                self.user_credential_window.destroy()
                exit()
        elif options == 'check':
            if messagebox.askyesno(title='Confirm', message='Do you want to exit'):
                self.user_credential_window.destroy()
                exit()

    def show_user(self, filename):
        show_window = tk.Tk()
        show_window.title('Users')
        show_window.geometry('400x300')

        show_frame = tk.Frame(show_window)
        show_frame.pack(fill='both')
        with open(filename, 'r', encoding='utf-8') as file:
            for i, line in enumerate(file):
                # Reading the first line of the configuration file and splitting the line into list. Then selecting the
                # second argument of the list
                if i == 0:
                    self.db_name = line.replace('\n', '').split(': ')[1]

            db = sqlite3.connect(self.db_name)
            cursor = db.cursor()

            # Getting all the users and their details from the table 'users'
            cursor.execute(f'SELECT * FROM users')

            heading = ['Users', 'Passwords', 'Account Type']
            for num in range(0, 3):
                label = tk.Label(show_frame, text=heading[num], anchor='center')
                label.grid(row=0, column=num, sticky=tk.E + tk.W)
            for i, row in enumerate(cursor):
                for j, value in enumerate(row):
                    entry = tk.Entry(show_frame)
                    entry.insert(0, value)
                    entry.grid(row=i+1, column=j, sticky=tk.E + tk.W)

        show_window.mainloop()

# ac = Access23()
# ac.create_user('./config.txt')
# ac.check_user('./config.txt')

