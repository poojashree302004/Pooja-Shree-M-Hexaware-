class SuspectIncidents():
    def __init__(self, Suspects = None, Incidents = None, RoleDescription = None, Officers = None):
        self.__Suspects = Suspects
        self.__Incidents = Incidents
        self.__RoleDescription = RoleDescription
        self.__Officers = Officers
        
    @property
    def suspects(self):
        return self.__Suspects
    
    @property
    def incidents(self):
        return self.__Incidents
    
    @property
    def roleDescription(self):
        return self.__RoleDescription
    
    @property
    def officers(self):
        return self.__Officers
    
    # @suspectID.setter
    # def get_suspectID(self, value):
    #     self.__SuspectID = value
        
    # @incidentID.setter
    # def get_incidentID(self, value):
    #     self.__IncidentID = value
        
    @roleDescription.setter
    def get_roleDescription(self, value):
        self.__RoleDescription = value
        
    # @addedByOfficerID.setter
    # def get_addedByOfficerID(self, value):
    #     self.__AddedByOfficerID = value
        
    # def __str__(self):
    #     return f"Suspect ID: {self.__SuspectID} \nIncident ID: {self.__IncidentID} \nRole Description: {self.__RoleDescription} \nAdded By Officer ID: {self.__AddedByOfficerID}"