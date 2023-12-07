import json
import os
import hashlib
import time
import sys
from ZvolvArithmetic.zauthentication.server_configuration import EnvVariables
from ZvolvArithmetic.zauthentication import excute_apis
from ZvolvArithmetic.zauthentication.loggerClass import LoggerClass as LogClass

folder_path = "/tmp"            # For server
# folder_path = os.getcwd()     # For local testing
CACHE_FILE_NAME = 'token_cache.json'
CACHE_FILE_PATH = os.path.join(folder_path, CACHE_FILE_NAME)
zvolv_business_tag_id = "98NCMBD2KBZ4R"

def load_token_cache():
    # Checking whether file is present or not
    if not os.path.isfile(CACHE_FILE_PATH):
        # Creating file with value {}
        with open(CACHE_FILE_PATH, 'w') as file:
            json.dump({}, file)

    # Reading value from file
    with open(CACHE_FILE_PATH, 'r') as cache_file:
        return json.load(cache_file)


def save_token_cache(token_cache):
    with open(CACHE_FILE_PATH, 'w') as cache_file:
        json.dump(token_cache, cache_file)


def zlogin(zvolv_access_key_id, zvolv_secret_access_key, zvolv_domain_context, zvolv_business_tag_id):
    token_cache = load_token_cache()
    business_domain, business_tag = zvolv_domain_context, zvolv_business_tag_id

    # Check if the token is already created and stored. Also, check if it should not be older than 60 seconds.
    if token_cache and business_domain in token_cache and token_cache and (time.time() - token_cache[business_domain]["serverTime"]) < 60:
        return token_cache[business_domain]

    # sha512pwd = hashlib.sha512(EnvVariables.get_admin_password()).hexdigest()
    # payload = {'email': EnvVariables.get_admin_email(), 'password': sha512pwd}

    email_id = zvolv_access_key_id
    sha512pwd = hashlib.sha512(zvolv_secret_access_key.encode('utf-8')).hexdigest()
    payload = {'email': email_id, 'password': sha512pwd}
    headers = {'businessDomain': business_domain, 'jwt': 'true', 'businessTagID': business_tag ,'Device':'browser'}
    # login_url = EnvVariables.get_localhost_url() + EnvVariables.get_api_17_version() + "user/login"
    login_url = "https://zvolv.co/rest/v17/user/login"

    login_response = excute_apis.execute(rest_url=login_url, method="POST", data=payload, headers=headers)
    # LogClass.warning("api-logs", {"message": "Logging Response", "response": login_response})

    if login_response:
        # Create login data to store in file
        token_cache = {
            business_domain: {}
        }
        for key, value in login_response.items():
            token_cache[business_domain][key] = value
        save_token_cache(token_cache)
        return login_response
    else:
        raise Exception('Failed to get login token')


def get_request_configs():
    if request:
        if request.headers.get("Businessdomain") == "lk-nso":
            return request.headers.get("Businessdomain"), "W4S3L2ZEFRVT2"
        else:
            return request.headers.get("Businessdomain"), "98NCMBD2KBZ4R"
    else:
        return "yogeshjadhav","98NCMBD2KBZ4R"

def generate_login_token(zvolv_access_key_id,zvolv_secret_access_key, zvolv_domain_context, zvolv_business_tag_id):
    login = zlogin(zvolv_access_key_id, zvolv_secret_access_key, zvolv_domain_context, zvolv_business_tag_id)
    print(login)
    return login["loginToken"]


def generate_request_headers(zvolv_access_key_id, zvolv_secret_access_key, zvolv_domain_context):
    business_domain = zvolv_domain_context
    auth_key = generate_login_token(zvolv_access_key_id, zvolv_secret_access_key, zvolv_domain_context, zvolv_business_tag_id)
    headers = {'domain': business_domain, 'Authorization': 'bearer ' + auth_key, 'Content-Type': 'application/json'}
    return headers