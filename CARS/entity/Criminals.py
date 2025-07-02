class Criminals():
    def __init__(self, CriminalID = None, IncidentID = None, SuspectID = None, AadhaarNumber = None, PunishmentDetails = None):
        self.__CriminalID = CriminalID
        self.__IncidentID = IncidentID
        self.__SuspectID = SuspectID
        self.__AadhaarNumber = AadhaarNumber
        self.__PunishmentDetails = PunishmentDetails
        
    @property
    def criminalID(self):
        return self.__CriminalID
    
    @property
    def incidentID(self):
        return self.__IncidentID
    
    @property
    def suspectID(self):
        return self.__SuspectID
    
    @property
    def aadhaarNumber(self):
        return self.__AadhaarNumber
    
    @property
    def punishmentDetails(self):
        return self.__PunishmentDetails
    
    @criminalID.setter
    def get_criminalID(self, value):
        self.__CriminalID = value
        
    @incidentID.setter
    def get_incidentID(self, value):
        self.__IncidentID = value
        
    @suspectID.setter
    def get_suspectID(self, value):
        self.__SuspectID = value
        
    @aadhaarNumber.setter
    def get_aadhaarNumber(self, value):
        self.__AadhaarNumber = value
        
    @punishmentDetails.setter
    def get_punishmentDetails(self, value):
        self.__PunishmentDetails = value
        
    # def __str__(self):
    #     return f"Criminal ID: {self.__CriminalID} \nIncident ID: {self.__IncidentID} \nSuspect ID: {self.__SuspectID} \nAadhaar Number: {self.__AadhaarNumber} \nPunishmenet Details: {self.__PunishmentDetails}"
    
    