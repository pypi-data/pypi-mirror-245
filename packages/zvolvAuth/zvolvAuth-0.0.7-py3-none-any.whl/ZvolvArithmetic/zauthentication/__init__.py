import logging
from ZvolvArithmetic.zauthentication.session import Session

__author__ = 'Zvolv'
__version__ = '0.0.1'

# The default zvolv session; autoloaded when needed.
DEFAULT_SESSION = None

def setup_default_session(**kwargs):
    """
    Set up a default session, passing through any parameters to the session
    constructor. There is no need to call this unless you wish to pass custom
    parameters, because a default session will be created for you.
    """
    global DEFAULT_SESSION
    DEFAULT_SESSION = Session(**kwargs)
    print(DEFAULT_SESSION)

def _get_default_session():
    """
    Get the default session, creating one if needed.

    :rtype: :py:class:`~.`
    :return: The default session
    """
    if DEFAULT_SESSION is None:
        print("please add ")
        zvolv_access_key_id  = input("Enter zvolv access key id  : ")
        zvolv_secret_access_key = input("Enter zvolv secret access key : ")
        zvolv_domain_context = input("Enter zvolv domain context : ")
        setup_default_session(zvolv_access_key_id=zvolv_access_key_id,zvolv_secret_access_key=zvolv_secret_access_key,zvolv_domain_context =zvolv_domain_context)

    return DEFAULT_SESSION

# zvolv_access_key_id='yogesh.rjadhav22@gmail.com'
# zvolv_secret_access_key='Pucsd!@3'
# zvolv_domain_context ='yogeshjadhav'
# setup_default_session(zvolv_access_key_id=zvolv_access_key_id,zvolv_secret_access_key=zvolv_secret_access_key,zvolv_domain_context =zvolv_domain_context)

# print(_get_default_session())