import logging

# from boto3.compat import _warn_deprecated_python
from sdkauthentication.session1 import Session

__author__ = ''
__version__ = '1.33.6'

# The default Boto3 session; autoloaded when needed.
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

    :rtype: :py:class:`~boto3.session.Session`
    :return: The default session
    """
    if DEFAULT_SESSION is None:
        setup_default_session()
    _warn_deprecated_python()

    return DEFAULT_SESSION


# setup_default_session(email_id='yogesh.rjadhav22@gmail.com',
#         access_key='Pucsd!@3',
#         businessDomain ='yogeshjadhav',
#         businessTagID ='98NCMBD2KBZ4R')




