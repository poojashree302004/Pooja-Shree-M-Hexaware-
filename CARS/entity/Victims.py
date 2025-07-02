class Victims:
    def __init__(self, VictimID=None, FirstName=None, LastName=None, DateOfBirth=None, Gender=None, ResidentialAddress=None, ContactNumber=None, AadhaarNumber=None, IncidentID=None):
        self.__VictimID = VictimID
        self.__FirstName = FirstName
        self.__LastName = LastName
        self.__DateOfBirth = DateOfBirth
        self.__Gender = Gender
        self.__ResidentialAddress = ResidentialAddress
        self.__ContactNumber = ContactNumber
        self.__AadhaarNumber = AadhaarNumber
        self.__IncidentID = IncidentID

    @property
    def victimID(self): 
        return self.__VictimID
    @victimID.setter
    def victimID(self, value): self.__VictimID = value
    
    @property
    def firstName(self): 
        return self.__FirstName
    @firstName.setter
    def firstName(self, value): 
        self.__FirstName = value

    @property
    def lastName(self): 
        return self.__LastName
    @lastName.setter
    def lastName(self, value): 
        self.__LastName = value

    @property
    def dateOfBirth(self): 
        return self.__DateOfBirth
    @dateOfBirth.setter
    def dateOfBirth(self, value): 
        self.__DateOfBirth = value

    @property
    def gender(self): 
        return self.__Gender
    @gender.setter
    def gender(self, value): 
        self.__Gender = value

    @property
    def residentialAddress(self): 
        return self.__ResidentialAddress
    @residentialAddress.setter
    def residentialAddress(self, value): 
        self.__ResidentialAddress = value

    @property
    def contactNumber(self): 
        return self.__ContactNumber
    @contactNumber.setter
    def contactNumber(self, value): 
        self.__ContactNumber = value

    @property
    def aadhaarNumber(self): 
        return self.__AadhaarNumber
    @aadhaarNumber.setter
    def aadhaarNumber(self, value): 
        self.__AadhaarNumber = value

    @property
    def incidentID(self): 
        return self.__IncidentID
    @incidentID.setter
    def incidentID(self, value): 
        self.__IncidentID = value
