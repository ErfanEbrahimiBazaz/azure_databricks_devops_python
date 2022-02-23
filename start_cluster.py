from email.header import Header
import requests  # noqa: E902
import time
import os
import json
import gc


DBRKS_REQ_HEADERS = {
    'Authorization': 'Bearer ' + os.environ['DBRKS_BEARER_TOKEN'],
    'X-Databricks-Azure-Workspace-Resource-Id': '/subscriptions/'+ os.environ['DBRKS_SUBSCRIPTION_ID'] +'/resourceGroups/'+ os.environ['DBRKS_RESOURCE_GROUP'] +'/providers/Microsoft.Databricks/workspaces/' + os.environ['DBRKS_WORKSPACE_NAME'],
    'X-Databricks-Azure-SP-Management-Token': os.environ['DBRKS_MANAGEMENT_TOKEN']}


# env_type = os.environ['ENV']
# if(env_type=='dev'):
#     # DBRKS_CLUSTER_ID = {'cluster_id': '0209-141629-oonfx6kc'}   
#     DBRKS_CLUSTER_ID = {'cluster_id': os.environ["DBRKS_CLUSTER_ID"]}   
# elif(env_type=='qa'):
#     # DBRKS_CLUSTER_ID = {'cluster_id': '0221-130916-sy5u5oas'}
#     DBRKS_CLUSTER_ID = {'cluster_id': os.environ["DBRKS_CLUSTER_ID_QA"]}  
# else:
#     DBRKS_CLUSTER_ID = {'cluster_id': '0221-181750-whbkqb6n'}
#     # DBRKS_CLUSTER_ID = {'cluster_id': os.environ["DBRKS_CLUSTER_ID_PRD"]}   



DBRKS_CLUSTER_ID = {'cluster_id': os.environ["DBRKS_CLUSTER_ID"]} # uncomment after resolving passing os variable issue from pipeline.

print('#############')
print('SubscriptionID_QA: {}'.format(os.environ['DBRKS_SUBSCRIPTION_ID']))
print('DBRKS_RESOURCE_GROUP: {}'.format(os.environ['DBRKS_RESOURCE_GROUP']))
print('DBRKS_WORKSPACE_NAME: {}'.format(os.environ['DBRKS_WORKSPACE_NAME']))
print('DBRKS_CLUSTER_ID: {}'.format(os.environ['DBRKS_CLUSTER_ID']))
print('DBRKS_INSTANCE: {}'.format(os.environ['DBRKS_INSTANCE']))
print('#############')

print('Outside methods')
print('Header')
print(DBRKS_REQ_HEADERS)
print('cluster Id out of methods')
print(DBRKS_CLUSTER_ID)


print('DBRKS_SUBSCRIPTION_ID: {}'.format(os.environ['DBRKS_SUBSCRIPTION_ID']))
def get_dbrks_cluster_info():
    DBRKS_INFO_ENDPOINT = 'api/2.0/clusters/get'
    print('Inside get_dbrks_cluster_info method')
    print('DBRKS_CLUSETR_ID: {}'.format(DBRKS_CLUSTER_ID))
    response = requests.get("https://"+os.environ['DBRKS_INSTANCE']+".azuredatabricks.net/" + DBRKS_INFO_ENDPOINT, headers=DBRKS_REQ_HEADERS, params=DBRKS_CLUSTER_ID)
    # response = requests.get("https://"+os.environ['DBRKS_INSTANCE']+".azuredatabricks.net/" + DBRKS_INFO_ENDPOINT, headers=DBRKS_REQ_HEADERS, params={'cluster_id': os.environ["DBRKS_CLUSTER_ID"]})
    if response.status_code == 200:
        return json.loads(response.content)
    else:
        raise Exception(json.loads(response.content))


def start_dbrks_cluster():
    DBRKS_START_ENDPOINT = 'api/2.0/clusters/start'
    print('Inside start_dbrks_cluster method')
    print('DBRKS_CLUSETR_ID: {}'.format(DBRKS_CLUSTER_ID))
    response = requests.post("https://"+os.environ['DBRKS_INSTANCE']+".azuredatabricks.net/" + DBRKS_START_ENDPOINT, headers=DBRKS_REQ_HEADERS, json=DBRKS_CLUSTER_ID)
    # response = requests.post("https://"+os.environ['DBRKS_INSTANCE']+".azuredatabricks.net/" + DBRKS_START_ENDPOINT, headers=DBRKS_REQ_HEADERS, json={'cluster_id': os.environ["DBRKS_CLUSTER_ID"]})
    if response.status_code != 200:
        raise Exception(json.loads(response.content))


def restart_dbrks_cluster():
    DBRKS_RESTART_ENDPOINT = 'api/2.0/clusters/restart'
    print('Inside restart_dbrks_cluster method')
    print('DBRKS_CLUSETR_ID: {}'.format(DBRKS_CLUSTER_ID))
    response = requests.post(
        "https://"+os.environ['DBRKS_INSTANCE']+".azuredatabricks.net/" + DBRKS_RESTART_ENDPOINT,
        headers=DBRKS_REQ_HEADERS,
        json=DBRKS_CLUSTER_ID
        # json={'cluster_id': os.environ["DBRKS_CLUSTER_ID"]}
        )
    if response.status_code != 200:
        raise Exception(json.loads(response.content))
        

def manage_dbrks_cluster_state():
    await_cluster = True
    started_terminated_cluster = False
    cluster_restarted = False
    start_time = time.time()
    loop_time = 1200  # 20 Minutes
    print('Inside manage_dbrks_cluster_state method')
    print('Environment variables DBRKS_CLUSETR_ID, DBRKS_SUBSCRIPTION_ID, DBRKS_RESOURCE_GROUP, DBRKS_WORKSPACE_NAME, DBRKS_INSTANCE')
    print('DBRKS_CLUSETR_ID: {}'.format(DBRKS_CLUSTER_ID))
    print('DBRKS_SUBSCRIPTION_ID: {}'.format(os.environ['DBRKS_SUBSCRIPTION_ID']))
    print('DBRKS_RESOURCE_GROUP: {}'.format(os.environ['DBRKS_RESOURCE_GROUP']))
    print('DBRKS_WORKSPACE_NAME: {}'.format(os.environ['DBRKS_WORKSPACE_NAME']))
    print('DBRKS_INSTANCE: {}'.format(os.environ['DBRKS_INSTANCE']))
    


    while await_cluster:
        current_time = time.time()
        elapsed_time = current_time - start_time
        if elapsed_time > loop_time:
            raise Exception('Error: Loop took over {} seconds to run.'.format(loop_time))
        if get_dbrks_cluster_info()['state'] == 'TERMINATED':
            print('Starting Terminated Cluster')
            started_terminated_cluster = True
            start_dbrks_cluster()
            time.sleep(60)
        elif get_dbrks_cluster_info()['state'] == 'RESTARTING':
            print('Cluster is Restarting')
            time.sleep(60)
        elif get_dbrks_cluster_info()['state'] == 'PENDING':
            print('Cluster is Pending Start')
            time.sleep(60)
        elif get_dbrks_cluster_info()['state'] == 'RUNNING' and not cluster_restarted and not started_terminated_cluster:
            print('Restarting Cluster')
            cluster_restarted = True
            restart_dbrks_cluster()
        else:
            print('Cluster is Running')
            await_cluster = False



manage_dbrks_cluster_state()

del DBRKS_CLUSTER_ID
del os.environ["DBRKS_CLUSTER_ID"]
del os.environ["DBRKS_SUBSCRIPTION_ID"]
del os.environ["DBRKS_RESOURCE_GROUP"]
del os.environ["DBRKS_WORKSPACE_NAME"]
del os.environ["DBRKS_INSTANCE"]
del os.environ["DBRKS_BEARER_TOKEN"]
del os.environ["DBRKS_MANAGEMENT_TOKEN"]
gc.collect()

