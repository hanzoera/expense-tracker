import MySQLdb

class Connection:

    def __init__(self):
        self.connection = None
        self.config = {
            'host' : 'localhost',
            'user' : 'root',
            'passwd' : '',
            'db' : 'expense_tracker',
        }

    def connect(self):
        try:
            if self.connection:
                print("Closing previous session...")
                self.close()

            print("Creating new session...")
            self.connection = MySQLdb.connect(**self.config)

            if self.connection.open:
                print("Database successfully connected...")
                self.connection.autocommit(True)
                return self.connection
            else:
                print("none//")
                return None
        
        except MySQLdb.Error as error:
            print(f"MySQLdb Error: {error}")
            print(f"Error Code: {error.args[0]}")
            print(f"Message: {error.args[1]}")

    