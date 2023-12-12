import os
import json
import os
import hashlib
import sys
import requests
from zvolv_sdk.server_configuration import EnvVariables

class Client():
    def __init__(
        self,
        zvolv_user_id: str = EnvVariables.get_zvolv_user_id(),
        zvolv_password: str = EnvVariables.get_zvolv_password(),
        zvolv_domain: str = EnvVariables.get_zvolv_domain(),
        zvolv_business_tag_id: str = "98NCMBD2KBZ4R",
        zvolv_service_url: str = EnvVariables.get_zvolv_localhost_url()
        
    ) -> None:
        self.zvolv_user_id = zvolv_user_id
        self.zvolv_password = zvolv_password
        self.zvolv_domain = zvolv_domain
        self.zvolv_business_tag_id = zvolv_business_tag_id
        self.zvolv_service_url = zvolv_service_url
    
    def __repr__(self):
        return '{}'.format(
            repr(self.login()),
        )

    def login(self):
        sha512pwd = hashlib.sha512(self.zvolv_password.encode('utf-8')).hexdigest()
        payload = {'email': self.zvolv_user_id, 'password': sha512pwd}
        headers = {'businessDomain': self.zvolv_domain, 'jwt': 'true', 'businessTagID': self.zvolv_business_tag_id ,'Device':'browser'}
        login_url = f"{self.zvolv_service_url}{EnvVariables.get_api_17_version()}user/login"
        login_response = requests.post(url=login_url, data=payload, headers=headers)
        print("****",login_response.status_code)

        if login_response.status_code == 200:
            json_response = login_response.json()
            return json_response
        else:
            raise Exception()