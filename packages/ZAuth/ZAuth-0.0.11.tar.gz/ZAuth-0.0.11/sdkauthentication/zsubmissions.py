import json
# import concurrent.futures
from sdkauthentication import zexcute_apis
from sdkauthentication.server_configuration import EnvVariables
from sdkauthentication.loggerClass import LoggerClass as LogClass

def get_all_submissions(formId, payload=None):
    """
    :param payload:
        {
            "limit":
            "skip":
            "filter": [
                {
                    "operator": "eq",
                    "name": "_id",
                    "value": "FormSubmissionID"
                }
            ],
            "elementsFilter": [
                {
                    "operator": "eq",
                    "label": "field_label",
                    "value": "field_value"
                },
                {
                    "operator": "eq",
                    "id": "element_id",
                    "value": "field_value"
                }
            ]
        }
    :return:
    """
    if payload is None:
        payload = {}
    url = 'http://bifrost/api/v1/submissions/' + str(formId) + '/find/all'
    response = zexcute_apis.execute(rest_url=url, method="POST", json=payload)
    return response


def get_and_update_submission(formId, payload):
    url = 'http://bifrost/api/v1/submissions/update/{0}'.format(formId)
    response = zexcute_apis.execute(rest_url=url, method="POST", json=payload)
    return response


def get_submission_by_id(submission_id):
    url = 'http://bifrost/api/v1/submissions/' + submission_id
    response = zexcute_apis.execute(rest_url=url, method="GET")
    return response


def get_submission_elements(submission_id):
    url = 'http://bifrost/api/v1/submissions/' + submission_id
    response = zexcute_apis.execute(rest_url=url, method="GET")
    return response["data"]["elements"][0]["elements"]


def get_form_id_of_submission(submission_id):
    url = 'http://bifrost/api/v1/submissions/' + submission_id
    response = zexcute_apis.execute(rest_url=url, method="GET")
    print(response)
    return response["data"]["elements"][0]["formId"]


def post_submission(payload, query_params=None, headers=None):
    """
    :param payload: {
        "formId": "output_form_id",
        "elements": [
            {
                "elementId": "element_id_1",
                "value": "element_value_1"
            },
            {
                "elementId": "element_id_2",
                "value": "element_value_2"
            },
        ]
    }
    :param query_params: {
        "skipAutomation": False,
        "skipValidations: True
    }
    :param headers: headers
    :return: {"message": "Submission created successfully", "data": {"raw": "", "next_key": [], "elements": [], "id": "64477065d135c8cefb93ad52"}, "error": false}
    """
    if query_params is None:
        query_params = {
            "skipValidations": True
        }
    else:
        query_params["skipValidations"] = True

    url = 'http://bifrost/api/v1/submissions/'
    response = zexcute_apis.execute(rest_url=url, method="POST", json=payload, query_params=query_params, headers=headers)
    return response


def put_submission(submission_id, payload, query_params=None, headers=None):
    """
    :param submission_id: FormSubmissionID/id
    :param payload: {
        "elements": [
            {
                "elementId": "element_id_1",
                "value": "element_value_1"
            },
            {
                "elementId": "element_id_2",
                "value": "element_value_2"
            },
        ]
    }
    :param query_params: {
        "skipAutomation": False,
        "skipValidations: True
    }
    :param headers: headers
    :return:
    """
    if query_params is None:
        query_params = {
            "skipValidations": True
        }
    else:
        query_params["skipValidations"] = True

    if "elements" not in payload:
        raise Exception("Elements list not provided")
    url = 'http://bifrost/api/v1/submissions/' + submission_id
    response = zexcute_apis.execute(rest_url=url, method="PUT", json=payload, query_params=query_params, headers=headers)
    return response


def delete_submissions(formID, submissionIds_list, truncate=False):
    payload = {"formId": formID, "submissionIds": submissionIds_list, "isTruncate": truncate}
    url = 'http://bifrost/api/v1/submissions/delete'
    response = zexcute_apis.execute(rest_url=url, method="POST", json=payload)
    return response


def search_submissions(form_id, search_keys=None, search_values=None, limit=None, skip=None, sort_descending=False, exact_match=True):
    """
    :param form_id: FormID
    :param search_keys: ["column1", "column2", "column3", ...]
    :param search_values: ["value1", "value2", "value3", ...]
    Note: If you want to search mutiple values for a single search_key: Send the values in an array.
    Example -  search_values: ["value1",["value_2x","value_2y","value_2z"],"value_3",...]
    :param limit: Set limit to search entry
    :param skip:
    :param sort_descending: True/False
    Note: If sort_descending True then newer entries will come first in response and if False then older entries will come first
    :param exact_match: True/False
    :return:
    """

    filter_name_mapping = {
        "FormSubmissionID": "_id"
    }

    filters = []
    element_filter = []
    if search_keys:
        for key, val in zip(search_keys, search_values):
            fields = {}
            if exact_match:
                if type(val) == list:
                    fields["operator"] = "in"
                    fields["arr_value"] = val
                else:
                    fields["operator"] = "eq"
                    fields["value"] = val
            else:
                fields["operator"] = "regex"
                fields["value"] = val

            if key in filter_name_mapping:
                fields["name"] = filter_name_mapping[key]
                filters.append(fields)
            else:
                fields["label"] = key
                element_filter.append(fields)

    payload = {
        "limit": limit,
        "skip": skip,
        "filter": filters,
        "elementsFilter": element_filter,
        "sort": {
            "field": "_id",
            "order": -1 if sort_descending else 1
        }
    }
    response = get_all_submissions(form_id, payload)
    return response["data"]["elements"]


def search_unpaginated_submissions(form_id, search_values, limit=100, skip=0):
    submissions = []
    filters = [{"name": "formId", "value": form_id, "operator": "eq"}]
    filters += [{"name": "elements.value", "value": values, "operator": "eq"} for values in search_values]
    payload = {
        "limit": limit,
        "skip": skip,
        "filter": filters
    }
    while True:
        submission_resp = get_all_submissions(payload)
        submissions += submission_resp["data"]["elements"]
        if len(submissions) == submission_resp["data"]["count"]:
            break
        else:
            payload["skip"] = len(submissions)
    return submissions


def search_and_update(form_id, search_keys, search_values, submission_inputs):
    filter_name_mapping = {
        "FormSubmissionID": "_id"
    }
    filters = []
    element_filter = []
    if search_keys:
        for i in range(len(search_keys)):
            fields = {}
            fields["operator"] = "eq"
            if search_keys[i] in ["FormSubmissionID"]:
                fields["name"] = filter_name_mapping[search_keys[i]]
                if search_values:
                    fields["value"] = search_values[i]
                else:
                    fields["value"] = None
                filters.append(fields)
            else:
                fields["label"] = search_keys[i]
                # fields["id"] = search_keys[i]
                if search_values:
                    fields["value"] = search_values[i]
                    if type(search_values[i]) == list:
                        fields["operator"] = "in"
                        fields["arr_value"] = fields["value"]
                        del fields["value"]
                else:
                    fields["value"] = None
                element_filter.append(fields)

    payload = {
        "filter": filters,
        "elementsFilter": element_filter,
        "filterOperator": "$and",
        "elements": submission_inputs
    }
    response = get_and_update_submission(formId=form_id, payload=payload)
    return response["data"]["elements"]


def post_submissions_in_parallel(payload):
    """
    Posts submissions concurrently using a thread pool.

    Parameters:
        payload (list): A list of dictionaries, each containing submission data.
            Each dictionary must contain at least the following keys:
                - "formId": The unique ID of the form.
                - "skipValidations" (optional): If True, skips validations during submission. Default is True if not provided.
                - "skipAutomation" (optional): If True, skips automation processes during submission. Default is True if not provided.

    Returns:
        list: A list of dictionaries containing form and submission IDs for each successfully posted submission.
            Each dictionary has the following keys:
                - "formId": The form ID from the payload.
                - "submissionId": The ID of the successfully posted submission.

        for example:
            [
                {
                    "formId": "64ca40ef48ee329704e56072",
                    "elements": [
                        {
                            "label": "Name",
                            "value": "test"
                        },
                        {
                            "label": "Name1",
                            "value": "test1"
                        },
                        {
                            "label": "Name2",
                            "value": "test2"
                        },
                        {
                            "label": "Name3",
                            "value": "test3"
                        },
                        {
                            "label": "Name4",
                            "value": "test4"
                        }
                    ],
                    "skipValidations": True,
                    "skipAutomation"  : True
                },
                {
                    "formId": "64cd0058e43b48604b8d1cb8",
                    "elements": [
                        {
                            "label": "Name",
                            "value": "test"
                        }
                    ]
                }
            ]

        response:
            [{\"formId\":\"64cd00eee43b48604b8d300a\",\"submissionId\":\"64d07dfd417c0382a8e42fb0\"},{\"formId\":\"64ca40ef48ee329704e56072\",\"submissionId\":\"64d07dfd417c0382a8e42fa8\"}]
    """
    from python.classes.modules.zmodule_v2 import zsession
    headers = zsession.generate_request_headers()
    lst_of_response = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=EnvVariables.get_workers() if EnvVariables.get_workers() else 2) as executor:
        # Use executor.submit() to schedule the post_url function to be called for each URL
        # This returns a Future object, which represents a computation that hasn't necessarily completed yet
        futures = {executor.submit(post_submission, each_payload, query_params={"skipValidations": each_payload["skipValidations"] if "skipValidations" in each_payload and each_payload["skipValidations"] else True, "skipAutomation": each_payload["skipAutomation"] if "skipAutomation" in each_payload and each_payload["skipAutomation"] else True}, headers=headers): each_payload for each_payload in payload}
        # Use as_completed to yield the Future objects as they complete
        for future in concurrent.futures.as_completed(futures):
            try:
                # Get the result of the computation
                response = future.result()
                payload = futures[future]
                lst_of_response.append({"formId": payload["formId"], "submissionId": response["data"]["id"]})
            except Exception as e:
                # LogClass.exception_log("script-logs",{"message": "Exception hit - quitting", "exception": e})
                raise e
    return lst_of_response


def put_submissions_in_parallel(payload):
    """
        Puts submissions concurrently using a thread pool.

        Parameters:
            payload (list): A list of dictionaries containing submission data.
                Each dictionary must contain the following keys:
                    - "submission_id": The unique ID of the submission.
                    - "payload": The data of the submission to be put.
                    - "skipValidations" (optional): If True, skips validations during submission. Default is True if not provided.
                    - "skipAutomation" (optional): If True, skips automation processes during submission. Default is True if not provided.

        Returns:
            list: A list of submission IDs for each successfully put submission.

        for example:
            [
                {
                    "submission_id": "64d07dfde43b48604b97664b",
                    "payload" : {
                        "elements": [
                            {
                                "label": "Name",
                                "value": "Shubham"
                            }
                        ]
                    },
                    "skipValidations" : True,
                    "skipAutomation"  : True
                }
            ]

        response:
            [\"64d07dfde43b48604b97664b\"]
    """
    from python.classes.modules.zmodule_v2 import zsession
    headers = zsession.generate_request_headers()
    lst_of_response = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=EnvVariables.get_workers() if EnvVariables.get_workers() else 2) as executor:
        # Use executor.submit() to schedule the post_url function to be called for each URL
        # This returns a Future object, which represents a computation that hasn't necessarily completed yet
        futures = {executor.submit(put_submission, submission_id=each_payload["submission_id"], payload=each_payload["payload"] ,query_params={
            "skipValidations": each_payload["skipValidations"] if "skipValidations" in each_payload and each_payload[
                "skipValidations"] else True,
            "skipAutomation": each_payload["skipAutomation"] if "skipAutomation" in each_payload and each_payload[
                "skipAutomation"] else True}, headers=headers): each_payload for each_payload in payload}
        # Use as_completed to yield the Future objects as they complete
        for future in concurrent.futures.as_completed(futures):
            try:
                # Get the result of the computation
                response = future.result()
                lst_of_response.append(response["data"]["id"])
            except Exception as e:
                # LogClass.exception_log("script-logs", {"message": "Exception hit - quitting", "exception": e})
                raise e
    return lst_of_response


def fetch_submissions_analytics(form_id ,keys=None, values=None, frm=None, to=None, orderby=None):
    """
        Fetches submissions from a form using analytics with optional filtering and sorting.

        Parameters:
            form_id (str): The ID of the form for which submissions are to be fetched.
            keys (list, optional): List of keys to filter submissions based on specific fields (e.g., ['field1', 'field2']).
            values (list, optional): List of values corresponding to the keys for filtering (e.g., ['value1', 'value2']).
            frm (int, optional): The starting record index from which submissions should be included (0-based index).
            to (int, optional): The ending record index until which submissions should be included (0-based index, inclusive).
            orderby (str, optional): The field to sort the submissions by (e.g., 'asc', 'desc').

        Returns:
            list: A list containing the fetched submissions based on the provided parameters.
        """
    if keys and values:
        if len(keys) != len(values):
            raise ValueError("The length of key and value lists must be the same.")

        structure = {
            "bool": {
                "must": []
            }
        }

        for i in range(len(keys)):
            term = {}
            terms = {}
            if isinstance(values[i], list):
                if all(isinstance(v, int) for v in values[i]):
                    terms[keys[i]] = values[i]
                elif all(isinstance(v, float) for v in values[i]):
                    terms[keys[i]] = values[i]
                elif all(isinstance(v, str) for v in values[i]):
                    terms[keys[i] + ".keyword"] = values[i]
            elif(isinstance(values[i], str)):
                term[keys[i] + ".keyword"] = values[i]

            structure["bool"]["must"].append({"term" if term else "terms": term if term else terms})
    else:
        structure = {
            "match_all": {}
        }

    payload = {
        "formId": form_id,
        "query": {
            "query": structure,
            "from": int(frm) if frm else 0,
            "size": int(to) if to else 150,
            "sort": [
                {
                    "id": {
                        "order": orderby if orderby else "desc"
                    }
                }
            ]
        }
    }

    url = 'http://bifrost/api/v1/analytics/search'
    response = zexcute_apis.execute(rest_url=url, method="POST", json=payload)
    return response

def get_submissions(syncRequestID, isCountRequest=0, skip=0, limit=0):
    url = "https://bifrost/api/v1/submissions/sync/request/{}/{}?skip={}&limit={}".format(syncRequestID, isCountRequest, skip, limit)
    response = zexcute_apis.execute(rest_url=url, method="GET")
    return response


def bulk_submission_or_update(payload, query_params=None):
    '''
    :param payload:     {
        "operations": [
            {
                "operation": "CREATE",
                "formId": "63610d203caa377b482d58f0",
                "elements": [
                    {
                        "label": "Name",
                        "value": "Test1"
                    }
                ]
            },
            {
                "operation": "CREATE",
                "formId": "63610d203caa377b482d58f0",
                "elements": [
                    {
                        "label": "Name",
                        "value": "Test2"
                    }
                ]
            }
        ]
    }
    :param query_params:
    :return:
    '''
    if query_params is None:
        query_params = {}

    url= "http://bifrost/api/v1/submissions/batch"
    response = zexcute_apis.execute(rest_url=url, method="POST", json=payload, query_params=query_params)
    return response


if __name__ == "__main__":
    print("check")
    get_form_id_of_submission("1141")



