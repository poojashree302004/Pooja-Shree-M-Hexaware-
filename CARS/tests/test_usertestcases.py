import sys
import os
import pytest

# Ensure proper path for importing project modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from entity.Suspects import Suspects
from entity.auth import Authentication
from exceptions.user_defined_exceptions import AuthenticationError, DatabaseError
from dao.CrimeAnalysisServiceImpl import CrimeAnalysisServiceImpl

service = CrimeAnalysisServiceImpl()

# ✅ Public access test
def test_public_access():
    user = Authentication.public_access()
    assert user['Role'] == 'Public'
    assert user['Username'] == 'public_user'

# ✅ Login invalid test
def test_login_invalid(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: 'wrong_user')
    monkeypatch.setattr('entity.auth.getpass', lambda _: 'wrong_pass')
    with pytest.raises(AuthenticationError):
        Authentication.login()

# ✅ Get officers by location
def test_get_officers_by_location():
    officers = service.get_officers_by_location("coimbatore", "Coimbatore")
    assert isinstance(officers, list)

# ✅ No incidents in ancient date range
def test_get_incidents_in_date_range_public_no_results():
    results = service.get_incidents_in_date_range_public("1900-01-01", "1900-01-02")
    assert isinstance(results, list)
    assert len(results) == 0

# ✅ Filter by city only
def test_get_incidents_by_area_city_public_city_only():
    results = service.get_incidents_by_area_city_public(area=None, city="coimbatore")
    assert isinstance(results, list)

# ✅ Invalid area + city should return empty list
def test_get_incidents_by_area_city_public_invalid():
    results = service.get_incidents_by_area_city_public(area="fakearea", city="fakecity")
    assert isinstance(results, list)
    assert len(results) == 0

# ✅ Filtered incidents combination
def test_filtered_incidents_combination():
    results = service.get_filtered_incidents(
        start_date="2020-01-01",
        end_date="2020-12-31",
        area="Coimbatore",
        city="coimbatore",
        incident_type="theft",
        officer_id=None
    )
    assert isinstance(results, list)

# ✅ Invalid officer ID returns empty list
def test_view_my_incidents_invalid():
    invalid_officer_id = -9999
    result = service.viewMyIncidents(invalid_officer_id)
    assert isinstance(result, list)
    assert len(result) == 0

# ✅ Add suspect twice (second time should fail)
def test_add_duplicate_suspect():
    suspect = Suspects(
        FirstName="John",
        LastName="Doe",
        DateOfBirth="1990-01-01",
        Gender="M",
        ResidentialAddress="Some Street",
        ContactNumber=9876543210,
        AadhaarNumber=123456689112
    )
    incidentID = 1
    officerID = 1
    roleDescription = "Suspect in prior theft"

    try:
        service.addSuspect(suspect, incidentID, officerID, roleDescription)
    except Exception:
        pass  # Allow first insert to silently fail if already exists

    with pytest.raises(DatabaseError):
        service.addSuspect(suspect, incidentID, officerID, roleDescription)

# ✅ Invalid suspect data
def test_add_invalid_suspect_data():
    suspect = Suspects(
        FirstName=None,
        LastName="",
        DateOfBirth="not-a-date",
        Gender="",
        ResidentialAddress=None,
        ContactNumber="abc123",
        AadhaarNumber=None
    )
    with pytest.raises(DatabaseError):
        service.addSuspect(suspect, 1, 1, "Invalid data")

# ✅ View all suspects: check response structure
def test_view_all_suspects_returns_list():
    suspects = service.viewAllSuspects()
    assert isinstance(suspects, list)
    if suspects:
        item = suspects[0]
        assert hasattr(item, "suspects")
        assert hasattr(item, "incidents")
        assert hasattr(item, "roleDescription")
        assert hasattr(item, "officers")
