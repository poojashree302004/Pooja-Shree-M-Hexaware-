CREATE DATABASE CrimeReportingSystem;
USE CrimeReportingSystem;

-- Creating LawEnforcementAgencies table
CREATE TABLE LawEnforcementAgencies 
(
	AgencyID INT AUTO_INCREMENT PRIMARY KEY, 
    AgencyName VARCHAR(150),
    Jurisdiction VARCHAR(100),
    EmailAddress VARCHAR(250)
)AUTO_INCREMENT = 500;

-- Creating Officers Table
CREATE TABLE Officers (
    OfficerID INT AUTO_INCREMENT PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    DateOfBirth DATE,
    Gender VARCHAR(20),
    BadgeNumber VARCHAR(20),
    Ranking VARCHAR(30),
    PostingCity VARCHAR(30),
    PostingState VARCHAR(30),
    ServiceJoiningDate DATE,
    ResidentialAddress TEXT,
    ContactNumber BIGINT,
    AgencyID INT,
    CONSTRAINT fk_Officers_LawEnforcementAgencies 
    FOREIGN KEY(AgencyID) 
    REFERENCES LawEnforcementAgencies(AgencyID)
)AUTO_INCREMENT = 1;

-- Creating Incidents Table
CREATE TABLE Incidents (
    IncidentID INT AUTO_INCREMENT PRIMARY KEY,
    IncidentType VARCHAR(100),
    IncidentDate DATE,
    Area VARCHAR(100),
    City VARCHAR(100),
    Description TEXT,
    Status ENUM ('Open', 'Under Investigation', 'Closed') NOT NULL DEFAULT 'Open',
    OfficerID INT,
    CONSTRAINT fk_Incidents_Officers
    FOREIGN KEY(OfficerID) 
    REFERENCES Officers(OfficerID)
)AUTO_INCREMENT = 1;

-- Creating Victims table
CREATE TABLE Victims (
    VictimID INT AUTO_INCREMENT PRIMARY KEY,
    FirstName VARCHAR(50),	
    LastName VARCHAR(50),
    DateOfBirth DATE,
    Gender VARCHAR(50),
    ResidentialAddress TEXT, 
    ContactNumber BIGINT,
    AadhaarNumber BIGINT,
    IncidentID INT,
    CONSTRAINT fk_Victims_Incidents 
    FOREIGN KEY(IncidentID) 
    REFERENCES Incidents(IncidentID)
)AUTO_INCREMENT = 100;

-- Creating Suspects table
CREATE TABLE Suspects
(
	SuspectID INT AUTO_INCREMENT PRIMARY KEY, 
    FirstName VARCHAR(100),
    LastName VARCHAR(100),
    DateOfBirth DATE, 
    Gender VARCHAR(50),
    ResidentialAddress TEXT,
    ContactNumber BIGINT,
    AadhaarNumber BIGINT UNIQUE
)AUTO_INCREMENT = 1000;

-- Creating Evidence Table
CREATE TABLE Evidence (
    EvidenceID INT AUTO_INCREMENT PRIMARY KEY,
    EvidenceName VARCHAR(20),
    Description TEXT,
    LocationFound TEXT,
    IncidentID INT,
    CONSTRAINT fk_Evidence_Incidents 
    FOREIGN KEY(IncidentID) 
    REFERENCES Incidents(IncidentID)
)AUTO_INCREMENT = 1;

-- Creating Reports Table
CREATE TABLE Reports (
    ReportID INT AUTO_INCREMENT PRIMARY KEY,
    IncidentID INT,
    ReportingOfficerID INT,
    ReportDate DATE,
    ReportDetails TEXT,
    STATUS ENUM('Draft', 'Finalized', 'Closed') NOT NULL DEFAULT 'Draft',
    CONSTRAINT fk_Reports_Incidents FOREIGN KEY(IncidentID) REFERENCES Incidents(IncidentID),
    CONSTRAINT fk_Reports_Officers FOREIGN KEY(ReportingOfficerID) REFERENCES Officers(OfficerID)
)AUTO_INCREMENT = 100;

CREATE TABLE Criminals (
	CriminalID INT AUTO_INCREMENT PRIMARY KEY,
    IncidentID INT, 
    SuspectID INT,
    AadhaarNumber BIGINT UNIQUE,
    PunishmentDetails TEXT,
    CONSTRAINT fk_Criminals_Incidents FOREIGN KEY(IncidentID) REFERENCES Incidents(IncidentID),
    CONSTRAINT fk_Criminals_Suspects FOREIGN KEY(SuspectID) REFERENCES Suspects(SuspectID)
)AUTO_INCREMENT = 1;

CREATE TABLE Users (
    UserID INT AUTO_INCREMENT PRIMARY KEY,
    Username VARCHAR(50) UNIQUE NOT NULL,
    Password VARCHAR(100) NOT NULL,
    Role ENUM('Officer', 'Admin') NOT NULL,  
    OfficerID INT NULL,
    FOREIGN KEY (OfficerID) REFERENCES Officers(OfficerID)
);

CREATE TABLE SuspectIncidents (
	SuspectID INT,
    IncidentID INT,
    AadhaarNumber BIGINT,
    RoleDescription TEXT,
    AddedByOfficerID INT,
    PRIMARY KEY(SuspectID, IncidentID),
    CONSTRAINT fk_SuspectIncidents_Suspects
    FOREIGN KEY(SuspectID) 
    REFERENCES Suspects(SuspectID),
    CONSTRAINT fk_SuspectIncidents_Incidents 
    FOREIGN KEY(IncidentID) 
    REFERENCES Incidents(IncidentID),
    CONSTRAINT fk_SuspectIncidents_Officers
    FOREIGN KEY(AddedByOfficerID) 
    REFERENCES Officers(OfficerID)
);

