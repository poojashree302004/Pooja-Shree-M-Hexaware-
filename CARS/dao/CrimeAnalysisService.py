from abc import ABC, abstractmethod

class ICrimeAnalysisService(ABC):
    @abstractmethod
    def create_incident(self, incident):
        pass
    
    @abstractmethod
    def update_incident_status(self, status, incidentID):
        pass
    
    @abstractmethod
    def get_incidents_in_date_range_public(self, start_date, end_date):
        pass
    
    @abstractmethod
    def get_incidents_by_area_city_public(self, area, city):
        pass
    
    @abstractmethod
    def get_filtered_incidents(self, start_date, end_date, area, city, incident_type, officer_id):
        pass
    
    @abstractmethod
    def create_officer(self, officer_data):
        pass
    
    @abstractmethod
    def get_officers_by_location(self, city, area):
        pass
    
    @abstractmethod
    def count_open_incidents_by_officer(self, officer_id):
        pass
    
    @abstractmethod
    def generate_incident_report(self, report):
        pass
    
    @abstractmethod
    def view_incident_report(self, incidentID):
        pass
    
    @abstractmethod
    def get_victims_by_incident(self, incidentID):
        pass
    
    @abstractmethod
    def get_suspects_by_incident(self, incidentID):
        pass
    
    @abstractmethod
    def get_evidence_by_incident(self, incidentID):
        pass
    
    @abstractmethod
    def update_incident_status(self, incidentID, updatedReport):
        pass
    
    @abstractmethod
    def viewIncident(self, incidentID):
        pass
    
    @abstractmethod
    def viewMyIncidents(self,officerID):
        pass
    
    @abstractmethod
    def viewAllIncidents(self):
        pass
    @abstractmethod
    def suspectCriminalRelation(self, aadhaarID):
        pass
    
    @abstractmethod
    def addSuspect(self, suspect):
        pass
    
    @abstractmethod
    def addCriminal(self, criminal):
        pass
    @abstractmethod
    def viewAllSuspects(self):
        pass
    @abstractmethod
    def viewAllCriminals(self):
        pass
    
    @abstractmethod
    def get_crime_analytics(self):
        pass
    
    @abstractmethod
    def get_criminal_analytics(self):
        pass
    @abstractmethod
    def get_all_officer_dashboard(self):
        pass
    @abstractmethod
    def print_recent_incidents(self):
        pass
    
    @abstractmethod
    def get_reports_by_status(self, status):
        pass
    