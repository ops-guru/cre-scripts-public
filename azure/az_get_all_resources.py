from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
import pandas as pd

# vars
sub_id = ''

# auth
credential = DefaultAzureCredential()
subscription_id = sub_id

resource_client = ResourceManagementClient(credential, subscription_id)

resources = resource_client.resources.list()


data = []
for resource in resources:
    data.append({
        'Name': resource.name,
        'ID': resource.id,
        'Type': resource.type,
        'Location': resource.location
    })

df = pd.DataFrame(data)

# Write to Excel
output_file = 'azure_resources.xlsx'
df.to_excel(output_file, index=False)

print(f"Resource details written to {output_file}")
