from dao.CrimeAnalysisService import ICrimeAnalysisService
from util.DB_Connections import DBConnections
from entity.Incidents import Incidents
from entity.Victims import Victims
from entity.Suspects import Suspects
from entity.Criminals import Criminals
from entity.Evidence import Evidence
from entity.SuspectIncidents import SuspectIncidents
from entity.LawEnforcementAgencies import LawEnforcementAgencies
from exceptions.user_defined_exceptions import DatabaseError, IncidentNotFoundException, DuplicateEntryException, SuspectNotFoundException, ReportNotFoundException, AgencyNotFoundException, OfficerNotFoundException, VictimNotFoundException, EvidenceNotFoundException, CriminalNotFoundException


class CrimeAnalysisServiceImpl(ICrimeAnalysisService):
    def __init__(self):
        self.connection = DBConnections.get_connection('db.properties')
    
    def create_incident(self, incident):
        try:
            cursor = self.connection.cursor()
            query = """
            INSERT INTO Incidents (IncidentType, IncidentDate, Area, City, 
                                 Description, Status, OfficerID)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                incident.incidentType, incident.incidentDate, incident.area,
                incident.city, incident.description, incident.status, incident.officerID
            ))
            self.connection.commit()
            return cursor.lastrowid
        
        except Exception as e:
            self.connection.rollback()
            raise DatabaseError(f"Failed to create incident: {str(e)}")



    
    def update_incident_status(self, status, incidentID):
        try:
            cursor = self.connection.cursor()
            query = "UPDATE Incidents SET Status = %s WHERE IncidentID = %s"
            cursor.execute(query, (status, incidentID))
            self.connection.commit()
            return cursor.rowcount > 0
        
        except IncidentNotFoundException as e:
            print("Incident not found.")
        except Exception as e:
            self.connection.rollback()
            raise DatabaseError(f"Failed to update incident status: {str(e)}")
    
    def get_incidents_in_date_range_public(self, start_date, end_date):
        try:
            incidents = []
            cursor = self.connection.cursor(dictionary=True)
            query = """
            SELECT IncidentType, IncidentDate, Area, City, Description FROM Incidents 
            WHERE IncidentDate BETWEEN %s AND %s
            ORDER BY IncidentDate
            """
            cursor.execute(query, (start_date, end_date))
            
            for row in cursor:
                incidents.append(Incidents( 
                    IncidentType = row['IncidentType'], 
                    IncidentDate = row['IncidentDate'],
                    Area = row['Area'], 
                    City = row['City'], 
                    Description = row['Description']
                ))
            return incidents
        except IncidentNotFoundException as e:
            print("Incident not found.")
        except Exception as e:
            raise DatabaseError(f"Failed to fetch incidents: {str(e)}") 
    
    def get_incidents_by_area_city_public(self, area=None, city=None):
        try:
            cursor = self.connection.cursor(dictionary=True)
            
            query = "SELECT IncidentType, IncidentDate, Area, City, Description FROM Incidents WHERE 1=1"
            params = []
            
            if area:
                query += " AND Area = %s"
                params.append(area)
                
            if city:
                query += " AND City = %s"
                params.append(city)
                
            query += " ORDER BY IncidentDate DESC"
            
            cursor.execute(query, params)
            incidents = cursor.fetchall()
            
            return -incidents
        
        except IncidentNotFoundException as e:
            print("Incident not found.")    
        except Exception as e:
            raise DatabaseError(f"Error fetching incidents by area/city: {str(e)}")
            
    def get_filtered_incidents(self, start_date=None, end_date=None, area=None, city=None, incident_type=None, officer_id=None):
    
        incidents = []
        try:
            cursor = self.connection.cursor(dictionary=True)
            
            query = "SELECT * FROM Incidents WHERE 1=1"
            params = []
            
            if start_date:
                query += " AND IncidentDate >= %s"
                params.append(start_date)
            if end_date:
                query += " AND IncidentDate <= %s"
                params.append(end_date)
            if area:
                query += " AND Area = %s"
                params.append(area)
            if city:
                query += " AND City = %s"
                params.append(city)
            if incident_type:
                query += " AND IncidentType = %s"
                params.append(incident_type)
            if officer_id:
                query += " AND OfficerID = %s"
                params.append(officer_id)
                
            query += " ORDER BY IncidentDate DESC"
            
            cursor.execute(query, params)
            
            for row in cursor:
                incidents.append({
                    'IncidentID': row['IncidentID'],
                    'IncidentType': row['IncidentType'],
                    'IncidentDate': row['IncidentDate'].strftime('%Y-%m-%d') if row['IncidentDate'] else None,
                    'Area': row['Area'],
                    'City': row['City'],
                    'Description': row['Description'],
                    'Status': row['Status'],
                    'OfficerID': row['OfficerID']
                })
            return incidents
        
        except IncidentNotFoundException as e:
            print("Incident not found.")    
        except Exception as e:
            raise DatabaseError(f"Filter error: {str(e)}")

    
    def create_officer(self, officer_data):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM lawenforcementagencies WHERE AgencyID = %s", 
                       (officer_data['agencyID'],))
            result = cursor.fetchone()
            if result[0] == 0:
                raise AgencyNotFoundException(f"AgencyID {officer_data['agencyID']} does not exist.")
            officer_query = """
            INSERT INTO Officers (FirstName, LastName, DateOfBirth, Gender, BadgeNumber, Ranking, PostingCity, PostingState, ServiceJoiningDate, ResidentialAddress, ContactNumber, AgencyID)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(officer_query, (
                officer_data['firstName'], 
                officer_data['lastName'],
                officer_data['dateOfBirth'], 
                officer_data['gender'], 
                officer_data['badgeNumber'], 
                officer_data['ranking'],
                officer_data['postingCity'], 
                officer_data['postingState'],
                officer_data['serviceJoiningDate'],
                officer_data['residentialAddress'], 
                officer_data['contactNumber'],
                officer_data['agencyID']
            ))
            officerID = cursor.lastrowid
        
            user_query = """
            INSERT INTO Users (Username, Password, Role, OfficerID)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(user_query, (
                officer_data['username'],
                officer_data['password'], 
                'Officer', officerID
            ))
            
            self.connection.commit()
            return officerID
        
        except AgencyNotFoundException as e:
            print("Agency not found.")
        except Exception as e:
            self.connection.rollback()
            raise DatabaseError(f"Failed to add officer: {str(e)}")
        
    def get_officers_by_location(self, city, area):
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = """
            SELECT * FROM Officers
            WHERE PostingCity = %s OR PostingState = %s
            """
            cursor.execute(query, (city, area))
            return cursor.fetchall()
        
        except OfficerNotFoundException as e:
            print("Officers not found. ")
        except Exception as e:
            raise DatabaseError(f"Failed to fetch officers: {str(e)}")
        
    def count_open_incidents_by_officer(self, officer_id):
        try:
            cursor = self.connection.cursor()
            query = """
            SELECT COUNT(*) FROM Incidents
            WHERE OfficerID = %s AND Status != 'Closed'
            """
            cursor.execute(query, (officer_id,))
            count = cursor.fetchone()[0]
            return count
        
        except OfficerNotFoundException as e:
            print("Officers not found. ")
        except IncidentNotFoundException as e:
            print("Incident not found.")
        except Exception as e:
            raise DatabaseError(f"Failed to count open cases: {str(e)}")

    def generate_incident_report(self, report):
        try:
            cursor = self.connection.cursor()

            check_officer_query = """
                SELECT OfficerID FROM Incidents WHERE IncidentID = %s
            """
            cursor.execute(check_officer_query, (report.incidents.incidentID,))
            result = cursor.fetchone()
            if not result:
                raise IncidentNotFoundException(f"Incident ID {report.incidents.incidentID} not found.")

            officer_in_charge = result[0]
            if officer_in_charge != report.officers.officerID:
                raise PermissionError(f"You are not authorized to generate a report for Incident ID {report.incidents.incidentID}.")

            cursor.execute("SELECT ReportID FROM Reports WHERE IncidentID = %s", (report.incidents.incidentID,))
            if cursor.fetchone():
                raise DuplicateEntryException(f"A report already exists for Incident ID {report.incidents.incidentID}.")

            insert_query = """
                INSERT INTO Reports (IncidentID, ReportingOfficerID, ReportDate, ReportDetails, Status)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (
                report.incidents.incidentID,
                report.officers.officerID,
                report.reportDate,
                report.reportDetails,
                report.status
            ))
            self.connection.commit()
            return cursor.lastrowid
        except (IncidentNotFoundException, PermissionError, DuplicateEntryException):
            raise
        except Exception as e:
            self.connection.rollback()
            raise DatabaseError(f"Failed to generate report: {str(e)}")

        
    def update_incident_report(self, report):
        try:
            cursor = self.connection.cursor()

            check_officer_query = """
                SELECT OfficerID FROM Incidents WHERE IncidentID = %s
            """
            cursor.execute(check_officer_query, (report.incidents.incidentID,))
            result = cursor.fetchone()
            if not result:
                raise IncidentNotFoundException(f"Incident ID {report.incidents.incidentID} not found.")

            officer_in_charge = result[0]
            if officer_in_charge != report.officers.officerID:
                raise PermissionError(f"You are not authorized to update the report for Incident ID {report.incidents.incidentID}.")

            update_query = """
                UPDATE Reports
                SET ReportDetails = %s, Status = %s, ReportDate = %s
                WHERE IncidentID = %s
            """
            cursor.execute(update_query, (
                report.reportDetails,
                report.status,
                report.reportDate,
                report.incidents.incidentID
            ))

            if cursor.rowcount == 0:
                raise ReportNotFoundException(f"No report found for Incident ID {report.incidents.incidentID}")

            self.connection.commit()
            return True

        except (IncidentNotFoundException, PermissionError, ReportNotFoundException):
            raise
        except Exception as e:
            self.connection.rollback()
            raise DatabaseError(f"Failed to update report: {str(e)}")



    def view_incident_report(self, incidentID):
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = """
                SELECT i.IncidentID, i.IncidentType, i.Area, i.City, i.Description, i.Status, 
                r.ReportDetails, r.ReportDate, r.Status AS ReportStatus
                FROM Incidents i
                JOIN Reports r 
                ON i.IncidentID = r.IncidentID
                WHERE i.IncidentID = %s
            """
            cursor.execute(query, (incidentID,))
            report = cursor.fetchone()
            return report
        
        except IncidentNotFoundException as e:
            print("Incident not found.")
        except Exception as e:
            raise DatabaseError(f"Failed to display report: {str(e)}")
        
    def get_victims_by_incident(self, incidentID):
        try: 
            cursor = self.connection.cursor()
            query = "SELECT * FROM Victims WHERE IncidentID = %s"
            cursor.execute(query, (incidentID,))
            results = cursor.fetchall()
            
            victims = []
            for result in results: 
                victim = Victims(
                    VictimID = result[0],
                    FirstName = result[1],
                    LastName = result[2],
                    DateOfBirth = result[3],
                    Gender = result[4],
                    ResidentialAddress = result[5],
                    ContactNumber = result[6],
                    AadhaarNumber = result[7],)
                victims.append(victim)
                
            return victims
        
        except IncidentNotFoundException as e:
            print("Incident not found.")
        except VictimNotFoundException as e:
            print("Victim not found.")
        except Exception as e:
            raise DatabaseError(f"Failed to fetch victims list: {str(e)}")
        
    def get_suspects_by_incident(self, incidentID):
        try:
            cursor = self.connection.cursor()
            query = """
                SELECT S.*, SI.IncidentID, SI.AddedByOfficerID, SI.RoleDescription
                FROM Suspects S
                JOIN SuspectIncidents SI ON S.AadhaarNumber = SI.AadhaarNumber
                WHERE SI.IncidentID = %s
            """
            cursor.execute(query, (incidentID,))
            results = cursor.fetchall()
            
            suspect_incidents = []
            for row in results:
                suspect = Suspects(
                    SuspectID=row[0],
                    FirstName=row[1],
                    LastName=row[2],
                    DateOfBirth=row[3],
                    Gender=row[4],
                    ResidentialAddress=row[5],
                    ContactNumber=row[6],
                    AadhaarNumber=row[7]
                )

                suspect_incident = SuspectIncidents(
                    Suspects=suspect,
                    Incidents=row[8],   
                    Officers=row[9],   
                    RoleDescription=row[10]
                )
                suspect_incidents.append(suspect_incident)
            
            return suspect_incidents
        
        except SuspectNotFoundException as e:
            print("Suspect not found.")
        except IncidentNotFoundException as e:
            print("Incident not found.")
        except Exception as e:
            raise DatabaseError(f"Failed to fetch suspects list: {str(e)}")

                
    def get_evidence_by_incident(self, incidentID):
        try: 
            cursor = self.connection.cursor()
            query = "SELECT * FROM Evidence WHERE IncidentID = %s"
            cursor.execute(query, (incidentID,))
            results = cursor.fetchall()
            
            evidences = []
            for result in results: 
                evidence = Evidence(
                    EvidenceID = result[0],
                    EvidenceName = result[1],
                    Description = result[2],
                    LocationFound = result[3])
                evidences.append(evidence)
                
            return evidences
        
        except IncidentNotFoundException as e:
            print("Incident not found.")
        except EvidenceNotFoundException as e:
            print("Victim not found.")
        except Exception as e:
            raise DatabaseError(f"Failed to fetch evidence list: {str(e)}")

    def update_incident_status(self, incidentID, updatedReport):
        try: 
            cursor = self.connection.cursor()
            query = "UPDATE Incidents SET Status = %s, ReportDetails = %s, ReportDate = %s WHERE IncidentID = %s"
            cursor.execute(query, (updatedReport.status, updatedReport.reportDetails, updatedReport.reportDate, incidentID))
            self.connection.commit()
            return cursor.rowcount
        
        except IncidentNotFoundException as e:
            print("Incident not found.")
        except Exception as e:
            self.connection.rollback()
            raise DatabaseError(f"Failed to update the status of the incident: {str(e)}")

    def viewIncident(self, incidentID):
        try: 
            cursor = self.connection.cursor()
            query = "SELECT * FROM Incidents WHERE IncidentID = %s"
            cursor.execute(query,(incidentID))
            result = cursor.fetchone()
            return result
        
        except IncidentNotFoundException as e:
            print("Incident not found.")
        except Exception as e:
            raise DatabaseError(f"Couldn't display the incident: {str(e)}")
        
    def viewMyIncidents(self,officerID):
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = "SELECT * FROM Incidents WHERE OfficerID = %s AND STATUS != 'Closed'"
            cursor.execute(query,(officerID,))
            results = cursor.fetchall()
            
            incidents = []
            for row in results:
                incident = Incidents(
                    IncidentID=row['IncidentID'],
                    IncidentType=row['IncidentType'],
                    IncidentDate=row['IncidentDate'],
                    Area=row['Area'],
                    City=row['City'],
                    Description=row['Description'],
                    Status=row['Status'],
                    OfficerID=row['OfficerID']
                )
                incidents.append(incident)
            return results
        
        except IncidentNotFoundException as e:
            print("Incident not found.")
        except Exception as e:
            raise DatabaseError(f"Couldn't display the incidents: {str(e)}")
        
    def viewAllIncidents(self):
        try: 
            cursor = self.connection.cursor()
            query = "SELECT * FROM Incidents"
            cursor.execute(query)
            results = cursor.fetchall()
            
            incidents = []
            for result in results: 
                incident = Incidents(
                    IncidentID = result[0],
                    IncidentType = result[1],
                    IncidentDate = result[2],
                    Area = result[3],
                    City = result[4],
                    Description = result[5],
                    Status = result[6],
                    OfficerID = result[7]
                )
                incidents.append(incident)
                
            return 
        except IncidentNotFoundException as e:
            print("Incident not found.")
        except Exception as e:
            raise DatabaseError(f"Couldn't display the incidents: {str(e)}")

    def suspectCriminalRelation(self, aadhaarNumber):
        try:
            cursor = self.connection.cursor()
            query = """
            SELECT C.CriminalID, C.IncidentID, C.PunishmentDetails
            FROM Suspects S
            JOIN Criminals C
            ON S.AadhaarNumber = C.AadhaarNumber
            WHERE S.AadhaarNumber = %s
            """
            cursor.execute(query,(aadhaarNumber,))
            results = cursor.fetchall()
            
            criminalRecords = []
            for result in results: 
                criminalRecord = Criminals(
                    CriminalID = result[0],
                    IncidentID = result[1],
                    PunishmentDetails = result[2]
                )
                criminalRecords.append(criminalRecord)
                
            return criminalRecords
        
        except SuspectNotFoundException as e:
            print("Suspects not found")
        except CriminalNotFoundException as e:
            print("Criminal not found")
        except Exception as e:
            raise DatabaseError(f"Failed to show the suspect and criminal relations: {str(e)}")    
        
    def addSuspect(self, suspect, incidentID, officerID, roleDescription):
        try:
            cursor = self.connection.cursor()
            check_query = """
                SELECT SuspectID FROM Suspects 
                WHERE AadhaarNumber = %s
                LIMIT 1
            """
            cursor.execute(check_query, (suspect.aadhaarNumber,))
            existing_suspect = cursor.fetchone()
            if existing_suspect:
                suspectID = existing_suspect[0]
                check_incident_query = """
                    SELECT * FROM SuspectIncidents 
                    WHERE AadhaarNumber = %s AND IncidentID = %s
                """
                cursor.execute(check_incident_query, (suspect.aadhaarNumber, incidentID))
                existing_link = cursor.fetchone()
                if existing_link:
                    raise DuplicateEntryException(f"Duplicate Entry: Suspect already assigned to Incident {incidentID}.")
                else:
                    insert_incident_query = """
                        INSERT INTO SuspectIncidents (SuspectID, AadhaarNumber, IncidentID, AddedByOfficerID, RoleDescription)
                        VALUES (%s, %s, %s, %s, %s)
                    """
                    cursor.execute(insert_incident_query, (suspectID, suspect.aadhaarNumber, incidentID, officerID, roleDescription))
                    self.connection.commit()
                    return suspectID
            else:
                insert_query = """
                    INSERT INTO Suspects (
                        FirstName, LastName, DateOfBirth, Gender,
                        ResidentialAddress, ContactNumber, AadhaarNumber
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(insert_query, (
                    suspect.firstName, suspect.lastName, suspect.dateOfBirth,
                    suspect.gender, suspect.residentialAddress, suspect.contactNumber, suspect.aadhaarNumber
                ))
                suspectID = cursor.lastrowid
                insert_incident_query = """
                    INSERT INTO SuspectIncidents (SuspectID, AadhaarNumber, IncidentID, AddedByOfficerID, RoleDescription)
                    VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(insert_incident_query, (suspectID, suspect.aadhaarNumber, incidentID, officerID, roleDescription))
                self.connection.commit()
                return suspectID
        except IncidentNotFoundException as e:
            print("Incident not found")
        except OfficerNotFoundException as e:
            print("Officer not found")
        except Exception as e:
            self.connection.rollback()
            raise DatabaseError(f"Failed to add suspect: {str(e)}")

        
    def addCriminal(self, criminal):
        try:
            cursor = self.connection.cursor()
            query_suspect = "SELECT SuspectID FROM Suspects WHERE AadhaarNumber = %s"
            cursor.execute(query_suspect, (criminal.aadhaarNumber,))
            result = cursor.fetchone()

            if not result:
                raise SuspectNotFoundException(f"No suspect found with Aadhaar: {criminal.aadhaarNumber}")

            suspect_id = result[0]

            duplicate_query = """
                SELECT CriminalID FROM Criminals 
                WHERE IncidentID = %s AND AadhaarNumber = %s
            """
            cursor.execute(duplicate_query, (criminal.incidentID, criminal.aadhaarNumber))
            duplicate = cursor.fetchone()

            if duplicate:
                print(f"Duplicate entry: Criminal record already exists for Incident ID {criminal.incidentID}")
                return None

            insert_query = """
                INSERT INTO Criminals (IncidentID, SuspectID, AadhaarNumber, PunishmentDetails)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(insert_query, (
                criminal.incidentID,
                suspect_id,
                criminal.aadhaarNumber,
                criminal.punishmentDetails
            ))

            self.connection.commit()
            return cursor.lastrowid

        except IncidentNotFoundException as e:
            print("Incidents not found.")
        except SuspectNotFoundException as e:
            print("Suspect not found.")
        except Exception as e:
            self.connection.rollback()
            raise DatabaseError(f"Failed to add criminal: {str(e)}")
        
    def addVictim(self, victim, incidentID, officerID, roleDescription):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT IncidentID FROM Incidents WHERE IncidentID = %s", (incidentID,))
            incident = cursor.fetchone()
            if not incident:
                raise IncidentNotFoundException(f"Incident ID {incidentID} not found.")

            cursor.execute("""
                SELECT VictimID FROM Victims 
                WHERE AadhaarNumber = %s AND IncidentID = %s
            """, (victim.aadhaarNumber, incidentID))
            existing = cursor.fetchone()
            if existing:
                print("Victim already exists for this incident.")
                return existing[0]

            
            insert_query = """
                INSERT INTO Victims (
                    FirstName, LastName, DateOfBirth, Gender,
                    ResidentialAddress, ContactNumber, AadhaarNumber, IncidentID
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (
                victim.firstName, victim.lastName, victim.dateOfBirth, victim.gender,
                victim.residentialAddress, victim.contactNumber, victim.aadhaarNumber, incidentID
            ))

            self.connection.commit()
            new_victim_id = cursor.lastrowid
            return new_victim_id

        except Exception as e:
            print(f"Database Error: {str(e)}")
            raise
        
    def viewAllSuspects(self):
        try: 
            cursor = self.connection.cursor()
            query = """
            SELECT SI.SuspectID, SI.IncidentID, SI.RoleDescription, SI.AddedByOfficerID, 
            FirstName, S.LastName, S.DateOfBirth, S.AadhaarNumber, S.ResidentialAddress, S.ContactNumber,
            I.IncidentDate, I.IncidentType, I.Description, I.Status
            FROM SuspectIncidents SI JOIN Suspects S ON SI.AadhaarNumber = S.AadhaarNumber
            JOIN Incidents I ON SI.IncidentID = I.IncidentID
            ORDER BY SI.SuspectID DESC
            """
            cursor.execute(query)
            results = cursor.fetchall()
            
            suspectsInfo = []
            for result in results: 
                suspect = Suspects(
                    SuspectID = result[0],
                    FirstName = result[4],
                    LastName = result[5],
                    DateOfBirth = result[6],
                    AadhaarNumber = result[7],
                    ResidentialAddress = result[8],
                    ContactNumber = result[9]
                )
                
                incident = Incidents(    
                    IncidentID = result[1],
                    IncidentDate = result[10],
                    IncidentType = result[11],
                    Description = result[12],
                    Status = result[13]
                )
                
                suspectIncident = SuspectIncidents(
                    Suspects = suspect,
                    Incidents = incident,
                    RoleDescription = result[2],
                    Officers = result[3]
                )
                suspectsInfo.append(suspectIncident)
                
            return suspectsInfo
        
        except IncidentNotFoundException as e:
            print("Incidents not found.")
        except SuspectNotFoundException as e:
            print("Suspect not found.")
        except Exception as e:
            raise DatabaseError(f"Couldn't display all suspects: {str(e)}")
        
    def viewAllCriminals(self):
        try: 
            cursor = self.connection.cursor()
            query = """
            SELECT C.CriminalID, C.IncidentID, C.PunishmentDetails,
            S.FirstName, S.LastName, S.DateOfBirth, S.Gender,S.ResidentialAddress, 
            S.ContactNumber, S.AadhaarNumber
            FROM Criminals C
            JOIN Suspects S
            ON S.AadhaarNumber = C.AadhaarNumber
            """
            cursor.execute(query)
            results = cursor.fetchall()
            
            criminals = []
            for result in results: 
                criminal_id      = result[0]
                incident_id      = result[1]
                aadhaar_number   = result[9]
                punishment       = result[2]
                first_name       = result[3]
                last_name        = result[4]
                dob              = result[5]
                gender           = result[6]
                address          = result[7]
                contact          = result[8]
               
                suspect = Suspects(
                    FirstName = first_name,
                    LastName = last_name,
                    DateOfBirth = dob,
                    Gender = gender,
                    ResidentialAddress = address,
                    ContactNumber = contact,
                    AadhaarNumber = aadhaar_number
                )             
                criminal = Criminals(
                    CriminalID = criminal_id,
                    IncidentID = incident_id,
                    AadhaarNumber = aadhaar_number,
                    PunishmentDetails = punishment
                )               
                criminal.suspect = suspect
                criminals.append(criminal)             
            return criminals       
        except IncidentNotFoundException as e:
            print("Incidents not found.")
        except SuspectNotFoundException as e:
            print("Suspect not found.")
        except CriminalNotFoundException as e:
            print("Criminal not found")
        except Exception as e:
            raise DatabaseError(f"Couldn't display all criminals: {str(e)}")
        
    def get_crime_analytics(self):
        try:
            cursor = self.connection.cursor(dictionary=True)
            hotspot_query = """
                SELECT City, Area, COUNT(*) as crime_count
                FROM Incidents
                GROUP BY City, Area
                ORDER BY crime_count DESC
                LIMIT 5
            """
            cursor.execute(hotspot_query)
            hotspots = cursor.fetchall()
            
            monthly_trends_query = """
                SELECT 
                    DATE_FORMAT(IncidentDate, '%M %Y') as month,
                    COUNT(*) as count
                FROM Incidents
                GROUP BY month
                ORDER BY MIN(IncidentDate)
            """
            cursor.execute(monthly_trends_query)
            monthly_trends = {row['month']: row['count'] for row in cursor}
            
            return {
                'hotspots': hotspots,
                'monthly_trends': monthly_trends
            }
        
        except IncidentNotFoundException as e:
            print("Incident not found")
        except Exception as e:
            raise DatabaseError(f"Failed to generate the crime analytics: {str(e)}")
        
    def get_criminal_analytics(self):
        try:
            cursor = self.connection.cursor(dictionary=True)
            
            top_criminals_query = """
                SELECT s.FirstName, s.LastName, COUNT(*) as crime_count
                FROM Criminals c
                JOIN Suspects s ON c.SuspectID = s.SuspectID
                GROUP BY c.SuspectID
                ORDER BY crime_count DESC
                LIMIT 5
            """
            cursor.execute(top_criminals_query)
            top_criminals = cursor.fetchall()
            
            crime_type_distribution_query = """
                SELECT IncidentType, COUNT(*) as count
                FROM Incidents
                GROUP BY IncidentType
            """
            cursor.execute(crime_type_distribution_query)
            crime_types = {row['IncidentType']: row['count'] for row in cursor}
            
            return {
                'top_criminals': top_criminals,
                'crime_types': crime_types
            }
            
        except CriminalNotFoundException as e:
            print("Criminal not found") 
        except IncidentNotFoundException as e:
            print("Incident not found")   
        except Exception as e:
            raise DatabaseError(f"Failed to generate the criminal analytics: {str(e)}")
        
    def get_all_officer_dashboard(self):
        try:
            cursor = self.connection.cursor(dictionary=True)
            
            query = """
            SELECT 
            o.OfficerID,
            o.FirstName,
            o.LastName,
            o.BadgeNumber,
            o.Ranking,
            o.PostingCity,
            o.PostingState,
            o.ServiceJoiningDate,
            COUNT(i.IncidentID) AS total_cases,
            SUM(CASE WHEN i.Status = 'Closed' THEN 1 ELSE 0 END) AS cases_closed
            FROM Officers o
            LEFT JOIN Incidents i ON o.OfficerID = i.OfficerID
            GROUP BY 
            o.OfficerID, o.FirstName, o.LastName, o.BadgeNumber, 
            o.Ranking, o.PostingCity, o.PostingState, o.ServiceJoiningDate
            ORDER BY total_cases DESC
            """
            
            cursor.execute(query)
            dashboard_data = cursor.fetchall()
            return dashboard_data
        
        except OfficerNotFoundException as e:
            print("Officers not found")
        except IncidentNotFoundException as e:
            print("Incidents not found")   
        except Exception as e:
            raise DatabaseError(f"Failed to fetch officer dashboard: {str(e)}")

        
    def print_recent_incidents(self):
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = """
                SELECT IncidentDate, IncidentType, Description, Area, City
                FROM Incidents
                WHERE IncidentDate >= DATE_SUB(CURDATE(), INTERVAL 1 MONTH)
                ORDER BY IncidentDate DESC
            """
            cursor.execute(query)
            incidents = cursor.fetchall()

            if not incidents:
                raise IncidentNotFoundException("No incidents found.")
            
            print("\nRECENT INCIDENTS REPORT (LAST 30 DAYS)")
            print("=" * 115)
            print(f"{'DATE':<12} | {'TYPE':<15} | {'AREA':<15} | {'CITY':<15} | {'DESCRIPTION'}")
            print("-" * 115)

            for incident in incidents:
                print(
                    f"{incident['IncidentDate'].strftime('%Y-%m-%d'):<12} | "
                    f"{incident['IncidentType'][:15]:<15} | "
                    f"{incident['Area'] + ', '} | "
                    f"{incident['City']:<20} | "
                    f"{incident['Description']}"
                )

        except IncidentNotFoundException as e:
            print("Incident not found")
        except Exception as e:
            raise DatabaseError(f"Couldn't print the recent incidents: {str(e)}")
        
    def get_reports_by_status(self, status):
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = """
                SELECT i.IncidentID, i.IncidentType, i.Area, i.City, i.Status,
                    r.ReportDate, r.ReportDetails
                FROM Reports r
                JOIN Incidents i ON r.IncidentID = i.IncidentID
                WHERE r.Status = %s
            """
            cursor.execute(query, (status,))
            return cursor.fetchall()
        
        except IncidentNotFoundException as e:
            print("Incident not found")
        except ReportNotFoundException as e:
            print("Report not found")
        except Exception as e:
            raise DatabaseError(f"Failed to fetch reports by status: {str(e)}")
        
    def view_all_agencies(self):
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = "SELECT * FROM LawEnforcementAgencies"
            cursor.execute(query)
            results = cursor.fetchall()
            
            agencies = []
            for row in results:
                agency = LawEnforcementAgencies(
                    AgencyID = row['AgencyID'],
                    AgencyName = row['AgencyName'],
                    Jurisdiction = row['Jurisdiction'],
                    EmailAddress = row['EmailAddress']
                )
                agencies.append(agency)           
            return agencies
        
        except AgencyNotFoundException as e:
            print("Agency not found")    
        except Exception as e:
            raise DatabaseError(f"Failed to fetch law enforcement agencies: {str(e)}")
        
    def close_case_by_admin(self, incident_id):
        try:
            cursor = self.connection.cursor()
            update_query = """
                UPDATE Reports
                SET Status = 'Closed'
                WHERE IncidentID = %s AND Status = 'Finalized'
            """
            cursor.execute(update_query, (incident_id,))
            self.connection.commit()
            return cursor.rowcount
        
        except ReportNotFoundException as e:
            print("Report not found")
        except IncidentNotFoundException as e:
            print("Incident not found")
        except Exception as e:
            self.connection.rollback()
            raise DatabaseError(f"Failed to close case: {str(e)}")



        
    