import os
import json
import os
import hashlib
import time
import sys
import requests
from zvolv_sdk.server_configuration import EnvVariables

class Client():
    def __init__(
        self,
        zvolv_access_key_id: str = EnvVariables.get_admin_email(),
        zvolv_secret_access_key: str = EnvVariables.get_admin_password(),
        zvolv_domain_context: str = EnvVariables.get_business_domain(),
        zvolv_business_tag_id: str = "98NCMBD2KBZ4R",
        zvolv_url: str =  "https://zvolv.co/rest/v17/user/login"
        
    ) -> None:
        self.zvolv_access_key_id = zvolv_access_key_id
        self.zvolv_secret_access_key = zvolv_secret_access_key
        self.zvolv_domain_context = zvolv_domain_context
        self.zvolv_business_tag_id = zvolv_business_tag_id
        self.zvolv_url = zvolv_url
    
    def __repr__(self):
        return '{}'.format(
            repr(self.login()),
        )

    def login(self):
        sha512pwd = hashlib.sha512(self.zvolv_secret_access_key.encode('utf-8')).hexdigest()
        payload = {'email': self.zvolv_access_key_id, 'password': sha512pwd}
        headers = {'businessDomain': self.zvolv_domain_context, 'jwt': 'true', 'businessTagID': self.zvolv_business_tag_id ,'Device':'browser'}
        login_url = self.zvolv_url
        login_response = self.execute(rest_url=login_url, method="POST", data=payload, headers=headers)
        if login_response.status_code == 200:
            json_response = login_response.json()
            return json_response
        else:
            print(f"Error: {login_response.status_code} - {response.text}")


    def execute(self,**kwargs):
        if kwargs['method'] == "GET":
            return requests.get(url=kwargs['rest_url'], headers=kwargs['headers'])
        elif kwargs['method'] == "POST":
            return requests.post(url=kwargs['rest_url'], data=kwargs['data'], headers=kwargs['headers'])
        elif kwargs['method'] == "PUT":
            return requests.put(url=kwargs['rest_url'], data=kwargs['data'], headers=kwargs['headers'])