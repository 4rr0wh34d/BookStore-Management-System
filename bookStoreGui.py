# This program utilizes and demonstrates the use of sqlite3 database in python. It allows user to create a database with
# a table and allow them to add, delete, update and search data into the table. It also uses custom module called
# excel23 to import and export Excel files.

# Import statements
import sqlite3
import os.path
import tkinter as tk
from tkinter import Toplevel
from tkinter import messagebox
from tkinter import filedialog as fd
# from tkinter import

# importing custom python file called excel23 to import or export Excel files
from excel23 import *

# importing custom python file to carry out authentication
from access23 import Access23  # as Access


# Class definition with various function and attributes
class BookStore:

    # Defining class constructor which receives a boolean value which indicates if the database configuration file
    # already exist or not (or if the program is running for the first time)
    # depending upon which the if else statement is executed
    def __init__(self, config_file_exist):

        # instance variables

        self.table_name = ''
        self.database_name = ''
        self.filename = ''
        self.headings = ''

        # Defining boolean variable to check if the database and table has been created or already exist.
        self.database_table_created = False

        # If the config file does not exist then create a config.txt file, create new user, create a database and table
        # and record the info in the config file.
        if not config_file_exist:

            # Creating an object of class Access23 and calling create_user function to create new user. If the user is
            # created, the create_user function returns True and the main menu window is displayed.
            access = Access23()
            access.create_user('./config.txt')

            # self.database_name = access.db_name

            with open('config.txt', 'r', encoding='utf-8') as file:

                for i, line in enumerate(file):
                    if i == 0:
                        self.database_name = line.replace('\n', '').split(': ')[1]

            try:
                self.db = sqlite3.connect(self.database_name)
                self.cursor = self.db.cursor()

                # Defining table window and frame
                self.tb_window = tk.Tk()
                self.tb_window.title('Creating Table')
                self.tb_window.geometry('300x200')

                # calling the create_table_details function to collect details of table to create it.
                self.get_table_details()

                self.tb_window.mainloop()

            except Exception as e:
                messagebox.showinfo('Database Error', f'{e}')

        # If the config file exist, then extract information from database to check the user credentials inputted by
        # the user and if it matches give access to the main menu window.
        else:

            # Calling the check_user function of class Access23 to check credentials against user inputs. If the check
            # is passed then get the database name from the config file and connect to the database. If connection
            # is successful program flow enters the main menu window.
            access = Access23()
            access.check_user('config.txt')

            # Opening configuration files 'config.txt' to get the database and table name created during initial
            # configuration
            with open('config.txt', 'r+', encoding='utf-8') as filehandle:

                for i, line in enumerate(filehandle):
                    # Getting the database name from the first line
                    if i == 0:
                        self.database_name = line.replace('\n', '').split(': ')[1]

                    # Getting the table name from the second line
                    elif i == 1:
                        self.table_name = line.replace('\n', '').split(': ')[1]

                    # Getting the table's fields' headings
                    elif i == 2:
                        temp_list = line.split(': ')[1]
                        self.headings = temp_list.split(' ')

            if os.path.exists('./' + self.database_name):
                self.db = sqlite3.connect('./' + self.database_name)
                self.cursor = self.db.cursor()
                self.database_table_created = True

                # query = f'SELECT * FROM {self.table_name}'
                # self.cursor.execute('SELECT * FROM ')

        # Checking if the database and table already exist or has been created, then give access to the main menu window

        if self.database_table_created:
            # Creating a root window
            self.root_window = tk.Tk()
            self.root_window.title("BookStore management system")
            self.root_window.geometry("400x250")

            # Creating a menubar
            self.menubar = tk.Menu(self.root_window)

            # Calling the main user menu
            self.user_menu()

    # Function to start creating database
    def get_table_details(self):

        tb_frame = tk.Frame(self.tb_window, padx=10, pady=10)

        # Label and Entry widget definition to get user input
        l_table_name = tk.Label(tb_frame, text='Create Table Name')
        l_table_name.grid(row=0, column=0, sticky=tk.E + tk.W)

        e_table_name = tk.Entry(tb_frame)
        e_table_name.grid(row=0, column=1, sticky=tk.E + tk.W)

        l_total_field = tk.Label(tb_frame, text='Number of Table Fields')
        l_total_field.grid(row=1, column=0, sticky=tk.E + tk.W)

        e_total_field = tk.Entry(tb_frame)
        e_total_field.grid(row=1, column=1, sticky=tk.E + tk.W)

        # Button to continue getting details to make the database and table. When button is clicked, a get_fields method
        # is called where database name, table name and size of fields to be created is passed as an argument.
        btn_next = tk.Button(tb_frame, text='Next',
                             command=lambda: self.get_fields(
                                 int(e_total_field.get()), e_table_name.get()))
        btn_next.grid(row=3, column=0, sticky=tk.E + tk.W)

        tb_frame.pack(fill='both')

    # Function to get fields for the table and create table
    def get_fields(self, size, table_name):  # database_name,

        # self.database_name = database_name
        self.table_name = table_name

        # Defining two dimension entry with 4 rows and 2 column. Each row receives table's field names and field types.
        en = [[tk.Entry for i in range(2)] for j in range(size)]
        # en = [[tk.Entry] * 2] * size

        parent_window = self.tb_window

        # Creating a child window 'fields_window' whose parent window is 'tb_window'
        fields_window = Toplevel(parent_window)

        # Setting window title and size
        fields_window.title('Creating table')
        fields_window.geometry('400x200')

        # Focusing the current window and disabling the parent window
        fields_window.grab_set()

        # Frame and label definition
        fields_frame = tk.Frame(fields_window)

        l_name = tk.Label(fields_frame, text='Field Name')
        l_name.grid(row=0, column=1, sticky=tk.E + tk.W)
        l_size = tk.Label(fields_frame, text='Field Data Type')
        l_size.grid(row=0, column=2, sticky=tk.E + tk.W)

        # laying label and a pair of entry widgets in a grid
        for i in range(size):
            l_field = tk.Label(fields_frame, text=f'Enter field {i}')
            l_field.grid(row=i+1, column=0, sticky=tk.E + tk.W)
            for j in range(2):

                en[i][j] = tk.Entry(fields_frame)
                en[i][j].grid(row=i+1, column=j+1, sticky=tk.E + tk.W)

        # When the button is pressed both entry fields and the field window is passed to create_table. Both entry fields
        # are passed as list.
        btn_create = tk.Button(fields_frame, text='Create', command=lambda: self.create_table(
            [f'{en[k][0].get()} {en[k][1].get()}' for k in range(size)], fields_window))
        btn_create.grid(row=size+1, column=2, sticky=tk.E + tk.W)

        fields_frame.pack(fill='both')

    # Function to create table
    def create_table(self, fields, get_window):
        # table_name = self.e_table_name.get()
        # Declaring empty string str_field_type to store table's field heading and their type
        str_headings_types = ''
        # Declaring empty string to store table's field heading.
        str_headings = ''
        size = len(fields)

        # Creating a string str_headings_types with all the table's fields' headings and type to create a query to
        # create a new table. String str_headings is created to store table's fields' heading to write to a config
        # file for future use while recreating a new Excel file with all the database records.
        for i, field in enumerate(fields):
            # checking to see if it is the last element of list 'fields' and skip the comma in str_headings_types
            # and space in case of str_headings
            if i == size - 1:
                str_headings_types += field
                str_headings += field.split(' ')[0]
            else:
                str_headings_types += field + ', '
                str_headings += field.split(' ')[0] + ' '

        # creating a query with table name and the fields
        query = f'CREATE TABLE IF NOT EXISTS {self.table_name}({str_headings_types})'
        self.cursor.execute(query)
        self.db.commit()

        # self.db.close()

        with open('config.txt', 'a+', encoding='utf-8') as filehandle:
            filehandle.write('Table Name: ' + self.table_name + '\n' + 'Headings: ' + str_headings)

        # Since the table creation was successful set table_created variable to True
        self.database_table_created = True

        get_window.destroy()
        self.tb_window.destroy()

    # Function to confirm whether to close window or not
    def user_menu(self):
        # Adding two menu called file_menu and about_menu
        file_menu = tk.Menu(self.menubar, tearoff=0)
        about_menu = tk.Menu(self.menubar, tearoff=0)

        # Adding the commands to the file_menu
        file_menu.add_command(label='Import from database',
                              command=lambda value='Import': self.handle_menubar(value))
        file_menu.add_command(label='Export to database',
                              command=lambda value='Export': self.handle_menubar(value))

        # Adding seperator in the file_menu and adding exit menu
        file_menu.add_separator()
        file_menu.add_command(label='Exit', command=self.confirm_close)

        # Finally adding the file_menu to a menubar.
        self.menubar.add_cascade(label='File', menu=file_menu)

        # Similarly adding command to about_menu and adding it to a menubar
        about_menu.add_command(label='About', command=self.handle_menubar)
        self.menubar.add_cascade(label='Help', menu=about_menu)

        # Creating a root frame to put all the tkinter widget to be displayed on top in the root window
        root_frame = tk.Frame(self.root_window, padx=10, pady=10)

        # Adding widget to a root_frame
        main_label = tk.Label(root_frame, text="Library Management System")
        main_label.grid(row=0, column=0, sticky=tk.E + tk.W)

        add_button = tk.Button(root_frame, text="Add Book", command=self.new_entry)
        add_button.grid(row=2, column=0, sticky=tk.E + tk.W)

        book_update = tk.Button(root_frame, text="Update Book", command=lambda: self.update_book(0))
        book_update.grid(row=3, column=0, sticky=tk.E + tk.W)

        book_delete = tk.Button(root_frame, text="Delete Book", command=self.delete_book)
        book_delete.grid(row=4, column=0, sticky=tk.E + tk.W)

        book_search = tk.Button(root_frame, text="Search Book", command=lambda: self.search_book(0))
        book_search.grid(row=5, column=0, sticky=tk.E + tk.W)

        book_view = tk.Button(root_frame, text="View books", command=lambda: self.view_all())
        book_view.grid(row=5, column=0, sticky=tk.E + tk.W)

        root_frame.pack()

        self.root_window.config(menu=self.menubar)
        self.root_window.protocol("WM_DELETE_WINDOW", self.confirm_close)
        self.root_window.mainloop()

    def confirm_close(self):
        if messagebox.askyesno(title="Quit", message="Confirm to close"):
            self.db.commit()
            self.db.close()
            self.root_window.destroy()

    # Function to upload and download data to and from database.
    def handle_menubar(self, value):

        # If the value of the argument received is Export then allow user to select the Excel file from where the data
        # is to be written to database. We use excel_to_sqlite methods of excel23 class to write or export to
        # the database.
        if value == 'Export':
            self.filename = fd.askopenfilename(title='Open File', initialdir='./')
            if self.filename is not None:
                xl = Excel23()
                xl.excel_to_sqlite(self.database_name, self.table_name, self.filename)

        # If the value is Import then write or import from database to a new Excel file created by the user.
        elif value == 'Import':
            self.filename = fd.asksaveasfilename(title='Save', initialdir='./')
            if self.filename is not None:
                xl = Excel23()
                xl.sqlite_to_excel(self.database_name, self.table_name, self.filename, self.headings)

    # Function to return to main window
    def return_back(self, get_current_window):
        # get_current_window.grab_release()
        get_current_window.destroy()
        # return self

# Function to display all the records from the table books using Entry widget.
    def view_all(self):

        self.cursor.execute(f'SELECT * FROM {self.table_name}')

        view_window = Toplevel(self.root_window)
        view_window.grab_set()

        view_window.title('View Book Database')
        view_window.geometry('550x300')
        view_frame = tk.Frame(view_window, padx=20, pady=10)

        id_label = tk.Label(view_frame, text='ID')
        id_label.grid(row=0, column=0, sticky=tk.E + tk.W)

        title_label = tk.Label(view_frame, text='Title')
        title_label.grid(row=0, column=1, sticky=tk.E + tk.W)

        author_label = tk.Label(view_frame, text='Author')
        author_label.grid(row=0, column=2, sticky=tk.E + tk.W)

        qty_label = tk.Label(view_frame, text='Qty')
        qty_label.grid(row=0, column=3, sticky=tk.E + tk.W)

        for i, row in enumerate(self.cursor):
            for j, value in enumerate(row):
                en = tk.Entry(view_frame)

                en.grid(row=i + 1, column=j, sticky=tk.E + tk.W)
                en.insert(0, value)
                en.config(state='disabled')

        view_frame.pack(fill='both', side='top')

        back_button = tk.Button(view_window, text='BACK',
                                command=lambda option=view_window: self.return_back(option))
        back_button.pack(side='bottom', padx=20, pady=20)

    # Function to check if the record with certain Book id exists.
    def check_id(self, get_id):
        self.cursor.execute('SELECT * FROM books WHERE id = ?', (get_id,))
        if self.cursor.fetchone() is None:
            return False
        else:
            return True

    # Function to enter new book record. User are allowed to enter details of new book that need to be added to the
    # database
    def new_entry(self):

        # Function to add new book to database
        def add_book(bid, title, author, qty):
            self.cursor.execute(f'INSERT INTO {self.table_name} VALUES(?, ?, ?, ?)', (bid, title, author, qty))
            self.db.commit()
            messagebox.showinfo('New Entry', 'New Record have been entered')
            get_id.delete(0, 'end')
            get_title.delete(0, 'end')
            get_author.delete(0, 'end')
            get_qty.delete(0, 'end')

        entry = Toplevel(self.root_window)
        entry .grab_set()

        entry.title('New book Entry')
        entry.geometry('400x250')

        entry_frame = tk.Frame(entry, padx=10, pady=10)

        id_label = tk.Label(entry_frame, text='Book ID : ')
        id_label.grid(row=0, column=0, sticky=tk.E+tk.W)
        get_id = tk.Entry(entry_frame)
        get_id.grid(row=0, column=1, sticky=tk.E+tk.W)

        title_label = tk.Label(entry_frame, text='Book Title : ')
        title_label.grid(row=1, column=0, sticky=tk.E + tk.W)
        get_title = tk.Entry(entry_frame)
        get_title.grid(row=1, column=1, sticky=tk.E + tk.W)

        author_label = tk.Label(entry_frame, text='Book Author : ')
        author_label.grid(row=2, column=0, sticky=tk.E + tk.W)
        get_author = tk.Entry(entry_frame)
        get_author.grid(row=2, column=1, sticky=tk.E + tk.W)

        qty_label = tk.Label(entry_frame, text='Book Qty : ')
        qty_label.grid(row=3, column=0, sticky=tk.E + tk.W)
        get_qty = tk.Entry(entry_frame)
        get_qty.grid(row=3, column=1, sticky=tk.E + tk.W)

        add_button = tk.Button(entry_frame, text='Add Book',
                               command=lambda: add_book(get_id.get(), get_title.get(), get_author.get(), get_qty.get()))
        add_button.grid(row=4, column=1, sticky=tk.E + tk.W)

        entry_frame.pack(fill='both')

        # Button definition to go back to previous window by calling return_back function
        back_button = tk.Button(entry, text='BACK', command=lambda option=entry: self.return_back(option))
        back_button.pack(side='right', padx=20, pady=20)

    # Function to update the book record. This function provides user to either update certain detail or all of the
    # details in the record. This function receives variable arguments. The first argument is an integer value(0,1 or 2)
    # which defines what information should be displayed. The second argument is the book id that needs to be updated.
    # The third argument is the tkinter window object of previous parent window. The remaining arguments are the book
    # title, author and quantity
    def update_book(self, *args):
        update_window = ''
        parent_window = ''

        mode = args[0]
        if mode == 0:
            # In case of 0 as first argument,the update_window's  parent window is the root window
            update_window = Toplevel(self.root_window)

            # Disabling the parent window and focusing on the current window
            update_window.grab_set()
            update_window.title('Update Window')
            update_window.geometry('550x250')

        elif 0 < mode < 3:
            # In case of 1 or 2 as first argument, the update_windows's parent window is the window passed as an
            # argument to the function update_book.
            parent_window = args[2]
            update_window = Toplevel(parent_window)
            # Disabling the parent window and focusing on the current window
            update_window.grab_set()
            update_window.title('Update Window')
            update_window.geometry('550x250')

        # if len(args) >= 3:
        #     update_window.geometry('550x250')
        #
        # else:
        #     update_window.geometry('300x200')

        update_frame_top = tk.Frame(update_window, padx=10, pady=10)

        id_label = tk.Label(update_frame_top, text='Book ID')
        id_label.grid(row=0, column=0, sticky=tk.W + tk.E)

        get_id = tk.Entry(update_frame_top)
        if len(args) >= 3:
            book_id = args[1]

            # Inserting the book_id received as argument and disabling the entry widget so no modification can be done
            # at this stage
            get_id.insert(0, book_id)
            get_id.config(state='disabled')

        get_id.grid(row=0, column=1, sticky=tk.E + tk.W)

        get_button = tk.Button(update_frame_top, text='Get Book',
                               command=lambda: self.update_book(1, get_id.get(), update_window))
        get_button.grid(row=1, column=1, sticky=tk.E + tk.W)

        update_frame_top.pack(fill='both')

        # This section only gets displayed after the user has clicked the 'Get Book' Button.
        if mode == 1:
            # Defining update_frame_bottom frame to be displayed only if the 1st argument received by the function is 1.
            update_frame_bottom = tk.Frame(update_window)
            book_id = args[1]
            # Defining 4 Entry  widget.
            en = [tk.Entry] * 4  # [tk.Entry for i in range(4)]

            if not self.check_id(book_id):
                messagebox.showinfo(f'Book with {book_id} not found')
                parent_window.destroy()

            else:
                self.cursor.execute(f'SELECT * FROM {self.table_name} WHERE id = ?', (book_id,))

                id_label = tk.Label(update_frame_bottom, text='Book ID')
                id_label.grid(row=0, column=0, sticky=tk.E + tk.W)

                title_label = tk.Label(update_frame_bottom, text='Title')
                title_label.grid(row=0, column=1, sticky=tk.E + tk.W)

                author_label = tk.Label(update_frame_bottom, text='Author')
                author_label.grid(row=0, column=2, sticky=tk.E + tk.W)

                qty_label = tk.Label(update_frame_bottom, text='Quantity')
                qty_label.grid(row=0, column=3, sticky=tk.E + tk.W)

                for i, value in enumerate(self.cursor.fetchone()):
                    en[i] = tk.Entry(update_frame_bottom)
                    en[i].insert(0, value)

                    en[i].grid(row=1, column=i, sticky=tk.E + tk.W)

                update_button = tk.Button(update_frame_bottom, text='Update', command=lambda: self.update_book(
                    2, book_id, update_window, en[1].get(), en[2].get(), en[3].get()))
                update_button.grid(row=2, column=0, sticky=tk.E + tk.W)

                update_frame_bottom.pack(fill='both')

        # This section only gets executed after user enters the 'Update' Button.
        elif mode == 2:
            book_id = args[1]
            parent_window = args[2]
            title = args[3]
            author = args[4]
            qty = args[5]

            update_frame_bottom = tk.Frame(update_window)

            self.cursor.execute(f'''UPDATE {self.table_name} SET Title = ?, Author = ?, Qty = ? WHERE id = ?''',
                                (title, author, qty, book_id))
            self.db.commit()

            self.cursor.execute(f'SELECT * FROM {self.table_name} where id = ?', (book_id,))
            title_label = tk.Label(update_frame_bottom, text='Title')
            title_label.grid(row=0, column=0, sticky=tk.E + tk.W)

            author_label = tk.Label(update_frame_bottom, text='Author')
            author_label.grid(row=0, column=1, sticky=tk.E + tk.W)

            qty_label = tk.Label(update_frame_bottom, text='Quantity')
            qty_label.grid(row=0, column=2, sticky=tk.E + tk.W)

            for i, value in enumerate(self.cursor.fetchone()):

                e = tk.Entry(update_frame_bottom)
                e.insert(0, value)
                e.config(state='disabled')
                e.grid(row=1, column=i, sticky=tk.E + tk.W)

            update_frame_bottom.pack(fill='both')

            messagebox.showinfo('Success', 'Books details Updated')

            # Destroying the current window
            update_window.destroy()
            # Destroying the parent window
            parent_window.destroy()

        # Back button displayed for only mode 0 and 1. When clicked, invokes the return_back function that destroys
        # the current window

        if mode <= 1:

            back_button = tk.Button(update_window, text='BACK',
                                    command=lambda option=update_window: self.return_back(option))
            back_button.pack(side='right', padx=20, pady=20)

    # Function delete the book record. The user is allowed to enter the book id to delete the record from the database.
    def delete_book(self):
        def delete_confirmation(book_id):
            if not self.check_id(book_id):
                messagebox.showinfo('Book Deleted', f'Book with {book_id} not found')

            else:
                self.cursor.execute(f'DELETE FROM {self.table_name} WHERE id = ?', (book_id,))
                self.db.commit()

                messagebox.showinfo('Book Deleted', f'Book with {book_id} id deleted')

        delete_window = Toplevel(self.root_window)
        delete_window.grab_set()

        delete_window.title('Delete Book')
        delete_window.geometry('300x200')

        delete_frame = tk.Frame(delete_window, padx=10, pady=10)

        id_label = tk.Label(delete_frame, text='Book ID ')
        id_label.grid(row=0, column=0, sticky=tk.E + tk.W)

        get_id = tk.Entry(delete_frame)
        get_id.grid(row=0, column=1, sticky=tk.E + tk.W)

        delete_button = tk.Button(delete_frame, text='Delete Book',
                                  command=lambda: delete_confirmation(get_id.get()))
        delete_button.grid(row=1, column=1, sticky=tk.E + tk.W)

        delete_frame.pack(fill='both')

        back_button = tk.Button(delete_window, text='BACK',
                                command=lambda option=delete_window: self.return_back(option))
        back_button.pack(side='right', padx=20, pady=20)

    # Function to search the book records. The function receives multiple arguments where the first argument is an int
    # value, 0 for displaying windows before search and 1 for displaying windows after search. The second argument is
    # the book id to search for. The third argument is the parent window object passed as an argument to the function.

    def search_book(self, *args):

        mode = args[0]

        # if mode is zero create toplevel window with root window as parent window otherwise create the window received
        # as argument as parent window
        if mode == 0:
            search_window = Toplevel(self.root_window)

        else:
            search_window = Toplevel(args[2])

        search_window.grab_set()

        # if the function receives 3 arguments then change the window size to 550x250.
        if len(args) == 3:
            search_window.geometry('550x250')

        else:
            search_window.geometry('300x200')

        search_window.title('Search Book : ')

        search_frame = tk.Frame(search_window, padx=10, pady=10)

        id_label = tk.Label(search_frame, text='Book ID ')
        id_label.grid(row=0, column=0, sticky=tk.E + tk.W)

        get_id = tk.Entry(search_frame)
        get_id.grid(row=0, column=1, sticky=tk.E + tk.W)

        search_btn = tk.Button(search_frame, text='Search',
                               command=lambda: self.search_book(1, get_id.get(), search_window))

        search_btn.grid(row=1, column=1, sticky=tk.E + tk.W)

        search_frame.pack(fill='both', side='top')

        # This section only gets executed after the user hit the search button.
        if mode == 1:
            book_id = args[1]

            get_id.insert(0, book_id)
            get_id.config(state='disabled')

            search_btn.config(state='disabled')

            found_frame = tk.Frame(search_window, padx=20, pady=20)

            if not self.check_id(book_id):
                messagebox.showinfo('Search Result', f'Book with {book_id} id not found')
            else:
                self.cursor.execute(f'SELECT * FROM {self.table_name} WHERE id = ?', (book_id,))

                id_label1 = tk.Label(found_frame, text='Book ID')
                id_label1.grid(row=0, column=0, sticky=tk.E + tk.W)

                title_label = tk.Label(found_frame, text='Title')
                title_label.grid(row=0, column=1, sticky=tk.E + tk.W)

                author_label = tk.Label(found_frame, text='Author')
                author_label.grid(row=0, column=2, sticky=tk.E + tk.W)

                qty_label = tk.Label(found_frame, text='Book Qty')
                qty_label.grid(row=0, column=3, sticky=tk.E + tk.W)

                for i, value in enumerate(self.cursor.fetchone()):
                    en = tk.Entry(found_frame)
                    en.grid(row=1, column=i, sticky=tk.E+tk.W)
                    en.insert(0, value)
                    en.config(state='disabled')

            found_frame.pack(fill='both')

        back_button = tk.Button(search_window, text='BACK',
                                command=lambda option=search_window: self.return_back(option))
        back_button.pack(side='right', padx=20, pady=20)


# Defining the main function
def main():

    database_status = False
    messagebox.showinfo('Welcome window', 'Welcome to bookstore management system \n\t\t Created by Prat Rai')
    if not os.path.exists('./config.txt'):
        # Instantiating the BookStore class with arguments to create and populate the database table
        BookStore(database_status)

    else:
        # Instantiating the BookStore class without the argument
        database_status = True
        BookStore(database_status)


# Entry point to the main program
if __name__ == '__main__':
    main()
