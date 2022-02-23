# azure_databricks_devops_python

To reproduce the error follow the steps below:

1. Make an Azure DevOps project and copy all these files into the repo.
2. You need to have some code that can generate a wheel. Either use your own code, or use the sample wheel here.
3. Create three Azure Subscriptions. In each subscription create one resource group and in each RG create a new databricks workspace. If you do not have access to three subscriptions, one is also possible with only one databricks.
4. If you have three databricks workspaces, create one cluster in each. If you have only one subscription and one databricks, create three databricks clusters.
5. Make a variable group in Azure DevOps called databricks-sp-vg. This variable group must contain the following values:

| Variable Name   | Description |  Value |
| ----------- | ----------- |
|      |       |        |
|    |        |       |
