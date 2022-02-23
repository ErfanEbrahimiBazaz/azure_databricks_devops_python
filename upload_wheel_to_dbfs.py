import requests
import os
import os.path


DBRKS_REQ_HEADERS = {
    'Authorization': 'Bearer ' + os.environ['DBRKS_BEARER_TOKEN'],
    'X-Databricks-Azure-Workspace-Resource-Id': '/subscriptions/'+ os.environ['DBRKS_SUBSCRIPTION_ID'] +'/resourceGroups/'+ os.environ['DBRKS_RESOURCE_GROUP'] +'/providers/Microsoft.Databricks/workspaces/' + os.environ['DBRKS_WORKSPACE_NAME'],
    'X-Databricks-Azure-SP-Management-Token': os.environ['DBRKS_MANAGEMENT_TOKEN']}

dbrks_rest_url = "https://"+os.environ['DBRKS_INSTANCE']+".azuredatabricks.net/api/2.0/dbfs/put"
# DBRKS_DBFS_WHL_LOCation = os.environ['DBRKS_DBFS_WHL_LOC']

wheel_location_in_pipeline = os.environ['SYSTEM_ARTIFACTSDIRECTORY'] + '/dist/' + os.path.basename(os.environ['WHL_NAME'])
print('#############################')
print('Constructed wheel location is: {}'.format(wheel_location_in_pipeline))
print('#############################')

# wheel_loaction = os.environ['SYSTEM_ARTIFACTSDIRECTORY'] + '/dist/' + os.path.basename(os.environ['WHL_NAME']) #'py_sample_package-0.6.5-py3-none-any.whl'
# print(wheel_loaction)
print('Wheel location according to code: {}'.format(wheel_location_in_pipeline))
print('Working directory {}'.format(os. getcwd()))
print('All files and folders in wheel location:')
print('System_ArtifactsDirectory location is {}'.format(os.environ['SYSTEM_ARTIFACTSDIRECTORY']))
os.listdir(os.environ['SYSTEM_ARTIFACTSDIRECTORY'])
print('End of listdir')
print('All files and folders in current working directory:')
os.listdir(os. getcwd())
print('End of listdir')
print('dbrks_rest_url is {}'.format(dbrks_rest_url))
print(DBRKS_REQ_HEADERS)


# print('DBRKS_DBFS_WHL_LOC: {}'.format(os.environ['DBRKS_DBFS_WHL_LOC']))

print('Old path: {}'.format('/Erfan_wheels/'+ os.path.basename(os.environ['WHL_NAME'])))

DBRKS_DBFS_WHL_LOCation = os.environ['DBRKS_DBFS_WHL_LOC']
print('New path: {}'.format('/' + os.environ['DBRKS_DBFS_WHL_LOC'] + '/'+ os.path.basename(os.environ['WHL_NAME'])))


f = open(wheel_location_in_pipeline, 'rb')
files = {"content": (wheel_location_in_pipeline, f)}
# response = requests.post(dbrks_rest_url, files=files, headers=DBRKS_REQ_HEADERS, data={'path': '/Erfan_wheels/py_sample_package-0.6.5-py3-none-any.whl', 'overwrite': 'true'})
# response = requests.post(dbrks_rest_url, files=files, headers=DBRKS_REQ_HEADERS, data={'path': '/Erfan_wheels/'+ os.path.basename(os.environ['WHL_NAME']), 'overwrite': 'true'})
# response = requests.post(dbrks_rest_url, files=files, headers=DBRKS_REQ_HEADERS, data={'path': '/' + os.environ['DBRKS_DBFS_WHL_LOC'] + '/'+ os.path.basename(os.environ['WHL_NAME']), 'overwrite': 'true'})
response = requests.post(dbrks_rest_url, files=files, headers=DBRKS_REQ_HEADERS, data={'path': '/' + DBRKS_DBFS_WHL_LOCation + '/'+ os.path.basename(os.environ['WHL_NAME']), 'overwrite': 'true'})
# response = requests.post(dbrks_rest_url, files=files, headers=DBRKS_REQ_HEADERS, data={'path': '/'+os.environ['DBRKS_DBFS_WHL_LOC'] + '/' + os.path.basename(os.environ['WHL_NAME']), 'overwrite': 'true'})
if response.status_code == 200:
    print(response.status_code)
else:
    raise Exception(response.text)
