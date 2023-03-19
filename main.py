import sys
import os
import json
import requests
from modules.get_subscription_details import get_sub
from modules.get_resource_group_details import get_rg
from modules.get_resource_details import get_resource
from modules.get_resource_summary import get_resource_summary
from modules.get_vm_details import get_vm,get_vm_data_disk,get_vm_network_interfaces,get_vm_metrics
from modules.get_network_details import get_vn,get_pip
from modules.get_storage_account import get_sa,get_sa_blob,get_sa_file_share,get_sa_table,get_sa_queue
from modules.get_policy import policy_assignment,policy_assessment, policy_rcs
from modules.get_azure_advisor import get_advised
from modules.get_sql_database import get_sql_server
from modules.get_sqlmi_database import get_sqlmi_server
from modules.get_data_factory import get_df
from modules.get_key_vault import get_active_kv, get_deleted_kv
from modules.get_load_balancer import get_lb
from modules.get_application_gateway import get_ag
from modules.get_vmss_details import get_vmss

print("Starting Login Process")

# Login and get access token
try:
    LOGIN_URL = "https://login.microsoftonline.com/"+os.environ.get('ARM_TENANT_ID')+"/oauth2/token"
    PARAMS_MGMT = {'grant_type':'client_credentials','client_id': ''+os.environ.get('ARM_CLIENT_ID')+'','client_secret':''+os.environ.get('ARM_CLIENT_SECRET')+'','resource':'https://management.azure.com/'}
    login = requests.post(url = LOGIN_URL, data = PARAMS_MGMT)
    jsonfy = login.json()
    token = jsonfy["access_token"]
    query_header = {"Content-Type": "application/json", "Authorization": "Bearer "+token}
    print("Login Successful")
except Exception as e:
    print("Error is ", e)
    print("Login Unsuccessful, please check your credentials")
    sys.exit(1)

# Get Subscription Details
try:
    get_sub(sys.argv[1], query_header)
except Exception as e:
    print("Error is ", e)
    sys.exit(1)

# Get Resource Group Details
try:
    get_rg(sys.argv[1], sys.argv[2], query_header)
except Exception as e:
    print("Error is ", e)
    sys.exit(1)

# Get Resource Details
try:
    get_resource(sys.argv[1], sys.argv[2], query_header)
except Exception as e:
    print("Error is ", e)
    sys.exit(1)

# Get Resource Type Summary
try:
    get_resource_summary(sys.argv[1], sys.argv[2], query_header)
except Exception as e:
    print("Error is ", e)
    sys.exit(1)

# Get VM Details
try:
    get_vm(sys.argv[1], sys.argv[2], query_header)
except Exception as e:
    print("Error is ", e)
    sys.exit(1)

# Get VM Data Disk Details
try:
    get_vm_data_disk(sys.argv[2], query_header)
except Exception as e:
    print("Error is ", e)
    sys.exit(1)

# Get VM Network Interface Details
try:
    get_vm_network_interfaces(sys.argv[2], query_header)
except Exception as e:
    print("Error is ", e)
    sys.exit(1)

# Get VM Metrics
try:
    get_vm_metrics(sys.argv[2], query_header)
except Exception as e:
    print("Error is ", e)
    sys.exit(1)

# Get Virtual Network Details
try:
    get_vn(sys.argv[2], query_header)
except Exception as e:
    print("Error is ", e)
    sys.exit(1)

# Get Public IP Address Details
try:
    get_pip(sys.argv[1], sys.argv[2], query_header)
except Exception as e:
    print("Error is ", e)
    sys.exit(1)

# Get Storage Account Details
try:
    get_sa(sys.argv[1], sys.argv[2], query_header)
except Exception as e:
    print("Error is ", e)
    sys.exit(1)

# Get Storage Account Blob Details
try:
    get_sa_blob(sys.argv[2], query_header)
except Exception as e:
    print("Error is ", e)
    sys.exit(1)

# Get Storage Account File Share Details
try:
    get_sa_file_share(sys.argv[2], query_header)
except Exception as e:
    print("Error is ", e)
    sys.exit(1)

# Get Storage Account Table Details
try:
    get_sa_table(sys.argv[2], query_header)
except Exception as e:
    print("Error is ", e)
    sys.exit(1)

# Get Storage Account Queue Details
try:
    get_sa_queue(sys.argv[2], query_header)
except Exception as e:
    print("Error is ", e)
    sys.exit(1)

# Get Policy Assignment Details
try:
    policy_assignment(sys.argv[1], sys.argv[2], query_header)
except Exception as e:
    print("Error is ", e)
    sys.exit(1)

# Get Policy Assessments Details
try:
    policy_assessment(sys.argv[1], sys.argv[2], query_header)
except Exception as e:
    print("Error is ", e)
    sys.exit(1)

# Get Regulatory Compliance Standard Details
try:
    policy_rcs(sys.argv[1], sys.argv[2], query_header)
except Exception as e:
    print("Error is ", e)
    sys.exit(1)

# Get Azure Advisor Recommendation
try:
    get_advised(sys.argv[1], sys.argv[2], query_header)
except Exception as e:
    print("Error is ", e)
    sys.exit(1)

# Get Azure SQL Database
try:
    get_sql_server(sys.argv[1], sys.argv[2], query_header)
except Exception as e:
    print("Error is ", e)
    sys.exit(1)

# Get Azure SQLMI Database
try:
    get_sqlmi_server(sys.argv[1], sys.argv[2], query_header)
except Exception as e:
    print("Error is ", e)
    sys.exit(1)

# Get Azure Data Factory
try:
    get_df(sys.argv[1], sys.argv[2], query_header)
except Exception as e:
    print("Error is ", e)
    sys.exit(1)

# Get Active Key Vault Details
try:
    get_active_kv(sys.argv[1], sys.argv[2], query_header)
except Exception as e:
    print("Error is ", e)
    sys.exit(1)

# Get Deleted Key Vault Details
try:
    get_deleted_kv(sys.argv[1], sys.argv[2], query_header)
except Exception as e:
    print("Error is ", e)
    sys.exit(1)

# Get Load Balancer Details
try:
    get_lb(sys.argv[1], sys.argv[2], query_header)
except Exception as e:
    print("Error is ", e)
    sys.exit(1)

# # Get Application Gateway Details
try:
    get_ag(sys.argv[1], sys.argv[2], query_header)
except Exception as e:
    print("Error is ", e)
    sys.exit(1)

# Get Virtual Machine Scale Set Details
try:
    get_vmss(sys.argv[1], sys.argv[2], query_header)
except Exception as e:
    print("Error is ", e)
    sys.exit(1)