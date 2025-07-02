class Evidence():
    def __init__(self, EvidenceID = None, EvidenceName = None, Description = None, LocationFound = None, Incidents = None):
        self.__EvidenceID = EvidenceID
        self.__EvidenceName = EvidenceName
        self.__Description = Description
        self.__LocationFound = LocationFound
        self.__Incidents = Incidents
        
    @property
    def evidenceID(self):
        return self.__EvidenceID
    
    @property
    def evidenceName(self):
        return self.__EvidenceName
    
    @property
    def description(self):
        return self.__Description
    
    @property
    def locationFound(self):
        return self.__LocationFound
    
    @property
    def incidents(self):
        return self.__Incidents
    
    @evidenceID.setter
    def get_evidenceID(self, value):
        self.__EvidenceID = value
        
    @evidenceName.setter
    def get_evidenceName(self, value):
        self.__EvidenceName = value
        
    @description.setter
    def get_description(self, value):
        self.__Description = value
        
    @locationFound.setter
    def get_locationFound(self, value):
        self.__LocationFound = value
        
    # @incidentID.setter
    # def get_incidentID(self, value):
    #     self.__IncidentID = value
        
    # def __str__(self):
    #     return f"Evidence ID: {self.__EvidenceID} \nEvidence Name: {self.__EvidenceName} \nDescription: {self.__Description} \nLocation Found: {self.__LocationFound} \nIncident ID: {self.__IncidentID}"
    
    