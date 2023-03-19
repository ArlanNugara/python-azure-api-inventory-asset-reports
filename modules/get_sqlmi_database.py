import requests
import json
import sys
import csv
import os

def get_sqlmi_server(subscription_id,subscription_name,header):
    print("Getting SQL Managed Instance details for ", subscription_name)
    sqlmi_server_excel_header = ["Subscription", "Resource Group", "Name", "Location", "Status", "Provisioning State", "SKU Name", "SKU Tier", "SKU Family", "SKU Capacity", "FQDN", "Licence Type", "Storage Account Type", "Storage Size(GB)", "Collation", "Public Endpoint Enabled", "Private Endpoint Connection", "TLS Version", "AAD Authentication", "Tags"]
    sqlmi_server_sql_header = ["sub", "rg_name", "name", "location", "status", "provisioning_state", "sku_name", "sku_tier", "sku_family", "sku_capacity", "fqdn", "licence_type", "storage_account_type", "storage_size", "collation", "public_endpoint_enabled", "private_endpoint_connection", "tls_version", "aad_authentication", "tags"]
    sqlmi_database_excel_header = ["Subscription", "Resource Group", "SQL Server", "Name", "Location", "Status", "Collation", "Creation Date"]
    sqlmi_database_sql_header = ["sub", "rg_name", "srv_name", "name", "location", "status", "collation", "creation_date"]
    with open('SQLMI Servers.csv', mode='w', newline='') as sqlmi_srv_excel_file_header:
        csvwriter = csv.writer(sqlmi_srv_excel_file_header, delimiter=',')
        csvwriter.writerow(sqlmi_server_excel_header)
    with open('sql_sqlmi_srv.csv', mode='w', newline='') as sqlmi_srv_sql_file_header:
        csvwriter = csv.writer(sqlmi_srv_sql_file_header, delimiter=',')
        csvwriter.writerow(sqlmi_server_sql_header)
    with open('SQLMI Databases.csv', mode='w', newline='') as sqlmi_dbs_excel_file_header:
        csvwriter = csv.writer(sqlmi_dbs_excel_file_header, delimiter=',')
        csvwriter.writerow(sqlmi_database_excel_header)
    with open('sql_sqlmi_dbs.csv', mode='w', newline='') as sqlmi_dbs_sql_file_header:
        csvwriter = csv.writer(sqlmi_dbs_sql_file_header, delimiter=',')
        csvwriter.writerow(sqlmi_database_sql_header)
    get_sqlmi_server_details = requests.get(url = "https://management.azure.com/subscriptions/"+subscription_id+"/providers/Microsoft.Sql/managedInstances?api-version=2021-02-01-preview", headers=header)
    get_sqlmi_server_details_to_json = get_sqlmi_server_details.json()
    if get_sqlmi_server_details.status_code == 200 or get_sqlmi_server_details.status_code == 204:
        if "value" in get_sqlmi_server_details_to_json:
            for server in get_sqlmi_server_details_to_json["value"]:
                sqlmi_srv_rg_name_split = server["id"].split('/')
                sqlmi_srv_rg_name = sqlmi_srv_rg_name_split[4]
                sqlmi_name = server["name"]
                sqlmi_location = server["location"]
                if "tags" in server:
                    all_tags = []
                    for key,value in server["tags"].items():
                        tag_value = ""+key+"="+value+""
                        all_tags.append(tag_value)
                    sqlmi_tag_excel_value = '\n'.join(all_tags)
                    sqlmi_tag_sql_value = ','.join(all_tags)
                else:
                    sqlmi_tag_excel_value = "No Tags"
                    sqlmi_tag_sql_value = "No Tags"
                if "sku" in server:
                    if "name" in server["sku"]:
                        sqlmi_sku_name = server["sku"]["name"]
                    else:
                        sqlmi_sku_name = None
                    if "tier" in server["sku"]:
                        sqlmi_sku_tier = server["sku"]["tier"]
                    else:
                        sqlmi_sku_tier = None
                    if "family" in server["sku"]:
                        sqlmi_sku_family = server["sku"]["family"]
                    else:
                        sqlmi_sku_family = None
                    if "capacity" in server["sku"]:
                        sqlmi_sku_capacity = server["sku"]["capacity"]
                    else:
                        sqlmi_sku_capacity = None
                else:
                    sqlmi_sku_name = None
                    sqlmi_sku_tier = None
                    sqlmi_sku_family = None
                    sqlmi_sku_capacity = None
                if "properties" in server:
                    if "state" in server["properties"]:
                        sqlmi_status = server["properties"]["state"]
                    else:
                        sqlmi_status = None
                    if "provisioningState" in server["properties"]:
                        sqlmi_provisioning_state = server["properties"]["provisioningState"]
                    else:
                        sqlmi_provisioning_state = None
                    if "fullyQualifiedDomainName" in server["properties"]:
                        sqlmi_fqdn = server["properties"]["fullyQualifiedDomainName"]
                    else:
                        sqlmi_fqdn = None
                    if "licenseType" in server["properties"]:
                        sqlmi_licence = server["properties"]["licenseType"]
                    else:
                        sqlmi_licence = None
                    if "storageAccountType" in server["properties"]:
                        sqlmi_sa_type = server["properties"]["storageAccountType"]
                    else:
                        sqlmi_sa_type = None
                    if "storageSizeInGB" in server["properties"]:
                        sqlmi_storage_gb = server["properties"]["storageSizeInGB"]
                    else:
                        sqlmi_storage_gb = None
                    if "collation" in server["properties"]:
                        sqlmi_collation = server["properties"]["collation"]
                    else:
                        sqlmi_collation = None
                    if "publicDataEndpointEnabled" in server["properties"]:
                        sqlmi_public_endpoint = server["properties"]["publicDataEndpointEnabled"]
                    else:
                        sqlmi_public_endpoint = None
                    if "privateEndpointConnections" in server["properties"]:
                        sqlmi_private_endpoint = len(server["properties"]["privateEndpointConnections"])
                    else:
                        sqlmi_private_endpoint = 0
                    if "minimalTlsVersion" in server["properties"]:
                        sqlmi_tls_version = server["properties"]["minimalTlsVersion"]
                    else:
                        sqlmi_tls_version = None
                    if "administrators" in server["properties"]:
                        sqlmi_aad_admin = "Yes"
                    else:
                        sqlmi_aad_admin = "No"
                else:
                    sqlmi_status = None
                    sqlmi_provisioning_state = None
                    sqlmi_fqdn = None
                    sqlmi_licence = None
                    sqlmi_sa_type = None
                    sqlmi_storage_gb = None
                    sqlmi_collation = None
                    sqlmi_public_endpoint = None
                    sqlmi_private_endpoint = None
                    sqlmi_tls_version = None
                    sqlmi_aad_admin = None
                # Write Data to CSV
                print("Writing CSV Data for SQLMI for ", subscription_name)
                sqlmi_server_excel_data = [subscription_name,sqlmi_srv_rg_name,sqlmi_name,sqlmi_location,sqlmi_status,sqlmi_provisioning_state,sqlmi_sku_name,sqlmi_sku_tier,sqlmi_sku_family,sqlmi_sku_capacity,sqlmi_fqdn,sqlmi_licence,sqlmi_sa_type,sqlmi_storage_gb,sqlmi_collation,sqlmi_public_endpoint,sqlmi_private_endpoint,sqlmi_tls_version,sqlmi_aad_admin,sqlmi_tag_excel_value]
                sqlmi_server_sql_data = [subscription_name,sqlmi_srv_rg_name,sqlmi_name,sqlmi_location,sqlmi_status,sqlmi_provisioning_state,sqlmi_sku_name,sqlmi_sku_tier,sqlmi_sku_family,sqlmi_sku_capacity,sqlmi_fqdn,sqlmi_licence,sqlmi_sa_type,sqlmi_storage_gb,sqlmi_collation,sqlmi_public_endpoint,sqlmi_private_endpoint,sqlmi_tls_version,sqlmi_aad_admin,sqlmi_tag_sql_value]
                with open('SQLMI Servers.csv', mode='a', newline='') as sqlmi_srv_excel_file_data:
                    csvwriter = csv.writer(sqlmi_srv_excel_file_data, delimiter=',')
                    csvwriter.writerow(sqlmi_server_excel_data)
                with open('sql_sqlmi_srv.csv', mode='a', newline='') as sqlmi_srv_sql_file_data:
                    csvwriter = csv.writer(sqlmi_srv_sql_file_data, delimiter=',')
                    csvwriter.writerow(sqlmi_server_sql_data)
                # Get SQLMI Database
                print("Getting Database Details for ", sqlmi_name)
                get_sqlmi_databases_details = requests.get(url = "https://management.azure.com"+server["id"]+"/databases?api-version=2021-02-01-preview", headers = header)
                get_sqlmi_databases_details_to_json = get_sqlmi_databases_details.json()
                if get_sqlmi_databases_details.status_code == 200 or get_sqlmi_databases_details.status_code == 204:
                    if "value" in get_sqlmi_databases_details_to_json:
                        for database in get_sqlmi_databases_details_to_json["value"]:
                            sqlmi_db_rg_name_split = database["id"].split('/')
                            sqlmi_db_rg_name = sqlmi_db_rg_name_split[4]
                            sqlmi_db_name = database["name"]
                            sqlmi_db_location = database["location"]
                            if "properties" in database:
                                if "status" in database["properties"]:
                                    sqlmi_db_status = database["properties"]["status"]
                                else:
                                    sqlmi_db_status = None
                                if "collation" in database["properties"]:
                                    sqlmi_db_collation = database["properties"]["collation"]
                                else:
                                    sqlmi_db_collation = None
                                if "creationDate" in database["properties"]:
                                    sqlmi_db_creation_date = database["properties"]["creationDate"]
                                else:
                                    sqlmi_db_creation_date = None
                            else:
                                sqlmi_db_status = None
                                sqlmi_db_collation = None
                                sqlmi_db_creation_date = None
                            # Write Data to CSV
                            print("Writing Database Details for ", sqlmi_name)
                            sqlmi_database_excel_data = [subscription_name, sqlmi_db_rg_name, sqlmi_name, sqlmi_db_name, sqlmi_db_location, sqlmi_db_status, sqlmi_db_collation, sqlmi_db_creation_date]
                            sqlmi_database_sql_data = [subscription_name, sqlmi_db_rg_name, sqlmi_name, sqlmi_db_name, sqlmi_db_location, sqlmi_db_status, sqlmi_db_collation, sqlmi_db_creation_date]
                            with open('SQLMI Databases.csv', mode='a', newline='') as sqlmi_dbs_excel_file_data:
                                csvwriter = csv.writer(sqlmi_dbs_excel_file_data, delimiter=',')
                                csvwriter.writerow(sqlmi_database_excel_data)
                            with open('sql_sqlmi_dbs.csv', mode='a', newline='') as sqlmi_dbs_sql_file_data:
                                csvwriter = csv.writer(sqlmi_dbs_sql_file_data, delimiter=',')
                                csvwriter.writerow(sqlmi_database_sql_data)
                    else:
                        print("No Database Found for ", sqlmi_name)
                        pass
                else:
                    print("Error getting SQL Database Details for ", sqlmi_name)
                    pass
                # Get SQLMI Firewall Rules
                print("Getting SQLMI Firewall Rules for ", sqlmi_name)

        else:
            print("No SQL Managed Instance Found for ", subscription_name)
            pass
    else:
        print("Error getting API response for SQLMI for ", subscription_name)
        pass