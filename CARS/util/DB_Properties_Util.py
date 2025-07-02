import configparser
import os
from exceptions.user_defined_exceptions import DatabaseError
import mysql.connector

class DBProperties():
    @staticmethod
    def get_connection_string(property_file_name):
        try:
            if not os.path.exists(property_file_name):
                raise FileNotFoundError(f"'{property_file_name}' file not found")
            
            config = configparser.ConfigParser()
            config.read(property_file_name)
            
            if 'database' not in config: 
                raise DatabaseError ("Database not found")
            
            return{
                'host' : config.get('database', 'host'),
                'database' : config.get('database', 'database'),
                'user' : config.get('database', 'user'),
                'password' : config.get('database', 'password'),
                'port' : config.get('database', 'port')
            }
            
        except mysql.connector.Error as e:
            raise DatabaseError(f"Database interaction failed: {e.msg}") from e