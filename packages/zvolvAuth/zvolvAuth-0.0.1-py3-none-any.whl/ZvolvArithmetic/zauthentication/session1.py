import copy
import os
from ZvolvArithmetic.zauthentication.zsession import generate_request_headers

class Session:
    """
    A session stores configuration state and allows you to create service

    :type zvolv_access_key_id: string
    :param zvolv_access_key_id: Email access key ID
    :type zvolv_secret_access_key: string
    :param zvolv_secret_access_key: password secret access key
    :type zvolv_domain_context: string
    :param zvolv_domain_context: zvolv business domain
    """

    def __init__(
        self,
        zvolv_access_key_id=None,
        zvolv_secret_access_key=None,
        zvolv_domain_context =None,
    ):
        if zvolv_access_key_id or zvolv_secret_access_key or zvolv_domain_context:
            self.set_credentials(
               zvolv_access_key_id, zvolv_secret_access_key, zvolv_domain_context,
            )
    
    def set_credentials(self,zvolv_access_key_id, zvolv_secret_access_key, zvolv_domain_context):
        print(generate_request_headers(zvolv_access_key_id, zvolv_secret_access_key, zvolv_domain_context))