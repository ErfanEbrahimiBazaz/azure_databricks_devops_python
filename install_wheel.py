import requests
import os


DBRKS_REQ_HEADERS = {
    'Authorization': 'Bearer ' + os.environ['DBRKS_BEARER_TOKEN'],
    'X-Databricks-Azure-Workspace-Resource-Id': '/subscriptions/'+ os.environ['DBRKS_SUBSCRIPTION_ID'] +'/resourceGroups/'+ os.environ['DBRKS_RESOURCE_GROUP'] +'/providers/Microsoft.Databricks/workspaces/' + os.environ['DBRKS_WORKSPACE_NAME'],
    'X-Databricks-Azure-SP-Management-Token': os.environ['DBRKS_MANAGEMENT_TOKEN']}

# DBRKS_REQ_BODY = {'cluster_id': os.environ["DBRKS_CLUSTER_ID"], 'libraries': [{'whl': 'dbfs:/Erfan_wheels/py_sample_package-0.6.5-py3-none-any.whl'}]}
print('Wheel name is {}'.format(os.environ['WHL_NAME']))
print('DBRKS_CLUSTER_ID before ENV definition is {}'.format(os.environ["DBRKS_CLUSTER_ID"]))
print('DBRKS_DBFS_WHL_LOC: {}'.format(os.environ["DBRKS_DBFS_WHL_LOC"]))


# env_type = os.environ['ENV']
# if(env_type=='dev'):
#     print('Inside DEV environment')
#     # DBRKS_CLUSTER_ID = {'cluster_id': '0209-141629-oonfx6kc'}   
#     DBRKS_CLUSTER_ID = {'cluster_id': os.environ["DBRKS_CLUSTER_ID"]}  
#     CLUSTER_ID =  os.environ["DBRKS_CLUSTER_ID"] 
# elif(env_type=='qa'):
#     # DBRKS_CLUSTER_ID = {'cluster_id': '0221-201240-xt67wkzl'}
#     print('Inside QA environment')
#     DBRKS_CLUSTER_ID = {'cluster_id': os.environ["DBRKS_CLUSTER_ID_QA"]}  
#     CLUSTER_ID =  os.environ["DBRKS_CLUSTER_ID_QA"]
# else:
#     print('Inside PROD environment')
#     # DBRKS_CLUSTER_ID = {'cluster_id': '0221-181750-whbkqb6n'}
#     DBRKS_CLUSTER_ID = {'cluster_id': os.environ["DBRKS_CLUSTER_ID_PRD"]} 
#     CLUSTER_ID =  os.environ["DBRKS_CLUSTER_ID_PRD"] 


# print('DBRKS_CLUSTER_ID after ENV definition is {}'.format(os.environ["DBRKS_CLUSTER_ID"]))

DBRKS_REQ_BODY = {'cluster_id': os.environ["DBRKS_CLUSTER_ID"], 'libraries': [{'whl': 'dbfs:/' + os.environ["DBRKS_DBFS_WHL_LOC"] + '/'+os.path.basename(os.environ['WHL_NAME'])}]}
# DBRKS_REQ_BODY = {'cluster_id': CLUSTER_ID, 'libraries': [{'whl': 'dbfs:/' + os.environ["DBRKS_DBFS_WHL_LOC"] + '/'+os.path.basename(os.environ['WHL_NAME'])}]}

# print('CLUSTER_ID is {}'.format(os.environ["DBRKS_CLUSTER_ID"]))

DBRKS_INSTALL_ENDPOINT = 'api/2.0/libraries/install'

response = requests.post(
    "https://"+os.environ['DBRKS_INSTANCE']+".azuredatabricks.net/" + DBRKS_INSTALL_ENDPOINT,
    headers=DBRKS_REQ_HEADERS,
    json=DBRKS_REQ_BODY)

if response.status_code != 200:
    raise Exception(response.content)
else:
    print(response.status_code)