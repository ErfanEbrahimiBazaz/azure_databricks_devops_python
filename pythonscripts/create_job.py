# from logging import raiseExceptions
import requests
import os
import json
# from os.path import isfile, join
# from os import listdir



# dbrks_create_job_url =  "https://"+os.environ['DBRKS_INSTANCE']+".azuredatabricks.net/api/2.0/jobs/create"
dbrks_create_job_url = "https://"+os.environ['DBRKS_INSTANCE']+".azuredatabricks.net/api/2.1/jobs/create"

DBRKS_REQ_HEADERS = {
    'Authorization': 'Bearer ' + os.environ['DBRKS_BEARER_TOKEN'],
    'X-Databricks-Azure-Workspace-Resource-Id': '/subscriptions/'+ os.environ['DBRKS_SUBSCRIPTION_ID'] +'/resourceGroups/'+ os.environ['DBRKS_RESOURCE_GROUP'] +'/providers/Microsoft.Databricks/workspaces/' + os.environ['DBRKS_WORKSPACE_NAME'],
    'X-Databricks-Azure-SP-Management-Token': os.environ['DBRKS_MANAGEMENT_TOKEN']}

print("DBRKS_CLUSTER_ID before setup is {}".format(os.environ["DBRKS_CLUSTER_ID"]))

def change_cluster_id():
    if len(os.environ['DBRKS_NEW_CLUSTER_ID'])==0:
        print("DBRKS_NEW_CLUSTER_ID is empty.")
        return os.environ['DBRKS_CLUSTER_ID']
    elif (os.environ['DBRKS_NEW_CLUSTER_ID'] is not None) and (not os.environ['DBRKS_NEW_CLUSTER_ID'].isspace()):
        print("DBRKS_NEW_CLUSTER_ID is not None.")
        print("DBRKS_NEW_CLUSTER_ID value is {}".format(os.environ["DBRKS_NEW_CLUSTER_ID"]))
        return os.environ['DBRKS_NEW_CLUSTER_ID']
    else:
        ## for backward compatibility
        print("DBRKS_NEW_CLUSTER_ID is None.")
        return os.environ['DBRKS_CLUSTER_ID']

os.environ['DBRKS_CLUSTER_ID'] = change_cluster_id()
print("DBRKS_CLUSTER_ID after setup is {}".format(os.environ["DBRKS_CLUSTER_ID"]))

CLUSTER_ID = "\"" + os.environ["DBRKS_CLUSTER_ID"] + "\""
NOTEBOOK_LOCATION = "\"" + os.environ["NOTEBOOK_LOCATION"] + "test-notebook" + "\""
print("Notebook path is {}".format(NOTEBOOK_LOCATION))
print(CLUSTER_ID)

body_json = """
    {
    "name": "A sample job to trigger from DevOps",
    "tasks": [
        {
        "task_key": "ExecuteNotebook",
        "description": "Execute uploaded notebook including tests",
        "depends_on": [],
        "existing_cluster_id": """ + CLUSTER_ID + """,
        "notebook_task": {
          "notebook_path": """ + NOTEBOOK_LOCATION + """,
          "base_parameters": {}
        },
        "timeout_seconds": 300,
        "max_retries": 1,
        "min_retry_interval_millis": 5000,
        "retry_on_timeout": false
      }
],
    "email_notifications": {},
    "name": "Run_Unit_Tests",
    "max_concurrent_runs": 1}
"""

print("Request body in json format:")
print(body_json)

response = requests.post(dbrks_create_job_url, headers=DBRKS_REQ_HEADERS, data=body_json) 

if response.status_code == 200:
    print("Job created successfully!")
    print(response.status_code)
    print(response.content)
    print("Job Id = {}".format(response.json()['job_id']))
    print("##vso[task.setvariable variable=DBRKS_JOB_ID;isOutput=true;]{b}".format(b=response.json()['job_id'])) 
else:
    print("job failed!")
    raise Exception(response.content)

## In case of missing " in request body: 
## Exception: b'{"error_code":"MALFORMED_REQUEST","message":"Invalid JSON given in the body of the request - failed to parse given JSON"}' 
# print("##vso[task.setvariable variable=DBRKS_BEARER_TOKEN;isOutput=true;]{b}".format(b=DBRKS_BEARER_TOKEN))
