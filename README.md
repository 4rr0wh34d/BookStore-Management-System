# Bookstore-Management-System

## GUI based program to manage bookstore written in python

A graphical user interface-based project written in python using tkinter, sqlite3 and openpyxl modules. This program allows the user to interact with the GUI to manage bookstore. It allows user to add new book details, update some or all of the book details, delete and search book details by book’s id and view all the records in the database. This project also features login function to authorize user. 

When the program runs for the first time, it allows us to create the user with administrator privilege who can create other users of different groups. It also allows users to create database with their desired name. These database would include two tables, one for storing the users and their credentials and would be pre-assigned, named as 'users'. The other table would be used to store details of the products i.e. books and users are free to name the table and also define the number of fields and their name. However the users should include 5 fields as compulsory for the program to run correctly. The fields that must be included are Product_Code, Product_Name, Product_Type, Price and Quantity. 

It also allows user to import data from excel file to be loaded into the sqlite database and also allow us to download the database data into an excel file. 

This Project includes 6 python scripts <ins>bookStoreGui.py</ins> which is the main file and the starting point for the program, <ins>access23.py</ins> which provides authentication functionality, <ins>excel23.py</ins> that provides functionality to read and write to Excel workbooks, <ins>epos23.py</ins> that provides users with the point of sale interface for transaction, <ins>editsqlite23.py</ins> for database query and lastly <ins>calculator23.py</ins> to provide calculator functionality to the users.

This project is an upgrade of my console based capstone project written as a part of bootcamp task.
