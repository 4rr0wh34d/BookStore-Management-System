# This program utilizes and demonstrates the use of sqlite3 database in python. It allows user to create a database with
# a table and allow them to add, delete, update and search data into the table. It also uses custom module called
# excel23 to import and export Excel files.

# Import statements
import sqlite3
import os.path
import tkinter as tk
from tkinter import ttk
from tkinter import Toplevel
from tkinter import messagebox
from tkinter import filedialog as fd
from editsqlite23 import *
# import epos23
from epos23 import Epos23
# from tkinter import
import time

# importing custom python file called excel23 to import or export Excel files
from excel23 import *

# importing custom python file to carry out authentication
from access23 import Access23  # as Access


# Class definition with various function and attributes
class BookStore:

    # Defining class constructor which receives a boolean value which indicates if the database configuration file
    # already exist or not (or if the program is running for the first time)
    # depending upon which the if else statement is executed
    def __init__(self, config_file_exist, config_file):

        # instance variables
        self.config_file = config_file
        self.table_name = ''
        self.database_name = ''
        self.filename = ''
        self.headings = ''
        self.width = 0
        self.height = 0
        # Defining boolean variable to check if the database and table has been created or already exist.
        self.database_table_created = False

        # If the config file does not exist then create a config.txt file, create new user, create a database and table
        # and record the info in the config file.
        if not config_file_exist:

            # Creating an object of class Access23 and calling create_user function to create new user. If the user is
            # created, the create_user function returns True and the main menu window is displayed.
            access = Access23()
            access.create_user(f'{self.config_file}')

            # self.database_name = access.db_name

            with open('config.txt', 'r', encoding='utf-8') as file:

                for i, line in enumerate(file):
                    if i == 0:
                        self.database_name = line.replace('\n', '').split(': ')[1]

            try:
                self.db = sqlite3.connect(self.database_name)
                self.cursor = self.db.cursor()

                # Defining table window and frame
                self.create_table_window = tk.Tk()

                self.width, self.height = self.create_table_window.winfo_screenwidth(), \
                    self.create_table_window.winfo_screenheight()

                self.create_table_window.title('Creating Table')
                self.create_table_window.geometry(f'{self.width//3}x{self.height//3}+{self.width//3}+{self.height//3}')

                # calling the create_table_details function to collect details of table to create it.
                self.get_table_details()

                self.create_table_window.mainloop()

            except Exception as e:
                messagebox.showinfo('Database Error', f'{e}')

        # If the config file exist, then extract information from database to check the user credentials inputted by
        # the user and if it matches give access to the main menu window.
        else:

            # Calling the check_user function of class Access23 to check credentials against user inputs. If the check
            # is passed then get the database name from the config file and connect to the database. If connection
            # is successful program flow enters the main menu window.
            access = Access23()
            access.check_user(f'{self.config_file}')

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

        # Checking if the database and table already exist or has been created, then give access to the main menu window

        if self.database_table_created:
            # Creating a root window
            self.root_window = tk.Tk()
            self.root_window.title("BookStore management system")
            self.width, self.height = self.root_window.winfo_screenwidth(), self.root_window.winfo_screenheight()
            self.root_window.geometry(f'{self.width//2}x{self.height//2}+{self.width//4}+{self.height//4}')

            # Creating a menubar
            self.menubar = tk.Menu(self.root_window)

            # Calling the main user menu
            self.user_menu()

    # Function to start creating database
    def get_table_details(self):

        tb_frame = tk.Frame(self.create_table_window, padx=10, pady=10)

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

        parent_window = self.create_table_window

        # Creating a child window 'fields_window' whose parent window is 'tb_window'
        fields_window = Toplevel(parent_window)

        # Setting window title and size
        fields_window.title('Creating table')
        fields_window.geometry(f'{self.width//3}x{self.height//3}+{self.width//3}+{self.height//3}')

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
        # Declaring empty string str_headings_type to store table's heading and their type
        str_headings_types = ''

        # Declaring empty string to store table's field heading and their data types.
        str_headings = ''
        str_data_types = ''

        size = len(fields)

        # Creating a string str_headings_types with all the table's fields' headings and type to create a query to
        # create a new table. String str_headings is created to store table's heading to write to a config
        # file for future use while recreating a new Excel file with all the database records.
        for i, field in enumerate(fields):
            # checking to see if it is the last element of list 'fields' and skip the comma in str_headings_types
            # and space in case of str_headings
            if i == size - 1:
                str_headings_types += field
                str_headings += field.split(' ')[0]
                str_data_types += field.split(' ')[1]
            else:
                str_headings_types += field + ', '
                str_headings += field.split(' ')[0] + ' '
                str_data_types += field.split(' ')[1] + ' '

        # creating a query with table name and the fields
        query = f'CREATE TABLE IF NOT EXISTS {self.table_name}({str_headings_types})'
        self.cursor.execute(query)
        self.db.commit()

        # self.db.close()

        with open('config.txt', 'a+', encoding='utf-8') as filehandle:
            filehandle.write('Table Name: ' + self.table_name + '\n' + 'Headings: ' + str_headings + '\n'
                             + 'Types: ' + str_data_types)

        # Assigning instance variable self.headings with the table heading to be passed into Excel23 class
        # even when the program is running for the first time.
        self.headings = str_headings
        # Since the table creation was successful set table_created variable to True
        self.database_table_created = True

        get_window.destroy()
        self.create_table_window.destroy()

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

        button_epos = tk.Button(root_frame, text="Epos/Till window", command=lambda: Epos23())
        button_epos.grid(row=1, column=0, sticky=tk.E + tk.W)

        add_button = tk.Button(root_frame, text="Add Book", command=self.new_entry)
        add_button.grid(row=2, column=0, sticky=tk.E + tk.W)

        book_update = tk.Button(root_frame, text="Update Book", command=lambda: self.update_book(0))
        book_update.grid(row=3, column=0, sticky=tk.E + tk.W)

        book_delete = tk.Button(root_frame, text="Delete Book", command=self.delete_book)
        book_delete.grid(row=4, column=0, sticky=tk.E + tk.W)

        book_search = tk.Button(root_frame, text="Search Book", command=lambda: self.search_book(0))
        book_search.grid(row=5, column=0, sticky=tk.E + tk.W)

        book_view = tk.Button(root_frame, text="View books", command=lambda: self.view_all())
        book_view.grid(row=6, column=0, sticky=tk.E + tk.W)

        root_frame.pack(expand=1, anchor='center')

        self.root_window.config(menu=self.menubar)
        self.root_window.protocol("WM_DELETE_WINDOW", self.confirm_close)
        # self.root_window.eval('tk::PlaceWindow . top')
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
                print(self.filename)
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
        view_frame = tk.Frame(view_window, padx=10, pady=10)

        # Getting table headings from the config file
        with open('./config.txt', 'r', encoding='utf-8') as file:
            for i, line in enumerate(file):
                if i == 2:
                    heading = line.replace('\n', '').split(': ')[1]

        # Converting headings list to tuples
        table_heading = tuple(heading.split(' '))

        scrollbar_yaxis = tk.Scrollbar(view_frame, orient='vertical')
        tree = ttk.Treeview(view_frame, columns=table_heading, show='headings')

        for size in range(len(table_heading)):
            tree.column(table_heading[size], anchor='center')
            tree.heading(table_heading[size], text=table_heading[size])

        tree.configure(yscrollcommand=scrollbar_yaxis)
        scrollbar_yaxis.configure(command=tree.yview)

        scrollbar_yaxis.pack(side='right', fill='y', anchor='w', expand=1)
        tree.pack(side='left', fill='both', expand=1)

        for row in self.cursor:
            tree.insert('', 'end', values=row)

        '''
        for i, row in enumerate(self.cursor):
            for j, value in enumerate(row):
                en = tk.Entry(view_frame)

                en.grid(row=i + 1, column=j, sticky=tk.E + tk.W)
                en.insert(0, value)
                en.config(state='disabled')
        '''

        view_frame.pack(fill='both', side='top')

        back_button = tk.Button(view_window, text='BACK',
                                command=lambda option=view_window: self.return_back(option))
        back_button.pack(side='bottom', padx=20, pady=20)
        self.root_window.eval(f'tk::PlaceWindow {str(view_window)} center')

    # Function to check if the record with certain Book id exists.
    def check_code(self, get_code):
        self.cursor.execute(f'SELECT * FROM {self.table_name} WHERE Product_Code = ?', (get_code,))
        if self.cursor.fetchone() is None:
            return False
        else:
            return True

    # Function to enter new book record. User are allowed to enter details of new book that need to be added to the
    # database
    def new_entry(self):

        # Getting the size of the fields using table heading
        total_fields = len(self.headings)

        # Declaring list of Entry
        entry = [tk.Entry for i in range(total_fields)]

        # Function to add new book to database

        def add_item(get_values):
            # Declaring variable to store number of '?' which represent the field values
            total_query = ''

            for num in range(len(get_values)):
                # checking if it is the last field
                if num == len(get_values) - 1:
                    total_query += '?'
                else:
                    total_query += '?, '

            self.cursor.execute(f'INSERT INTO {self.table_name} VALUES({total_query})', tuple(get_values))
            self.db.commit()
            messagebox.showinfo('New Entry', 'New Record have been entered')

            for num in range(len(get_values)):
                entry[num].delete(0, 'end')

        new_entry_window = Toplevel(self.root_window)
        new_entry_window .grab_set()

        new_entry_window.title('New book Entry')
        new_entry_window.geometry('400x250')

        new_entry_frame = tk.Frame(new_entry_window, padx=10, pady=10)

        for i, value in enumerate(self.headings):
            label = tk.Label(new_entry_frame, text=value)
            label.grid(row=i, column=0, sticky=tk.NSEW)
            entry[i] = tk.Entry(new_entry_frame)
            entry[i].grid(row=i, column=1, sticky=tk.NSEW)

        add_button = tk.Button(new_entry_frame, text='Add item',
                               command=lambda: add_item([entry[j].get() for j in range(total_fields)]))
        add_button.grid(row=len(self.headings), column=1, sticky=tk.E + tk.W)

        new_entry_frame.pack(fill='both', side='top')

        # Button definition to go back to previous window by calling return_back function
        back_button = tk.Button(new_entry_window, text='BACK',
                                command=lambda option=new_entry_window: self.return_back(option))
        back_button.pack(side='right', padx=20, pady=20)

        self.root_window.eval(f'tk::PlaceWindow {str(new_entry_window)} center')

    # Function to update the book record. This function provides user to either update certain detail or all of the
    # details in the record. This function receives variable arguments. The first argument is an integer value(0,1 or 2)
    # which defines what widgets should be displayed. The second argument is the book id that needs to be updated.
    # The third argument is the tkinter window object of previous parent window. The remaining arguments are the book
    # title, author and quantity
    def update_book(self, *args):

        get_field_heading =  ''
        mode = args[0]
        if mode == 0:
            # In case of 0 as first argument,the update_window's  parent window is the root window
            update_window = Toplevel(self.root_window)

            # Disabling the parent window and focusing on the current window
            update_window.grab_set()
            update_window.title('Update Window')
            update_window.geometry(
                f'{self.width//3}x{self.height//4}+{self.width//3 }+{self.height//3}')

        elif 0 < mode < 3:
            # In case of 1 or 2 as first argument, the update_windows's parent window is the window passed as an
            # argument to the function update_book.
            parent_window = args[2]
            update_window = Toplevel(parent_window)
            # Disabling the parent window and focusing on the current window
            update_window.grab_set()
            update_window.title('Update Window')
            update_window.geometry(
                f'{self.width//2}x{self.height//3}+{self.width//4}+{self.height//3}')

        update_frame_top = tk.Frame(update_window, padx=10, pady=10)

        label_get_product = tk.Label(update_frame_top, text='Enter value')
        label_get_product.grid(row=0, column=0, sticky=tk.W + tk.E)

        get_search_value = tk.Entry(update_frame_top)
        if len(args) > 1:
            search_value = args[1]

            # Inserting the book_id received as argument and disabling the entry widget so no modification can be done
            # at this stage
            get_search_value.insert(0, search_value)
            get_search_value.config(state='disabled')

        get_search_value.grid(row=0, column=1, sticky=tk.E + tk.W)

        get_button = tk.Button(update_frame_top, text='Search',
                               command=lambda: self.update_book(1, get_search_value.get(), update_window))
        get_button.grid(row=1, column=1, sticky=tk.E + tk.W)

        update_frame_top.pack(fill='both')

        # This section only gets displayed after the user has clicked the 'Get Book' Button.
        if mode == 1:
            # Defining update_frame_bottom frame to be displayed only if the 1st argument received by the function is 1.
            update_frame_bottom = tk.Frame(update_window)
            search_value = args[1]
            # Defining Entry  widget of same size as the heading.
            en = [tk.Entry] * len(self.headings)  # [tk.Entry for i in range(len(self.heading)]

            search = EditSqlite23(self.cursor, self.table_name, self.headings, search_value)
            search_result = search.search()

            if search_result is None:
                messagebox.showinfo(f'The product does not exist')
                update_window.destroy()
                parent_window.destroy()

            # if not self.check_id(book_id):
            #     messagebox.showinfo(f'Book with {book_id} not found')
            #     parent_window.destroy()

            else:
                # self.cursor.execute(f'SELECT * FROM {self.table_name} WHERE id = ?', (book_id,))

                for i, heading in enumerate(self.headings):
                    label = tk.Label(update_frame_bottom, text=heading)
                    label.grid(row=0, column=i, sticky=tk.E + tk.W)

                # for i, value in enumerate(self.cursor.fetchone()):

                for i, value in enumerate(search_result):
                    # Getting the book code from the first column of the table
                    if i == 0:
                        book_code = value
                    en[i] = tk.Entry(update_frame_bottom)
                    en[i].insert(0, value)
                    en[i].grid(row=1, column=i, sticky=tk.E + tk.W)

                    # In the case of first entry field or book id in our case we configure its state disabled so no
                    # editing can be done.
                    if i == 0:
                        en[i].config(state='disabled')

                update_button = tk.Button(update_frame_bottom, text='Update', command=lambda: self.update_book(
                    2, book_code, update_window, [en[j].get() for j in range(0, len(self.headings))]))
                update_button.grid(row=2, column=0, sticky=tk.E + tk.W)

                update_frame_bottom.pack(fill='both')

        # This section only gets executed after user enters the 'Update' Button.
        elif mode == 2:
            # Declaring empty string to store the query to the database
            query_string = ''
            book_code = args[1]

            # Getting the values to update
            values = args[3]

            # Rotating the list anti-clockwise by 1 step, i.e. moving book code to the end.
            new_values = values[1:] + values[:1]
            update_frame_bottom = tk.Frame(update_window)

            # Creating a query by skipping the id string
            for num, heading in enumerate(self.headings):
                # Skipping the first value ie Book code in the query_string
                if num == 0:
                    pass
                # if heading is the last value then skip the comma at the end
                elif num == (len(self.headings) - 1):
                    query_string += heading + ' = ?'
                else:
                    query_string += heading + ' = ?, '
            self.cursor.execute(f'''UPDATE {self.table_name} SET {query_string} WHERE Product_Code = ?''',
                                tuple(new_values))
            # self.cursor.execute(f'''UPDATE {self.table_name} SET Title = ?, Author = ?, Qty = ? WHERE id = ?''',
            #                     (title, author, qty, book_id))
            self.db.commit()

            self.cursor.execute(f'SELECT * FROM {self.table_name} where Product_code = ?', (book_code,))

            for i, heading in enumerate(self.headings):
                label = tk.Label(update_frame_bottom, text=heading)
                label.grid(row=0, column=i, sticky=tk.E + tk.W)

            for i, value in enumerate(self.cursor.fetchone()):

                e = tk.Entry(update_frame_bottom)
                e.insert(0, value)
                e.config(state='disabled')
                e.grid(row=1, column=i, sticky=tk.E + tk.W)

            update_frame_bottom.pack(fill='both')

            label = tk.Label(update_window, text='Database updated', font=('Arial', 18))
            label.pack(side='left', padx=10, pady=10)
        # Back button displayed for only mode 0 and 1. When clicked, invokes the return_back function that destroys
        # the current window

        back_button = tk.Button(update_window, text='BACK',
                                command=lambda option=update_window: self.return_back(option))
        back_button.pack(side='right', padx=10, pady=10)

    # Function delete the book record. The user is allowed to enter the book id to delete the record from the database.
    def delete_book(self):
        def delete_confirmation(book_code):
            if not self.check_code(book_code):
                messagebox.showinfo('Error Deleting book', f'Book with {book_code} not found')

            else:
                self.cursor.execute(f'DELETE FROM {self.table_name} WHERE Product_Code= ?', (book_code,))
                self.db.commit()

                messagebox.showinfo('Book Deleted', f'Book with {book_code} code deleted')

        delete_window = Toplevel(self.root_window)
        delete_window.grab_set()

        delete_window.title('Delete Book')
        delete_window.geometry('300x200')

        delete_frame = tk.Frame(delete_window, padx=10, pady=10)

        id_label = tk.Label(delete_frame, text='Book Code ')
        id_label.grid(row=0, column=0, sticky=tk.E + tk.W)

        get_code = tk.Entry(delete_frame)
        get_code.grid(row=0, column=1, sticky=tk.E + tk.W)

        delete_button = tk.Button(delete_frame, text='Delete',
                                  command=lambda: delete_confirmation(get_code.get()))
        delete_button.grid(row=1, column=1, sticky=tk.E + tk.W)

        delete_frame.pack(fill='both')

        back_button = tk.Button(delete_window, text='BACK',
                                command=lambda option=delete_window: self.return_back(option))
        back_button.pack(side='right', padx=20, pady=20)

        self.root_window.eval(f'tk::PlaceWindow {str(delete_window)} center')
    # Function to search the book records. The function receives multiple arguments where the first argument is an int
    # value, 0 for displaying windows before search and 1 for displaying windows after search. The second argument is
    # the book id to search for. The third argument is the parent window object passed as an argument to the function.

    def search_book(self, *args):

        mode = args[0]

        # if mode is zero create toplevel window with root window as parent window otherwise create the window received
        # as argument as parent window
        if mode == 0:
            search_window = Toplevel(self.root_window)

        elif mode == 1:
            search_window = Toplevel(args[2])

        search_window.grab_set()

        if len(args) == 3:
            search_window.geometry(f'{self.width//3}x{self.height//3}+{self.width//3}+{self.height//3}')

        else:
            search_window.geometry(f'{self.width//4}x{self.height//4}+{self.width//3}+{self.height//3}')

        search_window.title('Search Book : ')

        search_frame = tk.Frame(search_window, padx=10, pady=10)

        id_label = tk.Label(search_frame, text='Book Code ')
        id_label.grid(row=0, column=0, sticky=tk.E + tk.W)

        get_code = tk.Entry(search_frame)
        get_code.grid(row=0, column=1, sticky=tk.E + tk.W)

        search_btn = tk.Button(search_frame, text='Search',
                               command=lambda: self.search_book(1, get_code.get(), search_window))

        search_btn.grid(row=1, column=1, sticky=tk.E + tk.W)

        search_frame.pack(fill='both', side='top')

        # This section only gets executed after the user hit the search button.
        if mode == 1:
            book_code = args[1]

            get_code.insert(0, book_code)
            get_code.config(state='disabled')

            search_btn.config(state='disabled')

            found_frame = tk.Frame(search_window, padx=20, pady=20)

            if not self.check_code(book_code):
                messagebox.showinfo('Search Result', f'Book with {book_code} id not found')
            else:
                self.cursor.execute(f'SELECT * FROM {self.table_name} WHERE Product_Code = ?', (book_code,))

            for i, heading in enumerate(self.headings):
                label = tk.Label(found_frame, text=heading)
                label.grid(row=0, column=i, sticky=tk.E + tk.W)

            for i, value in enumerate(self.cursor.fetchone()):
                en = tk.Entry(found_frame)
                en.grid(row=1, column=i, sticky=tk.E+tk.W)
                en.insert(0, value)
                en.config(state='disabled')

            found_frame.pack(fill='both')

        back_button = tk.Button(search_window, text='BACK',
                                command=lambda option=search_window: self.return_back(option))
        back_button.pack(side='right', padx=20, pady=20)

        self.root_window.eval(f'tk::PlaceWindow {str(search_window)} center')


# Defining the main function
def main():

    database_status = False
    messagebox.showinfo('Welcome window', 'Welcome to bookstore management system \n\t\t Created by Prat Rai')
    config_file = 'config.txt'
    if not os.path.exists(config_file):
        # Instantiating the BookStore class with arguments to create and populate the database table
        BookStore(database_status, config_file)

    else:
        # Instantiating the BookStore class without the argument
        database_status = True
        BookStore(database_status, config_file)


# Entry point to the main program
if __name__ == '__main__':
    main()
