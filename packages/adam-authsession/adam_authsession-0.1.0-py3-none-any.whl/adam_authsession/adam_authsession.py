from adam_credmanager import adam_credmanager
from io import StringIO
import shutil
import binascii
import collections
import datetime
import hashlib
import sys
from urllib.parse import quote
from google.oauth2 import service_account
from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession
import os


# pip install six
import six
class Adam_token():
    def __init__(self, service_url, secret_name, project_id=None):
        self.projet_id=project_id
        self.json_file_name="auth_file.json"
        self.service_url=service_url
        self.secret_name=secret_name
    
    def getAuthSessionWithoutCache(self):
        self.__get_secret(secret_name=self.secret_name)
        credentials = service_account.IDTokenCredentials.from_service_account_file(
        self.json_file_name, target_audience=self.service_url)
        self.authed_session = AuthorizedSession(credentials)
        self.__cleanSecret()
        return self.authed_session

    def request(self, service_url):
        response = self.authed_session.get(service_url)
        return response
    
    def __cleanSecret(self):
            if os.path.exists(self.json_file_name):
                os.remove(self.json_file_name)
            else:
                print("The file does not exist")
    
    def __get_secret(self, secret_name):
        acm=adam_credmanager(self.projet_id)
        KF=StringIO(acm.get_secret(secret_name))
        try:
            with open(self.json_file_name, 'w') as fd:
                KF.seek(0)
                shutil.copyfileobj(KF, fd)
        except Exception as fserror:
            print("Error al escribir recuperar el certificado privado del fs", fserror)
            raise