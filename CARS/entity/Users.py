class User:
    def __init__(self, user_id=None, username=None, password=None, role='Officer', Officers=None):
        self.__user_id = user_id
        self.__username = username
        self.__password = password
        self.__role = role  
        self.__Officers = Officers

    @property
    def user_id(self):
        return self.__user_id
    
    @property
    def username(self):
        return self.__username
    
    @property
    def password(self):
        return self.__password
    
    @property
    def role(self):
        return self.__role
    
    @property
    def officers(self):
        return self.__Officers

    @user_id.setter
    def user_id(self, value):
        self.__user_id = value
        
    @username.setter
    def username(self, value):
        self.__username = value
        
    @password.setter
    def password(self, value):
        self.__password = value
        
    @role.setter
    def role(self, value):
        if value not in ('Officer', 'Admin'):
            raise ValueError("Role must be 'Officer' or 'Admin'")
        self.__role = value
        
    # @officer_id.setter
    # def officer_id(self, value):
    #     self.__officer_id = value

    # def __str__(self):
    #     return f"User: {self.__username}\nRole: ({self.__role})"