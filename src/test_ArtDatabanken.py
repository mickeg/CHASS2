import pytest
from ArtDatabanken import ArtDatabanken

adb = ArtDatabanken()


@pytest.fixture
def adbInstance():
    '''Returns an instance of Artdatabanken'''
    return adb

def test_adb_url(adbInstance):
    assert adbInstance.url == 'https://swedishspeciesobservation.artdatabankensoa.se/SwedishSpeciesObservationService.svc?singleWsdl'

def test_adb_username(adbInstance):
    assert adbInstance.usr == 'HackForSwedenUser'

def test_adb_password(adbInstance):
    assert adbInstance.pw == 'Hack4Swe2'

def test_adb_appidentifier(adbInstance):
    assert adbInstance.appIdent == 'HackForSweden'

