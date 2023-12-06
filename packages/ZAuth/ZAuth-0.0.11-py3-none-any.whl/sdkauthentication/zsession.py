import json
import os
import hashlib
import time
import sys
# from flask import request
from sdkauthentication.server_configuration import EnvVariables
from sdkauthentication import zexcute_apis
from sdkauthentication.loggerClass import LoggerClass as LogClass
from pprint import pprint
# from python.classes.modules.queue.receiver import *   
from sdkauthentication import receiverFunctionCalling

folder_path = "/tmp"            # For server
# folder_path = os.getcwd()     # For local testing
CACHE_FILE_NAME = 'token_cache.json'
CACHE_FILE_PATH = os.path.join(folder_path, CACHE_FILE_NAME)

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


def zlogin(email_id, access_key, businessDomain, businessTagID):
    token_cache = load_token_cache()
    # token_cache ={}
    print("****"*33,token_cache)
    # business_domain, business_tag = get_request_configs()

    business_domain, business_tag = businessDomain, businessTagID


    # Check if the token is already created and stored. Also, check if it should not be older than 60 seconds.
    if token_cache and business_domain in token_cache and token_cache and (time.time() - token_cache[business_domain]["serverTime"]) < 60:
        return token_cache[business_domain]

    
    # sha512pwd = hashlib.sha512(EnvVariables.get_admin_password()).hexdigest()
    # payload = {'email': EnvVariables.get_admin_email(), 'password': sha512pwd}
    #----------------------------------------------------------------------------------------------
    # ## i will give the user password
    # email = raw_input("enter username or email  ")
    # password = raw_input("enter the password  ")
    # password = hashlib.sha512(password).hexdigest()
    email = email_id
    password = access_key
    # password = hashlib.sha512(password).hexdigest()
    password = hashlib.sha512(password.encode('utf-8')).hexdigest()
    print("password ",password)
    payload = {'email': email, 'password': password}


    #-------------------------------------------------------------------------------------------------
    headers = {'businessDomain': business_domain, 'jwt': 'true', 'businessTagID': business_tag ,'Device':'browser'}
    # login_url = EnvVariables.get_localhost_url() + EnvVariables.get_api_17_version() + "user/login"
    # print(login_url)
    login_url = "https://zvolv.co/rest/v17/user/login"
    login_response = zexcute_apis.execute(rest_url=login_url, method="POST", data=payload, headers=headers)
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
        # return receiverFunctionCalling.businessDomain, receiverFunctionCalling.businessTag


def generate_login_token(email_id, access_key, businessDomain, businessTagID):
    login = zlogin(email_id, access_key, businessDomain, businessTagID)
    pprint(login)
    return login["loginToken"]


def generate_request_headers(email_id, access_key, businessDomain, businessTagID):
    # business_domain, business_tag = get_request_configs()
    business_domain, business_tag = businessDomain,businessTagID


    auth_key = generate_login_token(email_id, access_key, businessDomain, businessTagID)
    headers = {'domain': business_domain, 'Authorization': 'bearer ' + auth_key, 'Content-Type': 'application/json'}
    return headers


def get_api_v1_object():
    from python.classes.modules.common.common_api import CommonApi
    business_domain, business_tag = get_request_configs()
    return CommonApi(zviceID=business_tag, body={"BusinessTag": business_tag, "businessDomain": business_domain})


# if __name__ == "__main__":
#     generate_request_headers()