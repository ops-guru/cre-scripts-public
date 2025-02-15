# Option 1: Getting Azure Workload Inventory via Script
## Pre-requisites:
Install az related packages: <br />
> pip3 install pandas openpyxl azure-mgmt-resource azure-identity <br />
## Steps to Run: <br />
- To login to your Azure account, run the below command: <br />
> az login <br />

Then select the correct subscription when prompted. <br />

Then confirm the login by running: <br />

- Once authenticated, confirm if you are in the right subscription and tenant: <br />

> az account show <br />

Now open the az_get_all_resources.py and edit line numnber 6 with the subscription id of your account. <br />

To generate the report, now run: <br />

> python3 az_get_all_resources.py <br />

An excel file by the azure_resources.xlsx is generated.<br />
<br />

# Option 2: Getting Workload Inventory through Azure Console
Alternatively, the same can be obtained through the Azure console.
##Steps:
1. Login to Azure Portal <br />
2. In the search bar, search for Subscriptions
3. Click on the Subscription you want to view the resources for
4. In the Overview page, click on "View resources" in the bottom of the page. 
5. Click on "Export to CSV" to export the list of resources to a .csv file
