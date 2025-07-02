class Suspects():
    def __init__(self, SuspectID = None, FirstName = None, LastName = None, DateOfBirth = None, Gender = None, ResidentialAddress = None, ContactNumber = None, AadhaarNumber = None):
        self.__SuspectID = SuspectID
        self.__FirstName = FirstName
        self.__LastName = LastName
        self.__DateOfBirth = DateOfBirth
        self.__Gender = Gender
        self.__ResidentialAddress = ResidentialAddress
        self.__ContactNumber = ContactNumber
        self.__AadhaarNumber = AadhaarNumber
    
    @property
    def suspectID(self):
        return self.__SuspectID
        
    @property
    def firstName(self):
        return self.__FirstName
    
    @property
    def lastName(self):
        return self.__LastName
    
    @property
    def dateOfBirth(self):
        return self.__DateOfBirth
    
    @property
    def gender(self):
        return self.__Gender
    
    @property
    def residentialAddress(self):
        return self.__ResidentialAddress
    
    @property
    def contactNumber(self):
        return self.__ContactNumber
    
    @property
    def aadhaarNumber(self):
        return self.__AadhaarNumber
    
    @suspectID.setter
    def get_suspectID(self, value):
        self.__SuspectID = value
        
    @firstName.setter
    def get_firstName(self, value):
        self.__FirstName = value
        
    @lastName.setter
    def get_lastName(self, value):
        self.__LastName = value
        
    @dateOfBirth.setter
    def get_dateOfBirth(self, value):
        self.__DateOfBirth = value
        
    @gender.setter
    def get_gender(self, value):
        self.__Gender = value
        
    @residentialAddress.setter
    def get_residentialAddress(self, value):
        self.__ResidentialAddress = value
        
    @contactNumber.setter
    def get_contactNumber(self, value):
        self.__ContactNumber = value
        
    @aadhaarNumber.setter
    def get_aadhaarNumber(self, value):
        self.__AadhaarNumber = value
        
    def __str__(self):
        return f"Suspect ID: {self.__SuspectID} \nFirst Name: {self.__FirstName} \nLast Name: {self.__LastName} \nDate Of Birth: {self.__DateOfBirth} \nGender: {self.__Gender} \nResidential Address: {self.__ResidentialAddress} \nContact Number: {self.__ContactNumber} \nAadhaar Number: {self.__AadhaarNumber}"
    
    