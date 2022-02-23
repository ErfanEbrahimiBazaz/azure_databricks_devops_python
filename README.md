# azure_databricks_devops_python

To reproduce the error follow the steps below:

1. Make an Azure DevOps project and copy all these files into the repo.
2. You need to have some code that can generate a wheel. Either use your own code, or use the sample wheel here.
3. Create three Azure Subscriptions. In each subscription create one resource group and in each RG create a new databricks workspace. If you do not have access to three subscriptions, one is also possible with only one databricks.
4. If you have three databricks workspaces, create one cluster in each. If you have only one subscription and one databricks, create three databricks clusters.
5. In Azure Active Directory make an app registration to be able to connect Azure DevOps to Azure Databricks.
6. Make a variable group in Azure DevOps called databricks-sp-vg. This variable group must contain the following values:

| Variable Name   | Description |  Value |
| ----------- | ----------- | ----------- |
|  DBFS_WHL_LOC    |  Wheel location in DBFS (Azure Databricks File System) for DEV env    |    Any Name of your choice. It will be the folder name in DBFS    |
|  DBRKS_CLUSTER_ID  |    Copy paste the cluster Id you create in your Azure databricks workspace for DEV environment   |   It's the value coming after cluster in URL like clusters/02...oonfx6kc   |
|  DBRKS_CLUSTER_QA  | Copy paste the cluster Id you create in your Azure databricks workspace for DEV environment    |  It's the value coming after cluster in URL like clusters/02...oonfx6kc     |
|  DBRKS_DBFS_WHL_LOC_QA  |    Wheel location in DBFS (Azure Databricks File System) for DEV env      |    Any Name of your choice. It will be the folder name in DBFS   |
|  DBXInstance  |  name of databricks workspace  in DEV env      |       You can read it in Azure portal in your databricks service page |
|  DBXInstance_QA  |      name of databricks workspace  in QA env     |    You can read it in Azure portal in your databricks service page   |
|  ResourceGroup_QA  |    name of Azure Resource Group in QA env     | You can read it in Azure portal in RG page      |
|  SubscriptionID  |    name of Azure subscription in DEV environment   |  Read it from Azure      |
|  SubscriptionID_QA  |  name of Azure subscription in QA environment      |  Read it from Azure      |
|  SVCApplicationID  |   Service Connection Application Id     | You can read it from the Azure Active Directory App Registration      |
|  SVCDirectoryID  |    Service Connection Tenant Id     | You can read it from the Azure Active Directory App Registration      |
|  SVCSecretKey  |     Service Connection Secret Key    |      You can read it from the Azure Active Directory App Registration |
|  WorkspaceName  |   Databricks worksapce name in DEV env     |     From Azure portal for databricks service page  |
|  WorkspaceName_QA  |   Databricks worksapce name in QA env     |      From Azure portal for databricks service page |
