import logging
from ZvolvArithmetic.zauthentication.session1 import Session

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

def _get_default_session():
    """
    Get the default session, creating one if needed.

    :rtype: :py:class:`~.`
    :return: The default session
    """
    if DEFAULT_SESSION is None:
        setup_default_session()
    return DEFAULT_SESSION