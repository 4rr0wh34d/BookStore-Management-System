import sqlite3


class EditSqlite23:

    # Defining constructor that takes in the connection handle, table_name, table heading and value to search for.
    def __init__(self, connection, table_name, table_heading, search_value):
        self.connection = connection
        self.table_name = table_name
        self.table_heading = table_heading
        self.search_value = search_value
        self.search_field = ''

    def search(self):
        # looping through each field's heading in the table to determine the field of the value that needs to
        # be searched
        for heading in self.table_heading:
            # Search all field in the table

            self.connection.execute(f'SELECT * FROM {self.table_name} where {heading}=?', (self.search_value,))

            # If we get something from the sql query then we can assume we get the field we need to search.
            if not self.connection.fetchone() is None:
                self.search_field = heading
                break
            else:
                self.search_field = ''
                continue

        if self.search_field == '':
            return None

        else:
            self.connection.execute(f'SELECT * FROM {self.table_name} where {self.search_field}=?', (self.search_value,))

            value = self.connection.fetchone()
            return value
