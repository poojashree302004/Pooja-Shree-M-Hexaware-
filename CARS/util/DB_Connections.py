from util.DB_Properties_Util import DBProperties
from exceptions.user_defined_exceptions import DatabaseError
import mysql.connector

class DBConnections():
    @staticmethod
    def get_connection(property_file_name):
        try:
            conn_params = DBProperties.get_connection_string('db.properties')
            
            if not conn_params:
                raise DatabaseError("Database Error!")
            
            connection = mysql.connector.connect(
                host = conn_params['host'],
                database = conn_params['database'],
                user = conn_params['user'],
                password = conn_params['password'],
                port = int(conn_params.get('port', 3306)),
            )
            
            return connection
        
        except mysql.connector.Error as e:
            raise DatabaseError (f"Database interaction failed: {e.msg}") from e
        
        