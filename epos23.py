import tkinter as tk
from tkinter import ttk
from tkinter import Toplevel
from tkinter import messagebox
import sqlite3
from editsqlite23 import EditSqlite23
from calculator23 import Calculator23
import os


class Epos23:

    def __init__(self):

        # list that includes the headings to be displayed in tree view.
        self.display_headings = []
        # list to hold types of product to be displayed on button
        self.product_types = []

        # Variable to store the final amount
        self.total_amount = 0

        # list to record the id of the books or item that has been scanned or added.
        self.record_sale = []

        # Getting database name, table's name, table's headings and their data types from the configuration file
        with open('./config.txt', 'r', encoding='utf-8') as file:
            for i, line in enumerate(file):
                if i == 0:
                    self.database_name = (line.replace('\n', '').split(': ')[1])
                elif i == 1:
                    self.table_name = (line.replace('\n', '').split(': ')[1])
                elif i == 2:
                    self.headings = (line.replace('\n', '').split(': ')[1])
                elif i == 3:
                    self.data_types = line.replace('\n', '').split(': ')[1]

        self.sale_window = tk.Tk()
        self.sale_window.title('EPOS Till')

        wd, ht = self.sale_window.winfo_screenwidth(), self.sale_window.winfo_screenheight()
        self.sale_window.geometry(f'{wd}x{ht}')
        frame_width = wd/2

        # Left side Frame definitions
        self.left_frame = tk.Frame(self.sale_window, width=frame_width * 1.1, height=ht)
        self.top_left_frame = tk.Frame(self.left_frame, padx=1, pady=1, height=ht * 0.2)
        self.mid_left_frame = tk.Frame(self.left_frame, padx=1, pady=1, height=ht * 0.6)
        self.bottom_left_frame_east = tk.Frame(self.left_frame, padx=1, pady=1, height=ht * 0.2)
        self.bottom_left_frame_west = tk.Frame(self.left_frame, padx=1, pady=1, height=ht * 0.2)

        # Right side Frame definitions
        self.right_frame = tk.Frame(self.sale_window, width=frame_width * 0.9, height=ht)
        self.top_right_frame = tk.Frame(self.right_frame, padx=1, pady=1, height=ht * 0.5)
        self.bottom_right_frame = tk.Frame(self.right_frame, padx=1, pady=1)

        # Top left frame widgets display
        self.label_book_id = tk.Label(self.top_left_frame, text='Search')
        self.label_book_id.place(x=20, y=20)

        self.entry_get_id = tk.Entry(self.top_left_frame)
        self.entry_get_id.place(x=80, y=20)

        self.btn_add = tk.Button(self.top_left_frame, text='Add to sale',
                                 command=lambda: self.add_item())
        self.btn_add.place(x=220, y=15)

        self.label_total = tk.Label(self.top_left_frame, text='Total')
        self.label_total.place(x=frame_width-220, y=(ht*0.1)-25)

        self.entry_total = tk.Entry(self.top_left_frame)
        self.entry_total.config(state='disabled')
        self.entry_total.place(x=frame_width-180, y=(ht*0.1)-30)

        button_pay = tk.Button(self.top_left_frame, text='Pay',
                               command=lambda: self.pay_amount)
        button_pay.place(x=frame_width-180, y=(ht*0.1)-10)

        # Mid left frame widgets display.

        # Adding a string 'Amount' in the table's heading and splitting it into list. The amount item in the list will
        # represent the total amount in tree view. similarly adding the string called float that correspond to
        # the Amount's data types.

        self.headings += ' Amount'
        self.data_types += ' float'
        self.display_headings = self.headings.split(' ')
        table_data_types = self.data_types.split(' ')

        self.scroll_vertical = tk.Scrollbar(self.mid_left_frame, orient='vertical')
        # self.scroll_horizontal = tk.Scrollbar(self.mid_left_frame, orient='horizontal')

        self.tree = ttk.Treeview(self.mid_left_frame, columns=self.display_headings,
                                 show='headings')

        # Setting heading and column attributes of tree view.
        for i in range(len(self.display_headings)):
            self.tree.heading(self.display_headings[i], text=self.display_headings[i])

            # Checking the datatypes of columns and assigning the width accordingly. Column with Text datatype gets
            # larger width than the columns with integer and float datatypes.
            if table_data_types[i] == 'text':
                self.tree.column(self.display_headings[i], anchor='center', width=int(frame_width * 0.2))
            else:
                self.tree.column(self.display_headings[i], anchor='center', width=int(frame_width * 0.1))

        self.tree.configure(yscrollcommand=self.scroll_vertical.set)
        self.scroll_vertical.configure(command=self.tree.yview)
        # self.scroll_horizontal.configure(command=self.tree.xview)

        # self.scroll_horizontal.pack(side='bottom', fill='x', expand=1, anchor='n')

        self.scroll_vertical.pack(side='right', fill='y', expand=1)
        self.tree.pack(side='left', fill='both', expand=1)

        # Bottom left frame west side widgets display
        menu = ['Total', 'Del', 'Edit', 'CLR']
        for i, option in enumerate(menu):
            button = tk.Button(self.bottom_left_frame_west, text=option, width=10, height=2,
                               command=lambda value=option: self.handle_button_clicked(value))
            button.grid(row=0, column=i, sticky=tk.E+tk.W, padx=5)

        # Bottom left frame east side widgets display
        Calculator23(self.bottom_left_frame_east)

        # Top right frame and top left frame widgets

        get_product_types = []
        db = sqlite3.connect(self.database_name)
        cursor = db.cursor()

        cursor.execute(f'SELECT Product_Type from {self.table_name}')

        for row in cursor.fetchall():
            for value in row:
                get_product_types.append(value)

        db.close()
        # Removing duplicates product types from the list and sorting in ascending order
        get_product_types = sorted([*set(get_product_types)])

        # calling function to display product types in top right frame.
        self.display_product_types(0, get_product_types)

        self.top_left_frame.pack(side='top', fill='both', expand=1)
        self.mid_left_frame.pack(side='top', fill='both', expand=1)
        self.bottom_left_frame_west.pack(side='left', expand=1, anchor='nw', pady=20)
        self.bottom_left_frame_east.pack(side='right', expand=1, anchor='ne', padx=10, pady=50)

        self.top_right_frame.pack(side='top', fill='both', expand=1, anchor='n')
        self.bottom_right_frame.pack(side='bottom', fill='both', expand=1, anchor='n')

        self.left_frame.pack(side='left', fill='y', expand=1, anchor='w')
        self.right_frame.pack(side='right', fill='y', expand=1)
        # self.left_frame.grid(row=0, column=0, sticky=tk.NSEW)

        self.sale_window.mainloop()

    # def append(self, last):
    #     self.shop_list.insert('end', str(last))
    def pay_amount(self):
        print('To pay : ', self.entry_total.get())
        print('Paying functionality under construction')

    def add_item(self):

        # Boolean to check whether to add new item to tree view or edit the already existing item in tree view
        add = True

        data = []  # Declaring list variable to store each item detail to be written to the tree view.

        db = sqlite3.connect('./' + self.database_name)
        cursor = db.cursor()

        # creating and object of class EditSqlite23. The last element of the list self.display_headings is also not
        # passed using list slicing i.e. 'amount' as it does not exist in the database.
        edit = EditSqlite23(cursor, self.table_name, self.display_headings[:-1], self.entry_get_id.get())
        # Getting the result of search in a list.
        get_item_details = edit.search()

        if get_item_details is None:
            messagebox.showinfo('Not Found', 'Item not found')

        else:

            # Adding the value of first field of the table(ie book code) to a list record_sale to track the
            # quantity of the product(book) sold.
            self.record_sale.append(get_item_details[0])

            # Creating an item's details to be displayed on tree view ie name,qty,price etc
            # for row in get_item_details:
            for i, value in enumerate(get_item_details):  # getting value in each column in particular row
                # Getting the product(book) code.
                if i == 0:
                    product_code = value

                # if the query's result's column is Qty, calculate item's quantity up until now by counting
                # item's first field's value in recorded sale.
                if self.display_headings[i] == 'Qty' or self.display_headings[i] == 'Quantity':
                    total_qty = int(self.record_sale.count(product_code))
                    data.append(total_qty)

                # if the query's result's column is Price, store the price in get_price and append to data
                elif self.display_headings[i] == 'Price':

                    get_price = float(value)
                    data.append(get_price)
                    self.total_amount += get_price
                    self.entry_total.config(state='normal')
                    self.entry_total.delete(0, 'end')
                    self.entry_total.insert(0, str(round(self.total_amount, 2)))
                    self.entry_total.config(state='disabled')
                else:
                    data.append(value)

            for iid_name in self.tree.get_children():
                # checking if the item added is already in the tree view by comparing the first field's value and only
                # changing the amount and quantity in already existing entry

                if self.tree.item(iid_name)['values'][0] == get_item_details[0]:
                    position = self.tree.index(iid_name)
                    data.append(total_qty * get_price)
                    self.tree.delete(iid_name)
                    self.tree.insert('', index=position, values=data)
                    add = False
                    break

            # if id of the item is not in the tree view then inserting new entry with all details in the tree view.
            if add:
                data.append(get_price * total_qty)
                self.tree.insert('', 'end', values=data)
            db.commit()
            db.close()

    def delete_item(self):
        self.tree.delete(self.tree.selection()[0])

    def display_product_types(self, count, get_product_types):
        for i in range(3):
            for j in range(3):
                if count < len(get_product_types):
                    button = tk.Button(self.top_right_frame, text=get_product_types[count], height=2, width=10,
                                       command=lambda value=count:
                                       self.handle_product_type_clicked(get_product_types[value]))
                    button.grid(row=i, column=j, sticky=tk.E + tk.W, padx=30, pady=20)
                    count += 1
                else:
                    
                    break
        if count < len(get_product_types):
            button_next = tk.Button(self.top_right_frame, text='Next',
                                    command=lambda: self.display_product_types(count, get_product_types))
            button_next.grid(row=3, column=2, sticky=tk.NSEW, padx=10, pady=10)

    def handle_product_type_clicked(self, product_type):
        get_products_name = []  # list to add the title of the items
        # index = 0  # variable to store the count of the books
        db = sqlite3.connect('./' + self.database_name)
        cursor = db.cursor()

        edit = EditSqlite23(cursor, self.table_name, self.display_headings[:-1], product_type)

        # Getting all items of item_type
        get_all_products = edit.search()

        if get_all_products is not None:
            for i, value in enumerate(get_all_products):
                # Only get the column value from the row whose index matches the index of 'Title' heading.
                if self.display_headings[i] == 'Product_Name':
                    get_products_name.append(value)
        else:
            messagebox.showinfo('Error', 'Product not found')

        db.commit()
        db.close()
        # calling display_books function with initial index of 0
        self.display_products(0, get_products_name, product_type)

    def display_products(self, count, get_products_name, product_type):

        # Deleting all widgets in bottom_right_frame before displaying new widgets
        for widgets in self.bottom_right_frame.winfo_children():
            widgets.destroy()

        label = tk.Label(self.bottom_right_frame, text=product_type, font=('Arial', 18), anchor='n')
        label.grid(row=0, column=0, sticky=tk.E+tk.W)

        # Displaying products in the 3x3 row column format.
        for i in range(3):
            for j in range(3):
                if count <= len(get_products_name) - 1:

                    button = tk.Button(self.bottom_right_frame, wraplength=80, text=get_products_name[count], width=12, height=2)
                    button.configure(command=lambda value=count: self.add_button_item(get_products_name[value]))
                    button.grid(row=i+1, column=j, sticky=tk.NSEW, padx=30, pady=15)
                    count += 1

                else:
                    break

        # Checking if there is any more books to be displayed
        if count < len(get_products_name):
            button_next = tk.Button(self.bottom_right_frame, text='Next',
                                    command=lambda: self.display_products(count, get_products_name, product_type))
            button_next.grid(row=5, column=2, sticky=tk.NSEW, padx=10, pady=10)

    def add_button_item(self, get_each_item):
        db = sqlite3.connect('./' + self.database_name)
        cursor = db.cursor()

        edit = EditSqlite23(cursor, self.table_name, self.display_headings[:-1], get_each_item)
        # Getting the result of search
        get_item_details = edit.search()

        if get_item_details is None:
            messagebox.showinfo('Not Found', 'Item not found')

        else:
            # Getting the first field's value of the item details
            get_first_field_value = get_item_details[0]

            self.entry_get_id.delete(0, 'end')
            self.entry_get_id.insert(0, get_first_field_value)
            self.add_item()
            db.commit()
            db.close()

    def handle_button_clicked(self, choice):

        if choice == 'Total':
            self.get_total()
        elif choice == 'CLR':
            self.entry_total.config(state='normal')
            self.entry_total.delete(0, 'end')

        elif choice == 'Del':
            # Getting the iid of selected item and thus getting the last value of selected item which is the amount
            iid_name = self.tree.selection()[0]
            amount = float(self.tree.item(iid_name)['values'][-1])

            # Deleting the item
            self.tree.delete(iid_name)

            self.entry_total.config(state='normal')
            new_amount = float(self.entry_total.get()) - amount

            self.entry_total.delete(0, 'end')
            self.entry_total.insert(0, str(new_amount))
            self.entry_total.config(state='disabled')

        elif choice == 'Edit':

            if self.tree.selection()[0] is None:
                pass

            else:
                edit_window = Toplevel(self.sale_window)
                edit_window.grab_set()

                edit_window.geometry('300x200')
                edit_window.title('Edit Quantity')

                edit_frame = tk.Frame(edit_window)

                label = tk.Label(edit_frame, text='Qty')
                label.grid(row=0, column=0, sticky=tk.E+tk.W, padx=10, pady=10)

                entry = tk.Entry(edit_frame)
                entry.grid(row=0, column=1, sticky=tk.E+tk.W, padx=10, pady=10)

                button = tk.Button(edit_frame, text='Update',
                                   command=lambda: self.update(entry.get(), edit_window))
                button.grid(row=1, column=0, sticky=tk.E+tk.W, padx=10, pady=10)

                edit_frame.pack(side='top', fill='both', padx=5, pady=5)

    def get_total(self):

        total = 0
        for iid_name in self.tree.get_children():
            total += float(self.tree.item(iid_name)['values'][-1])

        self.entry_total.config(state='normal')
        self.entry_total.delete(0, 'end')
        self.entry_total.insert(0, str(total))
        self.entry_total.config(state='disabled')

    def update(self, update_qty, window):
        new_values = []
        # Getting the iid of selected item and thus getting the last value of selected item which is the amount
        iid_name = self.tree.selection()[0]
        # Getting the position of a selected item with the help of iid_name
        position = self.tree.index(iid_name)

        # Creating new values for item from existing tree view item except changing the quantity
        for i, value in enumerate(self.tree.item(iid_name)['values']):
            # if the item's value corresponds to Qty column then append the updated quantity to new values
            if self.display_headings[i] == 'Qty':
                new_values.append(update_qty)
            # If price needs to be updated then update the new price. work pending in future
            elif self.display_headings[i] == 'Price':
                price = float(self.tree.item(iid_name)['values'][i])
                new_values.append(price)
            # Appending new amount to the item
            elif self.display_headings[i] == 'Amount':
                new_values.append(int(update_qty) * price)

            else:
                new_values.append(self.tree.item(iid_name)['values'][i])

        self.tree.delete(iid_name)
        self.tree.insert('', position, values=new_values)
        self.get_total()

        window.destroy()

# e = Epos23()
