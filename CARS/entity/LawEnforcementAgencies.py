class LawEnforcementAgencies():
    def __init__(self, AgencyID = None, AgencyName = None, Jurisdiction = None, EmailAddress = None):
        self.__AgencyID = AgencyID
        self.__AgencyName = AgencyName
        self.__Jurisdiction = Jurisdiction
        self.__EmailAddress = EmailAddress
        
    @property
    def agencyID(self):
        return self.__AgencyID
    
    @property
    def agencyName(self):
        return self.__AgencyName
    
    @property
    def jurisdiction(self):
        return self.__Jurisdiction
    
    @property
    def emailAddress(self):
        return self.__EmailAddress
    
    @agencyID.setter
    def get_agencyID(self, value):
        self.__AgencyID = value
        
    @agencyName.setter
    def get_agencyName(self, value):
        self.__AgencyName = value
        
    @jurisdiction.setter
    def get_jurisdiction(self, value):
        self.__Jurisdiction = value
        
    @emailAddress.setter
    def get_emailAddress(self, value):
        self.__EmailAddress = value
        
    def __str__(self):
        return f"Agency ID: {self.__AgencyID} \nAgency Name: {self.__AgencyName} \nJurisdiction: {self.__Jurisdiction} \nEmail Address: {self.__EmailAddress}"
    
    