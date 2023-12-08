import os
from dotenv import load_dotenv

class EnvVariables(object):
    if(os.path.exists("../../.env")):
        load_dotenv()

    @staticmethod
    def get_val(key):
        return os.environ[key] if key in os.environ else None

    @staticmethod
    def get_localhost_url():
        return EnvVariables.get_val('LOCALHOST_URL')

    @staticmethod
    def get_api_base_url():
        return EnvVariables.get_val('BASE_URL')

    @staticmethod
    def get_api_version():
        return EnvVariables.get_val('API_VERSION')

    @staticmethod
    def get_api_17_version():
        return EnvVariables.get_val('API_VERSION_17')

    @staticmethod
    def get_admin_email():
        return EnvVariables.get_val('ADMIN_EMAIL')

    @staticmethod
    def get_admin_password():
        return EnvVariables.get_val('ADMIN_PASSWORD')

    @staticmethod
    def get_business_tag_id():
        return EnvVariables.get_val('BUSINESS_TAG_ID')

    @staticmethod
    def get_business_domain():
        return EnvVariables.get_val('BUSINESS_DOMAIN')
