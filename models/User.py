from config.DatabaseConnection import DatabaseConnection
import bcrypt
# This class represents a user in the system.
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
            
            # hashing the password
            hashed_password = self.hashPassword(password)

            # push the evaluated user credentials into the database
            sql_query = "INSERT INTO users (username, password) VALUES (%s, %s)"
            condition_values = (username, hashed_password) # tuple value
            cursor.execute(sql_query, condition_values)
            return True

        except Exception as error:
            print(f"Registration Error Message: {error}")
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
    
    # Returns the username to be used for opening the account data
    def validateLogin(self, username, password):
        # Create an instance of the database connection handler class
        database = DatabaseConnection()
        # Establish session through the login function
        database_conn = database.connect()
        
        cursor = database_conn.cursor()
        # get id to open own user data accordingly and the password for comparison 
        sql_query = "SELECT id, password FROM users WHERE username = %s"
        condition_values = (username,) # tuple value with one element (tuple value needed for cursor.execute)
        cursor.execute(sql_query, condition_values)
        result = cursor.fetchone()
        # pass individual values into its own variable
        user_id, stored_hash = result

        try:
            # check and convert into bytes if the stored_hash is a string value
            if isinstance(stored_hash, str):
                stored_hash = stored_hash.encode("utf-8")
            
            # compare the entered password with the stored hashed password
            if bcrypt.checkpw(password.encode("utf-8"), stored_hash):
                # Return user_id as part of a tuple needed for cursor.executed
                return (user_id,)
            else:
                return None

        except Exception as error:
            print(f"Login Error Message: {error}")
            return None
        
        finally:
            database.close()
            print("Database connection closed successfully.")

    # returns the hashed version of the password
    def hashPassword(self, password):
        raw_password = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(raw_password, salt)
        return hashed_password