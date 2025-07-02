class Reports():
    def __init__(self, ReportID = None, Incidents = None, Officers = None, ReportDate = None, ReportDetails = None, Status = None):
        self.__ReportID = ReportID
        self.__Incidents = Incidents
        self.__Officers = Officers
        self.__ReportDate = ReportDate
        self.__ReportDetails = ReportDetails
        self.__Status = Status
        
    @property
    def reportID(self):
        return self.__ReportID
    
    @property
    def incidents(self):
        return self.__Incidents
    
    @property
    def officers(self):
        return self.__Officers
    
    @property
    def reportDate(self):
        return self.__ReportDate
    
    @property
    def reportDetails(self):
        return self.__ReportDetails
    
    @property
    def status(self):
        return self.__Status
    
    @reportID.setter
    def get_reportID(self, value):
        self.__ReportID = value
        
    # @incidentID.setter
    # def get_incidentID(self, value):
    #     self.__IncidentID = value
        
    # @reportingOfficerID.setter
    # def get_reportingOfficerID(self, value):
    #     self.__ReportingOfficerID = value
        
    @reportDate.setter
    def get_reportDate(self, value):
        self.__ReportDate = value
        
    @reportDetails.setter
    def get_reportDetails(self, value):
        self.__ReportDetails = value
        
    @status.setter
    def get_status(self, value):
        self.__Status = value
        
    # def __str__(self):
    #     return f"Report ID: {self.__ReportID} \nIncident ID: {self.__IncidentID} \nReporting Officer ID: {self.__ReportingOfficerID} \nReport Date: {self.__ReportDate} \nReport Details: {self.__ReportDetails} \nStatus: {self.__Status}"
    
    