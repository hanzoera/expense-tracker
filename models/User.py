from config.DatabaseConnection import DatabaseConnection

class InnerUser:
    def registerUser(self, username, password):
        # create an instance of the database connection handler class
        database = DatabaseConnection()

        # establish session through the register function
        database_conn = database.connect()

        # cursor object to run and execute SQL queries
        cursor = database_conn.cursor()



        

        