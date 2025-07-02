class Incidents():
    def __init__(self, IncidentID = None, IncidentType = None, IncidentDate = None, Area = None, City = None, Description = None, Status = None, OfficerID = None):
        self.__IncidentID = IncidentID
        self.__IncidentType = IncidentType
        self.__IncidentDate = IncidentDate
        self.__Area = Area
        self.__City = City
        self.__Description = Description
        self.__Status = Status
        self.__OfficerID = OfficerID
    
    @property
    def incidentID(self):
        return self.__IncidentID
    
    @property
    def incidentType(self):
        return self.__IncidentType
        
    @property
    def incidentDate(self):
        return self.__IncidentDate
    
    @property
    def area(self):
        return self.__Area
    
    @property
    def city(self):
        return self.__City
    
    @property
    def description(self):
        return self.__Description
    
    @property
    def status(self):
        return self.__Status
    
    @property
    def officerID(self):
        return self.__OfficerID
    
    @incidentID.setter
    def get_incidentID(self, value):
        self.__IncidentID = value
        
    @incidentType.setter
    def get_incidentType(self, value):
        self.__IncidentType = value
        
    @incidentDate.setter
    def get_incidentDate(self, value):
        self.__IncidentDate = value
        
    @area.setter
    def get_area(self, value):
        self.__Area = value
        
    @city.setter
    def get_city(self, value):
        self.__City = value
        
    @description.setter
    def get_description(self, value):
        self.__Description = value
        
    @status.setter
    def get_status(self, value):
        self.__Status = value
        
    @officerID.setter
    def get_officerID(self, value):
        self.__OfficerID = value
        
    # def __str__(self):
    #     return f"Incident ID: {self.__IncidentID} \nIncident Type: {self.__IncidentType} \nIncident Date: {self.__IncidentDate} \nArea: {self.__Area} \nCity: {self.__City} \nDescription: {self.__Description} \nStatus: {self.__Status} \nOfficer ID: {self.__OfficerID}"
    
    