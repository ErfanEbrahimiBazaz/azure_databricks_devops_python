import requests  
import time
import os
import json


DBRKS_REQ_HEADERS = {
    'Authorization': 'Bearer ' + os.environ['DBRKS_BEARER_TOKEN'],
    'X-Databricks-Azure-Workspace-Resource-Id': '/subscriptions/'+ os.environ['DBRKS_SUBSCRIPTION_ID'] +'/resourceGroups/'+ os.environ['DBRKS_RESOURCE_GROUP'] +'/providers/Microsoft.Databricks/workspaces/' + os.environ['DBRKS_WORKSPACE_NAME'],
    'X-Databricks-Azure-SP-Management-Token': os.environ['DBRKS_MANAGEMENT_TOKEN']}

DBRKS_CLUSTER_ID = {'cluster_id': os.environ["DBRKS_CLUSTER_ID"]}

print("DBRKS_CLUSTER_ID before applying change_cluster_id() method is {}".format(os.environ["DBRKS_CLUSTER_ID"]))

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
DBRKS_CLUSTER_ID = {'cluster_id': os.environ["DBRKS_CLUSTER_ID"]}
print("DBRKS_CLUSTER_ID after applying change_cluster_id() method is {}".format(os.environ["DBRKS_CLUSTER_ID"]))

def delete_dbrks_cluster():
    DBRKS_ENDPOINT = 'api/2.0/clusters/permanent-delete'
    response = requests.post(
        "https://"+os.environ['DBRKS_INSTANCE']+".azuredatabricks.net/" + DBRKS_ENDPOINT,
        headers=DBRKS_REQ_HEADERS,
        json=DBRKS_CLUSTER_ID)
    if response.status_code != 200:
        raise Exception(json.loads(response.content))

        
delete_dbrks_cluster()