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

    @staticmethod
    def get_redis_host():
        return EnvVariables.get_val('REDIS_HOST')

    @staticmethod
    def get_redis_port():
        return EnvVariables.get_val('REDIS_PORT')

    @staticmethod
    def get_redis_db():
        return EnvVariables.get_val('REDIS_DB')

    @staticmethod
    def get_beanstalk_host():
        return EnvVariables.get_val('BEANSTALK_HOST')

    @staticmethod
    def get_beanstalk_port():
        return EnvVariables.get_val('BEANSTALK_PORT')

    @staticmethod
    def get_syslog_hanlder_address():
        return EnvVariables.get_val('SYSLOG_HANDLER_ADDRESS')

    @staticmethod
    def get_syslog_hanlder_port():
        return EnvVariables.get_val('SYSLOG_HANDLER_PORT')

    @staticmethod
    def get_csvfilepath():
        return EnvVariables.get_val('CSVFILEPATH')

    @staticmethod
    def get_workers():
        return EnvVariables.get_val('PARALLEL_PROCESS_WORKER_COUNT')