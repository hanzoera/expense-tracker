from config.DatabaseConnection import DatabaseConnection

# This class represents a user in the system .
# It handles user-related data and operations that interacts with the database.

class InnerUser:

    # Attempts to register a new user and returns a boolean value
    # to evaluate whether the registration was successful or not.
    # `is_registration_successful` var from [controllers/RegisterApp.py]
    # will inherit the value to display the result.
    def registerUser(self, username, password):
        # Create an instance of the database connection handler class
        database = DatabaseConnection()

        # Establish session through the register function
        database_conn = database.connect()

        try:
            # Cursor object to run and execute SQL queries for registration
            cursor = database_conn.cursor()
            print(f"Registering new user: {username}...")
            sql_query = "INSERT INTO users (username, password) VALUES (%s, %s)"
            cursor.execute(sql_query, (username, password))
            return True

        except Exception as error:
            print(f"Failed to register user: {username}")
            print(f"Error Message: {error}")
            return False

        finally:
            if cursor:
                try:
                    cursor.close()
                except Exception as error:
                    print(f"Failed to close cursor: {error}")
            # Finally close the connection with database after the query execution
            database.close()
            print("Database connection closed successfully.")