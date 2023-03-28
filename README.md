# Bookstore-Management-System

## GUI based program to manage bookstore written in python

A graphical user interface-based project written in python using tkinter, sqlite3 and openpyxl modules. This program allows the user to interact with the GUI to manage bookstore. It allows user to add new book details, update some or all of the book details, delete and search book details by book’s id and view all the records in the database. This project also features login function to authorize user. 

When the program runs for the first time, it allows us to create the user with administrator privilege who can create other users of different groups. It allows user to import data from excel file to be loaded into the sqlite database and also allow us to download the database data into an excel file. Also the user is allowed to create database and table with their desired name to store book details. However the table inside the database for storing users and their credentials are pre-assigned, named as 'users'. So the database with user define name consists of two table, one for storing users and other for storing book details.

This Project includes 3 python files <u>bookStoreGui.py</u> which is the main file as a start point for the program, <u>access23.py</u> which provides authentication functionality and <u>excel23.py</u> that provides functionality to manipulate excel files. 

This project is an upgrade of my console based capstone project written as a part of bootcamp task.
