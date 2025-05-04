import MySQLdb

# This class handles connection to the MySQL database.
# It is used by other classes (like InnerUser in models/user.py)
# to establish a reusable and consistent connection to the database.
# Any othe class that requires interaction with the database can import and use the class.

class DatabaseConnection:
    def __init__(self):
        # store the active connection object
        self.connection = None
        # configuration for connecting to the MySQL database
        self.config = {
            'host' : 'localhost',
            'user' : 'root',
            'passwd' : '',
            'db' : 'expense_tracker',
        }

    def connect(self):
        try:
            # check if connection already exists
            if self.connection: 
                print("Closing previous session...")
                self.close()

            print("Creating new session...")
            self.connection = MySQLdb.connect(**self.config)

            # check if connection with the database is open
            if self.connection.open:
                print("Database connection established successfully.")
                self.connection.autocommit(True)
                return self.connection
            else:
                print("Failed to establish connection to the database.")
                return None
        
        except MySQLdb.Error as error:
            # detailed SQL error message
            print(f"MySQLdb Error: {error}")
            print(f"Error Code: {error.args[0]}")
            print(f"Message: {error.args[1]}")
            return None

    def close(self):
        if self.connection and self.connection.open:
            self.connection.close()
        else:
            print("There is no connection to close.")