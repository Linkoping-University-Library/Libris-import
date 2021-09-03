import requests
import json
import os
import logging
from dotenv import load_dotenv


class FolioCommunication:

    def __init__(self):

        # Initialize environment variables
        load_dotenv()
        self.folio_endpoint = os.environ['FOLIO_ENDPOINT']
        self.username = os.environ['USERNAME']
        self.password = os.environ['PASSWORD']
        self.okapi_tenant = os.environ['OKAPI_TENANT']
        self.payload = {'username': self.username,
                        'password': self.password}

        # Define generic header without okapi token
        self.header = {'Accept': 'application/json',
                       'Content-Type': 'application/json',
                       'x-okapi-tenant': self.okapi_tenant}

        # Fetch okapi token
        self.okapi_token = self.getToken()

        # Add okapi token to header
        self.header['x-okapi-token'] = self.okapi_token

    def getToken(self):
        logging.info('Hämtar okapi token.')
        path = '/authn/login'
        url = self.folio_endpoint + path

        response = requests.post(url, data=json.dumps(
            self.payload), headers=self.header)
        okapiToken = response.headers['x-okapi-token']
        logging.info('Hämtade okapi token.')

        return okapiToken

    def uploadDefinitions(self, filename):
        path = '/data-import/uploadDefinitions'
        url = self.folio_endpoint + path
        payload = {'fileDefinitions': [{'name': filename}]}

        response = requests.post(
            url, data=json.dumps(payload), headers=self.header)

        return response.json()

    def uploadFile(self, uploadDefinitionId, fileDefinitionId, data):
        path = '/data-import/uploadDefinitions/' + uploadDefinitionId + '/files/' + fileDefinitionId
        url = self.folio_endpoint + path

        header = {'Content-Type': 'application/octet-stream',
                'x-okapi-tenant': self.okapi_tenant,
                'X-Okapi-Token': self.okapi_token}

        response = requests.post(url, data=data, headers=header)

        return response.json()

    def processFile(self, uploadDefinitionId, data):
        path = '/data-import/uploadDefinitions/' + uploadDefinitionId + '/processFiles?defaultMapping=true'
        url = self.folio_endpoint + path

        response = requests.post(url, data=json.dumps(data), headers=self.header)

        return response
