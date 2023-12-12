import os
import json
import os
import hashlib
import sys
import time
import requests
from zvolv_sdk.server_configuration import EnvVariables

class Client_one():

    #folder_path = "/tmp"            # For server
    folder_path = os.getcwd()     # For local testing
    CACHE_FILE_NAME = 'token_cache.json'
    CACHE_FILE_PATH = os.path.join(folder_path, CACHE_FILE_NAME)

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

    def load_token_cache(self):
        """ Checking whether file is present or not, Creating file with value {} and  Reading value from file """
        if not os.path.isfile(self.CACHE_FILE_PATH):
            with open(self.CACHE_FILE_PATH, 'w') as file:
                json.dump({}, file)

        with open(self.CACHE_FILE_PATH, 'r') as cache_file:
            return json.load(cache_file)

    def save_token_cache(self,token_cache):
        with open(self.CACHE_FILE_PATH, 'w') as cache_file:
            json.dump(token_cache, cache_file)
    

    def login(self):
            token_cache = self.load_token_cache()
            business_domain = self.zvolv_domain
            if token_cache and business_domain in token_cache and token_cache and (time.time() - token_cache[business_domain]["serverTime"]) < 60:
                return token_cache[business_domain]

            sha512pwd = hashlib.sha512(self.zvolv_password.encode('utf-8')).hexdigest()
            payload = {'email': self.zvolv_user_id, 'password': sha512pwd}
            headers = {'businessDomain': self.zvolv_domain, 'jwt': 'true', 'businessTagID': self.zvolv_business_tag_id ,'Device':'browser'}
            login_url = f"{self.zvolv_service_url}{EnvVariables.get_api_17_version()}user/login"
            login_response = requests.post(url=login_url, data=payload, headers=headers)

            if login_response.status_code == 200:
                token_cache = {
                    business_domain: {}
                }
                login_response = login_response.json()
                for key, value in login_response.items():
                    token_cache[business_domain][key] = value
                self.save_token_cache(token_cache)
                return login_response
            else:
                raise Exception()