# Inloggningsuppgifter till API (gäller tillfälligt):
# UserName= HackForSwedenUser;
# Password=Hack4Swe2;
# ApplicationIdentifier=HackForSweden

import sys
import getopt
from suds.client import Client
from suds import WebFault
import xmltodict
from suds.xsd.doctor import ImportDoctor, Import
from suds.sax.date import DateTime
import json
from flask import jsonify


class ArtDatabanken(object):

    def __init__(self):
        self.url = 'https://swedishspeciesobservation.artdatabankensoa.se/SwedishSpeciesObservationService.svc?singleWsdl'
        self.usr = 'HackForSwedenUser'
        self.pw = 'Hack4Swe2'
        self.appIdent = 'HackForSweden'
        self.session = ''
        self.wci = ''
        self.token = ''

        imp = Import('http://schemas.xmlsoap.org/soap/encoding/')
        imp.filter.add('ArtDatabanken.WebService.Data')
        doctor = ImportDoctor(imp)
    
        try:
            self.client = Client(self.url, doctor=doctor, retxml=True)
            res = self.client.service.Login(self.usr, self.pw, self.appIdent, 0)
            if(res):
                print("*** Logged in successfully. ***")
                self.session = xmltodict.parse(res)
                self.wci = self.client.factory.create(
                    'ns1:WebClientInformation')
                self.token = self.session['s:Envelope']['s:Body']['LoginResponse']['LoginResult']['a:Token']
                self.wci['Token'] = self.token
        except WebFault as e:
            print("*** Error loggin in: ", e)
            exit(1)

        except Exception as e:
            print("Error creating client: ", e)
            exit(1)
            

    def ping(self):
        online = self.client.service.Ping()
        if not online:
            print('*** Service not online. Exiting. ***')
            exit(1)
        print('*** Ping. Service is up and running. ***')
    
    def logout(self):
        try:
            res = self.client.service.Logout(self.wci)
            if(res):
                print("*** Logged out successfully. ***")
        except WebFault as e:
            print("*** Error logging out: ", e)
            exit(1)


    def getListOfMethods(self):
        return [method for method in self.client.wsdl.services[0].ports[0].methods]

    def getWebClientInformation(self):
        return self.client.factory.create('ns1:WebClientInformation')

    def getToken(self, session):
        return self.session['s:Envelope']['s:Body']['LoginResponse']['LoginResult']['a:Token']

    def getSpeciesObservationsByIds(self, observationId, coordinateSystem):
        aol = self.client.factory.create('ns3:ArrayOflong')
        aol.long.append(observationId)
        cs = self.client.factory.create('ns1:WebCoordinateSystem')
        csId = self.client.factory.create('ns0:CoordinateSystemId')
        soc = self.client.factory.create('ns1:WebSpeciesObservationSpecification')
        cs.Id = csId.coordinateSystem
        return self.client.service.GetSpeciesObservationsByIds(self.wci, aol, cs, soc)

    def getSpeciesObservationSearchCriteria(self, taxonId):
        sc = self.client.factory.create('ns1:WebSpeciesObservationSearchCriteria')
        ints = self.client.factory.create('ns3:ArrayOfint')
        ints.int.append(taxonId)
        sc['TaxonIds'] = ints
        cs = self.client.factory.create('ns1:WebCoordinateSystem')
        csId = self.client.factory.create('ns0:CoordinateSystemId')
        cs.Id = csId.WGS84
        return self.client.service.GetSpeciesObservationCountBySearchCriteria(self.wci, sc, cs)

    def getSpeciesObservationsBySearchCriteria(self, taxonId):
        sc = self.client.factory.create('ns1:WebSpeciesObservationSearchCriteria')
        ints = self.client.factory.create('ns3:ArrayOfint')
        ints.int.append(taxonId)
        sc['TaxonIds'] = ints
        cs = self.client.factory.create('ns1:WebCoordinateSystem')
        csId = self.client.factory.create('ns0:CoordinateSystemId')
        cs.Id = csId.WGS84
        return self.client.service.GetSpeciesObservationsBySearchCriteria(self.wci, sc, cs)

    def getSpeciesObservationCoordinatesBySearchCriteria(self, taxonId):
        print("*** Calling getSpeciesObservationCoordinatesBySearchCriteria() ***")
        sc = self.client.factory.create('ns1:WebSpeciesObservationSearchCriteria')
        ints = self.client.factory.create('ns3:ArrayOfint')
        ints.int.append(taxonId)
        sc['TaxonIds'] = ints

        dateTimeSearchCriteria = self.client.factory.create('ns1:WebDateTimeSearchCriteria')

        dateTimeBegin = self.client.factory.create('ns2:dateTime')
        
        print(dateTimeBegin)

        print(sc.ObservationDateTime.Begin)
        sc.ObservationDateTime.Begin = dateTimeBegin
        print(sc.ObservationDateTime.Begin)
        #print("printing taxonids")
        #print(sc.TaxonIds)
        #dateTimeSearchCriteria['Begin'] = dt
        #print(observationDateTime)
        #sc[observationDateTime] = observationDateTime
        #sc[dateTimeSearchCriteria] = 'observationDateTime'
        #print(sc.ObservationDateTime)
        #print(" ***** ")
        #print(observationDateTime)

        #sc.ObservationDateTime = dateTimeSearchCriteria

        cs = self.client.factory.create('ns1:WebCoordinateSystem')
        csId = self.client.factory.create('ns0:CoordinateSystemId')
        cs.Id = csId.WGS84
        observations = self.client.service.GetSpeciesObservationCoordinatesBySearchCriteria(self.wci, sc, cs)
        observationsJSON = json.loads(json.dumps(xmltodict.parse(observations), ensure_ascii=False))
        observationsCoordinates = observationsJSON['s:Envelope']['s:Body']['GetSpeciesObservationCoordinatesBySearchCriteriaResponse']['GetSpeciesObservationCoordinatesBySearchCriteriaResult']['a:WebSpeciesObservationCoordinate']
        self.logout()
        return jsonify(observationsCoordinates)
    
    def writeToFile(self, blob):
        with open('data.txt', 'wb') as file:
            file.write(blob)
