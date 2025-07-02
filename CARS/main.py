from entity.auth import Authentication
from dao.CrimeAnalysisServiceImpl import CrimeAnalysisServiceImpl
from exceptions.user_defined_exceptions import AuthenticationError, DatabaseError, IncidentNotFoundException, SuspectNotFoundException, CriminalNotFoundException, ReportNotFoundException, DuplicateEntryException, AgencyNotFoundException
from entity.Suspects import Suspects
from entity.Incidents import Incidents
from entity.Reports import Reports
from entity.Officers import Officers
from entity.Criminals import Criminals
from entity.Victims import Victims
from datetime import datetime,date
import mysql.connector 

class MainModule:
    def __init__(self):
        self.service = CrimeAnalysisServiceImpl()
        self.current_user = None
    
    def run(self):
        print("=== Crime Reporting System ===")
        self.current_user = Authentication.public_access()
        
        while True:
            if self.current_user['Role'] == 'Public':
                self.public_menu()
            elif self.current_user['Role'] == 'Officer':
                self.officer_menu()
            elif self.current_user['Role'] == 'Admin':
                self.admin_menu()
    
    def public_menu(self):
        print("\n=== Public Menu ===")
        print("1. View recent incidents")
        print("2. View incidents by date range")
        print("3. View incidents by area/city")
        print("4. Login as officer/admin")
        print("0. Exit")
        
        try: 
            choice = int(input("Enter your choice: "))
            
            if choice == 1:
                try:
                    self.service.print_recent_incidents()
                except mysql.connector.Error as e:
                    raise DatabaseError(f"Database Connection Failed: {str(e)}")
                except Exception as e:
                    print(f"Unexpected error: {str(e)}")
            elif choice == 2:
                try:
                    startDate = input("Start date (YYYY-MM-DD): ")
                    endDate = input("End date (YYYY-MM-DD): ")
                    incidents = self.service.get_incidents_in_date_range_public(startDate, endDate)
                    if not incidents:
                        raise IncidentNotFoundException("Incidents not found within this date range.")
                    
                    print(f"\nIncidents that happened between '{startDate}' and '{endDate}: \n")
                    print("-------------------------------------------------------------")
                    for incident in incidents: 
                        print(f"Incident Type: {incident.incidentType}")
                        print(f"Incident Date: {incident.incidentDate}")
                        print(f"Area: {incident.area}")
                        print(f"City: {incident.city}")
                        print(f"Description: {incident.description}")
                        print("-------------------------------------------------------------")
                except IncidentNotFoundException as e: 
                    print(f"No incidents found: {str(e)}")
                except mysql.connector.Error as e:
                    raise DatabaseError(f"Database Connection Failed: {e.msg}") from e
                
            elif choice == 3:
                try:
                    print("\nLeave the field blank if you don't want that filter")
                    area = input("Enter area: ").strip()
                    city = input("Enter city: ").strip()
                    if not area and not city:
                        print("Both fields cannot be left empty.")
                        return
                    incidents = self.service.get_incidents_by_area_city_public(area, city)
                    if not incidents: 
                        raise IncidentNotFoundException("Incidents not found in this area and city.")
                    location = ", ".join(filter(None, [area, city]))
                    print(f"Incidents that happened in {location}:")
                    print("-------------------------------------------------------------")
                    for incident in incidents:
                        print(f"Incident Type: {incident['IncidentType']}")
                        print(f"Incident Date: {incident['IncidentDate']}")
                        if area: print(f"Area: {incident['Area']}")
                        if city: print(f"City: {incident['City']}")
                        print(f"Description: {incident['Description']}")
                        print("-------------------------------------------------------------") 
                except IncidentNotFoundException as e: 
                    print(f"No incidents found: {str(e)}")
                except mysql.connector.Error as e:
                    raise DatabaseError(f"Database Connection Failed: {str(e)}")
                    
            elif choice == 4:
                try:
                    self.current_user = Authentication.login()
                    print(f"Welcome, {self.current_user['Username']}!")
                except AuthenticationError as e:
                    print(f"Authentication Error: {str(e)}")
            elif choice == 0:
                print("\nExiting C.A.R.S System..\n")
                exit()
                
            else:
                print("Please enter a number between 0 -3")
                return
            
        except ValueError as e:
            print("Invalid Input")
        except Exception as e:
            print(f"Unknown Error: {str(e)}")
    
    def officer_menu(self):
        print(f"\n=== Officer Menu ===")
        print("\n-- Incident Management --")
        print("1. View all incident details with assignments")
        print("2. View my assigned incidents")
        print("3. Filter incidents")
        
        print("\n-- Suspect Management --")
        print("4. Access suspects database")
        print("5. Create new suspect record")
        print("6. Access criminals database")
        
        print("\n-- Case Management --")
        print("7. Create new victim record")
        print("8. View case details (victims/suspects/evidence)")
        print("9. Generate/Update case report")
        print("10. View case report")

        print("11. Logout")

        try:  
            choice = int(input("Enter choice: "))
            
            if choice == 1:
                try: 
                    incidents = self.service.viewAllIncidents()
                    
                    if not incidents: 
                        raise IncidentNotFoundException(f"No incidents are found.")
                    
                    print("\n=== All Incidents ===")    
                    for i, incident in enumerate(incidents, start=1):
                        print(f"\nIncident {i}:")
                        print(f"  ID          : {incident.incidentID}")
                        print(f"  Type        : {incident.incidentType}")
                        print(f"  Date        : {incident.incidentDate}")
                        print(f"  Area        : {incident.area}")
                        print(f"  City        : {incident.city}")
                        print(f"  Description : {incident.description}")
                        print(f"  Status      : {incident.status}")
                        print(f"  Officer ID  : {incident.officerID}")
                        print("-----------------------------------------------------------")
                except mysql.connector.Error as e:
                    raise DatabaseError(f"Database Connection Failed: {str(e)}")
                except Exception as e:
                    print(f"Unknown error: {str(e)}")    
            
            elif choice == 2:
                try:
                    officerID = self.current_user['UserID']
                    incidents = self.service.viewMyIncidents(officerID)
                    if not incidents: 
                        raise IncidentNotFoundException(f"No incidents are found.")
                    
                    print("==== My Assignments ====") 
                    for i, incident in enumerate(incidents, start=1):
                        print(f"\nIncident {i}:")
                        print(f"  ID          : {incident['IncidentID']}")
                        print(f"  Type        : {incident['IncidentType']}")
                        print(f"  Date        : {incident['IncidentDate']}")
                        print(f"  Area        : {incident['Area']}")
                        print(f"  City        : {incident['City']}")
                        print(f"  Description : {incident['Description']}")
                        print(f"  Status      : {incident['Status']}")
                        print(f"  Officer ID  : {incident['OfficerID']}")
                except mysql.connector.Error as e:
                    raise DatabaseError(f"Database Connection Failed: {str(e)}")
                except Exception as e:
                    print(f"Unknown error: {str(e)}")
                    
            elif choice == 3:
                try:
                    print("\n==== Filtering the Incidents ====\n")
                    print("Fill the parameters on whose basis you wish to filter and leave the rest blank")
                    print("\nDate Filters:")
                    start_date = input("Enter the start date (YYYY-MM-DD): ").strip()
                    end_date = input("Enter the end date (YYYY-MM-DD): ").strip()
                    area = input("Enter the area: ").strip()
                    city = input("Enter the city: ").strip()
                    incidentType = input("Enter the type of incident: ").strip()
                    officerID_input = input("Enter the Officer ID: ")
                    officerID = int(officerID_input) if officerID_input else None 
                    
                    incidents = self.service.get_filtered_incidents(start_date,end_date,area,city,incidentType,officerID)
                    if not incidents:
                        raise IncidentNotFoundException("Incidents not found.")
                    print("==== Filtered Results ====") 
                    for i, incident in enumerate(incidents, start=1):
                        print(f"\nIncident {i}:")
                        print(f"  ID          : {incident['IncidentID']}")
                        print(f"  Type        : {incident['IncidentType']}")
                        print(f"  Date        : {incident['IncidentDate']}")
                        print(f"  Area        : {incident['Area']}")
                        print(f"  City        : {incident['City']}")
                        print(f"  Description : {incident['Description']}")
                        print(f"  Status      : {incident['Status']}")
                        print(f"  Officer ID  : {incident['OfficerID']}") 
                    
                except mysql.connector.Error as e:
                    raise DatabaseError(f"Database Connection Failed: {str(e)}")
                except Exception as e:
                    print(f"Unknown error: {str(e)}")
                    
            elif choice == 4:
                try:
                    suspects = self.service.viewAllSuspects()
                    if not suspects:
                        raise SuspectNotFoundException(f"Suspects not found")
                    print("==== Suspects Database ====")
                    for suspect_incident in suspects:
                        suspect = suspect_incident.suspects
                        print(f"  Suspect ID                 : {suspect.suspectID}")
                        print(f"  Name                       : {suspect.firstName} {suspect.lastName}")
                        print(f"  Date of Birth              : {suspect.dateOfBirth}")
                        print(f"  Aadhaar Number             : {suspect.aadhaarNumber}")
                        print(f"  Address                    : {suspect.residentialAddress}")
                        print(f"  Contact Number             : {suspect.contactNumber}")

                        incident = suspect_incident.incidents
                        print(f"  Incident ID                : {incident.incidentID}")
                        print(f"  Incident Type              : {incident.incidentType}")
                        print(f"  Incident Date              : {incident.incidentDate}")
                        print(f"  Description                : {incident.description}")
                        print(f"  Status                     : {incident.status}")

                        print(f"  Role in Incident           : {suspect_incident.roleDescription}")
                        print(f"  Added By Officer           : {suspect_incident.officers}")
                    
                        records = self.service.suspectCriminalRelation(suspect.aadhaarNumber)
                        if records:
                            print("  Previous Criminal Record   : Yes")
                            for record in records:
                                print(f"  Criminal ID                : {record.criminalID}")
                        else:
                            print("  Previous Criminal Record   : No")
                        print("-"*60)
                except mysql.connector.Error as e:
                    raise DatabaseError(f"Database Connection Failed: {str(e)}")
                except Exception as e:
                    print(f"Unknown error: {str(e)}")    
                    
            elif choice == 5:
                try:
                    print("==== Adding a new Suspect ====")
                    firstName = input("First Name: ").strip()
                    lastName = input("Last Name: ").strip()

                    try:
                        dob_input = input("Date of Birth (YYYY-MM-DD): ").strip()
                        dateOfBirth = datetime.strptime(dob_input, "%Y-%m-%d").date()
                    except ValueError:
                        print("Invalid date format. Please enter as YYYY-MM-DD.")
                        return

                    gender = input("Gender: ").strip()
                    residentialAddress = input("Residential Address: ").strip()
                    contactNumber = int(input("Contact Number: "))
                    aadhaarNumber = int(input("Aadhaar Number: "))

                    incidentID = int(input("Incident ID involved: "))
                    officerID = int(input("Your Officer ID: "))
                    roleDescription = input("Role in Incident: ").strip()

                    new_suspect = Suspects(
                        FirstName=firstName,
                        LastName=lastName,
                        DateOfBirth=dateOfBirth,
                        Gender=gender,
                        ResidentialAddress=residentialAddress,
                        ContactNumber=contactNumber,
                        AadhaarNumber=aadhaarNumber
                    )

                    suspectID = self.service.addSuspect(new_suspect, incidentID, officerID, roleDescription)
                    if not suspectID:
                        raise DatabaseError("Failed to create suspect")
                    print(f"Suspect added successfully with ID: {suspectID}")

                except mysql.connector.Error as e:
                    raise DatabaseError(f"Database Connection Failed: {str(e)}")
                except DuplicateEntryException as e:
                    print(e)
                except Exception as e:
                    print(f"Unknown error: {str(e)}")
                      
            elif choice == 6:
                try:
                    criminals = self.service.viewAllCriminals()
                    if not criminals:
                        raise CriminalNotFoundException(f"Criminals not found")
                    print("==== Criminals Database ====")
                    for criminal in criminals:
                        print(f"  Criminal ID        : {criminal.criminalID}")
                        print(f"  Incident ID        : {criminal.incidentID}")
                        print(f"  Punishment Details : {criminal.punishmentDetails}")
                        print(f"  Aadhaar Number     : {criminal.aadhaarNumber}")

                        suspect = criminal.suspect
                        print(f"  First Name         : {suspect.firstName}")
                        print(f"  Last Name          : {suspect.lastName}")
                        print(f"  Date of Birth      : {suspect.dateOfBirth}")
                        print(f"  Address            : {suspect.residentialAddress}")
                        print(f"  Contact Number     : {suspect.contactNumber}")
                        print(f"  Gender             : {suspect.gender}")
                        print("-------------------------------------------------------------------")
                        
                except mysql.connector.Error as e:
                    raise DatabaseError(f"Database Connection Failed: {e.msg}") from e
                except Exception as e:
                    print(f"Unknown error: {str(e)}") 
            
            elif choice == 7:
                try:
                    print("=== Add a New Victim ===")
                    firstName = input("First Name: ").strip()
                    lastName = input("Last Name: ").strip()

                    try:
                        dob_input = input("Date of Birth (YYYY-MM-DD): ").strip()
                        dateOfBirth = datetime.strptime(dob_input, "%Y-%m-%d").date()
                    except ValueError:
                        print("Invalid date format. Please enter as YYYY-MM-DD.")
                        return

                    gender = input("Gender: ").strip()
                    residentialAddress = input("Residential Address: ").strip()
                    
                    try:
                        contactNumber = int(input("Contact Number: "))
                        aadhaarNumber = int(input("Aadhaar Number: "))
                    except ValueError:
                        print("Contact Number and Aadhaar Number must be numeric.")
                        return

                    try:
                        incidentID = int(input("Incident ID involved: "))
                        officerID = int(input("Your Officer ID: "))
                    except ValueError:
                        print("Incident ID and Officer ID must be numeric.")
                        return
                    roleDescription = input("Role in Incident: ").strip()

                    new_victim = Victims(
                        FirstName=firstName,
                        LastName=lastName,
                        DateOfBirth=dateOfBirth,
                        Gender=gender,
                        ResidentialAddress=residentialAddress,
                        ContactNumber=contactNumber,
                        AadhaarNumber=aadhaarNumber,
                        IncidentID=incidentID
                    )
                    victimID = self.service.addVictim(new_victim, incidentID, officerID, roleDescription)
                    
                    if victimID:
                        print(f"Victim successfully associated with Incident {incidentID}. Victim ID: {victimID}")
                    else:
                        print(f"Victim with Aadhaar {aadhaarNumber} already exists for Incident {incidentID}.")

                except IncidentNotFoundException:
                    print("Error: Incident not found. Please verify the Incident ID.")
                except Exception as e:
                    print(f"Unexpected error: {str(e)}")

            elif choice == 8:
                try:
                    print("View Case Related Resources: \n")
                    incidentID = int(input("Enter the Incident ID: "))
                    victims = self.service.get_victims_by_incident(incidentID)
                    if not victims:
                        print(f"No victims found regarding Incident {incidentID}")
                    else:
                        print(f"\nVictims related to Case {incidentID}: \n")
                        for victim in victims: 
                            print(f"Victim ID: {victim.victimID}")
                            print(f"First Name: {victim.firstName}")
                            print(f"Last Name: {victim.lastName}")
                            print(f"Date Of Birth: {victim.dateOfBirth}")
                            print(f"Gender: {victim.gender}")
                            print(f"Residential Address: {victim.residentialAddress}")
                            print(f"Contact Number: {victim.contactNumber}")
                            print(f"Aadhaar Number: {victim.aadhaarNumber}")
                            print("-------------------------------------------------------------------")                       
                    suspects = self.service.get_suspects_by_incident(incidentID)
                    if not suspects:
                        print(f"No suspects found regarding Incident {incidentID}")
                    else:
                        print(f"\nSuspects related to Case {incidentID}: \n")
                        for suspect_incident in suspects: 
                            suspect = suspect_incident.suspects  
                            print(f"Suspect ID: {suspect.suspectID}")
                            print(f"First Name: {suspect.firstName}")
                            print(f"Last Name: {suspect.lastName}")
                            print(f"Date Of Birth: {suspect.dateOfBirth}")
                            print(f"Gender: {suspect.gender}")
                            print(f"Residential Address: {suspect.residentialAddress}")
                            print(f"Contact Number: {suspect.contactNumber}")
                            print(f"Aadhaar Number: {suspect.aadhaarNumber}")
                            print(f"Role in Incident: {suspect_incident.roleDescription}")
                            print(f"Added By Officer: {suspect_incident.officers}")
                            print("-------------------------------------------------------------------")         
                    evidences = self.service.get_evidence_by_incident(incidentID)
                    if not evidences:
                        print(f"No evidences found regarding Incident {incidentID}")
                    else:
                        print(f"\nEvidences related to Case {incidentID}: \n")
                        for evidence in evidences: 
                            print(f"Evidence ID: {evidence.evidenceID}")
                            print(f"Evidence Name: {evidence.evidenceName}")
                            print(f"Description: {evidence.description}")
                            print(f"Location Found: {evidence.locationFound}")
                            print("-------------------------------------------------------------------")  
                except mysql.connector.Error as e:
                    raise DatabaseError(f"Database Connection Failed: {e.msg}") from e
                except Exception as e:
                    print(f"Unknown error: {str(e)}") 
                    
            elif choice == 9:
                try:
                    choice = input("Do you wish to generate an incident report or update an existing report (Generate/Update): ").strip().lower()
                    officer_id = self.current_user['UserID']                
                    if choice == 'generate':
                        print("\n=== Generate Case Report ===")
                        incident_id = input("Enter Incident ID: ").strip()
                        report_details = input("Enter Report Details: ").strip()
                        status = input("Enter Report Status (Draft/Finalized): ").strip()
                        report_date = date.today()

                        incident = Incidents(IncidentID=incident_id)
                        officer = Officers(OfficerID=officer_id)

                        new_report = Reports(
                            Incidents=incident,
                            Officers=officer,
                            ReportDate=report_date,
                            ReportDetails=report_details,
                            Status=status
                        )
                        reportID = self.service.generate_incident_report(new_report)
                        print(f"Report generated successfully! Report ID: {reportID}")
                    elif choice == 'update':
                        print("==== Update Case Report ====\n")
                        incident_id = input("Enter Incident ID: ").strip()
                        report_details = input("Enter Updated Report Details: ").strip()
                        status = input("Enter Updated Status (Draft/Finalized): ").strip()
                        report_date = date.today()

                        incident = Incidents(IncidentID=incident_id)
                        officer = Officers(OfficerID=officer_id)

                        updated_report = Reports(
                            Incidents=incident,
                            Officers=officer,
                            ReportDate=report_date,
                            ReportDetails=report_details,
                            Status=status
                        )
                        if self.service.update_incident_report(updated_report):
                            print("Report updated successfully!")
                        else:
                            raise ReportNotFoundException()
                except DuplicateEntryException as e:
                    print(f"Duplicate Entry found. {str(e)}")
                except ReportNotFoundException as e:
                    print(f"Report not found. {str(e)}")
                except DatabaseError as e:
                    print(f"Database Error: {str(e)}")
                except Exception as e:
                    print(f"Unexpected Error: {str(e)}")
            elif choice == 10:
                try:
                    incidentID = int(input("Enter Incident ID: "))
                    report = self.service.view_incident_report(incidentID)
                    if not report:
                       print(f"No report found for Incident ID {incidentID}") 
                    else:
                        print("\n======================== Incident Report ========================")
                        print(f"Incident ID     : {report['IncidentID']}")
                        print(f"Incident Type   : {report['IncidentType']}")
                        print(f"Area            : {report['Area']}")
                        print(f"City            : {report['City']}")
                        print(f"Description     : {report['Description']}")
                        print(f"Incident Status : {report['Status']}")
                        print(f"Report Date     : {report['ReportDate']}")
                        print(f"Report Details  : {report['ReportDetails']}")
                        print(f"Report Status   : {report['ReportStatus']}")

                except mysql.connector.Error as e:
                    raise DatabaseError(f"Database Connection Failed: {e.msg}") from e
                except Exception as e:
                    print(f"Unexpected error: {str(e)}")  
                                  
            elif choice == 11:
                self.current_user = Authentication.public_access()
                
            else:
                print("Please enter a number between 0 - 3")
                
        except ValueError as e:
            print(f"Invalid input {str(e)}")
        except Exception as e:
            print(f"Unknown Error: {str(e)}")
    
    def admin_menu(self):
        print(f"\n=== Admin Menu ({self.current_user['Username']}) ===")
        print("\n-- Records Management --")
        print("1. Create criminal record")
        print("2. Create incident record")
        print("3. Add new officer")
        print("4. View case assignments")
        print("5. View all law enforcement agencies")

        print("\n-- Analytics --")
        print("6. Officer performance dashboard")
        print("7. Criminal analytics")
        print("8. Crime pattern analytics")
        
        print("\n-- Case Oversight --")
        print("9. Finalize reports & update case status")

        print("10. Logout")
        
        try:
            choice = int(input("Enter choice: "))
            
            if choice == 1:
                try:
                    print("\n=== Add Criminal Record ===")
                    incidentID = input("Enter Incident ID: ")
                    aadhaarNumber = input("Enter Aadhaar Number of criminal: ")
                    punishmentDetails = input("Enter Punishment Details: ")

                    criminal = Criminals(
                        IncidentID=incidentID,
                        AadhaarNumber=aadhaarNumber,
                        PunishmentDetails=punishmentDetails
                    )

                    criminal_id = self.service.addCriminal(criminal)
                    if criminal_id:
                        print(f"Criminal added successfully. Criminal ID: {criminal_id}")
                    else:
                        print("Criminal entry already exists in the database.")

                except SuspectNotFoundException as e:
                    print(f"Suspect ID not found in the database.")
                except DatabaseError as e:
                    print(f"Database Error: {str(e)}")
                except Exception as e:
                    print(f"Unexpected error: {str(e)}")
                    
            elif choice == 2:
                try:
                    print("\n=== Create New Incident ===")
                    incident_type = input("Incident Type: ")
                    incident_date = input("Incident Date (YYYY-MM-DD): ")
                    area = input("Area: ")
                    city = input("City: ")
                    description = input("Description: ")
                    status = "Open"

                    print("\nSearching for officers in the area...")

                    officers = self.service.get_officers_by_location(city, area)
                    if not officers:
                        print("No officers found for this location.")
                        return

                    print("\nAvailable Officers:")
                    for officer in officers:
                        officer_id = officer['OfficerID']
                        case_count = self.service.count_open_incidents_by_officer(officer_id)
                        print(f"Officer ID     : {officer_id}")
                        print(f"Name           : {officer['FirstName']} {officer['LastName']}")
                        print(f"Posting City   : {officer['PostingCity']}")
                        print(f"Posting State  : {officer['PostingState']}")
                        print(f"Current Cases  : {case_count}")
                        print("-" * 30)

                    assigned_id = int(input("Enter Officer ID to assign this case to: "))

                    incident = Incidents(
                        IncidentType=incident_type,
                        IncidentDate=incident_date,
                        Area=area,
                        City=city,
                        Description=description,
                        Status=status,
                        OfficerID=assigned_id
                    )

                    incidentID = self.service.create_incident(incident)
                    if incidentID: 
                        print(f"Incident created with ID {incidentID} and assigned to Officer {assigned_id}")
                    else: 
                        print("Incident Creation Failed. Please try again. ")

                except DatabaseError as e:
                    print(f"Database Error: {str(e)}")
                except Exception as e:
                    print(f"Unexpected Error: {str(e)}")

            
            elif choice == 3:
                try:
                    print("\n=== Create New Officer Account ===")
                    first_name = input("First Name: ")
                    last_name = input("Last Name: ")
                    dob = input("Date of Birth (YYYY-MM-DD): ")
                    gender = input("Gender: ")
                    badge_number = input("Badge Number: ")
                    ranking = input("Ranking (e.g., Inspector, Sub-Inspector): ")
                    posting_city = input("Posting City: ")
                    posting_state = input("Posting State: ")
                    service_joining_date = input("Service Joining Date (YYYY-MM-DD): ")
                    address = input("Residential Address: ")
                    contact = input("Contact Number: ")
                    agency_id = input("Agency ID: ")

                    print("\n--- Login Credentials ---")
                    username = input("Username: ")
                    password = input("Password: ")

                    officer_data = {
                        'firstName': first_name,
                        'lastName': last_name,
                        'dateOfBirth': dob,
                        'gender': gender,
                        'badgeNumber': badge_number,
                        'ranking': ranking,
                        'postingCity': posting_city,
                        'postingState': posting_state,
                        'serviceJoiningDate': service_joining_date,
                        'residentialAddress': address,
                        'contactNumber': contact,
                        'agencyID': agency_id,
                        'username': username,
                        'password': password
                    }

                    officerID = self.service.create_officer(officer_data)
                    if officerID:
                        print(f"Officer account created successfully. ID: {officerID}")
                    else:
                        print("Failed to create officer account.")

                except mysql.connector.Error as e:
                    raise DatabaseError(f"Database Connection Failed: {e.msg}") from e
                except Exception as e:
                    print(f"Unexpected Error: {str(e)}")
                    
            elif choice == 4:
                try: 
                    incidents = self.service.viewAllIncidents()
                    
                    if not incidents: 
                        raise IncidentNotFoundException(f"No incidents are found.")
                    
                    print("\n=== All Incidents ===")    
                    for i, incident in enumerate(incidents, start=1):
                        print(f"\nIncident {i}:")
                        print(f"  ID          : {incident.incidentID}")
                        print(f"  Type        : {incident.incidentType}")
                        print(f"  Date        : {incident.incidentDate}")
                        print(f"  Area        : {incident.area}")
                        print(f"  City        : {incident.city}")
                        print(f"  Description : {incident.description}")
                        print(f"  Status      : {incident.status}")
                        print(f"  Officer ID  : {incident.officerID}")
                        print("-----------------------------------------------------------")
                except mysql.connector.Error as e:
                    raise DatabaseError(f"Database Connection Failed: {str(e)}")
                except Exception as e:
                    print(f"Unknown error: {str(e)}")   
                    
            elif choice == 5:  
                try:
                    agencies = self.service.view_all_agencies()
                    if not agencies:
                        print("No Law Enforcement Agencies found.")
                    else:
                        print("\n=== Law Enforcement Agencies ===")
                        for agency in agencies:
                            print(agency)  
                            print()
                            print("-" * 40)
                            
                except AgencyNotFoundException as e:
                    print("Agency not found.")
                except Exception as e:
                    print(f"Unexpected Error: {str(e)}")
        
            elif choice == 6:
                try:
                    dashboard_data = self.service.get_all_officer_dashboard()
                    print("\n==== Officer Dashboard ====")
                    if not dashboard_data:
                        print("No officer data available.")
                    else:
                        for officer in dashboard_data:
                            print("\n------------------------------")
                            print(f"Officer ID         : {officer['OfficerID']}")
                            print(f"Name               : {officer['FirstName']} {officer['LastName']}")
                            print(f"Badge Number       : {officer['BadgeNumber']}")
                            print(f"Ranking            : {officer['Ranking']}")
                            print(f"Posting Location   : {officer['PostingCity']}, {officer['PostingState']}")
                            print(f"Service Joined On  : {officer['ServiceJoiningDate']}")
                            print(f"Total Cases        : {officer['total_cases']}")
                            print(f"Cases Closed       : {officer['cases_closed']}")
                except mysql.connector.Error as e:
                    raise DatabaseError(f"Database connection error: {e.msg}") from e
                except Exception as e:
                    print(f"Unexpected error: {str(e)}")
                    
            elif choice == 7:  
                try:
                    analytics = self.service.get_criminal_analytics()

                    print("\n==== Criminal Analytics Dashboard ====")

                    print("\nTop 5 Most Frequent Criminals:")
                    if analytics['top_criminals']:
                        index = 1
                        for criminal in analytics['top_criminals']:
                            print(f"  {index}. {criminal['FirstName']} {criminal['LastName']} - {criminal['crime_count']} cases")
                            index += 1
                    else:
                        print("  No data found for top criminals.")

                    print("\nCrime Type Distribution:")
                    if analytics['crime_types']:
                        for crime_type in analytics['crime_types']:
                            print(f"  {crime_type} : {analytics['crime_types'][crime_type]}")
                    else:
                        print("  No crime type data available.")

                except mysql.connector.Error as e:
                    raise DatabaseError(f"Database connection error: {e.msg}") from e
                except Exception as e:
                    print(f"Unknown error: {str(e)}")
                    
            elif choice == 8: 
                try:
                    analytics = self.service.get_crime_analytics()

                    print("\n==== Crime Analytics Dashboard ====")

                    print("\nTop 5 Crime Hotspots (City & Area):")
                    if analytics['hotspots']:
                        index = 1
                        for row in analytics['hotspots']:
                            print(f"  {index}. {row['City']}, {row['Area']} - {row['crime_count']} incidents")
                            index += 1
                    else:
                        print("  No hotspot data found.")

                    print("\nCrime Count by Month:")
                    if analytics['monthly_trends']:
                        for month in analytics['monthly_trends']:
                            print(f"  {month} : {analytics['monthly_trends'][month]}")
                    else:
                        print("  No monthly trend data available.")

                except mysql.connector.Error as e:
                    raise DatabaseError(f"Database connection error: {e.msg}") from e
                except Exception as e:
                    print(f"Unexpected error: {str(e)}")
                    
            elif choice == 9:
                try:
                    reports = self.service.get_reports_by_status("Finalized")
                    if not reports:
                        print("No reports are pending for review.")
                    else:
                        print("\n=== Reports Pending Review ===")
                        for report in reports:
                            print(f"\nIncident ID     : {report['IncidentID']}")
                            print(f"Type            : {report['IncidentType']}")
                            print(f"Area/City       : {report['Area']}, {report['City']}")
                            print(f"Status          : {report['Status']}")
                            print(f"Report Date     : {report['ReportDate']}")
                            print(f"Report Details  : {report['ReportDetails']}")
                        
                        incidentID = int(input("\nEnter the Incident ID to close: "))

                        rows_updated = self.service.close_case_by_admin(incidentID)
                        if rows_updated:
                            print(f"Case status of Incident: {incidentID} updated to 'CLOSED' successfully.")
                        else:
                            print("Failed to update case status.")
                except Exception as e:
                    print(f"Unexpected Error: {str(e)}")

            elif choice == 10:
                self.current_user = Authentication.public_access()
                    
        except ValueError as e:
            print("Please enter a number between 0 - 3")
        except Exception as e:
            print(f"Unexpected Error: {str(e)}")

if __name__ == "__main__":
    app = MainModule()
    app.run()