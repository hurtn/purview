#MIT License
#
#Copyright (c) 2021 Nick Hurt
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

from pyapacheatlas.auth import ServicePrincipalAuthentication
from pyapacheatlas.core import PurviewClient
import os 
import json

# Enter your Azure environment details here
tenant_id = ""
client_id = ""
client_secret = ""
purview_account_name = ""

# Enter the details about your Synapse environment and filter condition here
# This is instance name of your service. Note for Synapse this will normally be instanceName for dedicated pools or instanceName-ondemand for servless
# See the properties blade in your Azure portal for the FQDN or extract it from one of the assets you wish to delete 
synapaseInstance = "" # e.g. mysynapsedemo-ondemand for serverless
# Should you wish to delete all tables from all databases in Purview leave the this variable as an empty string
databaseName = "" # this is the database name, must include the / suffix if you want to include a database name. e.g. sales/ 
# This is normally tables, unless you want to delete schema objects also
entityTypesToDelete = "azure_synapse_serverless_sql_table"

# Intantiate authentication details
oauth = ServicePrincipalAuthentication(
    tenant_id=os.environ.get("TENANT_ID", tenant_id),
    client_id=os.environ.get("CLIENT_ID", client_id),
    client_secret=os.environ.get("CLIENT_SECRET", client_secret)
)

# Instantiate PurviewClient 
client = PurviewClient(
    account_name = os.environ.get("PURVIEW_NAME", purview_account_name),
    authentication=oauth
)

# Here are some search examples
# search = client.search_entities("name:demo*")
# search = client.search_entities("qualifiedName:demo*")

# For a more detailed search fitler condition, please see 
# https://github.com/wjohnson/pyapacheatlas/blob/master/samples/CRUD/identify_assets_to_delete_by_fqn.py

# This example deletes all defined entity types in a given database in Synapse
filter_setup = {"entityType": entityTypesToDelete} 
search = client.search_entities("mssql://" + synapaseInstance + ".sql.azuresynapse.net/"+ databaseName + "*", search_filter= filter_setup)

# The response is a Python dictionary that allows you to page through the
# search results without having to worry about paging or offsets.

for entity in search:
    # Important properties returned include...
    # id (the guid of the entity), name, qualifedName, @search.score
    print("Item to be deleted: " + json.dumps(entity["qualifiedName"])+" -- " +json.dumps(entity["entityType"]) + " -- " + json.dumps(entity["id"]))
    # Uncomment the next line if you wish to delete the assets from Purview
    #delete_response = client.delete_entity(guid=entity["id"])
    print("Deleted item: " + json.dumps(delete_response, indent=2))
