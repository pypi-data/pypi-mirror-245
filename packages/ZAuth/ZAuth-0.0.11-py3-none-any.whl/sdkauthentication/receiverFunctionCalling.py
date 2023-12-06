from sdkauthentication.server_configuration import EnvVariables
from sdkauthentication.loggerClass import LoggerClass as LogClass
import importlib
import os


class ReceiverFunctions(object):
    def __init__(self, CM):
        self.CM = CM

    def execute_master(self,body, jid):
        # LogClass.warning("script-logs", {"message": "Start of submission execution", "message_details": {"jid": jid}})

        # Declare global variables for zsession login
        global businessDomain, businessTag
        businessDomain = body["businessDomain"]
        businessTag = body["BusinessTag"]

        zviceID = body['BusinessTag']
        import python.oneclick as oneclick
        oneclick.mainworkflow(body,None,None)
        # LogClass.warning("script-logs", {"message": "Submission execution completed successfully", "message_details": {"jid": jid}})
