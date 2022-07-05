purview_account_name = "PurviewAccountName"
client_id = "SERVICEPRINCIPALID"
client_secret = "SERVICEPRINCIPALSECRET"
resource = "https://purview.azure.net"
tenant_id = "TENANTID"
synapse_workspace_name = "SYNAPSEWORKSPACENAME"

# oauth2 login
url = "https://login.microsoftonline.com/" + tenant_id + "/oauth2/token"

# Login and get token
payload='grant_type=client_credentials&client_id=' + client_id + '&client_secret=' + client_secret + '&resource=' + resource
headers = {
  'Content-Type': 'application/x-www-form-urlencoded',
}

# Get & set the access token
response = json.loads(requests.request("POST", url, headers=headers, data=payload).content)
access_token = response['access_token']

purview_endpoint = "https://"+purview_account_name+".catalog.purview.azure.com" 
url = purview_endpoint + "/api/search/query?api-version=2021-05-01-preview"


headers = {
  'Authorization': 'Bearer ' + access_token,
  'Content-Type': 'application/json'
}

#Search for assets based on keyword and entity type.
#Tables
payload = json.dumps({
  "keywords": "mssql://"+synapse_workspace_name+"-ondemand.sql.azuresynapse.net/*",
  "filter": {"entityType": "azure_synapse_serverless_sql_table"}
})

response = json.loads(requests.request("POST", url, headers=headers, data=payload).content)
print('Number of Synapse SQL Tables: ' + str(response['@search.count']))

#Views
payload = json.dumps({
  "keywords": "mssql://"+synapse_workspace_name+"-ondemand.sql.azuresynapse.net/*",
  "filter": {"entityType": "azure_synapse_serverless_sql_view"}
})

response = json.loads(requests.request("POST", url, headers=headers, data=payload).content)
print('Number of Synapse SQL Views: ' + str(response['@search.count']))
