from getpass import getpass
from util.DB_Connections import DBConnections
from exceptions.user_defined_exceptions import AuthenticationError

class Authentication:
    
    @staticmethod
    def login():
        print("\n=== Login ===")
        username = input("Username: ")
        password = getpass("Password: ")
        
        try:
            connection = DBConnections.get_connection('db.properties')
            cursor = connection.cursor(dictionary=True)
            
            query = "SELECT * FROM Users WHERE Username = %s AND Password = %s"
            cursor.execute(query, (username, password))
            user = cursor.fetchone()
            
            cursor.close()
            connection.close()
            
            if user:
                return user
            raise AuthenticationError("Invalid credentials! Please try again.")
            
        except Exception as e:
            raise AuthenticationError(f"Login failed: {str(e)}")
    
    @staticmethod
    def public_access():
        return {'UserID': 0, 'Role': 'Public', 'Username': 'public_user'}