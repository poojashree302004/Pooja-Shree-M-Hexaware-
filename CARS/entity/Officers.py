class Officers():
    def __init__(self, OfficerID = None, FirstName = None, LastName = None, DateOfBirth = None, Gender = None, BadgeNumber = None, Ranking = None, PostingCity = None, PostingState = None, ServiceJoiningDate = None, ResidentialAddress = None, ContactNumber = None, LawEnforcementAgency = None):
        self.__OfficerID = OfficerID
        self.__FirstName = FirstName
        self.__LastName = LastName
        self.__DateOfBirth = DateOfBirth
        self.__Gender = Gender
        self.__BadgeNumber = BadgeNumber
        self.__Ranking = Ranking
        self.__PostingCity = PostingCity
        self.__PostingState = PostingState
        self.__ServiceJoiningDate = ServiceJoiningDate
        self.__ResidentialAddress = ResidentialAddress
        self.__ContactNumber = ContactNumber
        self.__LawEnforcementAgency = LawEnforcementAgency
    
    @property
    def officerID(self):
        return self.__OfficerID
        
    @property
    def firstName(self):
        return self.__FirstName
    
    @property
    def lastName(self):
        return self.__LastName
    
    @property
    def dateOfBirth(self):
        return self.__DateOfBirth
    
    @property
    def gender(self):
        return self.__Gender
    
    @property
    def badgeNumber(self):
        return self.__BadgeNumber
    
    @property
    def ranking(self):
        return self.__Ranking
    
    @property
    def postingCity(self):
        return self.__PostingCity
    
    @property
    def postingState(self):
        return self.__PostingState
    
    @property
    def serviceJoiningDate(self):
        return self.__ServiceJoiningDate
    
    @property
    def residentialAddress(self):
        return self.__ResidentialAddress
    
    @property
    def contactNumber(self):
        return self.__ContactNumber
    @property
    def lawEnforcementAgency(self):
        return self.__AgencyID
    
    @officerID.setter
    def get_officerID(self, value):
        self.__OfficerID = value
        
    @firstName.setter
    def get_firstName(self, value):
        self.__FirstName = value
        
    @lastName.setter
    def get_lastName(self, value):
        self.__LastName = value
        
    @dateOfBirth.setter
    def get_dateOfBirth(self, value):
        self.__DateOfBirth = value
        
    @gender.setter
    def get_gender(self, value):
        self.__Gender = value
        
    @badgeNumber.setter
    def get_badgeNumber(self, value):
        self.__BadgeNumber = value
        
    @ranking.setter
    def get_ranking(self, value):
        self.__Ranking = value
        
    @postingCity.setter
    def get_postingCity(self, value):
        self.__PostingCity = value
        
    @serviceJoiningDate.setter
    def get_serviceJoiningDate(self, value):
        self.__ServiceJoiningDate = value
        
    @residentialAddress.setter
    def get_residentialAddress(self, value):
        self.__ResidentialAddress = value
        
    @contactNumber.setter
    def get_contactNumber(self, value):
        self.__ContactNumber = value
        
    # @agencyID.setter
    # def get_agencyID(self, value):
    #     self.__AgencyID = value
        
    # def __str__(self):
    #     return f"Officer ID: {self.__OfficerID} \nFirst Name: {self.__FirstName} \nLast Name: {self.__LastName} \nDate Of Birth: {self.__DateOfBirth} \nGender: {self.__Gender} \nBadge Number: {self.__BadgeNumber} \nRanking: {self.__Ranking} \nPosting City: {self.__PostingCity} \nPosting State: {self.__PostingState} \nService Joining Date: {self.__ServiceJoiningDate} \nResidential Address: {self.__ResidentialAddress} \nContact Number: {self.__ContactNumber} \nAgency ID: {self.__AgencyID}"
    
    