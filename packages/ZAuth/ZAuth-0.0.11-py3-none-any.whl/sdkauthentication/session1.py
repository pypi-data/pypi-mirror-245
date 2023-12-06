import copy
import os
from sdkauthentication.zsession import generate_request_headers

class Session:
    """
    A session stores configuration state and allows you to create service
    clients and resources.

    :type aws_access_key_id: string
    :param aws_access_key_id: AWS access key ID
    :type aws_secret_access_key: string
    :param aws_secret_access_key: AWS secret access key
    :type aws_session_token: string
    :param aws_session_token: AWS temporary session token
    :type region_name: string
    :param region_name: Default region when creating new connections
    :type botocore_session: botocore.session.Session
    :param botocore_session: Use this Botocore session instead of creating
                             a new default one.
    :type profile_name: string
    :param profile_name: The name of a profile to use. If not given, then
                         the default profile is used.
    """

    def __init__(
        self,
        email_id=None,
        access_key=None,
        businessDomain =None,
        businessTagID =None,
    ):
        if email_id or access_key or businessDomain or businessTagID:
            self.set_credentials(
               email_id, access_key, businessDomain, businessTagID
            )
    
    def set_credentials(self,email_id, access_key, businessDomain, businessTagID):
        print(email_id, access_key, businessDomain, businessTagID)
        print(generate_request_headers(email_id, access_key, businessDomain, businessTagID))

    
    def get_credentials(self):
        pass
        
       
        
