import requests
import json
import os


TOKEN_REQ_HEADERS = {'Authorization': 'Bearer '+ os.environ['DBRKS_BEARER_TOKEN'],
                     'X-Databricks-Azure-SP-Management-Token': os.environ['DBRKS_MANAGEMENT_TOKEN'],
                     'X-Databricks-Azure-Workspace-Resource-Id': '/subscriptions/'+os.environ['DBRKS_SUBSCRIPTION_ID']+'/resourceGroups/'+os.environ['DBRKS_RESOURCE_GROUP']+'/providers/Microsoft.Databricks/workspaces/'+os.environ['DBRKS_WORKSPACE_NAME']}



os.environ["CLUSTER_NAME"] = """ "temp-cluster-for-unittests" """
os.environ["SPARK_VERSION"] = """ "7.3.x-scala2.12" """

postjson = """{
    "cluster_name":""" + os.environ["CLUSTER_NAME"] + """,
    "spark_version": """ + os.environ["SPARK_VERSION"] + """,
    "node_type_id": "Standard_DS3_v2",
    "autotermination_minutes": 10,
    "autoscale" : {
        "min_workers": 1,
        "max_workers": 3
    }
}"""


# request_header = {'Authorization': 'Bearer ' + os.environ['DBRKS_BEARER_TOKEN']}

DBRKS_START_ENDPOINT = 'api/2.0/clusters/create'
request_url = 'https://' + os.environ["DBRKS_INSTANCE"] + '.azuredatabricks.net/' + DBRKS_START_ENDPOINT
print(request_url)
print(postjson)
print(json.loads(postjson))
response = requests.post(request_url, headers=TOKEN_REQ_HEADERS, data=postjson) 
# json.loads(postjson)) # data causes malformed error:
# Exception: {"error_code":"MALFORMED_REQUEST","message":"Invalid JSON given in the body of the request - failed to parse given JSON"}

if response.status_code == 200:
    print("Creating cluster")
else:
    raise Exception(response.text)


# DBRKS_START_ENDPOINT = 'api/2.0/clusters/create'
# print("https://" + os.environ["DBRX_INSTANCE"] + ".azuredatabricks.net/" + DBRKS_START_ENDPOINT)
# # response = requests.post("https://" + os.environ["DBRX_INSTANCE"] + ".azuredatabricks.net/" + DBRKS_START_ENDPOINT,
# #                          headers=request_header, json=json.loads(postjson))
# if response.status_code != 200:
#     raise Exception(response.text)

os.environ["DBRKS_CLUSTER_ID"] = response.json()["cluster_id"]
print(os.environ["DBRKS_CLUSTER_ID"])
 
# Refer to this link to make environment variables from task or script in the agent machine. 
# https://docs.microsoft.com/en-us/azure/devops/pipelines/scripts/logging-commands?view=azure-devops&tabs=bash#setvariable-initialize-or-modify-the-value-of-a-variable
print("##vso[task.setvariable variable=DBRKS_NEW_CLUSTER_ID;isOutput=true;]{b}".format(b=os.environ["DBRKS_CLUSTER_ID"]))

# response = requests.post("https://"+os.environ['DBRKS_INSTANCE']+".azuredatabricks.net/" + DBRKS_START_ENDPOINT, headers=DBRKS_REQ_HEADERS, json=json.loads(postjson))
# print(request_url)
# {"error_code":"MALFORMED_REQUEST","message":"Invalid JSON given in the body of the request - failed to parse given JSON"}
# Expecting property name enclosed in double quotes
